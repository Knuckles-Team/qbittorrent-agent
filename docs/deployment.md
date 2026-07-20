# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`qbittorrent-agent` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "qbittorrent": {
      "command": "qbittorrent-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
qbittorrent-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/qbittorrent-agent@sha256:<digest> qbittorrent-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "qbittorrent": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
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
| `QBITTORRENT_URL` | Required | qBittorrent WebUI base URL |
| `QBITTORRENT_USERNAME` | Required | WebUI user id |
| `QBITTORRENT_PASSWORD` | Required | WebUI password |
| `TLS_PROFILE` | _(empty)_ | Named `AgentConfig` transport-security profile; verification is mandatory |
| `TLS_PROFILES_REF` | _(empty)_ | Runtime secret reference for the TLS profile catalog |

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
    image: example/qbittorrent-agent@sha256:<digest>
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
    image: example/qbittorrent-agent@sha256:<digest>
    hostname: qbittorrent-agent-mcp
    env_file: [../.env]
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports: ["8000:8000"]

  qbittorrent-agent-agent:
    image: example/qbittorrent-agent@sha256:<digest>
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
# Internal (self-signed) — homelab .example.invalid zone
qbittorrent-agent.example.invalid {
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
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=qbittorrent-agent.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `qbittorrent-agent.example.invalid → <caddy-host-ip>` in the Technitium
web console (`http://technitium.example.invalid:5380`). The ecosystem
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
        "QBITTORRENT_URL": "<configured-endpoint>",
        "QBITTORRENT_USERNAME": "<configured-principal>",
        "QBITTORRENT_PASSWORD": "<runtime-secret>"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://qbittorrent-agent.example.invalid/mcp`
instead.
