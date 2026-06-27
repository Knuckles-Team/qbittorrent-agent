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

*Version: 0.33.0*

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

This table is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `qbittorrent_app` | `APPTOOL` | Manage qbittorrent app operations. |
| `qbittorrent_log` | `LOGTOOL` | Manage qbittorrent log operations. |
| `qbittorrent_rss` | `RSSTOOL` | Manage qbittorrent rss operations. |
| `qbittorrent_search` | `SEARCHTOOL` | Manage qbittorrent search operations. |
| `qbittorrent_sync` | `SYNCTOOL` | Manage qbittorrent sync operations. |
| `qbittorrent_torrents` | `TORRENTSTOOL` | Manage qbittorrent torrents operations. |
| `qbittorrent_transfer` | `TRANSFERTOOL` | Manage qbittorrent transfer operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>89 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `qbittorrent_add_peers` | `APITOOL` | Add peers. |
| `qbittorrent_add_rss_feed` | `APITOOL` | Add RSS feed. |
| `qbittorrent_add_rss_folder` | `APITOOL` | Add RSS folder. |
| `qbittorrent_add_torrent` | `APITOOL` | Add new torrent. |
| `qbittorrent_add_torrent_tags` | `APITOOL` | Add torrent tags. |
| `qbittorrent_add_trackers` | `APITOOL` | Add trackers to torrent. |
| `qbittorrent_ban_peers` | `APITOOL` | Ban peers. 'peers' is a string of peers separated by \| (host:port). |
| `qbittorrent_bottom_priority` | `APITOOL` | Minimal torrent priority. |
| `qbittorrent_create_category` | `APITOOL` | Add new category. |
| `qbittorrent_create_tags` | `APITOOL` | Create tags. |
| `qbittorrent_decrease_priority` | `APITOOL` | Decrease torrent priority. |
| `qbittorrent_delete_tags` | `APITOOL` | Delete tags. |
| `qbittorrent_delete_torrents` | `APITOOL` | Delete torrents. |
| `qbittorrent_edit_category` | `APITOOL` | Edit category. |
| `qbittorrent_edit_tracker` | `APITOOL` | Edit tracker. |
| `qbittorrent_enable_search_plugin` | `APITOOL` | Enable/disable search plugin. |
| `qbittorrent_get_api_version` | `APITOOL` | Get API version. |
| `qbittorrent_get_build_info` | `APITOOL` | Get build info. |
| `qbittorrent_get_categories` | `APITOOL` | Get all categories. |
| `qbittorrent_get_default_save_path` | `APITOOL` | Get default save path. |
| `qbittorrent_get_global_download_limit` | `APITOOL` | Get global download limit in bytes/second. |
| `qbittorrent_get_global_upload_limit` | `APITOOL` | Get global upload limit in bytes/second. |
| `qbittorrent_get_log` | `APITOOL` | Get main log. |
| `qbittorrent_get_main_data` | `APITOOL` | Get main data. |
| `qbittorrent_get_peer_log` | `APITOOL` | Get peer log. |
| `qbittorrent_get_preferences` | `APITOOL` | Get application preferences. |
| `qbittorrent_get_rss_items` | `APITOOL` | Get all RSS items. |
| `qbittorrent_get_rss_matching_articles` | `APITOOL` | Get all articles matching a rule. |
| `qbittorrent_get_rss_rules` | `APITOOL` | Get all auto-downloading rules. |
| `qbittorrent_get_search_plugins` | `APITOOL` | Get search plugins. |
| `qbittorrent_get_speed_limits_mode` | `APITOOL` | Get alternative speed limits state (1 if enabled, 0 otherwise). |
| `qbittorrent_get_tags` | `APITOOL` | Get all tags. |
| `qbittorrent_get_torrent_contents` | `APITOOL` | Get torrent contents. |
| `qbittorrent_get_torrent_download_limit` | `APITOOL` | Get torrent download limit. |
| `qbittorrent_get_torrent_peers_data` | `APITOOL` | Get torrent peers data. |
| `qbittorrent_get_torrent_piece_hashes` | `APITOOL` | Get torrent pieces' hashes. |
| `qbittorrent_get_torrent_piece_states` | `APITOOL` | Get torrent pieces' states. |
| `qbittorrent_get_torrent_properties` | `APITOOL` | Get torrent generic properties. |
| `qbittorrent_get_torrent_trackers` | `APITOOL` | Get torrent trackers. |
| `qbittorrent_get_torrent_upload_limit` | `APITOOL` | Get torrent upload limit. |
| `qbittorrent_get_torrent_webseeds` | `APITOOL` | Get torrent web seeds. |
| `qbittorrent_get_torrents` | `APITOOL` | Get torrent list. |
| `qbittorrent_get_transfer_info` | `APITOOL` | Get global transfer info. |
| `qbittorrent_get_version` | `APITOOL` | Get application version. |
| `qbittorrent_increase_priority` | `APITOOL` | Increase torrent priority. |
| `qbittorrent_install_search_plugin` | `APITOOL` | Install search plugin. |
| `qbittorrent_login` | `BASE_API_CLIENTTOOL` | Authenticate with qBittorrent and get SID cookie. |
| `qbittorrent_logout` | `BASE_API_CLIENTTOOL` | Log out from qBittorrent. |
| `qbittorrent_mark_rss_as_read` | `APITOOL` | Mark RSS as read. |
| `qbittorrent_move_rss_item` | `APITOOL` | Move RSS item. |
| `qbittorrent_pause_torrents` | `APITOOL` | Pause (stop) torrents. qBittorrent 5.x renamed the endpoint to torrents/stop. |
| `qbittorrent_reannounce_torrents` | `APITOOL` | Reannounce torrents. |
| `qbittorrent_recheck_torrents` | `APITOOL` | Recheck torrents. |
| `qbittorrent_refresh_rss_item` | `APITOOL` | Refresh RSS item. |
| `qbittorrent_remove_categories` | `APITOOL` | Remove categories. 'categories' is |
| `qbittorrent_remove_rss_item` | `APITOOL` | Remove RSS item. |
| `qbittorrent_remove_rss_rule` | `APITOOL` | Remove auto-downloading rule. |
| `qbittorrent_remove_torrent_tags` | `APITOOL` | Remove torrent tags. |
| `qbittorrent_remove_trackers` | `APITOOL` | Remove trackers. |
| `qbittorrent_rename_file` | `APITOOL` | Rename file. |
| `qbittorrent_rename_folder` | `APITOOL` | Rename folder. |
| `qbittorrent_rename_rss_rule` | `APITOOL` | Rename auto-downloading rule. |
| `qbittorrent_resume_torrents` | `APITOOL` | Resume (start) torrents. qBittorrent 5.x renamed the endpoint to torrents/start. |
| `qbittorrent_search_delete` | `APITOOL` | Delete search. |
| `qbittorrent_search_results` | `APITOOL` | Get search results. |
| `qbittorrent_search_start` | `APITOOL` | Start search. |
| `qbittorrent_search_status` | `APITOOL` | Get search status. |
| `qbittorrent_search_stop` | `APITOOL` | Stop search. |
| `qbittorrent_set_auto_management` | `APITOOL` | Set automatic torrent management. |
| `qbittorrent_set_file_priority` | `APITOOL` | Set file priority. |
| `qbittorrent_set_force_start` | `APITOOL` | Set force start. |
| `qbittorrent_set_global_download_limit` | `APITOOL` | Set global download limit in bytes/second. |
| `qbittorrent_set_global_upload_limit` | `APITOOL` | Set global upload limit in bytes/second. |
| `qbittorrent_set_preferences` | `APITOOL` | Set application preferences. |
| `qbittorrent_set_rss_rule` | `APITOOL` | Set auto-downloading rule. |
| `qbittorrent_set_super_seeding` | `APITOOL` | Set super seeding. |
| `qbittorrent_set_torrent_category` | `APITOOL` | Set torrent category. |
| `qbittorrent_set_torrent_download_limit` | `APITOOL` | Set torrent download limit. |
| `qbittorrent_set_torrent_location` | `APITOOL` | Set torrent location. |
| `qbittorrent_set_torrent_name` | `APITOOL` | Set torrent name. |
| `qbittorrent_set_torrent_share_limit` | `APITOOL` | Set torrent share limit. |
| `qbittorrent_set_torrent_upload_limit` | `APITOOL` | Set torrent upload limit. |
| `qbittorrent_shutdown_application` | `APITOOL` | Shutdown application. |
| `qbittorrent_toggle_first_last_piece_priority` | `APITOOL` | Set first/last piece priority. |
| `qbittorrent_toggle_sequential_download` | `APITOOL` | Toggle sequential download. |
| `qbittorrent_toggle_speed_limits_mode` | `APITOOL` | Toggle alternative speed limits. |
| `qbittorrent_top_priority` | `APITOOL` | Maximal torrent priority. |
| `qbittorrent_uninstall_search_plugin` | `APITOOL` | Uninstall search plugin. |
| `qbittorrent_update_search_plugins` | `APITOOL` | Update search plugins. |

</details>

_7 action-routed tool(s) (default) · 89 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

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

> **Install the slim `[mcp]` extra.** All examples below install
> `qbittorrent-agent[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "qbittorrent-agent[mcp]",
        "qbittorrent-mcp"
      ],
      "env": {
        "QBITTORRENT_URL": "http://localhost:8080",
        "QBITTORRENT_USERNAME": "your_qbittorrent_username_here",
        "QBITTORRENT_PASSWORD": "your_qbittorrent_password_here"
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
        "qbittorrent-agent[mcp]",
        "qbittorrent-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "QBITTORRENT_URL": "http://localhost:8080",
        "QBITTORRENT_USERNAME": "your_qbittorrent_username_here",
        "QBITTORRENT_PASSWORD": "your_qbittorrent_password_here"
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
  -e QBITTORRENT_URL="http://localhost:8080" \
  -e QBITTORRENT_USERNAME="your_value" \
  -e QBITTORRENT_PASSWORD="your_value" \
  knucklessg1/qbittorrent-agent:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `qbittorrent-agent[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `qbittorrent-agent[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `qbittorrent-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

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
export QBITTORRENT_URL="http://localhost:8080"
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
    image: knucklessg1/qbittorrent-agent:mcp
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

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `QBITTORRENT_URL` | `http://localhost:8080` | Unified qBittorrent Web UI base URL. |
| `QBITTORRENT_USERNAME` | `admin` |  |
| `QBITTORRENT_PASSWORD` | `your_qbittorrent_password_here` |  |
| `QBITTORRENT_SSL_VERIFY` | `True` | TLS verification for the API client (takes precedence over QBITTORRENT_AGENT_VERIFY) |
| `QBITTORRENT_AGENT_VERIFY` | `True` | TLS verification fallback for the API client (default: True) |
| `APPTOOL` | `True` |  |
| `LOGTOOL` | `True` |  |
| `SYNCTOOL` | `True` |  |
| `TRANSFERTOOL` | `True` |  |
| `TORRENTSTOOL` | `True` |  |
| `RSSTOOL` | `True` |  |
| `SEARCHTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_23 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


The agent and MCP server can be fully configured using the following environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| **`QBITTORRENT_URL`** | String | `http://localhost:8080` | Unified qBittorrent Web UI base URL. |
| **`QBITTORRENT_USERNAME`** | String | `None` | Username for authentication. |
| **`QBITTORRENT_PASSWORD`** | String | `None` | Password for authentication. |
| **`QBITTORRENT_SSL_VERIFY`** | Boolean | `True` | TLS verification for the API client (takes precedence over `QBITTORRENT_AGENT_VERIFY`). |
| **`QBITTORRENT_AGENT_VERIFY`** | Boolean | `True` | TLS verification fallback for the API client. |
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

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `qbittorrent-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `qbittorrent-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `qbittorrent-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "qbittorrent-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "qbittorrent-agent[agent]"

# Everything (development)
uv pip install "qbittorrent-agent[all]"      # or: python -m pip install "qbittorrent-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/qbittorrent-agent:mcp` | `--target mcp` | `qbittorrent-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `qbittorrent-mcp` |
| `knucklessg1/qbittorrent-agent:latest` | `--target agent` (default) | `qbittorrent-agent[agent]` — **full** agent runtime + epistemic-graph engine | `qbittorrent-agent` |

```bash
docker build --target mcp   -t knucklessg1/qbittorrent-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/qbittorrent-agent:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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
| Container, prod | deploy `knucklessg1/qbittorrent-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
