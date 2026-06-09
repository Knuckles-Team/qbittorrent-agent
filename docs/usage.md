# Usage — API / CLI / MCP

`qbittorrent-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`QbittorrentApi`) you import, and as **CLI** entry points.
The concept registry behind the tool domains is in [Concepts](concepts.md).

## As an MCP server

Once [deployed](deployment.md), the server registers seven action-dispatch tools, one
per qBittorrent WebUI domain. Each is toggled by its own environment switch (all
default to enabled):

| Tool | Domain | Covers |
|---|---|---|
| `qbittorrent_app` | App | version, build info, preferences, default save path |
| `qbittorrent_log` | Log | main log, peer log |
| `qbittorrent_sync` | Sync | main data, torrent peers data |
| `qbittorrent_transfer` | Transfer | transfer info, speed limits, global rate limits |
| `qbittorrent_torrents` | Torrents | list/add/control torrents, categories, tags, contents |
| `qbittorrent_rss` | RSS | feeds, rules, matching articles, auto-download |
| `qbittorrent_search` | Search | search plugins, queries, results |

Example agent prompts that map onto these tools:

- *"List every torrent currently downloading"* → `qbittorrent_torrents`
- *"What is the current global download speed limit?"* → `qbittorrent_transfer`
- *"Add an RSS auto-download rule for new episodes"* → `qbittorrent_rss`

## As a Python API

`QbittorrentApi` is a session-authenticated REST facade composed from per-domain
sub-clients (app, log, sync, transfer, torrents, RSS, search). It authenticates with
the qBittorrent WebUI on construction.

```python
from qbittorrent_agent import QbittorrentApi

api = QbittorrentApi(
    base_url="http://your-qbittorrent:8080",
    username="admin",
    password="your_password",
    verify=True,
)

# Reads
version = api.get_version()                 # qBittorrent application version
prefs = api.get_preferences()               # WebUI preferences
torrents = api.get_torrents()               # all torrents with their state
transfer = api.get_transfer_info()          # global transfer statistics
rules = api.get_rss_rules()                 # RSS auto-download rules
```

Build a client straight from the environment:

```python
from qbittorrent_agent.auth import get_client
api = get_client()        # reads QBITTORRENT_* from the environment / .env
```

The client raises a clear `RuntimeError` when the supplied credentials are rejected,
so configuration mistakes surface immediately rather than as opaque request failures.

## As a CLI

The package installs two console scripts:

```bash
# The MCP server (see Deployment for transports)
qbittorrent-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# The A2A agent server (connects to the MCP server over MCP_URL)
MCP_URL=http://localhost:8000/mcp \
  qbittorrent-agent --provider openai --model-id gpt-4o --host 0.0.0.0 --port 9004
```

Both accept `--help` for the full flag set, including provider, model, OTEL telemetry,
and web-UI options for the agent.
