# Heartbeat Tasks

These tasks are performed periodically by the qBittorrent Manager to ensure system health and operational readiness.

## Check Connectivity
### [default]
- **Command**: `get_version`
- **Goal**: Verify that the agent can connect to the qBittorrent WebUI.
- **Success Criteria**: Returns a version string (e.g., `v4.3.3`).

## Monitor Stalled Torrents
### [stalled-check]
- **Command**: `get_torrents(filter='stalled')`
- **Goal**: Identify torrents that are stalled and might require intervention.
- **Action**: Alert the user if stalled torrents are found and trackers are in error state.

## Log Error Scan
### [error-check]
- **Command**: `get_log(last_known_id=-1)`
- **Goal**: Scan for critical errors in the application log.
- **Action**: Summarize any critical log entries from the last hour.
