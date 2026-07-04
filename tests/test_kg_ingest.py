"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_torrents`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
qBittorrent torrent → :Torrent/:Tracker/:TorrentCategory mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from qbittorrent_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_torrents,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Torrent", "name": "t"},
            {"id": "b", "type": "Tracker"},
        ],
        [{"source": "a", "target": "b", "type": "announcesTo"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "qbittorrent-agent"
    assert c.txn.nodes["a"]["domain"] == "qbittorrent"
    assert c.edges.edges == [("a", "b", {"type": "announcesTo"})]


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
    assert tor["type"] == "Torrent"
    assert tor["infoHash"] == "abc123"
    assert tor["torrentState"] == "uploading"
    assert tor["shareRatio"] == 2.5
    assert tor["externalToolId"] == "abc123"
    assert (
        c.txn.nodes["qbittorrent:Tracker:http://tracker.example/announce"]["type"]
        == "Tracker"
    )
    assert c.txn.nodes["qbittorrent:TorrentCategory:linux"]["type"] == "TorrentCategory"
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:Tracker:http://tracker.example/announce",
        {"type": "announcesTo"},
    ) in c.edges.edges
    assert (
        "qbittorrent:Torrent:abc123",
        "qbittorrent:TorrentCategory:linux",
        {"type": "inCategory"},
    ) in c.edges.edges


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
    assert node["type"] == "Document"
    assert node["text"] == "hello"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Torrent"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_torrents([], client=_FakeClient()) is None
    assert ingest_documents([], client=_FakeClient()) is None
