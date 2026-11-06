---
name: qbittorrent-torrent-lifecycle
skill_type: skill
description: >-
  Manage the qBittorrent torrent lifecycle through the qbittorrent-mcp connector: list and filter torrents, add a torrent to a category, recover a stalled torrent, and prove category writes with a test category. Use when the agent must add, inspect, reannounce, recheck or organize torrents. Do NOT use for speed or ratio limits (qbittorrent-transfer-tuning) or knowledge-graph ingest (qbittorrent-kg-ingestion).
license: MIT
tags: [qbittorrent, torrent, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# qBittorrent Torrent Lifecycle

Use the typed tools of the `qbittorrent-mcp` connector: one tool per qBittorrent WebUI API operation, named `qbittorrent_<scope>_<action>` (for example `qbittorrent_torrents_info`). Each tool takes typed parameters; there is no `action` or `params_json` routing. A failed call raises with qBittorrent's own reason.

## Where the data lives

- **qBittorrent** (`qbittorrent_*` tools, `QBITTORRENT_URL`): the torrent client: completed downloads in the default save path `/downloads/complete`, incomplete ones in `/downloads/incomplete`; one category per consuming app (`radarr`, `sonarr`, `lidarr`, `chaptarr`, `prowlarr`), each a sub-folder the app imports from.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://qbittorrent-mcp/qbittorrent-contracts.ttl`, `qbt:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Recover a stalled torrent (`qbittorrent-recover-stalled-torrent`)

For one stalled torrent, read its trackers, reannounce, and recheck it if its data may be damaged.

1. `qbittorrent_torrents_info` (`filter` = "stalled") — Pick the stalled torrent by `hash`.
2. `qbittorrent_torrents_trackers` (`hash` = step1.result[].hash) — Tracker status 4 (not working) or a message names the cause.
3. `qbittorrent_torrents_reannounce` (`hashes` = step1.result[].hash) — Ask the trackers for peers again.
4. `qbittorrent_torrents_recheck` (`hashes` = step1.result[].hash) — Approval required: rehashes the data on disk (slow on large torrents).
5. `qbittorrent_torrents_properties` (`hash` = step1.result[].hash) — Confirm peers, seeds and progress after the reannounce.

Needs approval: `qbittorrent_torrents_recheck`.

### Prove category writes with a test category (`qbittorrent-category-roundtrip`)

Create a `zz-validation-<date>` category, confirm it lists, remove it, and confirm it is gone.

1. `qbittorrent_torrents_categories` — The categories before the test.
2. `qbittorrent_torrents_create_category` (`category` = "zz-validation-2026-11-06") — Creates the test category.
3. `qbittorrent_torrents_categories` — The test category lists.
4. `qbittorrent_torrents_remove_categories` (`categories` = "zz-validation-2026-11-06") — Removes only the test category (destructive; `confirm=true`).
5. `qbittorrent_torrents_categories` — The test category is gone.

Needs approval: `qbittorrent_torrents_remove_categories`.

### Add a torrent to a category (`qbittorrent-add-torrent`)

Add a magnet link or URL the operator asked for into the consuming app's category, and confirm it is listed.

1. `qbittorrent_torrents_categories` — The category must exist (one per consuming app).
2. `qbittorrent_torrents_add` (`urls` = operator input, `category` = operator input) — Approval required: adds the torrent.
3. `qbittorrent_torrents_info` (`category` = operator input) — The torrent lists in the category.

Needs approval: `qbittorrent_torrents_add`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, change limits or preferences, or add torrents need the operator's approval first; pass `confirm=true` only after it.
- Never delete a torrent's downloaded files, a real category or a real tag; only remove test objects named `zz-validation-<date>` that this run created.
- Never change preferences, credentials, the API key, or shut qBittorrent down without the operator's approval; read secrets from the credential store and never print them.
- Never add a torrent the operator or a linked app did not ask for.
- Identify a torrent by its info hash, never by its position in a list.
- Report a tool refusal or HTTP error as it is (the error carries qBittorrent's reason); never retry past a refusal or invent a result.
