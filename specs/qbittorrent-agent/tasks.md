# CONN-QBITTORRENT-AGENT — Implementation tasks

Governing spec: [spec.md](spec.md). Design: [plan.md](plan.md). Rows: [requirements.md](requirements.md).

- [x] `CONN-QBITTORRENT-AGENT-R001`: Add `_send` with one re-login retry in `api_client_base.py`.
- [x] `CONN-QBITTORRENT-AGENT-R002`: Route `_get` and `_post` through `_send`.
- [x] `CONN-QBITTORRENT-AGENT-R003`: Prove recovery through `get_version` in `tests/test_session_relogin.py`.
