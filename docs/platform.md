# Backing Platform — qBittorrent

`qbittorrent-agent` is a **client** of a qBittorrent WebUI (v2 API). This page
provides a Docker recipe for deploying one locally to serve as the target of
`QBITTORRENT_URL`. For production topologies, follow the upstream
[qBittorrent documentation](https://github.com/qbittorrent/qBittorrent/wiki) and the
[LinuxServer image documentation](https://docs.linuxserver.io/images/docker-qbittorrent/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors the upstream image. Systems offered only as a
    managed service have no local recipe.

## Single-node deployment (Compose)

The widely used `linuxserver/qbittorrent` image runs the WebUI on `:8080`. The
following stack provisions one qBittorrent instance with persistent configuration and
downloads:

```yaml
# docker/qbittorrent.compose.yml
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    hostname: qbittorrent
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - WEBUI_PORT=8080
    ports:
      - "8080:8080"            # WebUI / v2 REST API
      - "6881:6881"            # BitTorrent (TCP)
      - "6881:6881/udp"        # BitTorrent (UDP)
    volumes:
      - qbittorrent_config:/config
      - qbittorrent_downloads:/downloads

volumes:
  qbittorrent_config:
  qbittorrent_downloads:
```

```bash
docker compose -f docker/qbittorrent.compose.yml up -d

# The temporary WebUI password is printed on first boot:
docker compose -f docker/qbittorrent.compose.yml logs | grep -i password
```

## Connect qbittorrent-agent

```bash
export QBITTORRENT_URL=http://localhost:8080
export QBITTORRENT_USERNAME=admin
export QBITTORRENT_PASSWORD=<the-password-from-the-logs>
export QBITTORRENT_AGENT_VERIFY=False        # plain HTTP on the homelab

qbittorrent-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places qBittorrent and the MCP server on one Docker network, so the
server reaches the WebUI by container name:

```yaml
# docker/stack.compose.yml
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    hostname: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - WEBUI_PORT=8080
    ports: ["8080:8080"]
    volumes:
      - qbittorrent_config:/config
      - qbittorrent_downloads:/downloads

  qbittorrent-agent-mcp:
    image: knucklessg1/qbittorrent-agent:latest
    depends_on: [qbittorrent]
    environment:
      - QBITTORRENT_URL=http://qbittorrent:8080
      - QBITTORRENT_USERNAME=admin
      - QBITTORRENT_PASSWORD=your_password
      - QBITTORRENT_AGENT_VERIFY=False
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  qbittorrent_config:
  qbittorrent_downloads:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

## Manage qBittorrent from the agent

With the WebUI running and the connection variables set, the
[MCP tools](usage.md#as-an-mcp-server) drive torrent control, RSS automation, and
search end to end — add and pause torrents, inspect transfer statistics, and configure
RSS auto-download rules conversationally through the A2A agent.
