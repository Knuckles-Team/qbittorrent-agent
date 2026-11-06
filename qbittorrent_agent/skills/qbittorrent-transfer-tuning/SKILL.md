---
name: qbittorrent-transfer-tuning
skill_type: skill
description: >-
  Check transfer health and tune qBittorrent's speed and seeding limits through the qbittorrent-mcp connector. Use when the agent must read speeds and stalled torrents, or set global speed limits or per-torrent share limits. Do NOT use to add or delete torrents (qbittorrent-torrent-lifecycle).
license: MIT
tags: [qbittorrent, torrent, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# qBittorrent Transfer Tuning

Use the typed tools of the `qbittorrent-mcp` connector: one tool per qBittorrent WebUI API operation, named `qbittorrent_<scope>_<action>` (for example `qbittorrent_torrents_info`). Each tool takes typed parameters; there is no `action` or `params_json` routing. A failed call raises with qBittorrent's own reason.

## Where the data lives

- **qBittorrent** (`qbittorrent_*` tools, `QBITTORRENT_URL`): the torrent client: completed downloads in the default save path `/downloads/complete`, incomplete ones in `/downloads/incomplete`; one category per consuming app (`radarr`, `sonarr`, `lidarr`, `chaptarr`, `prowlarr`), each a sub-folder the app imports from.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://qbittorrent-mcp/qbittorrent-contracts.ttl`, `qbt:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Check transfer health (`qbittorrent-check-transfer-health`)

Read the connection status, speeds and limits, and list stalled and errored torrents with the log reasons.

1. `qbittorrent_transfer_info` — `connection_status` must be `connected`; speeds, totals and DHT nodes.
2. `qbittorrent_transfer_speed_limits_mode` — `1` means the alternative (slower) limits are on.
3. `qbittorrent_torrents_info` (`filter` = "stalled") — Stalled torrents (no peers or no progress).
4. `qbittorrent_torrents_info` (`filter` = "errored") — Errored torrents (missing files, disk errors).
5. `qbittorrent_log_main` (`normal` = false, `info` = false, `warning` = true, `critical` = true) — Warnings and critical messages: failed logins, IP bans, disk and tracker errors.

### Set seeding limits for completed torrents (`qbittorrent-set-share-limits`)

Read completed torrents' ratio and seeding time, and set their share limits with approval.

1. `qbittorrent_torrents_info` (`filter` = "completed") — Completed torrents with `ratio` and `seeding_time`.
2. `qbittorrent_torrents_properties` (`hash` = step1.result[].hash) — One torrent's current share limits.
3. `qbittorrent_torrents_set_share_limits` (`hashes` = step1.result[].hash, `ratio_limit` = operator input, `seeding_time_limit` = operator input, `inactive_seeding_time_limit` = -2, `share_limit_action` = "Default") — Approval required: `ratioLimit`, `seedingTimeLimit`, `inactiveSeedingTimeLimit` (-2 global, -1 none) and `shareLimitAction`.
4. `qbittorrent_torrents_properties` (`hash` = step1.result[].hash) — Confirm the new limits.

Needs approval: `qbittorrent_torrents_set_share_limits`.

### Set global speed limits (`qbittorrent-set-speed-limits`)

Read and set the global download and upload limits with approval.

1. `qbittorrent_transfer_download_limit` — Bytes per second; 0 is unlimited.
2. `qbittorrent_transfer_upload_limit` — Bytes per second; 0 is unlimited.
3. `qbittorrent_transfer_set_download_limit` (`limit` = operator input) — Approval required.
4. `qbittorrent_transfer_set_upload_limit` (`limit` = operator input) — Approval required.
5. `qbittorrent_transfer_info` — Confirm `dl_rate_limit` and `up_rate_limit`.

Needs approval: `qbittorrent_transfer_set_download_limit`, `qbittorrent_transfer_set_upload_limit`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, change limits or preferences, or add torrents need the operator's approval first; pass `confirm=true` only after it.
- Never delete a torrent's downloaded files, a real category or a real tag; only remove test objects named `zz-validation-<date>` that this run created.
- Never change preferences, credentials, the API key, or shut qBittorrent down without the operator's approval; read secrets from the credential store and never print them.
- Never add a torrent the operator or a linked app did not ask for.
- Identify a torrent by its info hash, never by its position in a list.
- Report a tool refusal or HTTP error as it is (the error carries qBittorrent's reason); never retry past a refusal or invent a result.
