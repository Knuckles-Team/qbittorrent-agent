# CONN-QBITTORRENT-AGENT-SURFACE — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

The census fixture is read from the qBittorrent 5.2.4 controllers. `scripts/generate_api_client.py` writes one method per operation, and the SDK serves each method as one typed tool. `BaseApiClient` keeps the login session and re-login, adds bearer API-key auth, raises on every failed status, and shapes answers as objects. The content tier is plain files: skills, prompts and two Turtle files; the tests check they agree with the served tools and with medulla core.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk 0.8, fastmcp, requests; tests add rdflib and medulla
- **Storage**: N/A
- **Testing**: pytest, in-process server and faked sessions
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; no `owl:imports` of core
- **Scale/Scope**: 8 rows, 121 operations

## Constitution Check

- One owner per concept: pass. Core classes stay in medulla.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass.

## Project Structure

```text
qbittorrent_agent/api/client.py                  written by scripts/generate_api_client.py
qbittorrent_agent/api/api_client_base.py         session, API key, error boundary, answer shape
qbittorrent_agent/mcp/mcp_kg.py                  the ingest tool
qbittorrent_agent/skills/<skill>/SKILL.md        skills with contracts
qbittorrent_agent/prompts/<role>.json            operator and role agent definitions
qbittorrent_agent/ontology/qbittorrent.ttl       classes, instance, save paths, routing, federation
qbittorrent_agent/ontology/qbittorrent-contracts.ttl  contracts, skills, prompts, tools
tests/fixtures/upstream_operations.json          census fixture
tests/test_surface.py                            bound tests
```

## Phase 0: Research

See [research.md](research.md). Unknowns resolved: which operations qBittorrent 5.2.4 serves (read from its controllers and the POST-only table, 121 plus 2 web sign-in), which HTTP verb each needs, which parameters each reads and their types, how 5.2 authenticates an API key (bearer `qbt_` key), and why the media apps lost their download client (stale passwords, then an IP ban after 5 failed logins).

## Phase 1: Design

The entities are in [data-model.md](data-model.md). The shortest proof is in [quickstart.md](quickstart.md).

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `spec`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

Each row's `Caller chain:` sentence in [requirements.md](requirements.md) traces the entry point to the code.

## Cross-repo seams

none. The connector calls scion-sdk in process and reads the medulla core ontology only in tests; the diagnose contract hands the fix to the arr apps by name only.
