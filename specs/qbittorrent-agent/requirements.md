# CONN-QBITTORRENT-AGENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-QBITTORRENT-AGENT-R001` | **Session recovery.** The client must log in again and retry once after a 401 or 403 response, in `qbittorrent_agent/api/api_client_base.py`. A second rejection must raise `UnauthorizedError`. | `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` and `::test_second_consecutive_rejection_raises_without_looping` must pass. |
| `CONN-QBITTORRENT-AGENT-R002` | **Wiring.** The `_get` and `_post` methods must call `_send` at `qbittorrent_agent/api/api_client_base.py:101` and `:110`. `_send` must call `login` at `:89`. | `tests/test_session_relogin.py::test_post_also_retries_on_401` must observe the retry through `_post`. |
| `CONN-QBITTORRENT-AGENT-R003` | **Hot-path proof.** A public operation must recover from an expired session through the real entry point. | `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` must call `get_version` against a faked transport. |
| `CONN-QBITTORRENT-AGENT-R004` | **Fleet name.** `pyproject.toml` declares `qbittorrent-mcp` as the single `scion_sdk.connector` entry point. The content pack, the manifest `connector`, the fingerprints and the ingest binding all carry `qbittorrent-mcp`. Proving test: `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name`. | Every connector name in the package is `qbittorrent-mcp`. |
