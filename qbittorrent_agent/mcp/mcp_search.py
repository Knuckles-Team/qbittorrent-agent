"""MCP tools for search operations.

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
async def _search_start_search(client, **kwargs):
    return await run_blocking(client.search_start, **kwargs)


async def _search_stop_search(client, **kwargs):
    return await run_blocking(client.search_stop, **kwargs)


async def _search_get_search_status(client, **kwargs):
    return await run_blocking(client.search_status, **kwargs)


async def _search_get_search_results(client, **kwargs):
    return await run_blocking(client.search_results, **kwargs)


async def _search_delete_search(client, **kwargs):
    return await run_blocking(client.search_delete, **kwargs)


async def _search_get_search_plugins(client, **kwargs):
    return await run_blocking(client.get_search_plugins, **kwargs)


async def _search_install_search_plugin(client, **kwargs):
    return await run_blocking(client.install_search_plugin, **kwargs)


async def _search_uninstall_search_plugin(client, **kwargs):
    return await run_blocking(client.uninstall_search_plugin, **kwargs)


async def _search_enable_search_plugin(client, **kwargs):
    return await run_blocking(client.enable_search_plugin, **kwargs)


async def _search_update_search_plugins(client, **kwargs):
    return await run_blocking(client.update_search_plugins, **kwargs)


_SEARCH_ACTION_HANDLERS: dict[str, Any] = {
    "start_search": _search_start_search,
    "stop_search": _search_stop_search,
    "get_search_status": _search_get_search_status,
    "get_search_results": _search_get_search_results,
    "delete_search": _search_delete_search,
    "get_search_plugins": _search_get_search_plugins,
    "install_search_plugin": _search_install_search_plugin,
    "uninstall_search_plugin": _search_uninstall_search_plugin,
    "enable_search_plugin": _search_enable_search_plugin,
    "update_search_plugins": _search_update_search_plugins,
}


def register_search_tools(mcp: FastMCP):
    @mcp.tool(tags={"search"})
    async def qbittorrent_search(
        action: str = Field(
            description="Action to perform. Must be one of: 'start_search', 'stop_search', 'get_search_status', 'get_search_results', 'delete_search', 'get_search_plugins', 'install_search_plugin', 'uninstall_search_plugin', 'enable_search_plugin', 'update_search_plugins'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage qbittorrent search operations."""
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
            "start_search",
            "stop_search",
            "get_search_status",
            "get_search_results",
            "delete_search",
            "get_search_plugins",
            "install_search_plugin",
            "uninstall_search_plugin",
            "enable_search_plugin",
            "update_search_plugins",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _SEARCH_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        raise ValueError(f"Unknown action: {action}")
