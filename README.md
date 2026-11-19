# Qbittorrent Agent
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/qbittorrent-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/qbittorrent-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/qbittorrent-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/qbittorrent-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/qbittorrent-agent)
![PyPI - License](https://img.shields.io/pypi/l/qbittorrent-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/qbittorrent-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/qbittorrent-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/qbittorrent-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/qbittorrent-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/qbittorrent-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/qbittorrent-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/qbittorrent-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/qbittorrent-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/qbittorrent-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/qbittorrent-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/qbittorrent-agent)

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, and guidance for provisioning the qBittorrent backing service are
> maintained in the [official documentation](https://knuckles-team.github.io/qbittorrent-agent/).

---

## Table of Contents

- [Documentation](#documentation)

- [Overview](#overview)
- [Key Features](#key-features)
- [CLI or API](#cli-or-api)
- [MCP](#mcp)
  - [Available MCP Tools](#available-mcp-tools)
  - [MCP Configuration Examples](#mcp-configuration-examples)
  - [Dynamic Tool Selection & Visibility](#dynamic-tool-selection--visibility)
- [Agent](#agent)
  - [Running the Agent CLI](#running-the-agent-cli)
  - [Docker Compose Orchestration](#docker-compose-orchestration)
- [Environment Variables](#environment-variables)
- [Security & Governance](#security--governance)
  - [Access Control & Policy Enforcement](#access-control--policy-enforcement)
  - [Runtime Security Grid](#runtime-security-grid)
- [Installation](#installation)
- [Repository Owners](#repository-owners)
- [Contribute](#contribute)

---

## Overview

**Qbittorrent Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with AI agent for qBittorrent management, RSS automation, and search..

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/qbittorrent-agent/) and is
the recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/qbittorrent-agent/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/qbittorrent-agent/deployment/) | run the MCP server and A2A agent, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/qbittorrent-agent/usage/) | the MCP tools, the `QbittorrentApi` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/qbittorrent-agent/platform/) | deploy qBittorrent with Docker |
| [Overview](https://knuckles-team.github.io/qbittorrent-agent/overview/) | concept overview and enterprise readiness |
| [Architecture](https://knuckles-team.github.io/qbittorrent-agent/architecture/) | agent, MCP server, layered client |
| [Concepts](https://knuckles-team.github.io/qbittorrent-agent/concepts/) | concept registry (`CONCEPT:QBT-*`) |

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Complete support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the AI agent for qBittorrent management, RSS automation, and search. API. The operator can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server use dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

Every qBittorrent WebUI API operation (121, qBittorrent 5.2.4) is one typed tool, plus `qbittorrent_ingest_torrents` (knowledge-graph ingest). There are no action-routed tools. A failed call raises with qBittorrent's reason.

| Tool | Operation | Description |
|---|---|---|
| `qbittorrent_app_webapi_version` | `GET /api/v2/app/webapiVersion` | Get the WebUI API version. |
| `qbittorrent_app_version` | `GET /api/v2/app/version` | Get the qBittorrent application version. |
| `qbittorrent_app_build_info` | `GET /api/v2/app/buildInfo` | Get build info: Qt, libtorrent, Boost, OpenSSL, zlib versions and bitness. |
| `qbittorrent_app_process_info` | `GET /api/v2/app/processInfo` | Get process info of the running qBittorrent. |
| `qbittorrent_app_shutdown` | `POST /api/v2/app/shutdown` | Shut down the qBittorrent application. |
| `qbittorrent_app_preferences` | `GET /api/v2/app/preferences` | Get all application preferences. |
| `qbittorrent_app_set_preferences` | `POST /api/v2/app/setPreferences` | Set application preferences; only the keys sent change. |
| `qbittorrent_app_default_save_path` | `GET /api/v2/app/defaultSavePath` | Get the default save path. |
| `qbittorrent_app_send_test_email` | `POST /api/v2/app/sendTestEmail` | Send a test email with the configured email notification settings. |
| `qbittorrent_app_get_directory_content` | `GET /api/v2/app/getDirectoryContent` | List the content of a directory on the qBittorrent host. |
| `qbittorrent_app_cookies` | `GET /api/v2/app/cookies` | Get the cookies used for downloading torrents and RSS. |
| `qbittorrent_app_set_cookies` | `POST /api/v2/app/setCookies` | Set the cookies used for downloading torrents and RSS. |
| `qbittorrent_app_rotate_api_key` | `POST /api/v2/app/rotateAPIKey` | Create or replace the WebUI API key. |
| `qbittorrent_app_delete_api_key` | `POST /api/v2/app/deleteAPIKey` | Delete the WebUI API key. |
| `qbittorrent_app_network_interface_list` | `GET /api/v2/app/networkInterfaceList` | List the network interfaces. |
| `qbittorrent_app_network_interface_address_list` | `GET /api/v2/app/networkInterfaceAddressList` | List the addresses of a network interface. |
| `qbittorrent_clientdata_load` | `GET /api/v2/clientdata/load` | Load WebUI client data stored on the server. |
| `qbittorrent_clientdata_store` | `POST /api/v2/clientdata/store` | Store WebUI client data on the server. |
| `qbittorrent_log_main` | `GET /api/v2/log/main` | Get the main log, filtered by severity. |
| `qbittorrent_log_peers` | `GET /api/v2/log/peers` | Get the peer log. |
| `qbittorrent_rss_add_folder` | `POST /api/v2/rss/addFolder` | Add an RSS folder. |
| `qbittorrent_rss_add_feed` | `POST /api/v2/rss/addFeed` | Add an RSS feed. |
| `qbittorrent_rss_set_feed_url` | `POST /api/v2/rss/setFeedURL` | Change the URL of an RSS feed. |
| `qbittorrent_rss_set_feed_refresh_interval` | `GET /api/v2/rss/setFeedRefreshInterval` | Set the refresh interval of an RSS feed. |
| `qbittorrent_rss_remove_item` | `POST /api/v2/rss/removeItem` | Remove an RSS feed or folder. |
| `qbittorrent_rss_move_item` | `POST /api/v2/rss/moveItem` | Move or rename an RSS feed or folder. |
| `qbittorrent_rss_items` | `GET /api/v2/rss/items` | List RSS feeds and folders, optionally with articles. |
| `qbittorrent_rss_mark_as_read` | `POST /api/v2/rss/markAsRead` | Mark an RSS item or article as read. |
| `qbittorrent_rss_refresh_item` | `POST /api/v2/rss/refreshItem` | Refresh an RSS feed or folder. |
| `qbittorrent_rss_set_rule` | `POST /api/v2/rss/setRule` | Create or update an RSS auto-download rule. |
| `qbittorrent_rss_rename_rule` | `POST /api/v2/rss/renameRule` | Rename an RSS auto-download rule. |
| `qbittorrent_rss_remove_rule` | `POST /api/v2/rss/removeRule` | Remove an RSS auto-download rule. |
| `qbittorrent_rss_rules` | `GET /api/v2/rss/rules` | List RSS auto-download rules. |
| `qbittorrent_rss_matching_articles` | `GET /api/v2/rss/matchingArticles` | List the articles that match an RSS auto-download rule. |
| `qbittorrent_search_start` | `POST /api/v2/search/start` | Start a search job with the search plugins. |
| `qbittorrent_search_stop` | `POST /api/v2/search/stop` | Stop a search job. |
| `qbittorrent_search_status` | `GET /api/v2/search/status` | Get the status of one or all search jobs. |
| `qbittorrent_search_results` | `GET /api/v2/search/results` | Get the results of a search job. |
| `qbittorrent_search_delete` | `POST /api/v2/search/delete` | Delete a search job. |
| `qbittorrent_search_download_torrent` | `GET /api/v2/search/downloadTorrent` | Download a torrent found by a search plugin. |
| `qbittorrent_search_plugins` | `GET /api/v2/search/plugins` | List the search plugins. |
| `qbittorrent_search_install_plugin` | `POST /api/v2/search/installPlugin` | Install search plugins from URLs or paths. |
| `qbittorrent_search_uninstall_plugin` | `POST /api/v2/search/uninstallPlugin` | Uninstall search plugins. |
| `qbittorrent_search_enable_plugin` | `POST /api/v2/search/enablePlugin` | Enable or disable search plugins. |
| `qbittorrent_search_update_plugins` | `POST /api/v2/search/updatePlugins` | Update all search plugins. |
| `qbittorrent_sync_maindata` | `GET /api/v2/sync/maindata` | Get the main data changes since a response id (full state when rid is 0). |
| `qbittorrent_sync_torrent_peers` | `GET /api/v2/sync/torrentPeers` | Get the peer data changes of one torrent since a response id. |
| `qbittorrent_torrentcreator_add_task` | `POST /api/v2/torrentcreator/addTask` | Create a torrent from a file or folder on the qBittorrent host. |
| `qbittorrent_torrentcreator_status` | `GET /api/v2/torrentcreator/status` | Get the status of one or all torrent-creator tasks. |
| `qbittorrent_torrentcreator_torrent_file` | `GET /api/v2/torrentcreator/torrentFile` | Get the .torrent file a creator task produced. |
| `qbittorrent_torrentcreator_delete_task` | `POST /api/v2/torrentcreator/deleteTask` | Delete a torrent-creator task. |
| `qbittorrent_torrents_count` | `GET /api/v2/torrents/count` | Count the torrents. |
| `qbittorrent_torrents_info` | `GET /api/v2/torrents/info` | List torrents, filtered and sorted. |
| `qbittorrent_torrents_properties` | `GET /api/v2/torrents/properties` | Get the generic properties of one torrent. |
| `qbittorrent_torrents_trackers` | `GET /api/v2/torrents/trackers` | List the trackers of one torrent. |
| `qbittorrent_torrents_webseeds` | `GET /api/v2/torrents/webseeds` | List the web seeds of one torrent. |
| `qbittorrent_torrents_add_web_seeds` | `POST /api/v2/torrents/addWebSeeds` | Add web seeds to a torrent. |
| `qbittorrent_torrents_edit_web_seed` | `POST /api/v2/torrents/editWebSeed` | Replace a web seed URL of a torrent. |
| `qbittorrent_torrents_remove_web_seeds` | `POST /api/v2/torrents/removeWebSeeds` | Remove web seeds from a torrent. |
| `qbittorrent_torrents_files` | `GET /api/v2/torrents/files` | List the files of one torrent. |
| `qbittorrent_torrents_piece_hashes` | `GET /api/v2/torrents/pieceHashes` | Get the piece hashes of one torrent. |
| `qbittorrent_torrents_piece_states` | `GET /api/v2/torrents/pieceStates` | Get the piece states of one torrent. |
| `qbittorrent_torrents_piece_availability` | `GET /api/v2/torrents/pieceAvailability` | Get the piece availability of one torrent. |
| `qbittorrent_torrents_start` | `POST /api/v2/torrents/start` | Start (resume) torrents. |
| `qbittorrent_torrents_stop` | `POST /api/v2/torrents/stop` | Stop (pause) torrents. |
| `qbittorrent_torrents_recheck` | `POST /api/v2/torrents/recheck` | Recheck torrents. |
| `qbittorrent_torrents_reannounce` | `POST /api/v2/torrents/reannounce` | Reannounce torrents to their trackers. |
| `qbittorrent_torrents_rename` | `POST /api/v2/torrents/rename` | Rename a torrent. |
| `qbittorrent_torrents_set_comment` | `POST /api/v2/torrents/setComment` | Set the comment of torrents. |
| `qbittorrent_torrents_set_category` | `POST /api/v2/torrents/setCategory` | Set the category of torrents. |
| `qbittorrent_torrents_create_category` | `POST /api/v2/torrents/createCategory` | Create a category. |
| `qbittorrent_torrents_edit_category` | `POST /api/v2/torrents/editCategory` | Edit a category's save and download paths. |
| `qbittorrent_torrents_remove_categories` | `POST /api/v2/torrents/removeCategories` | Remove categories. |
| `qbittorrent_torrents_categories` | `GET /api/v2/torrents/categories` | List all categories. |
| `qbittorrent_torrents_add_tags` | `POST /api/v2/torrents/addTags` | Add tags to torrents. |
| `qbittorrent_torrents_set_tags` | `POST /api/v2/torrents/setTags` | Replace the tags of torrents. |
| `qbittorrent_torrents_remove_tags` | `POST /api/v2/torrents/removeTags` | Remove tags from torrents (all tags when none are given). |
| `qbittorrent_torrents_create_tags` | `POST /api/v2/torrents/createTags` | Create tags. |
| `qbittorrent_torrents_delete_tags` | `POST /api/v2/torrents/deleteTags` | Delete tags. |
| `qbittorrent_torrents_tags` | `GET /api/v2/torrents/tags` | List all tags. |
| `qbittorrent_torrents_add` | `POST /api/v2/torrents/add` | Add torrents from URLs, magnet links or uploaded .torrent files. |
| `qbittorrent_torrents_delete` | `POST /api/v2/torrents/delete` | Delete torrents, optionally with their downloaded files. |
| `qbittorrent_torrents_add_trackers` | `POST /api/v2/torrents/addTrackers` | Add trackers to a torrent. |
| `qbittorrent_torrents_edit_tracker` | `POST /api/v2/torrents/editTracker` | Replace a tracker URL of a torrent. |
| `qbittorrent_torrents_remove_trackers` | `POST /api/v2/torrents/removeTrackers` | Remove trackers from a torrent. |
| `qbittorrent_torrents_add_peers` | `POST /api/v2/torrents/addPeers` | Add peers to torrents. |
| `qbittorrent_torrents_file_prio` | `POST /api/v2/torrents/filePrio` | Set the priority of files in a torrent. |
| `qbittorrent_torrents_upload_limit` | `GET /api/v2/torrents/uploadLimit` | Get the upload limit of torrents. |
| `qbittorrent_torrents_download_limit` | `GET /api/v2/torrents/downloadLimit` | Get the download limit of torrents. |
| `qbittorrent_torrents_set_upload_limit` | `POST /api/v2/torrents/setUploadLimit` | Set the upload limit of torrents. |
| `qbittorrent_torrents_set_download_limit` | `POST /api/v2/torrents/setDownloadLimit` | Set the download limit of torrents. |
| `qbittorrent_torrents_set_share_limits` | `POST /api/v2/torrents/setShareLimits` | Set the share (ratio and seeding time) limits of torrents. |
| `qbittorrent_torrents_increase_prio` | `POST /api/v2/torrents/increasePrio` | Raise the queue priority of torrents. |
| `qbittorrent_torrents_decrease_prio` | `POST /api/v2/torrents/decreasePrio` | Lower the queue priority of torrents. |
| `qbittorrent_torrents_top_prio` | `POST /api/v2/torrents/topPrio` | Move torrents to the top of the queue. |
| `qbittorrent_torrents_bottom_prio` | `POST /api/v2/torrents/bottomPrio` | Move torrents to the bottom of the queue. |
| `qbittorrent_torrents_set_location` | `POST /api/v2/torrents/setLocation` | Move the data of torrents to a new location. |
| `qbittorrent_torrents_set_save_path` | `POST /api/v2/torrents/setSavePath` | Set the save path of torrents. |
| `qbittorrent_torrents_set_download_path` | `POST /api/v2/torrents/setDownloadPath` | Set the incomplete-download path of torrents. |
| `qbittorrent_torrents_set_auto_management` | `POST /api/v2/torrents/setAutoManagement` | Turn automatic torrent management on or off. |
| `qbittorrent_torrents_set_super_seeding` | `POST /api/v2/torrents/setSuperSeeding` | Turn super seeding on or off. |
| `qbittorrent_torrents_set_force_start` | `POST /api/v2/torrents/setForceStart` | Turn force start on or off. |
| `qbittorrent_torrents_toggle_sequential_download` | `POST /api/v2/torrents/toggleSequentialDownload` | Toggle sequential download. |
| `qbittorrent_torrents_toggle_first_last_piece_prio` | `POST /api/v2/torrents/toggleFirstLastPiecePrio` | Toggle first and last piece priority. |
| `qbittorrent_torrents_rename_file` | `POST /api/v2/torrents/renameFile` | Rename a file in a torrent. |
| `qbittorrent_torrents_rename_folder` | `POST /api/v2/torrents/renameFolder` | Rename a folder in a torrent. |
| `qbittorrent_torrents_export` | `GET /api/v2/torrents/export` | Export a torrent as a .torrent file. |
| `qbittorrent_torrents_ssl_parameters` | `GET /api/v2/torrents/SSLParameters` | Get the SSL parameters of a torrent. |
| `qbittorrent_torrents_set_ssl_parameters` | `POST /api/v2/torrents/setSSLParameters` | Set the SSL parameters of a torrent. |
| `qbittorrent_torrents_fetch_metadata` | `POST /api/v2/torrents/fetchMetadata` | Fetch the metadata of a magnet link or URL without adding it. |
| `qbittorrent_torrents_parse_metadata` | `POST /api/v2/torrents/parseMetadata` | Parse uploaded .torrent files and return their metadata. |
| `qbittorrent_torrents_save_metadata` | `GET /api/v2/torrents/saveMetadata` | Save fetched metadata as a .torrent file. |
| `qbittorrent_transfer_info` | `GET /api/v2/transfer/info` | Get global transfer info: speeds, totals, connection status. |
| `qbittorrent_transfer_speed_limits_mode` | `GET /api/v2/transfer/speedLimitsMode` | Get whether the alternative speed limits are on. |
| `qbittorrent_transfer_set_speed_limits_mode` | `POST /api/v2/transfer/setSpeedLimitsMode` | Turn the alternative speed limits on (1) or off (0). |
| `qbittorrent_transfer_toggle_speed_limits_mode` | `POST /api/v2/transfer/toggleSpeedLimitsMode` | Toggle the alternative speed limits. |
| `qbittorrent_transfer_upload_limit` | `GET /api/v2/transfer/uploadLimit` | Get the global upload limit. |
| `qbittorrent_transfer_download_limit` | `GET /api/v2/transfer/downloadLimit` | Get the global download limit. |
| `qbittorrent_transfer_set_upload_limit` | `POST /api/v2/transfer/setUploadLimit` | Set the global upload limit. |
| `qbittorrent_transfer_set_download_limit` | `POST /api/v2/transfer/setDownloadLimit` | Set the global download limit. |
| `qbittorrent_transfer_ban_peers` | `POST /api/v2/transfer/banPeers` | Ban peers. |
| `qbittorrent_ingest_torrents` | (connector) | Ingest torrents into the knowledge graph as typed Torrent, Tracker and Category nodes. |

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts smoothly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export QBITTORRENT_URL="<configured-endpoint>"
export QBITTORRENT_USERNAME="your_value"
export QBITTORRENT_PASSWORD="your_value"

# Run the agent server
qbittorrent-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  qbittorrent-agent-mcp:
    init: true
    user: "10001:10001"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    pids_limit: 256
    mem_limit: ${AGENT_CONTAINER_MEMORY_LIMIT:-4g}
    cpus: ${AGENT_CONTAINER_CPU_LIMIT:-2.0}
    tmpfs:
      - /tmp:rw,noexec,nosuid,nodev,size=64m
    image: ${QBITTORRENT_AGENT_MCP_IMAGE:?set-QBITTORRENT_AGENT_MCP_IMAGE-to-image@sha256-digest}
    container_name: qbittorrent-agent-mcp
    hostname: qbittorrent-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "127.0.0.1:8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  qbittorrent-agent-agent:
    init: true
    user: "10001:10001"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    pids_limit: 256
    mem_limit: ${AGENT_CONTAINER_MEMORY_LIMIT:-4g}
    cpus: ${AGENT_CONTAINER_CPU_LIMIT:-2.0}
    tmpfs:
      - /tmp:rw,noexec,nosuid,nodev,size=64m
    image: ${QBITTORRENT_AGENT_AGENT_IMAGE:?set-QBITTORRENT_AGENT_AGENT_IMAGE-to-image@sha256-digest}
    container_name: qbittorrent-agent-agent
    hostname: qbittorrent-agent-agent
    restart: always
    depends_on:
      - qbittorrent-agent-mcp
    env_file:
      - ../.env
    command: [ "qbittorrent-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://qbittorrent-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "127.0.0.1:9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `QBITTORRENT_URL` | — | Unified qBittorrent Web UI base URL. |
| `QBITTORRENT_USERNAME` | — |  |
| `QBITTORRENT_PASSWORD` | secret-injected |  |
| `QBITTORRENT_TLS_PROFILE` | `private-pki` | TLS verification is mandatory (no boolean downgrade). Select a named runtime profile from AgentConfig; falls back to the global TLS_PROFILE if unset. |
| `TLS_PROFILE` | `private-pki` |  |
| `TLS_PROFILES_REF` | `secret://runtime/tls-profiles` |  |
| `APPTOOL` | `True` |  |
| `LOGTOOL` | `True` |  |
| `SYNCTOOL` | `True` |  |
| `TRANSFERTOOL` | `True` |  |
| `TORRENTSTOOL` | `True` |  |
| `RSSTOOL` | `True` |  |
| `SEARCHTOOL` | `True` |  |

#### Inherited scion-sdk variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `intent` | Tool surface: `intent` \| `condensed` \| `verbose` \| `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_24 package + 16 inherited variable(s). Auto-generated from `.env.example` + the shared scion-sdk set — do not edit._
<!-- ENV-VARS-TABLE:END -->


The agent and MCP server can be fully configured using the following environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| **`QBITTORRENT_URL`** | String | Required | Unified qBittorrent Web UI base URL. |
| **`QBITTORRENT_USERNAME`** | String | `None` | Username for authentication. |
| **`QBITTORRENT_PASSWORD`** | String | `None` | Password for authentication. |
| **`TLS_PROFILE`** | String | — | Named `AgentConfig` transport-security profile; verification is mandatory. |
| **`TLS_PROFILES_REF`** | Secret reference | — | Runtime reference for the TLS profile catalog. |
| **`APPTOOL`** | Boolean | `True` | Toggle to enable/disable the App tool module. |
| **`LOGTOOL`** | Boolean | `True` | Toggle to enable/disable the Log tool module. |
| **`SYNCTOOL`** | Boolean | `True` | Toggle to enable/disable the Sync tool module. |
| **`TRANSFERTOOL`** | Boolean | `True` | Toggle to enable/disable the Transfer tool module. |
| **`TORRENTSTOOL`** | Boolean | `True` | Toggle to enable/disable the Torrents tool module. |
| **`RSSTOOL`** | Boolean | `True` | Toggle to enable/disable the RSS tool module. |
| **`SEARCHTOOL`** | Boolean | `True` | Toggle to enable/disable the Search tool module. |
| **`TRANSPORT`** | String | `stdio` | Server transport protocol (`stdio`, `sse`, or `streamable-http`). |
| **`HOST`** | String | `127.0.0.1` | The network interface/IP to bind the server to. |
| **`PORT`** | Integer | `8000` | The port to run the server on when using HTTP-based transports. |
| **`MCP_TOOL_MODE`** | String | `condensed` | Tool surface: `condensed`, `verbose`, or `both`. |
| **`MCP_ENABLED_TOOLS`** / **`MCP_DISABLED_TOOLS`** | String | `None` | Comma-separated tool allow/deny list. |
| **`MCP_ENABLED_TAGS`** / **`MCP_DISABLED_TAGS`** | String | `None` | Comma-separated tag allow/deny list. |
| **`DEBUG`** | Boolean | `False` | Verbose logging. |
| **`PYTHONUNBUFFERED`** | Integer | `1` | Unbuffered stdout (recommended in containers). |
| **`ENABLE_OTEL`** | Boolean | `True` | Enable OpenTelemetry export. |
| **`OTEL_EXPORTER_OTLP_ENDPOINT`** | String | `None` | OTLP collector endpoint. |
| **`OTEL_EXPORTER_OTLP_PUBLIC_KEY`** / **`OTEL_EXPORTER_OTLP_SECRET_KEY`** | String | `None` | OTLP auth keys. |
| **`OTEL_EXPORTER_OTLP_PROTOCOL`** | String | `None` | OTLP protocol (e.g. `http/protobuf`). |
| **`EUNOMIA_TYPE`** | String | `none` | Authorization mode: `none`, `embedded`, `remote`. |
| **`EUNOMIA_POLICY_FILE`** | String | `mcp_policies.json` | Embedded Eunomia policy file. |
| **`EUNOMIA_REMOTE_URL`** | String | `None` | Remote Eunomia server URL. |
| **`MCP_URL`** | String | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to (full `[agent]` runtime only). |
| **`PROVIDER`** | String | `openai` | LLM provider (full `[agent]` runtime only). |
| **`MODEL_ID`** | String | `gpt-4o` | Model id (full `[agent]` runtime only). |
| **`ENABLE_WEB_UI`** | Boolean | `True` | Serve the AG-UI web interface (full `[agent]` runtime only). |

---

## Security & Governance

Built directly upon the enterprise-ready [`scion-sdk`](https://github.com/Knuckles-Team/scion-sdk) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Feature | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Pick the extra that matches what the operator want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `qbittorrent-agent[mcp]` | Connector-focused MCP server (`scion-sdk[mcp]` — FastMCP/FastAPI + `medulla[full]`) | The operator only run the **MCP server** (smallest install / image) |
| `qbittorrent-agent[agent]` | Agent runtime (`scion-sdk[agent,logfire]` — model orchestration + `medulla[full]`) | The operator run the **integrated agent** |
| `qbittorrent-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "qbittorrent-agent[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "qbittorrent-agent[agent]"

# Everything (development)
uv pip install "qbittorrent-agent[all]"      # or: python -m pip install "qbittorrent-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/qbittorrent-agent:mcp` | `--target mcp` | `qbittorrent-agent[mcp]` — **connector-focused**, includes `medulla[full]`; no model-orchestration stack | `qbittorrent-mcp` |
| `example/qbittorrent-agent@sha256:<digest>` | `--target agent` (default) | `qbittorrent-agent[agent]` — **agent runtime**, model orchestration + `medulla[full]` | `qbittorrent-agent` |

```bash
docker build --target mcp   -t example/qbittorrent-agent:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/qbittorrent-agent:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`medulla`)

Both `[mcp]` and `[agent]` carry the **medulla** engine through the required
Meristem core dependency (`medulla[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` also enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**medulla as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[medulla deployment guide](https://knuckles-team.github.io/medulla/deployment/).

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by running local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Run test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `qbittorrent-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx qbittorrent-mcp` · or `uv tool install qbittorrent-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy the pinned `${QBITTORRENT_AGENT_AGENT_IMAGE}` digest (see `docker/agent.compose.yml`) via docker-compose / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, Arbora delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
