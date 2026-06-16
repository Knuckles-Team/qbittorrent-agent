"""MCP tools for search operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


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
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

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

        if action == "start_search":
            return await run_blocking(client.search_start, **kwargs)
        if action == "stop_search":
            return await run_blocking(client.search_stop, **kwargs)
        if action == "get_search_status":
            return await run_blocking(client.search_status, **kwargs)
        if action == "get_search_results":
            return await run_blocking(client.search_results, **kwargs)
        if action == "delete_search":
            return await run_blocking(client.search_delete, **kwargs)
        if action == "get_search_plugins":
            return await run_blocking(client.get_search_plugins, **kwargs)
        if action == "install_search_plugin":
            return await run_blocking(client.install_search_plugin, **kwargs)
        if action == "uninstall_search_plugin":
            return await run_blocking(client.uninstall_search_plugin, **kwargs)
        if action == "enable_search_plugin":
            return await run_blocking(client.enable_search_plugin, **kwargs)
        if action == "update_search_plugins":
            return await run_blocking(client.update_search_plugins, **kwargs)
        raise ValueError(f"Unknown action: {action}")
