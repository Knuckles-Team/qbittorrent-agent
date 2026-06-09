# Concept Registry — qbittorrent-agent

> **Prefix**: `CONCEPT:QBT-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:QBT-001` | App Operations | MCP tool domain `app` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-002` | Log Operations | MCP tool domain `log` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-003` | Rss Operations | MCP tool domain `rss` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-004` | Search & Discovery | MCP tool domain `search` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-005` | Sync Operations | MCP tool domain `sync` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-006` | Torrent Management | MCP tool domain `torrents` — Action-routed dynamic tool registration |
| `CONCEPT:QBT-007` | Transfer Operations | MCP tool domain `transfer` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `qbittorrent_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all QBT-* concepts.
