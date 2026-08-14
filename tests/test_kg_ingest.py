"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_torrents`` seam with a fake
ChangeEnvelope-capable engine client (no engine required), asserting the committed
nodes/edges and the qBittorrent torrent -> :Torrent/:Tracker/:TorrentCategory mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake client mirrors agent-utilities' own sanctioned test double
(``agent-utilities/tests/knowledge_graph/test_native_ingest.py``) — the ``txn``-only
fake is retired; ``native_ingest`` now hard-requires an injected client exposing
``.changes``/``.nodes``/``.rdf``/``.supports()``. Unlike most fleet connectors,
``qbittorrent_agent.kg_ingest`` is a **best-effort** surface (its MCP tools must never
raise when the KG stack is down), so it converts ``NativeIngestError`` into ``None``
rather than propagating it — those semantics are exercised explicitly below.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from qbittorrent_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_torrents,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Torrent", "name": "t"},
            {"id": "b", "node_type": "Tracker"},
        ],
        [{"source": "a", "target": "b", "relationship": "announcesTo"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "qbittorrent-agent"
    assert c.nodes.values["a"]["domain"] == "qbittorrent"
    assert c.changes.edges == [("a", "b", {"relationship": "announcesTo"})]


def test_ingest_torrents_maps_torrent_tracker_category():
    c = _FakeClient()
    res = ingest_torrents(
        [
            {
                "hash": "abc123",
                "name": "Ubuntu ISO",
                "state": "uploading",
                "progress": 1.0,
                "ratio": 2.5,
                "size": 4096,
                "save_path": "/downloads",
                "category": "linux",
                "tracker": "http://tracker.example/announce",
                "tags": "iso,os",
            }
        ],
        client=c,
    )
    # 1 torrent + 1 tracker + 1 category = 3 nodes; 2 edges
    assert res == {"nodes": 3, "edges": 2}
    tor = c.nodes.values["qbittorrent:Torrent:abc123"]
    assert tor["node_type"] == "Torrent"
    assert tor["infoHash"] == "abc123"
    assert tor["torrentState"] == "uploading"
    assert tor["shareRatio"] == 2.5
    assert tor["externalToolId"] == "abc123"
    assert (
        c.nodes.values["qbittorrent:Tracker:http://tracker.example/announce"][
            "node_type"
        ]
        == "Tracker"
    )
    assert (
        c.nodes.values["qbittorrent:TorrentCategory:linux"]["node_type"]
        == "TorrentCategory"
    )
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:Tracker:http://tracker.example/announce",
        {"relationship": "announcesTo"},
    ) in c.changes.edges
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:TorrentCategory:linux",
        {"relationship": "inCategory"},
    ) in c.changes.edges


def test_ingest_torrents_dedupes_shared_tracker_and_category():
    c = _FakeClient()
    res = ingest_torrents(
        [
            {"hash": "h1", "name": "a", "category": "x", "tracker": "udp://tk/a"},
            {"hash": "h2", "name": "b", "category": "x", "tracker": "udp://tk/a"},
        ],
        client=c,
    )
    # 2 torrents + 1 shared tracker + 1 shared category = 4 nodes; 4 edges
    assert res == {"nodes": 4, "edges": 4}


def test_ingest_torrents_skips_records_without_hash():
    c = _FakeClient()
    res = ingest_torrents([{"name": "no-hash"}], client=c)
    assert res is None
    assert c.changes.applied == []


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "qbittorrent:Document:1", "text": "hello", "title": "T"}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.nodes.values["qbittorrent:Document:1"]
    assert node["text"] == "hello"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op (best-effort surface).
    assert ingest_entities([{"id": "a", "node_type": "Torrent"}]) is None


def test_ingest_rejects_retired_structural_alias_as_noop():
    # qbittorrent_agent's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating NativeIngestError.
    c = _FakeClient()
    assert ingest_entities([{"id": "a", "type": "Torrent"}], client=c) is None
    assert c.changes.applied == []


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_torrents([], client=_FakeClient()) is None
    assert ingest_documents([], client=_FakeClient()) is None
