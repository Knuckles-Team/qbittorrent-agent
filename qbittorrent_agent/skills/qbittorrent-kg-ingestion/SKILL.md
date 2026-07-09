---
name: qbittorrent-kg-ingestion
skill_type: skill
description: >-
  Natively ingest qBittorrent torrents into the epistemic-graph knowledge graph as
  typed :Torrent nodes (plus :Tracker and :TorrentCategory nodes with :announcesTo /
  :inCategory links) via the qbittorrent-agent MCP server's qbittorrent_ingest_torrents
  tool. Use when the agent must record the current torrent inventory in the KG, make
  torrents queryable alongside other sources, or refresh the graph after adds/deletes.
  Do NOT use to add/control torrents (use qbittorrent-torrent-lifecycle) or to change
  speed/ratio limits (use qbittorrent-transfer-tuning).
license: MIT
tags: [qbittorrent, knowledge-graph, ingestion, torrent, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# qBittorrent KG Ingestion

Push the live qBittorrent torrent inventory into the ONE epistemic-graph knowledge
graph as **typed OWL nodes** — `:Torrent`, `:Tracker`, `:TorrentCategory` — with
`:announcesTo` and `:inCategory` links, so torrents are queryable next to every other
ingested source. Backed by `qbittorrent_agent.kg_ingest` (CONCEPT:AU-KG.ingest.enterprise-source-extractor).

## When to use
- Record the current torrent list in the KG (one call lists + pushes).
- Refresh graph state after adding, deleting, or recategorizing torrents.
- Make torrents / their trackers / categories available to cross-source KG queries.

## When NOT to use
- Adding, pausing, deleting, or organizing torrents → `qbittorrent-torrent-lifecycle`.
- Bandwidth / ratio / seeding limits → `qbittorrent-transfer-tuning`.
- Ad-hoc reads you don't want persisted → the plain `qbittorrent_torrents` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`qbittorrent-agent`** MCP server.
Ingestion is **best-effort**: with no reachable epistemic-graph engine the tool
returns `{"ingested": null}` and is a clean no-op — the connector still works.

| Variable | Required | Notes |
|----------|----------|-------|
| `QBITTORRENT_URL` | ✅ | WebUI base URL (default `http://localhost:8080`) |
| `QBITTORRENT_USERNAME` | ✅ | WebUI user (default `admin`) |
| `QBITTORRENT_PASSWORD` | ✅ | WebUI password |
| `QBITTORRENT_SSL_VERIFY` | optional | TLS verification toggle (alias `QBITTORRENT_AGENT_VERIFY`) |

## Tools & actions
| Tool | Purpose |
|------|---------|
| `qbittorrent_ingest_torrents` | List torrents via the API and push them into the KG as typed nodes + links. |

### Key parameters
- `params_json` — a **JSON string** of `get_torrents` filters forwarded to the list
  call (all optional): `filter`, `category`, `tag`, `sort`, `limit`, `offset`,
  `hashes`. Empty `{}` ingests every torrent.

### Mapping (records → graph)
- torrent → `:Torrent` id `qbittorrent:Torrent:<hash>` (infoHash, name, torrentState,
  progress, shareRatio, sizeBytes, savePath, tags).
- primary `tracker` URL → `:Tracker` id `qbittorrent:Tracker:<url>` + `:announcesTo`.
- `category` → `:TorrentCategory` id `qbittorrent:TorrentCategory:<name>` + `:inCategory`.

## Recipes (`params_json`)
Ingest every torrent:
```json
{}
```
Ingest only a category into the KG:
```json
{"category":"linux-isos"}
```
Ingest just the completed/seeding torrents:
```json
{"filter":"completed"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- The return is `{"listed": N, "ingested": {"nodes": n, "edges": m}}`; `ingested:null`
  means no engine was reachable (expected in a zero-infra run), not a failure.
- Node ids are keyed on the **info hash** / tracker URL / category name, so re-running
  is idempotent (MERGE-by-id) — safe to call on a schedule.
- The full-detail per-torrent tracker list comes from `qbittorrent_torrents`
  `get_torrent_trackers`; this tool records only the torrent's **primary** announce
  URL for the `:announcesTo` link.

## Related
- `qbittorrent-torrent-lifecycle` / `qbittorrent-transfer-tuning` — the operational tools.
- Ontology: `qbittorrent_agent/ontology/qbittorrent.ttl` (federated into the KG hub).
- **Prompt:** composed by the `qbittorrent_torrent_specialist` prompt.
