---
name: qbittorrent-torrent-lifecycle
skill_type: skill
description: >-
  Manage the qBittorrent torrent lifecycle via the qbittorrent-agent MCP server —
  add torrents from magnet/URL/.torrent, list and filter, pause/resume/recheck/
  reannounce, delete (with or without data), and organize with categories and
  tags. Use when the agent must add a download, triage the transfer list, stop or
  resume seeding, prune completed torrents, or (re)categorize/tag them. Do NOT use
  for speed/ratio throttling (use qbittorrent-transfer-tuning), or for pushing
  torrent state into the knowledge graph (use qbittorrent-kg-ingestion).
license: MIT
tags: [qbittorrent, torrent, bittorrent, download, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# qBittorrent Torrent Lifecycle

Domain-typed access to the qBittorrent **torrents** surface (Web API `torrents/*`)
for adding, inspecting, controlling, and organizing torrents. Prefer the condensed
`qbittorrent_torrents` tool — it carries the qBittorrent field conventions and
returns torrent-shaped records.

## When to use
- Add a torrent from a magnet link, HTTP(S) URL, or local `.torrent` file.
- List / filter the transfer list (by state, category, or tag) and read a torrent's
  properties, trackers, or file contents.
- Control a torrent: pause, resume, recheck, reannounce, or delete it.
- Organize: set a category, add/remove tags, move save location, adjust queue priority.

## When NOT to use
- Bandwidth, ratio, or seeding-time limits → `qbittorrent-transfer-tuning`.
- Recording torrents/trackers/categories into the knowledge graph →
  `qbittorrent-kg-ingestion`.
- RSS auto-download rules or plugin search → the `qbittorrent_rss` /
  `qbittorrent_search` tools directly.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`qbittorrent-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `QBITTORRENT_URL` | ✅ | WebUI base URL (default `http://localhost:8080`) |
| `QBITTORRENT_USERNAME` | ✅ | WebUI user (default `admin`) |
| `QBITTORRENT_PASSWORD` | ✅ | WebUI password |
| `QBITTORRENT_SSL_VERIFY` | optional | TLS verification toggle (alias `QBITTORRENT_AGENT_VERIFY`) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (used
below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions (subset) |
|----------------|------------------|
| `qbittorrent_torrents` | `get_torrent_list`, `get_torrent_properties`, `get_torrent_trackers`, `get_torrent_contents`, `add_new_torrent`, `pause_torrents`, `resume_torrents`, `recheck_torrents`, `reannounce_torrents`, `delete_torrents`, `set_torrent_category`, `add_torrent_tags`, `remove_torrent_tags`, `set_torrent_location`, `get_all_categories`, `add_new_category` |

### Key parameters
- `hashes` — one info hash, a `\|`-separated list, or `"all"` (bulk control actions).
- `hash` — single info hash (properties, trackers, contents, rename).
- `urls` — newline-separated magnet/HTTP URLs for `add_new_torrent`; or
  `torrent_files` a list of local `.torrent` paths. Extra add kwargs: `category`,
  `savepath`, `tags`, `paused`.
- `delete_files` — boolean for `delete_torrents`; `false` keeps the data on disk.
- `filter` / `category` / `tag` — narrow `get_torrent_list`.

## Recipes (`params_json`)
List all downloading torrents (name/state/progress via the returned records):
```json
{"filter":"downloading","sort":"progress","reverse":true}
```
Add a magnet into a category, paused:
```json
{"urls":"magnet:?xt=urn:btih:HASH&dn=Example","category":"linux-isos","paused":"true"}
```
Pause then recheck a specific torrent:
```json
{"hashes":"8c212779b4abde7c6bc608063a0d008b7e40ce32"}
```
Delete a torrent but keep the downloaded files:
```json
{"hashes":"8c212779b4abde7c6bc608063a0d008b7e40ce32","delete_files":false}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Info hashes are **lowercase hex**; a wrong-case hash silently matches nothing.
- qBittorrent 5.x renamed pause/resume endpoints to `torrents/stop` / `torrents/start`
  — the client maps `pause_torrents` / `resume_torrents` onto them, so keep using
  those action names.
- `delete_torrents` with `delete_files:true` is irreversible — confirm intent first;
  the default here keeps files.
- `add_new_torrent` returns qBittorrent's terse `Ok.`/`Fails.` body, not the new
  hash — re-list by name/category to confirm the add.

## Related
- `qbittorrent-transfer-tuning` — speed, ratio, and seeding-time limits.
- `qbittorrent-kg-ingestion` — push torrents/trackers/categories into the KG.
- **Prompt:** composed by the `qbittorrent_torrent_specialist` prompt.
