# Qbittorrent Transfer Tuning

Tune qBittorrent throughput and seeding policy via the qbittorrent-agent MCP server — global and per-torrent download/upload speed limits, share limits (ratio + seeding-time), the alternate speed-limits (scheduler) mode, and transfer/session stats. Use when the agent must throttle or uncap bandwidth, enforce a seed ratio or seeding-time before stopping, flip alternate speed limits, or read live transfer speeds. Do NOT use to add/pause/delete torrents (use qbittorrent-torrent-lifecycle) or to ingest state into the KG (use qbittorrent-kg-ingestion).

# qBittorrent Transfer Tuning

Domain-typed access to qBittorrent's **transfer** surface (`transfer/*`) plus the
per-torrent limit actions on `torrents/*`, for bandwidth shaping and seeding policy.

## When to use
- Set or read the **global** download/upload speed caps.
- Set **per-torrent** download/upload limits.
- Enforce **share limits** — a max ratio and/or seeding-time before a torrent stops.
- Toggle / read the **alternate speed limits** (scheduler) mode.
- Read live global transfer info (speeds, session totals, connection status).

## When NOT to use
- Adding, pausing, deleting, categorizing torrents → `qbittorrent-torrent-lifecycle`.
- Writing torrents/trackers into the knowledge graph → `qbittorrent-kg-ingestion`.
- Editing the full preferences blob (proxy, scheduler days/hours) → the
  `qbittorrent_app` tool's `set_preferences` action.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`qbittorrent-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `QBITTORRENT_URL` | ✅ | WebUI base URL (default `[configured-endpoint]`) |
| `QBITTORRENT_USERNAME` | ✅ | WebUI user |
| `QBITTORRENT_PASSWORD` | ✅ | WebUI password |
| `TLS_PROFILE` / `TLS_PROFILES_REF` | optional | Named runtime trust profile and secret-backed catalog; verification is mandatory |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface vs. the
one-to-one verbose tools.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `qbittorrent_transfer` | `get_global_transfer_info`, `get_speed_limits_mode`, `toggle_speed_limits_mode`, `get_global_download_limit`, `set_global_download_limit`, `get_global_upload_limit`, `set_global_upload_limit`, `ban_peers` |
| `qbittorrent_torrents` | `get_torrent_download_limit`, `set_torrent_download_limit`, `get_torrent_upload_limit`, `set_torrent_upload_limit`, `set_torrent_share_limit` |

### Key parameters
- `limit` — speed cap in **bytes/second**; `0` means unlimited.
- `hashes` — target torrent(s) for the per-torrent limit actions (`"all"` allowed).
- `set_torrent_share_limit` — `ratio_limit` (float; `-1` unlimited, `-2` global),
  `seeding_time_limit` (minutes; `-1`/`-2` same convention), optional
  `inactive_seeding_time_limit`.

## Recipes (`params_json`)
Cap global download at 5 MiB/s (`qbittorrent_transfer` → `set_global_download_limit`):
```json
{"limit":5242880}
```
Uncap global upload (`set_global_upload_limit`):
```json
{"limit":0}
```
Stop a torrent after ratio 2.0 or 3 days of seeding
(`qbittorrent_torrents` → `set_torrent_share_limit`):
```json
{"hashes":"8c212779b4abde7c6bc608063a0d008b7e40ce32","ratio_limit":2.0,"seeding_time_limit":4320}
```
Throttle one torrent's upload to 512 KiB/s (`set_torrent_upload_limit`):
```json
{"hashes":"8c212779b4abde7c6bc608063a0d008b7e40ce32","limit":524288}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Limits are **bytes/second**, not bits or KiB — convert before sending (5 MiB/s =
  `5242880`). `0` = unlimited, not "stop".
- Share-limit sentinels: `-1` = unlimited, `-2` = use the global setting. A plain
  `0` ratio means "stop immediately once seeding starts".
- `toggle_speed_limits_mode` is a **toggle**, not a setter — read
  `get_speed_limits_mode` (0 = normal, 1 = alternate) first if you need a specific
  state.
- Alternate limits only take effect for the whole client, not per-torrent.

## Related
- `qbittorrent-torrent-lifecycle` — add/control/organize torrents.
- `qbittorrent-kg-ingestion` — record transfer/seeding state in the KG.
- **Prompt:** composed by the `qbittorrent_torrent_specialist` prompt.
