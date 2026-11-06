# CONN-QBITTORRENT-AGENT-SURFACE — The qBittorrent tool surface and its content

Owner: qbittorrent-agent. Cross-repo IDs: `CONN-ARR-MCP-SUITE-R011` (the arr apps' side of the download-client workflow).

## Purpose and user stories

An operator runs qBittorrent, the download client of the arr media suite, through one connector. Every WebUI API operation must be one typed tool, a failed call must say why, and an agent must know which tools to call, in which order, and where the data lives. Arbora builds agents from the connector's prompts, so each prompt is a complete agent definition.

## Why a new spec

`CONN-QBITTORRENT-AGENT` owns only session recovery and the fleet name; `CONN-QBITTORRENT-AGENT-CONNECTOR-CONTENT` owns only how the SDK serves packaged content. No spec owned the tool surface or what the content says.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: SDK tool registration and content serving (scion-sdk), the fleet gateway catalog (arbora), the core ontology (medulla), and the arr apps' download-client settings (arr-mcp).

## User Scenarios & Testing

### User Story 1 - Every operation is a typed tool that fails loudly (Priority: P1)

An operator calls any qBittorrent operation as one typed tool, and a refused call reports qBittorrent's reason instead of success.

**Acceptance Scenarios**:

1. **Given** the connector is built, **When** the tools are listed, **Then** each census operation has one tool (`CONN-QBITTORRENT-AGENT-SURFACE-R001`) and none routes by action (`CONN-QBITTORRENT-AGENT-SURFACE-R002`).
2. **Given** qBittorrent answers 409, **When** a tool runs, **Then** it raises with the reason (`CONN-QBITTORRENT-AGENT-SURFACE-R003`).

### User Story 2 - Agents follow tool-use contracts (Priority: P1)

An agent built from a connector prompt runs a named workflow, such as recovering a stalled torrent, with the steps the contract gives.

**Acceptance Scenarios**:

1. **Given** the content is served, **When** an agent reads a skill, **Then** each workflow names served tools in order (`CONN-QBITTORRENT-AGENT-SURFACE-R004`).
2. **Given** arbora reads the prompts, **When** it builds an agent, **Then** the prompt gives role, goal, skills, tools, data locations, guardrails and outputs (`CONN-QBITTORRENT-AGENT-SURFACE-R005`).

### User Story 3 - The graph knows where downloads go (Priority: P2)

A graph query answers where qBittorrent stores downloads, which category belongs to which app, and which apps send downloads to it, with every class under medulla core.

**Acceptance Scenarios**:

1. **Given** the ontology is loaded, **When** a query asks where Radarr's downloads land, **Then** it gets category `radarr` and its folder (`CONN-QBITTORRENT-AGENT-SURFACE-R006`).
2. **Given** medulla core is loaded, **When** the classes are checked, **Then** each reaches `bfo:Entity` without an import (`CONN-QBITTORRENT-AGENT-SURFACE-R007`) and ingest emits core classes (`CONN-QBITTORRENT-AGENT-SURFACE-R008`).

### Edge Cases

- qBittorrent ignores unknown hashes on bulk operations (`torrents/stop` answers 200); the contracts read the torrent first.
- A placeholder `QBITTORRENT_API_KEY` must not lock the client out: it falls back to the login session.
- Five failed logins ban the caller's IP for `web_ui_ban_duration`; the diagnose contract reads the log before anything retries.

## Requirements

- **FR-001**: Every WebUI API operation is one tool. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R001`.
- **FR-002**: Typed tools only. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R002`.
- **FR-003**: A failed call says why; answers are objects; API-key auth. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R003`.
- **FR-004**: Skills carry the workflows as tool-use contracts. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R004`.
- **FR-005**: Prompts are agent definitions. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R005`.
- **FR-006**: Data location, routing and federation. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R006`.
- **FR-007**: Every class rolls up to medulla core. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R007`.
- **FR-008**: Ingest uses core classes and a served tool. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R008`.

## Success Criteria

- **SC-001**: 121 of 121 census operations are served as typed tools. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R001`.
- **SC-002**: 0 tools route by action or take `params_json`. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R002`.
- **SC-003**: 100% of failed calls raise with their status. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R003`.
- **SC-004**: 100% of classes reach `BFO_0000001` through medulla core. Rows: `CONN-QBITTORRENT-AGENT-SURFACE-R007`.

## Assumptions

- The census fixture matches the deployed qBittorrent 5.2.4 (WebAPI 2.15.1).
- The SDK serves packaged skills, prompts and ontology files (`CONN-QBITTORRENT-AGENT-CONNECTOR-CONTENT-R001`).

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-QBITTORRENT-AGENT-SURFACE-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-QBITTORRENT-AGENT-SURFACE-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-QBITTORRENT-AGENT-SURFACE-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-QBITTORRENT-AGENT-SURFACE-R004` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
| FR-005 | `CONN-QBITTORRENT-AGENT-SURFACE-R005` | [plan.md](plan.md) | T-005 | [test-spec.md](test-spec.md) |
| FR-006 | `CONN-QBITTORRENT-AGENT-SURFACE-R006` | [plan.md](plan.md) | T-006 | [test-spec.md](test-spec.md) |
| FR-007 | `CONN-QBITTORRENT-AGENT-SURFACE-R007` | [plan.md](plan.md) | T-007 | [test-spec.md](test-spec.md) |
| FR-008 | `CONN-QBITTORRENT-AGENT-SURFACE-R008` | [plan.md](plan.md) | T-008 | [test-spec.md](test-spec.md) |
