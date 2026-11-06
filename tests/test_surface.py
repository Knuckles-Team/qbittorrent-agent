"""The qBittorrent surface: every WebUI API operation is one typed tool (CONN-QBITTORRENT-AGENT-SURFACE).

Bound tests of ``specs/surface/requirements.md``: the census against the
qBittorrent 5.2.4 controllers, the typed-only surface, the response boundary,
and the content tier (skills, agent-definition prompts and the ontology with
its tool-use contracts and its roll-up to medulla core).
"""

from __future__ import annotations

import ast
import asyncio
import base64
import importlib.util
import json
import re
from pathlib import Path

import pytest
import requests

rdflib = pytest.importorskip("rdflib")
from rdflib.namespace import OWL, RDF, RDFS  # noqa: E402

ID = "CONN-QBITTORRENT-AGENT-SURFACE"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "qbittorrent_agent"
CENSUS = json.loads((ROOT / "tests/fixtures/upstream_operations.json").read_text())
KG = "http://knuckles.team/kg#"
QBT = "http://knuckles.team/kg/qbittorrent#"
BFO_ENTITY = rdflib.URIRef("http://purl.obolibrary.org/obo/BFO_0000001")


def _client_routes() -> dict[tuple[str, str], str]:
    tree = ast.parse((PKG / "api/client.py").read_text())
    found = {}
    for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
        for fn in cls.body:
            if not isinstance(fn, ast.FunctionDef) or fn.name.startswith("_"):
                continue
            for call in ast.walk(fn):
                if isinstance(call, ast.Call) and getattr(call.func, "attr", "") == "_call":
                    found[(call.args[0].value, call.args[1].value)] = fn.name
                    break
    return found


@pytest.fixture(scope="module")
def served():
    from fastmcp import Client
    from scion_sdk.connector import build_server

    _, mcp = build_server("qbittorrent_agent", command_args=[])

    async def collect():
        async with Client(mcp) as client:
            return (
                await client.list_tools(),
                await client.list_prompts(),
                await client.list_resources(),
            )

    tools, prompts, resources = asyncio.run(collect())
    return (
        {t.name: t for t in tools},
        {p.name: p for p in prompts},
        {str(r.uri) for r in resources},
    )


# --- R001 -------------------------------------------------------------------


@pytest.mark.spec(f"{ID}-R001")
def test_every_upstream_operation_has_a_client_method():
    ours = _client_routes()
    upstream = {(op["verb"], op["route"]) for op in CENSUS["operations"]}
    assert len(upstream) == 121
    assert not sorted(upstream - set(ours)), "operations without a tool"
    assert not sorted(set(ours) - upstream), "routes the upstream does not serve"


@pytest.mark.spec(f"{ID}-R001")
def test_every_client_method_is_served_as_a_tool(served):
    tools, _, _ = served
    for method in _client_routes().values():
        assert f"qbittorrent_{method}" in tools
    assert "qbittorrent_torrents_pause" not in tools  # removed upstream in 5.x


# --- R002 -------------------------------------------------------------------


@pytest.mark.spec(f"{ID}-R002")
def test_no_action_routed_or_untyped_tool(served):
    tools, _, _ = served
    for name, tool in tools.items():
        properties = set((tool.input_schema or {}).get("properties", {}))
        assert "params_json" not in properties, name
        assert "action" not in properties, name
        assert not ({"method", "endpoint"} <= properties), name


@pytest.mark.spec(f"{ID}-R002")
def test_destructive_operations_ask_for_confirmation(served):
    tools, _, _ = served
    for name in (
        "qbittorrent_torrents_delete",
        "qbittorrent_torrents_remove_categories",
        "qbittorrent_torrents_delete_tags",
        "qbittorrent_rss_remove_item",
        "qbittorrent_app_delete_api_key",
    ):
        assert tools[name].annotations.destructive_hint is True, name
    assert tools["qbittorrent_torrents_info"].annotations.read_only_hint is True


# --- R003 -------------------------------------------------------------------


class _Resp:
    def __init__(self, status, body=b"", ctype="text/plain"):
        self.status_code = status
        self.content = body
        self.text = body.decode()
        self.headers = {"content-type": ctype}

    def json(self):
        return json.loads(self.text)


def _api(answer, seen):
    from qbittorrent_agent.api import Api

    api = Api.__new__(Api)
    api.base_url, api.api_url, api.api_key = "http://q", "http://q/api/v2", None
    api._authenticated = True

    class Session:
        def get(self, url, **kw):
            seen.append(("GET", url, kw))
            return answer

        post = lambda self, url, **kw: (seen.append(("POST", url, kw)), answer)[1]  # noqa: E731

    api.session = Session()
    return api


@pytest.mark.spec(f"{ID}-R003")
def test_a_failed_call_raises_with_qbittorrents_reason():
    from qbittorrent_agent.api import QbittorrentApiError

    api = _api(_Resp(409, b"Category name is invalid"), [])
    with pytest.raises(QbittorrentApiError, match="HTTP 409: Category name is invalid"):
        api.torrents_create_category(category="bad\\name")
    api = _api(_Resp(404, b"Not Found"), [])
    with pytest.raises(QbittorrentApiError, match="HTTP 404"):
        api.torrents_properties(hash="0" * 40)


@pytest.mark.spec(f"{ID}-R003")
def test_answers_are_json_objects_and_values_travel_on_the_wire():
    seen = []
    api = _api(_Resp(200, b'[{"hash": "a"}]', "application/json"), seen)
    assert api.torrents_info(filter="stalled", reverse=True) == {"result": [{"hash": "a"}]}
    assert seen[0][2]["params"] == {"filter": "stalled", "reverse": "true"}
    api = _api(_Resp(200, b"v5.2.4"), seen)
    assert api.app_version() == {"result": "v5.2.4"}
    api = _api(_Resp(200, b""), seen)
    assert api.app_set_preferences(preferences={"dl_limit": 0}) == {"status": "success"}
    assert json.loads(seen[-1][2]["data"]["json"]) == {"dl_limit": 0}
    api = _api(_Resp(200, b"d8:announce", "application/x-bittorrent"), seen)
    out = api.torrents_export(hash="a" * 40)
    assert base64.b64decode(out["content_base64"]) == b"d8:announce"


@pytest.mark.spec(f"{ID}-R003")
def test_api_key_is_a_bearer_and_a_placeholder_falls_back_to_login(monkeypatch):
    from qbittorrent_agent.api import api_client_base as base

    assert base.is_api_key("qbt_" + "x" * 28)
    assert not base.is_api_key("unused")
    logins = []
    monkeypatch.setattr(base.BaseApiClient, "login", lambda self: logins.append(1))

    class Profile:
        def configure_requests_session(self, session):
            return session

    client = base.BaseApiClient("http://q", "u", "p", tls_profile=Profile(), api_key="qbt_" + "x" * 28)
    assert client.session.headers["Authorization"].startswith("Bearer qbt_")
    assert logins == []
    base.BaseApiClient("http://q", "u", "p", tls_profile=Profile(), api_key="unused")
    assert logins == [1]
    assert isinstance(client.session, requests.Session)


# --- R004 / R005: content tier ------------------------------------------------


@pytest.fixture(scope="module")
def graph():
    g = rdflib.Graph()
    for path in sorted((PKG / "ontology").glob("*.ttl")):
        g.parse(path, format="turtle")
    return g


def _contract_tools(g):
    return {str(o) for o in g.objects(None, rdflib.URIRef(QBT + "toolName"))}


@pytest.mark.spec(f"{ID}-R004")
def test_contract_and_skill_tools_are_served(graph, served):
    tools, _, _ = served
    assert not sorted(_contract_tools(graph) - set(tools))
    named = re.compile(r"`(qbittorrent_[a-z0-9_]+)`")
    for skill in (PKG / "skills").glob("*/SKILL.md"):
        if skill.parent.name == "qbittorrent-agent-development":
            continue
        for name in named.findall(skill.read_text()):
            assert name in tools, f"{skill.parent.name}: {name}"


@pytest.mark.spec(f"{ID}-R004")
def test_contract_steps_are_ordered_and_bound(graph):
    has_step = rdflib.URIRef(QBT + "hasStep")
    contracts = list(graph.subjects(RDF.type, rdflib.URIRef(QBT + "ToolUseContract")))
    assert len(contracts) >= 9
    for contract in contracts:
        steps = list(graph.objects(contract, has_step))
        positions = sorted(int(graph.value(s, rdflib.URIRef(QBT + "stepIndex"))) for s in steps)
        assert positions == list(range(1, len(steps) + 1)), contract
        for step in steps:
            assert graph.value(step, rdflib.URIRef(QBT + "callsTool")) is not None
        skill = graph.value(contract, rdflib.URIRef(QBT + "contractOf"))
        name = str(graph.value(skill, rdflib.URIRef(QBT + "skillName")))
        assert (PKG / "skills" / name / "SKILL.md").is_file()


PROMPTS = sorted(p.stem for p in (PKG / "prompts").glob("*.json"))


@pytest.mark.spec(f"{ID}-R005")
def test_operator_and_role_prompts_exist():
    assert {"torrent_operator", "torrent_download_monitor", "seeding_manager", "download_client_steward"} <= set(PROMPTS)


@pytest.mark.spec(f"{ID}-R005")
@pytest.mark.parametrize("name", PROMPTS)
def test_prompt_is_a_complete_agent_definition(name, served, graph):
    tools, prompts, _ = served
    assert name in prompts
    doc = json.loads((PKG / "prompts" / f"{name}.json").read_text())
    assert doc["role"] == "system"
    text = doc["instructions"]["core_directive"]
    for section in ("Goal:", "Skills", "Workflows", "Data locations:", "Guardrails:", "Outputs:"):
        assert section in text, f"{name}: {section}"
    for tool in doc["tools"]:
        assert tool in tools
    node = rdflib.URIRef(QBT + f"prompt-{name}")
    linked = {
        str(graph.value(t, rdflib.URIRef(QBT + "toolName")))
        for t in graph.objects(node, rdflib.URIRef(QBT + "usesTool"))
    }
    assert linked == set(doc["tools"])
    assert str(graph.value(node, rdflib.URIRef(QBT + "systemPromptForRole"))) == doc["systemPromptFor"]


# --- R006 / R007 ----------------------------------------------------------------


@pytest.mark.spec(f"{ID}-R006")
def test_data_locations_routing_and_federation(graph):
    instance = rdflib.URIRef(QBT + "instance-qbittorrent")
    assert str(graph.value(instance, rdflib.URIRef(QBT + "urlSetting"))) == "QBITTORRENT_URL"
    paths = {
        str(graph.value(p, rdflib.URIRef(QBT + "path")))
        for p in graph.objects(instance, rdflib.URIRef(QBT + "storesIn"))
    }
    assert "/downloads/complete" in paths
    routes = list(graph.subjects(RDF.type, rdflib.URIRef(QBT + "RoutingRule")))
    links = list(graph.subjects(RDF.type, rdflib.URIRef(QBT + "FederationLink")))
    assert len(routes) >= 4 and len(links) >= 4


def _core_graph():
    spec = importlib.util.find_spec("medulla")
    assert spec is not None and spec.submodule_search_locations
    core = rdflib.Graph()
    for location in spec.submodule_search_locations:
        for path in sorted(Path(location, "ontology").glob("*.ttl")):
            if not path.name.endswith(".shapes.ttl"):
                core.parse(path, format="turtle")
    return core


@pytest.mark.spec(f"{ID}-R007")
def test_every_class_reaches_medulla_core_without_imports(graph):
    assert list(graph.objects(None, OWL.imports)) == []
    core = _core_graph()
    merged = core + graph
    core_classes = set(core.subjects(RDF.type, OWL.Class))
    classes = list(graph.subjects(RDF.type, OWL.Class))
    assert len(classes) >= 15
    for cls in classes:
        assert str(cls).startswith(QBT), f"{cls}: core classes are never redeclared"
        ancestors = set(merged.transitive_objects(cls, RDFS.subClassOf)) - {cls}
        assert ancestors & core_classes, cls
        assert BFO_ENTITY in ancestors, cls


# --- R008 -------------------------------------------------------------------------


@pytest.mark.spec(f"{ID}-R008")
def test_ingest_uses_core_classes_and_a_pinned_served_tool(served):
    import yaml
    from fastmcp import Client
    from scion_sdk.connector import build_server
    from scion_sdk.manifest.live_contract import validate_live_tool_contract

    core = _core_graph()
    source = (PKG / "kg_ingest.py").read_text()
    for node_type in set(re.findall(r'"node_type": "([A-Za-z]+)"', source)):
        assert (rdflib.URIRef(KG + node_type), RDF.type, OWL.Class) in core, node_type
    tools, _, _ = served
    presets = yaml.safe_load((PKG / "ontology/mappings/source.yaml").read_text())
    _, mcp = build_server("qbittorrent_agent", command_args=[])

    async def listing():
        async with Client(mcp) as client:
            return await client.session.list_tools()

    listed = asyncio.run(listing())
    for preset in presets["sync"]:
        assert preset["tool"] in tools and "action" not in preset
        live = validate_live_tool_contract(listed, tool_name=preset["tool"])
        assert live.compatibility_sha256 == preset["tool_schema_sha256"]
