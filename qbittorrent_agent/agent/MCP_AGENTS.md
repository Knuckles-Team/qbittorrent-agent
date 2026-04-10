# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Qbittorrent App Specialist | Expert specialist for app domain tasks. | You are a Qbittorrent App specialist. Help users manage and interact with App functionality using the available tools. | qbittorrent-agent_app_toolset | app | qbittorrent-agent |
| Qbittorrent Torrents Specialist | Expert specialist for torrents domain tasks. | You are a Qbittorrent Torrents specialist. Help users manage and interact with Torrents functionality using the available tools. | qbittorrent-agent_torrents_toolset | torrents | qbittorrent-agent |
| Qbittorrent Transfer Specialist | Expert specialist for transfer domain tasks. | You are a Qbittorrent Transfer specialist. Help users manage and interact with Transfer functionality using the available tools. | qbittorrent-agent_transfer_toolset | transfer | qbittorrent-agent |
| Qbittorrent Rss Specialist | Expert specialist for rss domain tasks. | You are a Qbittorrent Rss specialist. Help users manage and interact with Rss functionality using the available tools. | qbittorrent-agent_rss_toolset | rss | qbittorrent-agent |
| Qbittorrent Search Specialist | Expert specialist for search domain tasks. | You are a Qbittorrent Search specialist. Help users manage and interact with Search functionality using the available tools. | qbittorrent-agent_search_toolset | search | qbittorrent-agent |
| Qbittorrent Log Specialist | Expert specialist for log domain tasks. | You are a Qbittorrent Log specialist. Help users manage and interact with Log functionality using the available tools. | qbittorrent-agent_log_toolset | log | qbittorrent-agent |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| qbittorrent-agent_app_toolset | Static hint toolset for app based on config env. | app | qbittorrent-agent |
| qbittorrent-agent_torrents_toolset | Static hint toolset for torrents based on config env. | torrents | qbittorrent-agent |
| qbittorrent-agent_transfer_toolset | Static hint toolset for transfer based on config env. | transfer | qbittorrent-agent |
| qbittorrent-agent_rss_toolset | Static hint toolset for rss based on config env. | rss | qbittorrent-agent |
| qbittorrent-agent_search_toolset | Static hint toolset for search based on config env. | search | qbittorrent-agent |
| qbittorrent-agent_log_toolset | Static hint toolset for log based on config env. | log | qbittorrent-agent |
