# CONN-QBITTORRENT-AGENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-QBITTORRENT-AGENT-R001` | `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` | `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` and `::test_second_consecutive_rejection_raises_without_looping` must pass. |
| T-002 | `CONN-QBITTORRENT-AGENT-R002` | `tests/test_session_relogin.py::test_post_also_retries_on_401` | `tests/test_session_relogin.py::test_post_also_retries_on_401` must observe the retry through `_post`. |
| T-003 | `CONN-QBITTORRENT-AGENT-R003` | `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` | `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` must call `get_version` against a faked transport. |
| T-004 | `CONN-QBITTORRENT-AGENT-R004` | `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` | Every connector name in the package is `qbittorrent-mcp`. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
