# CONN-QBITTORRENT-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `qbittorrent-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `qbittorrent_agent` from it.
