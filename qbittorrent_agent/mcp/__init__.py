"""Tool registrars beyond the API operations.

Every qBittorrent WebUI API operation is served as one typed tool from the
client methods (``qbittorrent_agent/api/client.py``,
CONN-QBITTORRENT-AGENT-SURFACE-R001). This package registers only the
knowledge-graph ingest tool.
"""

from qbittorrent_agent.mcp.mcp_kg import register_kg_tools

__all__ = ["register_kg_tools"]
