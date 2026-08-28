"""MCP tools for transfer operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


# One tiny extracted handler per action -- each preserves the exact
# client-method call and kwargs passthrough the if/elif chain used to
# perform inline. Kept module-level (not nested) so each has CCN 1 and
# is independently addressable/testable.
async def _transfer_get_global_transfer_info(client, **kwargs):
    return await run_blocking(client.get_transfer_info, **kwargs)


async def _transfer_get_speed_limits_mode(client, **kwargs):
    return await run_blocking(client.get_speed_limits_mode, **kwargs)


async def _transfer_toggle_speed_limits_mode(client, **kwargs):
    return await run_blocking(client.toggle_speed_limits_mode, **kwargs)


async def _transfer_get_global_download_limit(client, **kwargs):
    return await run_blocking(client.get_global_download_limit, **kwargs)


async def _transfer_set_global_download_limit(client, **kwargs):
    return await run_blocking(client.set_global_download_limit, **kwargs)


async def _transfer_get_global_upload_limit(client, **kwargs):
    return await run_blocking(client.get_global_upload_limit, **kwargs)


async def _transfer_set_global_upload_limit(client, **kwargs):
    return await run_blocking(client.set_global_upload_limit, **kwargs)


async def _transfer_ban_peers(client, **kwargs):
    return await run_blocking(client.ban_peers, **kwargs)


_TRANSFER_ACTION_HANDLERS: dict[str, Any] = {
    "get_global_transfer_info": _transfer_get_global_transfer_info,
    "get_speed_limits_mode": _transfer_get_speed_limits_mode,
    "toggle_speed_limits_mode": _transfer_toggle_speed_limits_mode,
    "get_global_download_limit": _transfer_get_global_download_limit,
    "set_global_download_limit": _transfer_set_global_download_limit,
    "get_global_upload_limit": _transfer_get_global_upload_limit,
    "set_global_upload_limit": _transfer_set_global_upload_limit,
    "ban_peers": _transfer_ban_peers,
}


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
        except Exception:
            return {"error": "Operation failed"}

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

        handler = _TRANSFER_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        raise ValueError(f"Unknown action: {action}")
