# qbittorrent-agent

qBittorrent management **MCP Server + A2A Agent** for the agent-utilities ecosystem
— typed, deterministic tools for torrent control, RSS automation, and search over
the qBittorrent WebUI API.

!!! info "Official documentation"
    This site is the canonical reference for `qbittorrent-agent`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/qbittorrent-agent)](https://pypi.org/project/qbittorrent-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/qbittorrent-agent)](https://github.com/Knuckles-Team/qbittorrent-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/qbittorrent-agent)

## Overview

`qbittorrent-agent` wraps the qBittorrent WebUI v2 REST API with typed,
deterministic MCP tools, and ships a companion Pydantic-AI **A2A agent** server. It
provides:

- **`QbittorrentApi`** — a session-authenticated REST facade over the qBittorrent
  WebUI, composed from per-domain sub-clients (app, log, sync, transfer, torrents,
  RSS, search).
- **Seven action-dispatch MCP tools** — `qbittorrent_app`, `qbittorrent_log`,
  `qbittorrent_sync`, `qbittorrent_transfer`, `qbittorrent_torrents`,
  `qbittorrent_rss`, and `qbittorrent_search`, each individually toggled by an
  environment switch.
- **An A2A agent server** (`qbittorrent-agent`) that calls the MCP tool surface for
  conversational and multi-step torrent workflows.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP server and A2A agent, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `QbittorrentApi` client, and the CLI entry points.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy qBittorrent with Docker.
- :material-sitemap: **[Architecture](architecture.md)** — agent, MCP server, layered client.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:QBT-*` registry.

</div>

## Quick start

```bash
pip install "qbittorrent-agent[mcp]"
qbittorrent-mcp                  # stdio MCP server (default transport)
```

Connect it to a qBittorrent instance:

```bash
export QBITTORRENT_URL=http://your-qbittorrent:8080
export QBITTORRENT_USERNAME=admin
export QBITTORRENT_PASSWORD=your_password
qbittorrent-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the A2A agent, reverse proxy,
DNS).
