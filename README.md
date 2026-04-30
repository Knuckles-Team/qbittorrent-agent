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

*Version: 0.1.8*

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
