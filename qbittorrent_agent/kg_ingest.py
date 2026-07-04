"""Native epistemic-graph ingestion for qBittorrent records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The qbittorrent-agent connector
natively pushes its data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:Torrent`, `:Tracker`, `:TorrentCategory`) + links (`:announcesTo`,
`:inCategory`), using the lightweight engine client (``GraphComputeEngine()._client`` +
``txn``) — the same fast client the blob ``MediaStore`` uses, NOT the heavy in-process
ingestion engine.

Entirely best-effort and dependency-/engine-guarded: with no agent-utilities KG stack
or no reachable engine, every entry point **no-ops** (returns ``None``), so the
connector keeps working with zero KG infrastructure. It prefers the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` when present, and otherwise
falls back to a self-contained txn write (the primitive is not yet in the installed
agent_utilities). Nodes carry the shared provenance (``domain``/``source``) and match
the classes federated by ``qbittorrent_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("qbittorrent_agent.kg")

_SOURCE = "qbittorrent-agent"
_DOMAIN = "qbittorrent"
_DEFAULT_GRAPH = "__commons__"


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        graph = getattr(engine, "graph_name", None) or _DEFAULT_GRAPH
        return client, graph
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _write_nodes(
    client: Any,
    graph: str,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    source: str,
    domain: str,
) -> dict[str, int] | None:
    """Stamp provenance, MERGE the nodes in one txn, then add the edges."""
    nodes = [n for n in nodes if n.get("id")]
    if not nodes:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest[%s]: wrote %d nodes, %d edges", domain, len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph via the fast engine client.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    Prefers the shared ``native_ingest`` primitive; otherwise self-contained.
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None

    # Prefer the shared primitive when it is importable AND no client is injected.
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_entities as _shared,
            )

            return _shared(
                entities, relationships, source=source, domain=domain, graph=graph
            )
        except Exception as e:  # noqa: BLE001 — primitive absent; self-contained path
            logger.debug("KG ingest: shared primitive unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    return _write_nodes(
        client,
        graph or _DEFAULT_GRAPH,
        entities,
        relationships,
        source=source,
        domain=domain,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    documents = [
        d
        for d in (documents or [])
        if d.get("id") and (d.get("text") or d.get("content"))
    ]
    if not documents:
        return None
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_documents as _shared,
            )

            return _shared(documents, source=source, domain=domain, graph=graph)
        except Exception as e:  # noqa: BLE001 — primitive absent; self-contained path
            logger.debug("KG ingest: shared primitive unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    nodes: list[dict[str, Any]] = []
    for doc in documents:
        text = doc.get("text") or doc.get("content")
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["type"] = "Document"
        node["text"] = text
        nodes.append(node)
    return _write_nodes(
        client, graph or _DEFAULT_GRAPH, nodes, None, source=source, domain=domain
    )


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
                "type": "Torrent",
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
                    {"id": tkid, "type": "Tracker", "trackerUrl": tracker_url}
                )
            relationships.append({"source": tid, "target": tkid, "type": "announcesTo"})

        category = (tor.get("category") or "").strip()
        if category:
            catid = f"qbittorrent:TorrentCategory:{category}"
            if catid not in seen_categories:
                seen_categories.add(catid)
                entities.append(
                    {"id": catid, "type": "TorrentCategory", "name": category}
                )
            relationships.append({"source": tid, "target": catid, "type": "inCategory"})

    return ingest_entities(entities, relationships, client=client, graph=graph)
