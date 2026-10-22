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

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).
