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

*Version: 0.30.0*

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
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the AI agent for qBittorrent management, RSS automation, and search. API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **App** | `APP_TOOL` | `True` | Manage qbittorrent app operations. Action-routed methods: `get_api_version`, `get_application_version`, `get_build_info`, `get_default_save_path`, `get_preferences`, `set_preferences`, `shutdown_application`. |
| **Log** | `LOG_TOOL` | `True` | Manage qbittorrent log operations. Action-routed methods: `get_main_log`, `get_peer_log`. |
| **Sync** | `SYNC_TOOL` | `True` | Manage qbittorrent sync operations. Action-routed methods: `get_main_data`, `get_torrent_peers_data`. |
| **Transfer** | `TRANSFER_TOOL` | `True` | Manage qbittorrent transfer operations. Action-routed methods: `ban_peers`, `get_global_download_limit`, `get_global_transfer_info`, `get_global_upload_limit`, `get_speed_limits_mode`, `set_global_download_limit`, `set_global_upload_limit`, `toggle_speed_limits_mode`. |
| **Torrents** | `TORRENTS_TOOL` | `True` | Manage qbittorrent torrents operations. Action-routed methods: `add_new_category`, `add_new_torrent`, `add_peers`, `add_torrent_tags`, `add_trackers_to_torrent`, `bottom_torrent_priority`, `create_tags`, `decrease_torrent_priority`, `delete_tags`, `delete_torrents`, `edit_category`, `edit_tracker`, `get_all_categories`, `get_all_tags`, `get_torrent_contents`, `get_torrent_download_limit`, `get_torrent_list`, `get_torrent_piece_hashes`, `get_torrent_piece_states`, `get_torrent_properties`, `get_torrent_trackers`, `get_torrent_upload_limit`, `get_torrent_webseeds`, `increase_torrent_priority`, `pause_torrents`, `reannounce_torrents`, `recheck_torrents`, `remove_categories`, `remove_torrent_tags`, `remove_trackers`, `rename_file`, `rename_folder`, `resume_torrents`, `set_auto_management`, `set_file_priority`, `set_force_start`, `set_super_seeding`, `set_torrent_category`, `set_torrent_download_limit`, `set_torrent_location`, `set_torrent_name`, `set_torrent_share_limit`, `set_torrent_upload_limit`, `toggle_first_last_piece_priority`, `toggle_sequential_download`, `top_torrent_priority`. |
| **Rss** | `RSS_TOOL` | `True` | Manage qbittorrent rss operations. Action-routed methods: `add_rss_feed`, `add_rss_folder`, `get_all_rss_articles_matching_rule`, `get_all_rss_auto_downloading_rules`, `get_all_rss_items`, `mark_rss_as_read`, `move_rss_item`, `refresh_rss_item`, `remove_rss_auto_downloading_rule`, `remove_rss_item`, `rename_rss_auto_downloading_rule`, `set_rss_auto_downloading_rule`. |
| **Search** | `SEARCH_TOOL` | `True` | Manage qbittorrent search operations. Action-routed methods: `delete_search`, `enable_search_plugin`, `get_search_plugins`, `get_search_results`, `get_search_status`, `install_search_plugin`, `start_search`, `stop_search`, `uninstall_search_plugin`, `update_search_plugins`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "qbittorrent-agent",
        "qbittorrent-mcp"
      ],
      "env": {
        "QBITTORRENT_HOST": "your_qbittorrent_host_here",
        "QBITTORRENT_PORT": "your_qbittorrent_port_here",
        "QBITTORRENT_USERNAME": "your_qbittorrent_username_here",
        "QBITTORRENT_PASSWORD": "your_qbittorrent_password_here",
        "QBITTORRENT_API_KEY": "your_qbittorrent_api_key_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "qbittorrent-agent",
        "qbittorrent-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "QBITTORRENT_HOST": "your_qbittorrent_host_here",
        "QBITTORRENT_PORT": "your_qbittorrent_port_here",
        "QBITTORRENT_USERNAME": "your_qbittorrent_username_here",
        "QBITTORRENT_PASSWORD": "your_qbittorrent_password_here",
        "QBITTORRENT_API_KEY": "your_qbittorrent_api_key_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "url": "http://localhost:8000/qbittorrent-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name qbittorrent-agent-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e QBITTORRENT_HOST="your_value" \
  -e QBITTORRENT_PORT="your_value" \
  -e QBITTORRENT_USERNAME="your_value" \
  -e QBITTORRENT_PASSWORD="your_value" \
  -e QBITTORRENT_API_KEY="your_value" \
  knucklessg1/qbittorrent-agent:latest
```

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`qbittorrent-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/qbittorrent-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://qbittorrent-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export QBITTORRENT_HOST="your_value"
export QBITTORRENT_PORT="your_value"
export QBITTORRENT_USERNAME="your_value"
export QBITTORRENT_PASSWORD="your_value"
export QBITTORRENT_API_KEY="your_value"

# Run the agent server
qbittorrent-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  qbittorrent-agent-mcp:
    image: knucklessg1/qbittorrent-agent:latest
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
      - "8000:8000"
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
    image: knucklessg1/qbittorrent-agent:latest
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
      - "9004:9004"
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

---

## Environment Variables

The agent and MCP server can be fully configured using the following environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| **`QBITTORRENT_HOST`** | String | `None` | **Required**. Hostname or IP address of the qBittorrent Web UI server. |
| **`QBITTORRENT_PORT`** | Integer | `8080` | Port of the qBittorrent Web UI server. |
| **`QBITTORRENT_USERNAME`** | String | `None` | Username for authentication. |
| **`QBITTORRENT_PASSWORD`** | String | `None` | Password for authentication. |
| **`QBITTORRENT_API_KEY`** | String | `None` | Optional API Key for credential-less authentication. |
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
| **`AUTH_TYPE`** | String | `none` | Security authentication mode (`none`, `oidc`). |
| **`POLICY_MODE`** | String | `none` | Eunomia policy enforcement mode (`none`, `embedded`, `remote`). |
| **`LOGFIRE_TOKEN`** | String | `None` | Optional telemetry token to export metrics/logs to Logfire. |

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install qbittorrent-agent[all]

# Using standard pip
python -m pip install qbittorrent-agent[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
