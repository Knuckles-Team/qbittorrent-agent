"""Write the qBittorrent WebUI API client from the census fixture.

Usage::

    python scripts/generate_api_client.py

One method per upstream operation (CONN-QBITTORRENT-AGENT-SURFACE-R001), read
from ``tests/fixtures/upstream_operations.json``: the method name is
``<scope>_<action>`` in snake case, each parameter is a typed keyword with the
upstream name on the wire, and the docstring carries ``VERB /api/v2/<route>``
so the SDK annotates the tool from the verb. One class per API scope gives
each tool its domain tag. The output is source: review it and commit it.
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/upstream_operations.json"
TARGET = ROOT / "qbittorrent_agent/api/client.py"

_HEADER = '''"""qBittorrent WebUI API client: one method per upstream operation.

Written by ``scripts/generate_api_client.py`` from
``tests/fixtures/upstream_operations.json`` ({source}). Every method is served
as one typed MCP tool ``qbittorrent_<scope>_<action>``
(CONN-QBITTORRENT-AGENT-SURFACE-R001).
"""

# ruff: noqa: E501, A002

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from qbittorrent_agent.api.api_client_base import BaseApiClient
'''


def snake(name: str) -> str:
    name = name.replace("SSL", "Ssl").replace("API", "Api").replace("URL", "Url")
    out = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return out + "_" if keyword.iskeyword(out) else out


def method(op: dict) -> str:
    scope, action = op["route"].split("/", 1)
    name = f"{scope}_{snake(action)}"
    sig, call = ["self"], []
    params = sorted(op["params"], key=lambda p: not p["required"])
    if params or op["files"]:
        sig.append("*")
    for p in params:
        arg = p.get("arg") or snake(p["name"])
        desc = json.dumps(p["description"] or p["name"])
        typ = p["type"] if p["required"] else f"{p['type']} | None"
        default = "" if p["required"] else " = None"
        sig.append(f"{arg}: Annotated[{typ}, Field(description={desc})]{default}")
        call.append(f'"{p["name"]}": {arg}')
    if op["files"]:
        sig.append(
            'torrent_files: Annotated[dict[str, str] | None, Field(description="Uploaded .torrent files: file name to base64 content")] = None'
        )
    body = [f"    def {name}({', '.join(sig)}) -> Any:"]
    body.append(f'        """{op["summary"]}.\n\n        {op["verb"]} /api/v2/{op["route"]}\n        """')
    args = [f'"{op["verb"]}"', f'"{op["route"]}"']
    if call:
        args.append("{" + ", ".join(call) + "}")
    if op["files"]:
        if not call:
            args.append("None")
        args.append("torrent_files")
    body.append(f"        return self._call({', '.join(args)})")
    return "\n".join(body)


def main() -> None:
    census = json.loads(FIXTURE.read_text())
    scopes: dict[str, list[str]] = {}
    for op in census["operations"]:
        scopes.setdefault(op["route"].split("/", 1)[0], []).append(method(op))
    out = _HEADER.format(source=census["source"].split(";")[0])
    names = []
    for scope, methods in scopes.items():
        cls = "".join(w.title() for w in re.split(r"[^a-z]", scope)) + "Api"
        cls = {"TorrentcreatorApi": "TorrentCreatorApi", "ClientdataApi": "ClientDataApi"}.get(cls, cls)
        names.append(cls)
        out += f'\n\nclass {cls}(BaseApiClient):\n    """The `{scope}` scope of the WebUI API."""\n\n' + "\n\n".join(methods) + "\n"
    out += "\n\nclass Api(" + ", ".join(names) + '):\n    """The qBittorrent WebUI API: every scope in one client."""\n'
    TARGET.write_text(out)
    print(f"{TARGET.relative_to(ROOT)}: {len(census['operations'])} operations")


if __name__ == "__main__":
    main()
