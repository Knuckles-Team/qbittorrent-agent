# qBittorrent Manager - A2A | AG-UI | MCP

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

*Version: 0.11.0*

## Overview

**qBittorrent Manager MCP Server + A2A Agent**

AI agent for qBittorrent management, RSS automation, and search.

This repository is actively maintained - Contributions are welcome!

## MCP

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `QBITTORRENT_URL`: The URL of the target service.
*   `QBITTORRENT_PASSWORD`: The API token or access token.

#### Run in stdio mode (default):
```bash
export QBITTORRENT_URL="http://localhost:8080"
export QBITTORRENT_PASSWORD="your_token"
qbittorrent-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export QBITTORRENT_URL="http://localhost:8080"
export QBITTORRENT_PASSWORD="your_token"
qbittorrent-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

## A2A Agent

### Run A2A Server
```bash
export QBITTORRENT_URL="http://localhost:8080"
export QBITTORRENT_PASSWORD="your_token"
qbittorrent-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Docker

### Build

```bash
docker build -t qbittorrent-agent .
```

### Run MCP Server

```bash
docker run -d \
  --name qbittorrent-agent \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e QBITTORRENT_URL="http://your-service:8080" \
  -e QBITTORRENT_PASSWORD="your_token" \
  knucklessg1/qbittorrent-agent:latest
```

### Deploy with Docker Compose

```yaml
services:
  qbittorrent-agent:
    image: knucklessg1/qbittorrent-agent:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - QBITTORRENT_URL=http://your-service:8080
      - QBITTORRENT_PASSWORD=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "qbittorrent": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "qbittorrent-agent",
        "qbittorrent-mcp"
      ],
      "env": {
        "QBITTORRENT_URL": "http://your-service:8080",
        "QBITTORRENT_PASSWORD": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install qbittorrent-agent
```
```bash
uv pip install qbittorrent-agent
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## MCP Configuration Examples

### 1. Standard IO (stdio) Deployment

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uv",
      "args": [
        "run",
        "qbittorrent-mcp"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "QBITTORRENT_AGENT_VERIFY": "<YOUR_QBITTORRENT_AGENT_VERIFY>",
        "QBITTORRENT_PASSWORD": "<YOUR_QBITTORRENT_PASSWORD>",
        "QBITTORRENT_URL": "<YOUR_QBITTORRENT_URL>",
        "QBITTORRENT_USERNAME": "<YOUR_QBITTORRENT_USERNAME>"
      }
    }
  }
}
```

### 2. Streamable HTTP (SSE) Deployment

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uv",
      "args": [
        "run",
        "qbittorrent-mcp",
        "--transport",
        "http",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "QBITTORRENT_AGENT_VERIFY": "<YOUR_QBITTORRENT_AGENT_VERIFY>",
        "QBITTORRENT_PASSWORD": "<YOUR_QBITTORRENT_PASSWORD>",
        "QBITTORRENT_URL": "<YOUR_QBITTORRENT_URL>",
        "QBITTORRENT_USERNAME": "<YOUR_QBITTORRENT_USERNAME>"
      }
    }
  }
}
```

## Available MCP Tools

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

| Tool Name | Description |
|-----------|-------------|
| `qbittorrent_app` | Consolidated Action-Routed tool for app. Methods: get_application_version, get_api_version, get_build_info, shutdown_application, get_preferences, set_preferences, get_default_save_path |
| `qbittorrent_log` | Consolidated Action-Routed tool for log. Methods: get_main_log, get_peer_log |
| `qbittorrent_rss` | Consolidated Action-Routed tool for rss. Methods: add_rss_folder, add_rss_feed, remove_rss_item, move_rss_item, get_all_rss_items, mark_rss_as_read, refresh_rss_item, set_rss_auto_downloading_rule, rename_rss_auto_downloading_rule, remove_rss_auto_downloading_rule, get_all_rss_auto_downloading_rules, get_all_rss_articles_matching_rule |
| `qbittorrent_search` | Consolidated Action-Routed tool for search. Methods: start_search, stop_search, get_search_status, get_search_results, delete_search, get_search_plugins, install_search_plugin, uninstall_search_plugin, enable_search_plugin, update_search_plugins |
| `qbittorrent_sync` | Consolidated Action-Routed tool for sync. Methods: get_main_data, get_torrent_peers_data |
| `qbittorrent_torrents` | Consolidated Action-Routed tool for torrents. Methods: get_torrent_list, get_torrent_properties, get_torrent_trackers, get_torrent_webseeds, get_torrent_contents, get_torrent_piece_states, get_torrent_piece_hashes, pause_torrents, resume_torrents, delete_torrents, recheck_torrents, reannounce_torrents, edit_tracker, remove_trackers, add_peers, add_new_torrent, add_trackers_to_torrent, increase_torrent_priority, decrease_torrent_priority, top_torrent_priority, bottom_torrent_priority, set_file_priority, get_torrent_download_limit, set_torrent_download_limit, set_torrent_share_limit, get_torrent_upload_limit, set_torrent_upload_limit, set_torrent_location, set_torrent_name, set_torrent_category, get_all_categories, add_new_category, edit_category, remove_categories, add_torrent_tags, remove_torrent_tags, get_all_tags, create_tags, delete_tags, set_auto_management, toggle_sequential_download, toggle_first_last_piece_priority, set_force_start, set_super_seeding, rename_file, rename_folder |
| `qbittorrent_transfer` | Consolidated Action-Routed tool for transfer. Methods: get_global_transfer_info, get_speed_limits_mode, toggle_speed_limits_mode, get_global_download_limit, set_global_download_limit, get_global_upload_limit, set_global_upload_limit, ban_peers |
