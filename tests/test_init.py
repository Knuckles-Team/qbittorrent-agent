from fastmcp import FastMCP

from qbittorrent_agent.mcp_server import get_mcp_instance


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "qbittorrent" in mcp.name.lower()


def test_import_qbittorrent_agent():
    """Test that the package can be imported."""
    pass
