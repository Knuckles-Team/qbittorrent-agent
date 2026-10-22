# CONN-QBITTORRENT-AGENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Existing system and reuse

`BaseApiClient` in `qbittorrent_agent/api/api_client_base.py` owns the HTTP session.
It logs in once at construction. The session cookie then expires and calls fail with 403.
The fix reuses the existing `login` method. It adds no second client.

## Architecture

All API calls pass through `_send`. The `_get` and `_post` methods call `_send`.
`_send` retries a call once after a 401 or 403 response. It logs in again first.
A second rejection raises `UnauthorizedError`. A failed login raises `UnauthorizedError`.
The login call does not pass through `_send`, so it never retries itself.

## Interfaces and data model

No wire, schema, or tool change. Log lines carry no credentials and no cookie values.

## Live integration path

An MCP tool calls an `Api` method, such as `get_version` in `api_client_app.py`.
The method calls `_get` or `_post`. Both call `_send` at `api_client_base.py:101` and `:110`.
`_send` calls `login` at `api_client_base.py:89` after a rejection.

## Quality and release gates

Run `pytest tests/test_session_relogin.py` with a faked transport. No network is used.
Run `pipelines-hook spec-standard` and `pipelines-hook spec-status --write`.

## Risks, alternatives, and decisions

A bounded single retry avoids a login loop against a banned address.
