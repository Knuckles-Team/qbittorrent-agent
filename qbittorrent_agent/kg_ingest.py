"""Native epistemic-graph ingestion for qBittorrent records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The qbittorrent-agent connector
natively pushes its data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:Torrent`, `:Tracker`, `:TorrentCategory`) + links (`:announcesTo`,
`:inCategory`), through the agent-connector-sdk knowledge-ingest facade — the one
connector write path; there is no self-contained fallback transaction here.

The MCP tool surface (``qbittorrent_agent.mcp_server``) exposes these as best-effort
tools that must never raise on an unreachable/misconfigured KG stack, so
``ingest_entities`` / ``ingest_documents`` stay **best-effort**: they return ``None``
(never raise) for empty input or when the SDK's facade reports :class:`IngestError`
(no reachable engine, or a malformed record). Nodes carry the binding's provenance and
match the classes federated by ``qbittorrent_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("qbittorrent_agent.kg")

_BINDING = IngestBinding(connector="qbittorrent-agent", stream="qbittorrent")


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={k: v for k, v in record.items() if k not in ("id", "node_type")},
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    props = {
        k: v for k, v in record.items() if k not in ("source", "target", "relationship")
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=props or None,
    )


def _to_document(record: dict[str, Any]) -> Document:
    return Document(
        id=record.get("id"),
        text=record.get("text"),
        title=record.get("title"),
        source_uri=record.get("source_uri"),
        properties={
            k: v
            for k, v in record.items()
            if k not in ("id", "text", "title", "source_uri")
        },
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph. Best-effort, never raises.

    ``entities``: ``[{"id":..., "node_type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "relationship":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (empty input / no reachable engine /
    malformed record). ``ingest`` may be injected (tests); otherwise the process-owned
    knowledge-ingest service is resolved on demand.
    """
    if not entities:
        return None
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships or ()),
    )
    try:
        service = ingest or current_ingest()
        receipt = await service.submit(_BINDING, change_set)
    except IngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder). Best-effort.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    if not documents:
        return None
    change_set = ChangeSet(documents=tuple(_to_document(d) for d in documents))
    try:
        service = ingest or current_ingest()
        receipt = await service.submit(_BINDING, change_set)
    except IngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_torrents(
    torrents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
        entities.append(_build_torrent_entity(tor, thash, tid))

        tracker_entity, tracker_rel = _torrent_tracker_link(tor, tid, seen_trackers)
        if tracker_entity is not None:
            entities.append(tracker_entity)
        if tracker_rel is not None:
            relationships.append(tracker_rel)

        category_entity, category_rel = _torrent_category_link(
            tor, tid, seen_categories
        )
        if category_entity is not None:
            entities.append(category_entity)
        if category_rel is not None:
            relationships.append(category_rel)

    return await ingest_entities(entities, relationships, ingest=ingest)


def _build_torrent_entity(
    tor: dict[str, Any], thash: str, tid: str
) -> dict[str, Any]:
    """Map one qBittorrent torrent record to a ``:Torrent`` entity dict."""
    return {
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


def _torrent_tracker_link(
    tor: dict[str, Any], tid: str, seen_trackers: set[str]
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Build the (deduped) ``:Tracker`` entity and ``:announcesTo`` relationship.

    Returns ``(entity, relationship)`` where ``entity`` is ``None`` when this
    tracker was already emitted for a prior torrent in the same batch, and
    both are ``None`` when the torrent has no tracker URL.
    """
    tracker_url = (tor.get("tracker") or "").strip()
    if not tracker_url:
        return None, None
    tkid = f"qbittorrent:Tracker:{tracker_url}"
    entity = None
    if tkid not in seen_trackers:
        seen_trackers.add(tkid)
        entity = {"id": tkid, "node_type": "Tracker", "trackerUrl": tracker_url}
    relationship = {"source": tid, "target": tkid, "relationship": "announcesTo"}
    return entity, relationship


def _torrent_category_link(
    tor: dict[str, Any], tid: str, seen_categories: set[str]
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Build the (deduped) ``:TorrentCategory`` entity and ``:inCategory`` relationship.

    Returns ``(entity, relationship)`` where ``entity`` is ``None`` when this
    category was already emitted for a prior torrent in the same batch, and
    both are ``None`` when the torrent has no category.
    """
    category = (tor.get("category") or "").strip()
    if not category:
        return None, None
    catid = f"qbittorrent:TorrentCategory:{category}"
    entity = None
    if catid not in seen_categories:
        seen_categories.add(catid)
        entity = {"id": catid, "node_type": "TorrentCategory", "name": category}
    relationship = {"source": tid, "target": catid, "relationship": "inCategory"}
    return entity, relationship
