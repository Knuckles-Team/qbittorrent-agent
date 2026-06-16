"""MCP tools for sync operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


def register_sync_tools(mcp: FastMCP):
    @mcp.tool(tags={"sync"})
    async def qbittorrent_sync(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_main_data', 'get_torrent_peers_data'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage qbittorrent sync operations."""
        if ctx:
            import inspect

            res = ctx.info("Executing tool...")
            if inspect.isawaitable(res):
                await res
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_main_data",
            "get_torrent_peers_data",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_main_data":
            return await run_blocking(client.get_main_data, **kwargs)
        if action == "get_torrent_peers_data":
            return await run_blocking(client.get_torrent_peers_data, **kwargs)
        raise ValueError(f"Unknown action: {action}")
