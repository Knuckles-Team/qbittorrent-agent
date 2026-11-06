# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [3.0.0] - 2026-11-06

### Changed
- Every qBittorrent WebUI API operation (121, from the 5.2.4 controllers) is one typed tool `qbittorrent_<scope>_<action>`, written by `scripts/generate_api_client.py`. Tool names follow the upstream operations.
- `qbittorrent_ingest_torrents` takes typed `filter`, `category`, `tag` and `limit`.
- Require `scion-sdk>=0.8.2,<0.9`.

### Removed
- The action-routed tools and the tools for `torrents/pause` and `torrents/resume`, which qBittorrent 5.x removed (use `qbittorrent_torrents_stop` / `qbittorrent_torrents_start`).
- The `torrent_specialist` prompt.

### Fixed
- A failed call raises `QbittorrentApiError` with qBittorrent's reason instead of reporting success.
- Every tool answers a JSON object.

### Added
- WebUI API-key (bearer) authentication when `QBITTORRENT_API_KEY` holds a qBittorrent 5.2 key.
- Skills with 9 tool-use contracts, four agent-definition prompts (`torrent_operator`, `torrent_download_monitor`, `seeding_manager`, `download_client_steward`), and an ontology of the instance, save paths, per-app categories, routing and federation with the arr apps, rolled up to medulla core.

## [2.3.10] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.8] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

## [0.1.7] - 2026-04-29

### Added
- Initial release
