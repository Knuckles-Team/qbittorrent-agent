# CONN-QBITTORRENT-AGENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `qbittorrent-agent` delivers the rows of `CONN-QBITTORRENT-AGENT`. The live caller is the `qbittorrent-mcp` console script. The owner is the `qbittorrent_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 4 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `qbittorrent_agent/api/api_client_base.py` (existing)
- `qbittorrent_agent/mcp_server.py` (existing)
- `tests/test_session_relogin.py` (existing)
- `pyproject.toml` (existing)
- `qbittorrent_agent/__init__.py` (existing)
- `tests/test_fleet_name.py` (existing)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

### Summary

This plan states how `qbittorrent-agent` delivers the rows of `CONN-QBITTORRENT-AGENT`. The live caller is the `qbittorrent-mcp` console script. The owner is the `qbittorrent_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 4 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `qbittorrent_agent/api/api_client_base.py` (existing)
- `qbittorrent_agent/mcp_server.py` (existing)
- `tests/test_session_relogin.py` (existing)
- `pyproject.toml` (existing)
- `qbittorrent_agent/__init__.py` (existing)
- `tests/test_fleet_name.py` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `qbittorrent-agent` delivers the rows of `CONN-QBITTORRENT-AGENT`. The live caller is the `qbittorrent-mcp` console script. The owner is the `qbittorrent_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 4 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `qbittorrent_agent/api/api_client_base.py` (existing)
- `qbittorrent_agent/mcp_server.py` (existing)
- `tests/test_session_relogin.py` (existing)
- `pyproject.toml` (existing)
- `qbittorrent_agent/__init__.py` (existing)
- `tests/test_fleet_name.py` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `qbittorrent-agent` delivers the rows of `CONN-QBITTORRENT-AGENT`. The live caller is the `qbittorrent-mcp` console script. The owner is the `qbittorrent_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 4 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `qbittorrent_agent/api/api_client_base.py` (existing)
- `tests/test_session_relogin.py` (existing)
- `pyproject.toml` (existing)
- `qbittorrent_agent/__init__.py` (existing)
- `tests/test_fleet_name.py` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Existing system and reuse

`BaseApiClient` in `qbittorrent_agent/api/api_client_base.py` owns the HTTP session.
It logs in once at construction. The session cookie then expires and calls fail with 403.
The fix reuses the existing `login` method. It adds no second client.

### Architecture

All API calls pass through `_send`. The `_get` and `_post` methods call `_send`.
`_send` retries a call once after a 401 or 403 response. It logs in again first.
A second rejection raises `UnauthorizedError`. A failed login raises `UnauthorizedError`.
The login call does not pass through `_send`, so it never retries itself.

### Interfaces and data model

No wire, schema, or tool change. Log lines carry no credentials and no cookie values.

### Live integration path

An MCP tool calls an `Api` method, such as `get_version` in `api_client_app.py`.
The method calls `_get` or `_post`. Both call `_send` at `api_client_base.py:101` and `:110`.
`_send` calls `login` at `api_client_base.py:89` after a rejection.

### Quality and release gates

Run `pytest tests/test_session_relogin.py` with a faked transport. No network is used.
Run `pipelines-hook spec-standard` and `pipelines-hook spec-status --write`.

### Risks, alternatives, and decisions

A bounded single retry avoids a login loop against a banned address.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-QBITTORRENT-AGENT-R004`: `qbittorrent-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `qbittorrent_agent:connector` (`qbittorrent_agent/__init__.py:93`); `connector_name("qbittorrent_agent")` in the SDK resolves the same entry point name for the content pack, the manifest and the ingest binding.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-QBITTORRENT-AGENT-R001`: an MCP tool of `qbittorrent_agent/mcp_server.py` calls a domain client, which calls `_get` (`qbittorrent_agent/api/api_client_base.py:98`) or `_post` (`qbittorrent_agent/api/api_client_base.py:105`), which call `_send` (`qbittorrent_agent/api/api_client_base.py:80`); `_send` calls `login` (`qbittorrent_agent/api/api_client_base.py:89`) after a 401 or 403.
- `CONN-QBITTORRENT-AGENT-R002`: `_get` and `_post` in `qbittorrent_agent/api/api_client_base.py` call `_send`; `_send` calls `login`.
- `CONN-QBITTORRENT-AGENT-R003`: a public operation such as `get_version` on the API client calls `_get`, which calls `_send` and the re-login path.
- `CONN-QBITTORRENT-AGENT-R004`: `qbittorrent-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `qbittorrent_agent:connector` (`qbittorrent_agent/__init__.py:93`); `connector_name("qbittorrent_agent")` in the SDK resolves the same entry point name for the content pack, the manifest and the ingest binding.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-QBITTORRENT-AGENT-R001`: an MCP tool of `qbittorrent_agent/mcp_server.py` calls a domain client, which calls `_get` (`qbittorrent_agent/api/api_client_base.py:98`) or `_post` (`qbittorrent_agent/api/api_client_base.py:105`), which call `_send` (`qbittorrent_agent/api/api_client_base.py:80`); `_send` calls `login` (`qbittorrent_agent/api/api_client_base.py:89`) after a 401 or 403.
- `CONN-QBITTORRENT-AGENT-R002`: `_get` and `_post` in `qbittorrent_agent/api/api_client_base.py` call `_send`; `_send` calls `login`.
- `CONN-QBITTORRENT-AGENT-R003`: a public operation such as `get_version` on the API client calls `_get`, which calls `_send` and the re-login path.
- `CONN-QBITTORRENT-AGENT-R004`: `qbittorrent-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `qbittorrent_agent:connector` (`qbittorrent_agent/__init__.py:93`); `connector_name("qbittorrent_agent")` in the SDK resolves the same entry point name for the content pack, the manifest and the ingest binding.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-QBITTORRENT-AGENT-R001`: an MCP tool of `qbittorrent_agent/mcp_server.py` calls a domain client, which calls `_get` (`qbittorrent_agent/api/api_client_base.py:98`) or `_post` (`qbittorrent_agent/api/api_client_base.py:105`), which call `_send` (`qbittorrent_agent/api/api_client_base.py:80`); `_send` calls `login` (`qbittorrent_agent/api/api_client_base.py:89`) after a 401 or 403.
- `CONN-QBITTORRENT-AGENT-R002`: `_get` and `_post` in `qbittorrent_agent/api/api_client_base.py` call `_send`; `_send` calls `login`.
- `CONN-QBITTORRENT-AGENT-R003`: a public operation such as `get_version` on the API client calls `_get`, which calls `_send` and the re-login path.
- `CONN-QBITTORRENT-AGENT-R004`: `qbittorrent-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `qbittorrent_agent:connector` (`qbittorrent_agent/__init__.py:93`); `connector_name("qbittorrent_agent")` in the SDK resolves the same entry point name for the content pack, the manifest and the ingest binding.

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.
