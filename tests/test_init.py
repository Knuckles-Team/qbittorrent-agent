from fastmcp import FastMCP

from scion_sdk.connector import build_server


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    _, mcp = build_server("qbittorrent_agent", command_args=[])
    assert isinstance(mcp, FastMCP)
    assert "qbittorrent" in mcp.name.lower()


def test_import_qbittorrent_agent():
    """Test that the package can be imported."""
    pass
