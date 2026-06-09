# Installation

`qbittorrent-agent` is a standard Python package and a prebuilt container image. Pick
the path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **qBittorrent WebUI** (v2 API) — see [Backing Platform](platform.md) to
  deploy one locally.

## From PyPI (recommended)

```bash
pip install qbittorrent-agent
```

### Optional extras

The base install carries the MCP-server runtime via `agent-utilities[mcp]`. Install
the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| `agent` | `pip install "qbittorrent-agent[agent]"` | Pydantic-AI agent + Logfire tracing (`agent-utilities[agent,logfire]`) |
| `all` | `pip install "qbittorrent-agent[all]"` | The MCP server, the agent, and Logfire tracing |
| `test` | `pip install "qbittorrent-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run both the MCP server and the A2A agent
pip install "qbittorrent-agent[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/qbittorrent-agent.git
cd qbittorrent-agent
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run qbittorrent-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint
`qbittorrent-mcp`):

```bash
docker pull knucklessg1/qbittorrent-agent:latest

docker run --rm -i \
  -e QBITTORRENT_URL=http://your-qbittorrent:8080 \
  -e QBITTORRENT_USERNAME=admin \
  -e QBITTORRENT_PASSWORD=your_password \
  knucklessg1/qbittorrent-agent:latest        # stdio transport (default)
```

For an HTTP server with a published port, and to run the companion A2A agent, see
[Deployment](deployment.md).

## Verify the install

```bash
qbittorrent-mcp --help
python -c "import qbittorrent_agent; print(qbittorrent_agent.QbittorrentApi)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server and A2A agent behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the `QbittorrentApi` client, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
