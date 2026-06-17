#!/usr/bin/python
"""qBittorrent MCP Server.

Provides the FastMCP tools wrapper for managing qBittorrent endpoints.
Tracks execution limits, budgets, and action workflows.

Action Execution Pipeline
Guardrail Engine
"""

import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    resolve_action,
    run_blocking,
)
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from qbittorrent_agent.auth import get_client

__version__ = "0.33.0"

logger = get_logger(name="qbittorrent-agent")
logger.setLevel(logging.INFO)


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
    ) -> Any:
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


def register_log_tools(mcp: FastMCP):
    @mcp.tool(tags={"log"})
    async def qbittorrent_log(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_main_log', 'get_peer_log'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage qbittorrent log operations."""
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

        valid_actions = ("get_main_log", "get_peer_log")
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_main_log":
            return await run_blocking(client.get_log, **kwargs)
        if action == "get_peer_log":
            return await run_blocking(client.get_peer_log, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
    ) -> Any:
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

        valid_actions = ("get_main_data", "get_torrent_peers_data")
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_main_data":
            return await run_blocking(client.get_main_data, **kwargs)
        if action == "get_torrent_peers_data":
            return await run_blocking(client.get_torrent_peers_data, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
    ) -> Any:
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


def register_torrents_tools(mcp: FastMCP):
    @mcp.tool(tags={"torrents"})
    async def qbittorrent_torrents(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_torrent_list', 'get_torrent_properties', 'get_torrent_trackers', 'get_torrent_webseeds', 'get_torrent_contents', 'get_torrent_piece_states', 'get_torrent_piece_hashes', 'pause_torrents', 'resume_torrents', 'delete_torrents', 'recheck_torrents', 'reannounce_torrents', 'edit_tracker', 'remove_trackers', 'add_peers', 'add_new_torrent', 'add_trackers_to_torrent', 'increase_torrent_priority', 'decrease_torrent_priority', 'top_torrent_priority', 'bottom_torrent_priority', 'set_file_priority', 'get_torrent_download_limit', 'set_torrent_download_limit', 'set_torrent_share_limit', 'get_torrent_upload_limit', 'set_torrent_upload_limit', 'set_torrent_location', 'set_torrent_name', 'set_torrent_category', 'get_all_categories', 'add_new_category', 'edit_category', 'remove_categories', 'add_torrent_tags', 'remove_torrent_tags', 'get_all_tags', 'create_tags', 'delete_tags', 'set_auto_management', 'toggle_sequential_download', 'toggle_first_last_piece_priority', 'set_force_start', 'set_super_seeding', 'rename_file', 'rename_folder'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage qbittorrent torrents operations."""
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
            "get_torrent_list",
            "get_torrent_properties",
            "get_torrent_trackers",
            "get_torrent_webseeds",
            "get_torrent_contents",
            "get_torrent_piece_states",
            "get_torrent_piece_hashes",
            "pause_torrents",
            "resume_torrents",
            "delete_torrents",
            "recheck_torrents",
            "reannounce_torrents",
            "edit_tracker",
            "remove_trackers",
            "add_peers",
            "add_new_torrent",
            "add_trackers_to_torrent",
            "increase_torrent_priority",
            "decrease_torrent_priority",
            "top_torrent_priority",
            "bottom_torrent_priority",
            "set_file_priority",
            "get_torrent_download_limit",
            "set_torrent_download_limit",
            "set_torrent_share_limit",
            "get_torrent_upload_limit",
            "set_torrent_upload_limit",
            "set_torrent_location",
            "set_torrent_name",
            "set_torrent_category",
            "get_all_categories",
            "add_new_category",
            "edit_category",
            "remove_categories",
            "add_torrent_tags",
            "remove_torrent_tags",
            "get_all_tags",
            "create_tags",
            "delete_tags",
            "set_auto_management",
            "toggle_sequential_download",
            "toggle_first_last_piece_priority",
            "set_force_start",
            "set_super_seeding",
            "rename_file",
            "rename_folder",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_torrent_list":
            return await run_blocking(client.get_torrents, **kwargs)
        if action == "get_torrent_properties":
            return await run_blocking(client.get_torrent_properties, **kwargs)
        if action == "get_torrent_trackers":
            return await run_blocking(client.get_torrent_trackers, **kwargs)
        if action == "get_torrent_webseeds":
            return await run_blocking(client.get_torrent_webseeds, **kwargs)
        if action == "get_torrent_contents":
            return await run_blocking(client.get_torrent_contents, **kwargs)
        if action == "get_torrent_piece_states":
            return await run_blocking(client.get_torrent_piece_states, **kwargs)
        if action == "get_torrent_piece_hashes":
            return await run_blocking(client.get_torrent_piece_hashes, **kwargs)
        if action == "pause_torrents":
            return await run_blocking(client.pause_torrents, **kwargs)
        if action == "resume_torrents":
            return await run_blocking(client.resume_torrents, **kwargs)
        if action == "delete_torrents":
            return await run_blocking(client.delete_torrents, **kwargs)
        if action == "recheck_torrents":
            return await run_blocking(client.recheck_torrents, **kwargs)
        if action == "reannounce_torrents":
            return await run_blocking(client.reannounce_torrents, **kwargs)
        if action == "edit_tracker":
            return await run_blocking(client.edit_tracker, **kwargs)
        if action == "remove_trackers":
            return await run_blocking(client.remove_trackers, **kwargs)
        if action == "add_peers":
            return await run_blocking(client.add_peers, **kwargs)
        if action == "add_new_torrent":
            return await run_blocking(client.add_torrent, **kwargs)
        if action == "add_trackers_to_torrent":
            return await run_blocking(client.add_trackers, **kwargs)
        if action == "increase_torrent_priority":
            return await run_blocking(client.increase_priority, **kwargs)
        if action == "decrease_torrent_priority":
            return await run_blocking(client.decrease_priority, **kwargs)
        if action == "top_torrent_priority":
            return await run_blocking(client.top_priority, **kwargs)
        if action == "bottom_torrent_priority":
            return await run_blocking(client.bottom_priority, **kwargs)
        if action == "set_file_priority":
            return await run_blocking(client.set_file_priority, **kwargs)
        if action == "get_torrent_download_limit":
            return await run_blocking(client.get_torrent_download_limit, **kwargs)
        if action == "set_torrent_download_limit":
            return await run_blocking(client.set_torrent_download_limit, **kwargs)
        if action == "set_torrent_share_limit":
            return await run_blocking(client.set_torrent_share_limit, **kwargs)
        if action == "get_torrent_upload_limit":
            return await run_blocking(client.get_torrent_upload_limit, **kwargs)
        if action == "set_torrent_upload_limit":
            return await run_blocking(client.set_torrent_upload_limit, **kwargs)
        if action == "set_torrent_location":
            return await run_blocking(client.set_torrent_location, **kwargs)
        if action == "set_torrent_name":
            return await run_blocking(client.set_torrent_name, **kwargs)
        if action == "set_torrent_category":
            return await run_blocking(client.set_torrent_category, **kwargs)
        if action == "get_all_categories":
            return await run_blocking(client.get_categories, **kwargs)
        if action == "add_new_category":
            return await run_blocking(client.create_category, **kwargs)
        if action == "edit_category":
            return await run_blocking(client.edit_category, **kwargs)
        if action == "remove_categories":
            return await run_blocking(client.remove_categories, **kwargs)
        if action == "add_torrent_tags":
            return await run_blocking(client.add_torrent_tags, **kwargs)
        if action == "remove_torrent_tags":
            return await run_blocking(client.remove_torrent_tags, **kwargs)
        if action == "get_all_tags":
            return await run_blocking(client.get_tags, **kwargs)
        if action == "create_tags":
            return await run_blocking(client.create_tags, **kwargs)
        if action == "delete_tags":
            return await run_blocking(client.delete_tags, **kwargs)
        if action == "set_auto_management":
            return await run_blocking(client.set_auto_management, **kwargs)
        if action == "toggle_sequential_download":
            return await run_blocking(client.toggle_sequential_download, **kwargs)
        if action == "toggle_first_last_piece_priority":
            return await run_blocking(client.toggle_first_last_piece_priority, **kwargs)
        if action == "set_force_start":
            return await run_blocking(client.set_force_start, **kwargs)
        if action == "set_super_seeding":
            return await run_blocking(client.set_super_seeding, **kwargs)
        if action == "rename_file":
            return await run_blocking(client.rename_file, **kwargs)
        if action == "rename_folder":
            return await run_blocking(client.rename_folder, **kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_rss_tools(mcp: FastMCP):
    @mcp.tool(tags={"rss"})
    async def qbittorrent_rss(
        action: str = Field(
            description="Action to perform. Must be one of: 'add_rss_folder', 'add_rss_feed', 'remove_rss_item', 'move_rss_item', 'get_all_rss_items', 'mark_rss_as_read', 'refresh_rss_item', 'set_rss_auto_downloading_rule', 'rename_rss_auto_downloading_rule', 'remove_rss_auto_downloading_rule', 'get_all_rss_auto_downloading_rules', 'get_all_rss_articles_matching_rule'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage qbittorrent rss operations."""
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
            "add_rss_folder",
            "add_rss_feed",
            "remove_rss_item",
            "move_rss_item",
            "get_all_rss_items",
            "mark_rss_as_read",
            "refresh_rss_item",
            "set_rss_auto_downloading_rule",
            "rename_rss_auto_downloading_rule",
            "remove_rss_auto_downloading_rule",
            "get_all_rss_auto_downloading_rules",
            "get_all_rss_articles_matching_rule",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "add_rss_folder":
            return await run_blocking(client.add_rss_folder, **kwargs)
        if action == "add_rss_feed":
            return await run_blocking(client.add_rss_feed, **kwargs)
        if action == "remove_rss_item":
            return await run_blocking(client.remove_rss_item, **kwargs)
        if action == "move_rss_item":
            return await run_blocking(client.move_rss_item, **kwargs)
        if action == "get_all_rss_items":
            return await run_blocking(client.get_rss_items, **kwargs)
        if action == "mark_rss_as_read":
            return await run_blocking(client.mark_rss_as_read, **kwargs)
        if action == "refresh_rss_item":
            return await run_blocking(client.refresh_rss_item, **kwargs)
        if action == "set_rss_auto_downloading_rule":
            return await run_blocking(client.set_rss_rule, **kwargs)
        if action == "rename_rss_auto_downloading_rule":
            return await run_blocking(client.rename_rss_rule, **kwargs)
        if action == "remove_rss_auto_downloading_rule":
            return await run_blocking(client.remove_rss_rule, **kwargs)
        if action == "get_all_rss_auto_downloading_rules":
            return await run_blocking(client.get_rss_rules, **kwargs)
        if action == "get_all_rss_articles_matching_rule":
            return await run_blocking(client.get_rss_matching_articles, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
    ) -> Any:
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


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="qbittorrent-agent MCP",
        version=__version__,
        instructions="qbittorrent-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_APPTOOL = to_boolean(os.getenv("APPTOOL", "True"))
    if DEFAULT_APPTOOL:
        register_app_tools(mcp)
    DEFAULT_LOGTOOL = to_boolean(os.getenv("LOGTOOL", "True"))
    if DEFAULT_LOGTOOL:
        register_log_tools(mcp)
    DEFAULT_SYNCTOOL = to_boolean(os.getenv("SYNCTOOL", "True"))
    if DEFAULT_SYNCTOOL:
        register_sync_tools(mcp)
    DEFAULT_TRANSFERTOOL = to_boolean(os.getenv("TRANSFERTOOL", "True"))
    if DEFAULT_TRANSFERTOOL:
        register_transfer_tools(mcp)
    DEFAULT_TORRENTSTOOL = to_boolean(os.getenv("TORRENTSTOOL", "True"))
    if DEFAULT_TORRENTSTOOL:
        register_torrents_tools(mcp)
    DEFAULT_RSSTOOL = to_boolean(os.getenv("RSSTOOL", "True"))
    if DEFAULT_RSSTOOL:
        register_rss_tools(mcp)
    DEFAULT_SEARCHTOOL = to_boolean(os.getenv("SEARCHTOOL", "True"))
    if DEFAULT_SEARCHTOOL:
        register_search_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"qbittorrent-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
