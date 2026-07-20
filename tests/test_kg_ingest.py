"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_torrents`` seam with a fake engine
client (no engine required), asserting the single-transaction node/edge staging and commit and the
qBittorrent torrent → :Torrent/:Tracker/:TorrentCategory mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from qbittorrent_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_torrents,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Torrent", "name": "t"},
            {"id": "b", "node_type": "Tracker"},
        ],
        [{"source": "a", "target": "b", "relationship": "announcesTo"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "qbittorrent-agent"
    assert c.txn.nodes["a"]["domain"] == "qbittorrent"
    assert c.txn.edges == [("a", "b", {"relationship": "announcesTo"})]


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
        graph="__commons__",
    )
    # 1 torrent + 1 tracker + 1 category = 3 nodes; 2 edges
    assert res == {"nodes": 3, "edges": 2}
    tor = c.txn.nodes["qbittorrent:Torrent:abc123"]
    assert tor["node_type"] == "Torrent"
    assert tor["infoHash"] == "abc123"
    assert tor["torrentState"] == "uploading"
    assert tor["shareRatio"] == 2.5
    assert tor["externalToolId"] == "abc123"
    assert (
        c.txn.nodes["qbittorrent:Tracker:http://tracker.example/announce"]["node_type"]
        == "Tracker"
    )
    assert c.txn.nodes["qbittorrent:TorrentCategory:linux"]["node_type"] == "TorrentCategory"
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:Tracker:http://tracker.example/announce",
        {"relationship": "announcesTo"},
    ) in c.txn.edges
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:TorrentCategory:linux",
        {"relationship": "inCategory"},
    ) in c.txn.edges


def test_ingest_torrents_dedupes_shared_tracker_and_category():
    c = _FakeClient()
    res = ingest_torrents(
        [
            {"hash": "h1", "name": "a", "category": "x", "tracker": "udp://tk/a"},
            {"hash": "h2", "name": "b", "category": "x", "tracker": "udp://tk/a"},
        ],
        client=c,
        graph="__commons__",
    )
    # 2 torrents + 1 shared tracker + 1 shared category = 4 nodes; 4 edges
    assert res == {"nodes": 4, "edges": 4}


def test_ingest_torrents_skips_records_without_hash():
    c = _FakeClient()
    res = ingest_torrents([{"name": "no-hash"}], client=c, graph="__commons__")
    assert res is None


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "qbittorrent:Document:1", "text": "hello", "title": "T"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["qbittorrent:Document:1"]
    assert node["node_type"] == "Document"
    assert node["text"] == "hello"


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "Torrent"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
