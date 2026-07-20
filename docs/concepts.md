# Concept Registry — qbittorrent-agent

> **Prefix**: `CONCEPT:QBT-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:QB-OS.governance.qbt` | App Operations | MCP tool domain `app` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-2` | Log Operations | MCP tool domain `log` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-3` | Rss Operations | MCP tool domain `rss` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-4` | Search & Discovery | MCP tool domain `search` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-5` | Sync Operations | MCP tool domain `sync` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-6` | Torrent Management | MCP tool domain `torrents` — Action-routed dynamic tool registration |
| `CONCEPT:QB-OS.governance.qbt-7` | Transfer Operations | MCP tool domain `transfer` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-utilities |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-utilities |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `qbittorrent_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all QBT-* concepts.
