"""MCP tools for transfer operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


def register_transfer_tools(mcp: FastMCP):
    @mcp.tool(tags={"transfer"})
    async def qbittorrent_transfer(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_global_transfer_info', 'get_speed_limits_mode', 'toggle_speed_limits_mode', 'get_global_download_limit', 'set_global_download_limit', 'get_global_upload_limit', 'set_global_upload_limit', 'ban_peers'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage qbittorrent transfer operations."""
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
            "get_global_transfer_info",
            "get_speed_limits_mode",
            "toggle_speed_limits_mode",
            "get_global_download_limit",
            "set_global_download_limit",
            "get_global_upload_limit",
            "set_global_upload_limit",
            "ban_peers",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_global_transfer_info":
            return await run_blocking(client.get_transfer_info, **kwargs)
        if action == "get_speed_limits_mode":
            return await run_blocking(client.get_speed_limits_mode, **kwargs)
        if action == "toggle_speed_limits_mode":
            return await run_blocking(client.toggle_speed_limits_mode, **kwargs)
        if action == "get_global_download_limit":
            return await run_blocking(client.get_global_download_limit, **kwargs)
        if action == "set_global_download_limit":
            return await run_blocking(client.set_global_download_limit, **kwargs)
        if action == "get_global_upload_limit":
            return await run_blocking(client.get_global_upload_limit, **kwargs)
        if action == "set_global_upload_limit":
            return await run_blocking(client.set_global_upload_limit, **kwargs)
        if action == "ban_peers":
            return await run_blocking(client.ban_peers, **kwargs)
        raise ValueError(f"Unknown action: {action}")
