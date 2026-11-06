---
name: qbittorrent-download-client
skill_type: skill
description: >-
  Keep qBittorrent working as the download client of the arr media apps through the qbittorrent-mcp connector: diagnose login failures and IP bans, and provision each app's category. Use when Radarr, Sonarr, Lidarr or Chaptarr report the client unavailable or a new app needs a category. Do NOT use to change the apps' own settings (arr-mcp `arr-repair-download-client`).
license: MIT
tags: [qbittorrent, torrent, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# qBittorrent as the Media Apps' Download Client

Use the typed tools of the `qbittorrent-mcp` connector: one tool per qBittorrent WebUI API operation, named `qbittorrent_<scope>_<action>` (for example `qbittorrent_torrents_info`). Each tool takes typed parameters; there is no `action` or `params_json` routing. A failed call raises with qBittorrent's own reason.

## Where the data lives

- **qBittorrent** (`qbittorrent_*` tools, `QBITTORRENT_URL`): the torrent client: completed downloads in the default save path `/downloads/complete`, incomplete ones in `/downloads/incomplete`; one category per consuming app (`radarr`, `sonarr`, `lidarr`, `chaptarr`, `prowlarr`), each a sub-folder the app imports from.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://qbittorrent-mcp/qbittorrent-contracts.ttl`, `qbt:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Diagnose an app that cannot reach qBittorrent (`qbittorrent-diagnose-app-connection`)

When an arr app reports its qBittorrent client unavailable, read the login failures and bans in the log and the WebUI auth settings, then hand the fix to the arr-mcp `arr-repair-download-client` workflow.

1. `qbittorrent_log_main` (`normal` = false, `info` = false, `warning` = true, `critical` = false) — `WebAPI login failure ... invalid credentials` names the caller IP and user; `IP has been banned` means five failures locked it out for `web_ui_ban_duration` seconds.
2. `qbittorrent_app_preferences` — `web_ui_max_auth_fail_count`, `web_ui_ban_duration`, `bypass_local_auth`, `bypass_auth_subnet_whitelist_enabled`.
3. `qbittorrent_torrents_categories` — Each consuming app's category exists.

### Provision a category for a consuming app (`qbittorrent-provision-app-category`)

Create the category an arr app sends its downloads to, so they land in the app's import folder.

1. `qbittorrent_torrents_categories` — Skip if the app's category exists.
2. `qbittorrent_app_default_save_path` — Category folders sit under the default save path.
3. `qbittorrent_torrents_create_category` (`category` = the app name (radarr, sonarr, lidarr, chaptarr)) — Approval required: creates the category (`savePath` empty = default path plus the category name).
4. `qbittorrent_torrents_categories` — Confirm it lists.

Needs approval: `qbittorrent_torrents_create_category`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, change limits or preferences, or add torrents need the operator's approval first; pass `confirm=true` only after it.
- Never delete a torrent's downloaded files, a real category or a real tag; only remove test objects named `zz-validation-<date>` that this run created.
- Never change preferences, credentials, the API key, or shut qBittorrent down without the operator's approval; read secrets from the credential store and never print them.
- Never add a torrent the operator or a linked app did not ask for.
- Identify a torrent by its info hash, never by its position in a list.
- Report a tool refusal or HTTP error as it is (the error carries qBittorrent's reason); never retry past a refusal or invent a result.
