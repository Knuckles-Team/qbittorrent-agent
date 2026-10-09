"""MCP tools for app operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_connector_sdk.mcp.action_dispatch import resolve_action
from agent_connector_sdk.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


# One tiny extracted handler per action -- each preserves the exact
# client-method call and kwargs passthrough the if/elif chain used to
# perform inline. Kept module-level (not nested) so each has CCN 1 and
# is independently addressable/testable.
async def _app_get_application_version(client, **kwargs):
    return await run_blocking(client.get_version, **kwargs)


async def _app_get_api_version(client, **kwargs):
    return await run_blocking(client.get_api_version, **kwargs)


async def _app_get_build_info(client, **kwargs):
    return await run_blocking(client.get_build_info, **kwargs)


async def _app_shutdown_application(client, **kwargs):
    return await run_blocking(client.shutdown_application, **kwargs)


async def _app_get_preferences(client, **kwargs):
    return await run_blocking(client.get_preferences, **kwargs)


async def _app_set_preferences(client, **kwargs):
    return await run_blocking(client.set_preferences, **kwargs)


async def _app_get_default_save_path(client, **kwargs):
    return await run_blocking(client.get_default_save_path, **kwargs)


_APP_ACTION_HANDLERS: dict[str, Any] = {
    "get_application_version": _app_get_application_version,
    "get_api_version": _app_get_api_version,
    "get_build_info": _app_get_build_info,
    "shutdown_application": _app_shutdown_application,
    "get_preferences": _app_get_preferences,
    "set_preferences": _app_set_preferences,
    "get_default_save_path": _app_get_default_save_path,
}


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
        except Exception:
            return {"error": "Operation failed"}

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

        handler = _APP_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        raise ValueError(f"Unknown action: {action}")
