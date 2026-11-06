---
name: qbittorrent-kg-ingestion
skill_type: skill
description: >-
  Ingest qBittorrent torrents into the knowledge graph through the qbittorrent-mcp connector as typed Torrent, Tracker and Category nodes. Use when the torrent inventory must be queryable with other sources. Do NOT use to change torrents.
license: MIT
tags: [qbittorrent, torrent, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# qBittorrent Knowledge-Graph Ingestion

Use the typed tools of the `qbittorrent-mcp` connector: one tool per qBittorrent WebUI API operation, named `qbittorrent_<scope>_<action>` (for example `qbittorrent_torrents_info`). Each tool takes typed parameters; there is no `action` or `params_json` routing. A failed call raises with qBittorrent's own reason.

## Where the data lives

- **qBittorrent** (`qbittorrent_*` tools, `QBITTORRENT_URL`): the torrent client: completed downloads in the default save path `/downloads/complete`, incomplete ones in `/downloads/incomplete`; one category per consuming app (`radarr`, `sonarr`, `lidarr`, `chaptarr`, `prowlarr`), each a sub-folder the app imports from.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://qbittorrent-mcp/qbittorrent-contracts.ttl`, `qbt:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Ingest torrents into the knowledge graph (`qbittorrent-ingest-torrents`)

Count the torrents and push them, with trackers and categories, into the knowledge graph.

1. `qbittorrent_torrents_count` — How many torrents the ingest will list.
2. `qbittorrent_ingest_torrents` (`filter` = operator input or none) — Lists torrents through `qbittorrent_torrents_info` and writes typed nodes; returns `listed` and `ingested`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, change limits or preferences, or add torrents need the operator's approval first; pass `confirm=true` only after it.
- Never delete a torrent's downloaded files, a real category or a real tag; only remove test objects named `zz-validation-<date>` that this run created.
- Never change preferences, credentials, the API key, or shut qBittorrent down without the operator's approval; read secrets from the credential store and never print them.
- Never add a torrent the operator or a linked app did not ask for.
- Identify a torrent by its info hash, never by its position in a list.
- Report a tool refusal or HTTP error as it is (the error carries qBittorrent's reason); never retry past a refusal or invent a result.
