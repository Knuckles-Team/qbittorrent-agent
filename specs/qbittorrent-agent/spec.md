# CONN-QBITTORRENT-AGENT — qBittorrent session handling

## Outcome

The connector must keep a valid qBittorrent WebUI session for its whole lifetime.
The connector must recover from an expired session without operator action.

## Scope and owner

The `qbittorrent-agent` repository owns qBittorrent API calls and session handling.
The shared connector SDK owns transport, TLS, and error types.
The shared pipelines repository owns quality gates and delivery rendering.

Component: Connector integration
Code: ../../qbittorrent_agent/api/api_client_base.py ../../tests/test_session_relogin.py

## Non-goals

This specification grants no service access and creates no credentials.
The connector must not log credentials or cookie values.

## Why a new spec

The repository holds no local spec. The search of `specs/` found only the template.
No other owner states session recovery for qBittorrent.

## User Scenarios & Testing

### User Story 1 - Session recovery (Priority: P1)

The fleet operator and the engine rely on this behaviour of `qbittorrent-agent`: The client must log in again and retry once after a 401 or 403 response, in `qbittorrent_agent/api/api_client_base.py`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `qbittorrent-agent` connector built from the default branch, **When** `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` runs, **Then** `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` and `::test_second_consecutive_rejection_raises_without_looping` must pass.

### User Story 2 - Wiring (Priority: P1)

The fleet operator and the engine rely on this behaviour of `qbittorrent-agent`: The `_get` and `_post` methods must call `_send` at `qbittorrent_agent/api/api_client_base.py:117` and `:126`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `qbittorrent-agent` connector built from the default branch, **When** `tests/test_session_relogin.py::test_post_also_retries_on_401` runs, **Then** `tests/test_session_relogin.py::test_post_also_retries_on_401` must observe the retry through `_post`.

### User Story 3 - Hot-path proof (Priority: P1)

The fleet operator and the engine rely on this behaviour of `qbittorrent-agent`: A public operation must recover from an expired session through the real entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `qbittorrent-agent` connector built from the default branch, **When** `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` runs, **Then** `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` must call `app_version` against a faked transport.

### User Story 4 - Fleet name (Priority: P2)

The fleet operator and the engine rely on this behaviour of `qbittorrent-agent`: `pyproject.toml` declares `qbittorrent-mcp` as the single `scion_sdk.connector` entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `qbittorrent-agent` connector built from the default branch, **When** `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` runs, **Then** every connector name in the package is `qbittorrent-mcp`.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Session recovery. Rows: `CONN-QBITTORRENT-AGENT-R001`.
- **FR-002**: Wiring. Rows: `CONN-QBITTORRENT-AGENT-R002`.
- **FR-003**: Hot-path proof. Rows: `CONN-QBITTORRENT-AGENT-R003`.
- **FR-004**: Fleet name. Rows: `CONN-QBITTORRENT-AGENT-R004`.

## Success Criteria

- **SC-001**: `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` and `::test_second_consecutive_rejection_raises_without_looping` must pass. Rows: `CONN-QBITTORRENT-AGENT-R001`.
- **SC-002**: `tests/test_session_relogin.py::test_post_also_retries_on_401` must observe the retry through `_post`. Rows: `CONN-QBITTORRENT-AGENT-R002`.
- **SC-003**: `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` must call `app_version` against a faked transport. Rows: `CONN-QBITTORRENT-AGENT-R003`.
- **SC-004**: Every connector name in the package is `qbittorrent-mcp`. Rows: `CONN-QBITTORRENT-AGENT-R004`.

## Assumptions

- The `qbittorrent-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-QBITTORRENT-AGENT-R001` | plan.md Production caller chain | T-001 | tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once |
| FR-002 | `CONN-QBITTORRENT-AGENT-R002` | plan.md Production caller chain | T-002 | tests/test_session_relogin.py::test_post_also_retries_on_401 |
| FR-003 | `CONN-QBITTORRENT-AGENT-R003` | plan.md Production caller chain | T-003 | tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session |
| FR-004 | `CONN-QBITTORRENT-AGENT-R004` | plan.md Production caller chain | T-004 | tests/test_fleet_name.py::test_connector_name_is_the_fleet_name |
