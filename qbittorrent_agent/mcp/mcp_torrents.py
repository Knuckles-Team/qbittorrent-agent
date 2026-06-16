"""MCP tools for torrents operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


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
    ) -> dict:
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
