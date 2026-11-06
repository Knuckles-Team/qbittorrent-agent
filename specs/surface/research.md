# CONN-QBITTORRENT-AGENT-SURFACE — Research

Governing spec: [spec.md](spec.md).

## Census (2026-11-06)

| Scope | Upstream operations | Tools before | After |
|---|---|---|---|
| app | 16 | 7 | 16 |
| clientdata | 2 | 0 | 2 |
| log | 2 | 2 | 2 |
| rss | 14 | 12 | 14 |
| search | 11 | 10 | 11 |
| sync | 2 | 1 | 2 |
| torrentcreator | 4 | 0 | 4 |
| torrents | 61 | 49 (2 on removed routes) | 61 |
| transfer | 9 | 7 | 9 |
| total | 121 (+2 web sign-in) | 88 | 121, plus `qbittorrent_ingest_torrents` |

## Findings

- A failed call (404, 409) was logged and reported as success.
- `pause` and `resume` called `torrents/pause` and `torrents/resume`, which qBittorrent 5.x removed (now `stop`/`start`).
- The ingest tool took `params_json`, and its preset named the removed `qbittorrent_torrents` action tool.
- The ontology redeclared core `:Torrent` and `:Tracker` and an undeclared `:TorrentCategory`, with no data locations or routing.
- Live: Radarr, Sonarr and Lidarr held a stale qBittorrent password; their retries banned `127.0.0.1` for an hour, so every app reported its download client unavailable. The diagnose contract reads this from the log.
- qBittorrent 5.2 accepts a WebUI API key as a bearer token (no login, no ban); the deployed `QBITTORRENT_API_KEY` is a placeholder, so the client falls back to the session.
