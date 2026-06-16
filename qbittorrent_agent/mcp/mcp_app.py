"""MCP tools for app operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


def register_app_tools(mcp: FastMCP):
    @mcp.tool(tags={"app"})
    async def qbittorrent_app(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_application_version', 'get_api_version', 'get_build_info', 'shutdown_application', 'get_preferences', 'set_preferences', 'get_default_save_path'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage qbittorrent app operations."""
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
            "get_application_version",
            "get_api_version",
            "get_build_info",
            "shutdown_application",
            "get_preferences",
            "set_preferences",
            "get_default_save_path",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_application_version":
            return await run_blocking(client.get_version, **kwargs)
        if action == "get_api_version":
            return await run_blocking(client.get_api_version, **kwargs)
        if action == "get_build_info":
            return await run_blocking(client.get_build_info, **kwargs)
        if action == "shutdown_application":
            return await run_blocking(client.shutdown_application, **kwargs)
        if action == "get_preferences":
            return await run_blocking(client.get_preferences, **kwargs)
        if action == "set_preferences":
            return await run_blocking(client.set_preferences, **kwargs)
        if action == "get_default_save_path":
            return await run_blocking(client.get_default_save_path, **kwargs)
        raise ValueError(f"Unknown action: {action}")
