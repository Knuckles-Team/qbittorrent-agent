"""MCP tool registration modules for qbittorrent-agent.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from qbittorrent_agent.mcp.mcp_app import register_app_tools
from qbittorrent_agent.mcp.mcp_log import register_log_tools
from qbittorrent_agent.mcp.mcp_rss import register_rss_tools
from qbittorrent_agent.mcp.mcp_search import register_search_tools
from qbittorrent_agent.mcp.mcp_sync import register_sync_tools
from qbittorrent_agent.mcp.mcp_torrents import register_torrents_tools
from qbittorrent_agent.mcp.mcp_transfer import register_transfer_tools

__all__ = [
    "register_app_tools",
    "register_log_tools",
    "register_rss_tools",
    "register_search_tools",
    "register_sync_tools",
    "register_torrents_tools",
    "register_transfer_tools",
]
