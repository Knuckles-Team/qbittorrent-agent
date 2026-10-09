"""Knowledge-ingest typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_torrents`` seam against a fake
epistemic-graph transport (no engine required), letting the agent-connector-sdk's own
request builder run on top of it so the test exercises the SDK's validation contract
rather than re-deriving it. Unlike most fleet connectors, ``qbittorrent_agent.kg_ingest``
is a **best-effort** surface (its MCP tools must never raise when the KG stack is
down), so it converts :class:`IngestError` into ``None`` rather than propagating it —
those semantics are exercised explicitly below.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from qbittorrent_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_torrents,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Torrent", "name": "t"},
            {"id": "b", "node_type": "Tracker"},
        ],
        [{"source": "a", "target": "b", "relationship": "announcesTo"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert {r.record_id for r in request.records} == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["name"] == "t"
    assert request.relationships[0].source.record_id == "a"
    assert request.relationships[0].target.record_id == "b"


@pytest.mark.asyncio
async def test_ingest_torrents_maps_torrent_tracker_category(ingest):
    service, transport = ingest
    res = await ingest_torrents(
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
        ingest=service,
    )
    # 1 torrent + 1 tracker + 1 category = 3 nodes; 2 edges
    assert res == {"nodes": 3, "edges": 2}
    request = transport.requests[0]
    tor = next(
        r for r in request.records if r.record_id == "qbittorrent:Torrent:abc123"
    )
    assert tor.payload["infoHash"] == "abc123"
    assert tor.payload["torrentState"] == "uploading"
    assert tor.payload["shareRatio"] == 2.5
    assert tor.payload["externalToolId"] == "abc123"
    assert any(
        r.record_id == "qbittorrent:Tracker:http://tracker.example/announce"
        for r in request.records
    )
    assert any(
        r.record_id == "qbittorrent:TorrentCategory:linux" for r in request.records
    )
    rel_pairs = {(r.source.record_id, r.target.record_id) for r in request.relationships}
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:Tracker:http://tracker.example/announce",
    ) in rel_pairs
    assert ("qbittorrent:Torrent:abc123", "qbittorrent:TorrentCategory:linux") in rel_pairs


@pytest.mark.asyncio
async def test_ingest_torrents_dedupes_shared_tracker_and_category(ingest):
    service, _transport = ingest
    res = await ingest_torrents(
        [
            {"hash": "h1", "name": "a", "category": "x", "tracker": "udp://tk/a"},
            {"hash": "h2", "name": "b", "category": "x", "tracker": "udp://tk/a"},
        ],
        ingest=service,
    )
    # 2 torrents + 1 shared tracker + 1 shared category = 4 nodes; 4 edges
    assert res == {"nodes": 4, "edges": 4}


@pytest.mark.asyncio
async def test_ingest_torrents_skips_records_without_hash(ingest):
    service, transport = ingest
    res = await ingest_torrents([{"name": "no-hash"}], ingest=service)
    assert res is None
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_documents_writes_document_nodes(ingest):
    service, transport = ingest
    res = await ingest_documents(
        [{"id": "qbittorrent:Document:1", "text": "hello", "title": "T"}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert transport.requests[0].records[0].record_id == "qbittorrent:Document:1"


@pytest.mark.asyncio
async def test_ingest_noops_without_engine():
    # No injected service + no reachable engine -> clean no-op (best-effort surface).
    assert await ingest_entities([{"id": "a", "node_type": "Torrent"}]) is None


@pytest.mark.asyncio
async def test_ingest_rejects_retired_structural_alias_as_noop(ingest):
    # qbittorrent_agent's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating IngestError.
    service, transport = ingest
    assert await ingest_entities([{"id": "a", "type": "Torrent"}], ingest=service) is None
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_empty_is_noop(ingest):
    service, _transport = ingest
    assert await ingest_entities([], ingest=service) is None
    assert await ingest_torrents([], ingest=service) is None
    assert await ingest_documents([], ingest=service) is None
