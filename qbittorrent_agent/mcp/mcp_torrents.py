"""MCP tools for torrents operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

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

        if action == "get_torrent_list":
            return client.get_torrents(**kwargs)
        if action == "get_torrent_properties":
            return client.get_torrent_properties(**kwargs)
        if action == "get_torrent_trackers":
            return client.get_torrent_trackers(**kwargs)
        if action == "get_torrent_webseeds":
            return client.get_torrent_webseeds(**kwargs)
        if action == "get_torrent_contents":
            return client.get_torrent_contents(**kwargs)
        if action == "get_torrent_piece_states":
            return client.get_torrent_piece_states(**kwargs)
        if action == "get_torrent_piece_hashes":
            return client.get_torrent_piece_hashes(**kwargs)
        if action == "pause_torrents":
            return client.pause_torrents(**kwargs)
        if action == "resume_torrents":
            return client.resume_torrents(**kwargs)
        if action == "delete_torrents":
            return client.delete_torrents(**kwargs)
        if action == "recheck_torrents":
            return client.recheck_torrents(**kwargs)
        if action == "reannounce_torrents":
            return client.reannounce_torrents(**kwargs)
        if action == "edit_tracker":
            return client.edit_tracker(**kwargs)
        if action == "remove_trackers":
            return client.remove_trackers(**kwargs)
        if action == "add_peers":
            return client.add_peers(**kwargs)
        if action == "add_new_torrent":
            return client.add_torrent(**kwargs)
        if action == "add_trackers_to_torrent":
            return client.add_trackers(**kwargs)
        if action == "increase_torrent_priority":
            return client.increase_priority(**kwargs)
        if action == "decrease_torrent_priority":
            return client.decrease_priority(**kwargs)
        if action == "top_torrent_priority":
            return client.top_priority(**kwargs)
        if action == "bottom_torrent_priority":
            return client.bottom_priority(**kwargs)
        if action == "set_file_priority":
            return client.set_file_priority(**kwargs)
        if action == "get_torrent_download_limit":
            return client.get_torrent_download_limit(**kwargs)
        if action == "set_torrent_download_limit":
            return client.set_torrent_download_limit(**kwargs)
        if action == "set_torrent_share_limit":
            return client.set_torrent_share_limit(**kwargs)
        if action == "get_torrent_upload_limit":
            return client.get_torrent_upload_limit(**kwargs)
        if action == "set_torrent_upload_limit":
            return client.set_torrent_upload_limit(**kwargs)
        if action == "set_torrent_location":
            return client.set_torrent_location(**kwargs)
        if action == "set_torrent_name":
            return client.set_torrent_name(**kwargs)
        if action == "set_torrent_category":
            return client.set_torrent_category(**kwargs)
        if action == "get_all_categories":
            return client.get_categories(**kwargs)
        if action == "add_new_category":
            return client.create_category(**kwargs)
        if action == "edit_category":
            return client.edit_category(**kwargs)
        if action == "remove_categories":
            return client.remove_categories(**kwargs)
        if action == "add_torrent_tags":
            return client.add_torrent_tags(**kwargs)
        if action == "remove_torrent_tags":
            return client.remove_torrent_tags(**kwargs)
        if action == "get_all_tags":
            return client.get_tags(**kwargs)
        if action == "create_tags":
            return client.create_tags(**kwargs)
        if action == "delete_tags":
            return client.delete_tags(**kwargs)
        if action == "set_auto_management":
            return client.set_auto_management(**kwargs)
        if action == "toggle_sequential_download":
            return client.toggle_sequential_download(**kwargs)
        if action == "toggle_first_last_piece_priority":
            return client.toggle_first_last_piece_priority(**kwargs)
        if action == "set_force_start":
            return client.set_force_start(**kwargs)
        if action == "set_super_seeding":
            return client.set_super_seeding(**kwargs)
        if action == "rename_file":
            return client.rename_file(**kwargs)
        if action == "rename_folder":
            return client.rename_folder(**kwargs)
        raise ValueError(f"Unknown action: {action}")
