"""Knowledge-graph ingest tool for qBittorrent (Wire-First).

Lists torrents through the typed ``torrents_info`` operation and pushes them
into the knowledge graph as typed nodes (see ``qbittorrent_agent.kg_ingest``).
Every WebUI API operation is its own tool, served from the client methods;
this module adds only the tool that is not an API operation.
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field
from scion_sdk.mcp.concurrency import run_blocking

from qbittorrent_agent.auth import get_client


def _records(resp: Any) -> list[dict[str, Any]]:
    """The torrent list from a ``torrents_info`` answer (``{"result": [...]}``)."""
    data = resp.get("result", resp) if isinstance(resp, dict) else resp
    records = data if isinstance(data, list) else [data]
    return [r for r in records if isinstance(r, dict)]


def register_kg_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"kg", "ingest"})
    async def qbittorrent_ingest_torrents(
        filter: str | None = Field(
            default=None,
            description="State filter: all, downloading, seeding, completed, stopped, active, ...",
        ),
        category: str | None = Field(default=None, description="Only this category"),
        tag: str | None = Field(default=None, description="Only this tag"),
        limit: int | None = Field(
            default=None, description="At most this many torrents"
        ),
    ) -> dict[str, Any]:
        """Ingest qBittorrent torrents into the knowledge graph as typed nodes.

        Lists torrents with `qbittorrent_torrents_info` and pushes them, with their
        trackers and categories, as typed nodes. Returns how many were listed and
        what the engine accepted.
        """
        from qbittorrent_agent.kg_ingest import ingest_torrents

        client = get_client()
        resp = await run_blocking(
            client.torrents_info, filter=filter, category=category, tag=tag, limit=limit
        )
        torrents = _records(resp)
        result = await ingest_torrents(torrents)
        return {"listed": len(torrents), "ingested": result}
