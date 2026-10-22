# CONN-QBITTORRENT-AGENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | `CONN-QBITTORRENT-AGENT-R001` | Unit | Faked transport returns 403 then 200. | One extra login occurs. The call returns the 200 body. | `tests/test_session_relogin.py::test_expired_session_logs_in_again_and_retries_once` |
| T-002 | `CONN-QBITTORRENT-AGENT-R001` | Unit | Faked transport returns 403 twice. | The call raises `UnauthorizedError`. Login runs twice in total. | `tests/test_session_relogin.py::test_second_consecutive_rejection_raises_without_looping` |
| T-003 | `CONN-QBITTORRENT-AGENT-R002` | Unit | Faked transport returns 401 then 200 on a POST. | The POST retries once after login. | `tests/test_session_relogin.py::test_post_also_retries_on_401` |
| T-004 | `CONN-QBITTORRENT-AGENT-R003` | Integration | `get_version` with a 403 then 200 transport. | The call returns the 200 body. | `tests/test_session_relogin.py::test_public_operation_recovers_from_expired_session` |

## Negative and boundary cases

The second consecutive rejection raises. The login call never retries itself.

## Quality and release proof

Run `pytest tests/test_session_relogin.py`. Run `pipelines-hook spec-standard`.
| T-005 | `CONN-QBITTORRENT-AGENT-R004` | `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` | Every connector name in the package is `qbittorrent-mcp`. |
