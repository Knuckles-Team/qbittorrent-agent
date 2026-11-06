---
name: qbittorrent-agent-operations
skill_type: skill
description: >-
  Operate qBittorrent through the qbittorrent-mcp connector: pick the skill and workflow for a torrent, transfer, download-client or ingest task. Use as the entry point for any qBittorrent request.
license: MIT
tags: [qbittorrent, operations, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# qBittorrent Operations

The connector serves one typed tool per WebUI API operation (`qbittorrent_<scope>_<action>`; scopes `app`, `clientdata`, `log`, `rss`, `search`, `sync`, `torrentcreator`, `torrents`, `transfer`) plus `qbittorrent_ingest_torrents`.

## Where the data lives

- **qBittorrent** (`qbittorrent_*` tools, `QBITTORRENT_URL`): the torrent client: completed downloads in the default save path `/downloads/complete`, incomplete ones in `/downloads/incomplete`; one category per consuming app (`radarr`, `sonarr`, `lidarr`, `chaptarr`, `prowlarr`), each a sub-folder the app imports from.

## Which skill

- `qbittorrent-torrent-lifecycle`: Manage the qBittorrent torrent lifecycle through the qbittorrent-mcp connector: list and filter torrents, add a torrent to a category, recover a stalled torrent, and prove category writes with a test category. Use when the agent must add, inspect, reannounce, recheck or organize torrents. Do NOT use for speed or ratio limits (qbittorrent-transfer-tuning) or knowledge-graph ingest (qbittorrent-kg-ingestion).
- `qbittorrent-transfer-tuning`: Check transfer health and tune qBittorrent's speed and seeding limits through the qbittorrent-mcp connector. Use when the agent must read speeds and stalled torrents, or set global speed limits or per-torrent share limits. Do NOT use to add or delete torrents (qbittorrent-torrent-lifecycle).
- `qbittorrent-download-client`: Keep qBittorrent working as the download client of the arr media apps through the qbittorrent-mcp connector: diagnose login failures and IP bans, and provision each app's category. Use when Radarr, Sonarr, Lidarr or Chaptarr report the client unavailable or a new app needs a category. Do NOT use to change the apps' own settings (arr-mcp `arr-repair-download-client`).
- `qbittorrent-kg-ingestion`: Ingest qBittorrent torrents into the knowledge graph through the qbittorrent-mcp connector as typed Torrent, Tracker and Category nodes. Use when the torrent inventory must be queryable with other sources. Do NOT use to change torrents.

## Workflows (tool-use contracts)

- `qbittorrent-check-transfer-health` (qbittorrent-transfer-tuning): Read the connection status, speeds and limits, and list stalled and errored torrents with the log reasons.
- `qbittorrent-recover-stalled-torrent` (qbittorrent-torrent-lifecycle): For one stalled torrent, read its trackers, reannounce, and recheck it if its data may be damaged.
- `qbittorrent-category-roundtrip` (qbittorrent-torrent-lifecycle): Create a `zz-validation-<date>` category, confirm it lists, remove it, and confirm it is gone.
- `qbittorrent-add-torrent` (qbittorrent-torrent-lifecycle): Add a magnet link or URL the operator asked for into the consuming app's category, and confirm it is listed.
- `qbittorrent-set-share-limits` (qbittorrent-transfer-tuning): Read completed torrents' ratio and seeding time, and set their share limits with approval.
- `qbittorrent-set-speed-limits` (qbittorrent-transfer-tuning): Read and set the global download and upload limits with approval.
- `qbittorrent-diagnose-app-connection` (qbittorrent-download-client): When an arr app reports its qBittorrent client unavailable, read the login failures and bans in the log and the WebUI auth settings, then hand the fix to the arr-mcp `arr-repair-download-client` workflow.
- `qbittorrent-provision-app-category` (qbittorrent-download-client): Create the category an arr app sends its downloads to, so they land in the app's import folder.
- `qbittorrent-ingest-torrents` (qbittorrent-kg-ingestion): Count the torrents and push them, with trackers and categories, into the knowledge graph.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, change limits or preferences, or add torrents need the operator's approval first; pass `confirm=true` only after it.
- Never delete a torrent's downloaded files, a real category or a real tag; only remove test objects named `zz-validation-<date>` that this run created.
- Never change preferences, credentials, the API key, or shut qBittorrent down without the operator's approval; read secrets from the credential store and never print them.
- Never add a torrent the operator or a linked app did not ask for.
- Identify a torrent by its info hash, never by its position in a list.
- Report a tool refusal or HTTP error as it is (the error carries qBittorrent's reason); never retry past a refusal or invent a result.
