"""Native epistemic-graph ingestion for qBittorrent records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The qbittorrent-agent connector
natively pushes its data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:Torrent`, `:Tracker`, `:TorrentCategory`) + links (`:announcesTo`,
`:inCategory`), through the required ``agent_utilities.knowledge_graph.memory.native_ingest``
authority — the one connector write path; there is no self-contained fallback
transaction here.

The MCP tool surface (``qbittorrent_agent.mcp_server``) exposes these as best-effort
tools that must never raise on an unreachable/misconfigured KG stack, so
``ingest_entities`` / ``ingest_documents`` stay **best-effort**: they return ``None``
(never raise) for empty input or when the shared primitive reports
:class:`NativeIngestError` (no reachable engine, or a malformed record). Nodes carry
the shared provenance (``domain``/``source``) and match the classes federated by
``qbittorrent_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    NativeIngestError,
    ingest_documents as _native_ingest_documents,
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("qbittorrent_agent.kg")

_SOURCE = "qbittorrent-agent"
_DOMAIN = "qbittorrent"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph. Best-effort, never raises.

    ``entities``: ``[{"id":..., "node_type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "relationship":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (empty input / no reachable engine /
    malformed record). ``client``/``graph`` may be injected (tests); otherwise the
    process-owned governed authority is resolved on demand.
    """
    if not entities:
        return None
    try:
        return _native_ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder). Best-effort.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    if not documents:
        return None
    try:
        return _native_ingest_documents(
            documents, source=source, domain=domain, client=client, graph=graph
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def ingest_torrents(
    torrents: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map qBittorrent torrent-list records → ``:Torrent`` (+ ``:Tracker`` /
    ``:TorrentCategory``) nodes and links, then ingest.

    Accepts raw ``torrents/info`` dicts (or ``TorrentInfo.model_dump()``). Skips any
    record without a ``hash``. The primary announce URL (``tracker``) becomes a
    ``:Tracker`` node linked by ``:announcesTo``; a non-empty ``category`` becomes a
    ``:TorrentCategory`` linked by ``:inCategory``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    seen_trackers: set[str] = set()
    seen_categories: set[str] = set()

    for tor in torrents or []:
        thash = tor.get("hash")
        if not thash:
            continue
        tid = f"qbittorrent:Torrent:{thash}"
        entities.append(
            {
                "id": tid,
                "node_type": "Torrent",
                "name": tor.get("name"),
                "infoHash": thash,
                "torrentState": tor.get("state"),
                "progress": tor.get("progress"),
                "shareRatio": tor.get("ratio"),
                "sizeBytes": tor.get("size"),
                "savePath": tor.get("save_path"),
                "tags": tor.get("tags") or None,
                "added_on": tor.get("added_on"),
                "completion_on": tor.get("completion_on"),
                "externalToolId": str(thash),
            }
        )

        tracker_url = (tor.get("tracker") or "").strip()
        if tracker_url:
            tkid = f"qbittorrent:Tracker:{tracker_url}"
            if tkid not in seen_trackers:
                seen_trackers.add(tkid)
                entities.append(
                    {"id": tkid, "node_type": "Tracker", "trackerUrl": tracker_url}
                )
            relationships.append(
                {"source": tid, "target": tkid, "relationship": "announcesTo"}
            )

        category = (tor.get("category") or "").strip()
        if category:
            catid = f"qbittorrent:TorrentCategory:{category}"
            if catid not in seen_categories:
                seen_categories.add(catid)
                entities.append(
                    {"id": catid, "node_type": "TorrentCategory", "name": category}
                )
            relationships.append(
                {"source": tid, "target": catid, "relationship": "inCategory"}
            )

    return ingest_entities(entities, relationships, client=client, graph=graph)
