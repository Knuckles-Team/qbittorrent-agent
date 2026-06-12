# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`qbittorrent-agent` exposes its MCP server (console script `qbittorrent-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "qbittorrent-mcp": {
      "command": "uvx",
      "args": ["--from", "qbittorrent-agent", "qbittorrent-mcp"],
      "env": {
        "QBITTORRENT_HOST": "<your-qbittorrent_host>",
        "QBITTORRENT_USERNAME": "<your-qbittorrent_username>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from qbittorrent-agent qbittorrent-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "qbittorrent-mcp": {
      "command": "uvx",
      "args": ["--from", "qbittorrent-agent", "qbittorrent-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "QBITTORRENT_HOST": "<your-qbittorrent_host>",
        "QBITTORRENT_USERNAME": "<your-qbittorrent_username>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "qbittorrent-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "qbittorrent-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "QBITTORRENT_HOST=<your-qbittorrent_host>",
        "-e", "QBITTORRENT_USERNAME=<your-qbittorrent_username>",
        "knucklessg1/qbittorrent-agent:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name qbittorrent-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e QBITTORRENT_HOST="<your-qbittorrent_host>" \
  -e QBITTORRENT_USERNAME="<your-qbittorrent_username>" \
  knucklessg1/qbittorrent-agent:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "qbittorrent-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run qbittorrent-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on the internal `*.arpa` zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "qbittorrent-mcp": { "url": "http://qbittorrent-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://qbittorrent-mcp.arpa` to the container's `:8000`
streamable-http listener; `http://qbittorrent-mcp.arpa/health` returns
`{"status":"OK"}` when the service is live.
<!-- END GENERATED: deployment-options -->

This page covers running `qbittorrent-agent` as a long-lived service: the MCP-server
transports, the companion A2A agent server, a Docker Compose stack, putting it behind
a Caddy reverse proxy, and giving it a DNS name with Technitium. To provision the
**qBittorrent** instance it connects to, see [Backing Platform](platform.md).

> `qbittorrent-agent` ships **two** console scripts: an **MCP server**
> (`qbittorrent-mcp`) exposing the typed tool surface, and an **A2A agent server**
> (`qbittorrent-agent`) that calls those tools for conversational and multi-step
> workflows.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    qbittorrent-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    qbittorrent-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    qbittorrent-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`qbittorrent-agent` is configured entirely from the environment. The **required**
connection set:

| Var | Default | Meaning |
|---|---|---|
| `QBITTORRENT_URL` | `http://localhost:8080` | qBittorrent WebUI base URL (overrides host/port) |
| `QBITTORRENT_HOST` | `127.0.0.1` | WebUI host (used when `QBITTORRENT_URL` is unset) |
| `QBITTORRENT_PORT` | `8080` | WebUI port (used when `QBITTORRENT_URL` is unset) |
| `QBITTORRENT_USERNAME` | `admin` | WebUI user id |
| `QBITTORRENT_PASSWORD` | `adminadmin` | WebUI password |
| `QBITTORRENT_AGENT_VERIFY` | `True` | Verify TLS for the API client |

The per-domain tool sets are toggled independently and default to enabled:

| Var | Default | Tool domain |
|---|---|---|
| `APPTOOL` | `True` | `qbittorrent_app` |
| `LOGTOOL` | `True` | `qbittorrent_log` |
| `SYNCTOOL` | `True` | `qbittorrent_sync` |
| `TRANSFERTOOL` | `True` | `qbittorrent_transfer` |
| `TORRENTSTOOL` | `True` | `qbittorrent_torrents` |
| `RSSTOOL` | `True` | `qbittorrent_rss` |
| `SEARCHTOOL` | `True` | `qbittorrent_search` |

Plus `HOST` / `PORT` / `TRANSPORT` for HTTP transports. The complete set, including
telemetry (`ENABLE_OTEL`, `OTEL_*`) and access governance (`EUNOMIA_*`), is documented
in [`.env.example`](https://github.com/Knuckles-Team/qbittorrent-agent/blob/main/.env.example).
Copy it to `.env` and fill in only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/qbittorrent-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  qbittorrent-agent-mcp:
    image: knucklessg1/qbittorrent-agent:latest
    container_name: qbittorrent-agent-mcp
    hostname: qbittorrent-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit QBITTORRENT_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## A2A agent server

`qbittorrent-agent` also ships a Pydantic-AI **A2A agent** (console script
`qbittorrent-agent`). It connects to the MCP server over `MCP_URL`, auto-discovers the
tool surface from `mcp_config.json`, and serves an A2A / AG-UI endpoint on its own
port:

```bash
export MCP_URL=http://qbittorrent-agent-mcp:8000/mcp
qbittorrent-agent --provider openai --model-id gpt-4o --host 0.0.0.0 --port 9004
```

The repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/qbittorrent-agent/blob/main/docker/agent.compose.yml),
which deploys the MCP server and the agent together — the agent waits on the MCP
service and is wired to it by container name:

```yaml
services:
  qbittorrent-agent-mcp:
    image: knucklessg1/qbittorrent-agent:latest
    hostname: qbittorrent-agent-mcp
    env_file: [../.env]
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports: ["8000:8000"]

  qbittorrent-agent-agent:
    image: knucklessg1/qbittorrent-agent:latest
    depends_on: [qbittorrent-agent-mcp]
    command: ["qbittorrent-agent"]
    env_file: [../.env]
    environment:
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://qbittorrent-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports: ["9004:9004"]
```

```bash
docker compose -f docker/agent.compose.yml up -d
curl -s http://localhost:9004/health         # agent health endpoint
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
qbittorrent-agent.arpa {
    tls internal
    reverse_proxy qbittorrent-agent-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
qbittorrent-agent.example.com {
    reverse_proxy qbittorrent-agent-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=qbittorrent-agent.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `qbittorrent-agent.arpa → <caddy-host-ip>` in the Technitium
web console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "qbittorrent-agent": {
      "command": "uv",
      "args": ["run", "qbittorrent-mcp"],
      "env": {
        "QBITTORRENT_URL": "http://your-qbittorrent:8080",
        "QBITTORRENT_USERNAME": "admin",
        "QBITTORRENT_PASSWORD": "your_password"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://qbittorrent-agent.arpa/mcp`
instead.
