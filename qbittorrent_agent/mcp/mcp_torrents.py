"""MCP tools for torrents operations.

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
async def _torrents_get_torrent_list(client, **kwargs):
    return await run_blocking(client.get_torrents, **kwargs)


async def _torrents_get_torrent_properties(client, **kwargs):
    return await run_blocking(client.get_torrent_properties, **kwargs)


async def _torrents_get_torrent_trackers(client, **kwargs):
    return await run_blocking(client.get_torrent_trackers, **kwargs)


async def _torrents_get_torrent_webseeds(client, **kwargs):
    return await run_blocking(client.get_torrent_webseeds, **kwargs)


async def _torrents_get_torrent_contents(client, **kwargs):
    return await run_blocking(client.get_torrent_contents, **kwargs)


async def _torrents_get_torrent_piece_states(client, **kwargs):
    return await run_blocking(client.get_torrent_piece_states, **kwargs)


async def _torrents_get_torrent_piece_hashes(client, **kwargs):
    return await run_blocking(client.get_torrent_piece_hashes, **kwargs)


async def _torrents_pause_torrents(client, **kwargs):
    return await run_blocking(client.pause_torrents, **kwargs)


async def _torrents_resume_torrents(client, **kwargs):
    return await run_blocking(client.resume_torrents, **kwargs)


async def _torrents_delete_torrents(client, **kwargs):
    return await run_blocking(client.delete_torrents, **kwargs)


async def _torrents_recheck_torrents(client, **kwargs):
    return await run_blocking(client.recheck_torrents, **kwargs)


async def _torrents_reannounce_torrents(client, **kwargs):
    return await run_blocking(client.reannounce_torrents, **kwargs)


async def _torrents_edit_tracker(client, **kwargs):
    return await run_blocking(client.edit_tracker, **kwargs)


async def _torrents_remove_trackers(client, **kwargs):
    return await run_blocking(client.remove_trackers, **kwargs)


async def _torrents_add_peers(client, **kwargs):
    return await run_blocking(client.add_peers, **kwargs)


async def _torrents_add_new_torrent(client, **kwargs):
    return await run_blocking(client.add_torrent, **kwargs)


async def _torrents_add_trackers_to_torrent(client, **kwargs):
    return await run_blocking(client.add_trackers, **kwargs)


async def _torrents_increase_torrent_priority(client, **kwargs):
    return await run_blocking(client.increase_priority, **kwargs)


async def _torrents_decrease_torrent_priority(client, **kwargs):
    return await run_blocking(client.decrease_priority, **kwargs)


async def _torrents_top_torrent_priority(client, **kwargs):
    return await run_blocking(client.top_priority, **kwargs)


async def _torrents_bottom_torrent_priority(client, **kwargs):
    return await run_blocking(client.bottom_priority, **kwargs)


async def _torrents_set_file_priority(client, **kwargs):
    return await run_blocking(client.set_file_priority, **kwargs)


async def _torrents_get_torrent_download_limit(client, **kwargs):
    return await run_blocking(client.get_torrent_download_limit, **kwargs)


async def _torrents_set_torrent_download_limit(client, **kwargs):
    return await run_blocking(client.set_torrent_download_limit, **kwargs)


async def _torrents_set_torrent_share_limit(client, **kwargs):
    return await run_blocking(client.set_torrent_share_limit, **kwargs)


async def _torrents_get_torrent_upload_limit(client, **kwargs):
    return await run_blocking(client.get_torrent_upload_limit, **kwargs)


async def _torrents_set_torrent_upload_limit(client, **kwargs):
    return await run_blocking(client.set_torrent_upload_limit, **kwargs)


async def _torrents_set_torrent_location(client, **kwargs):
    return await run_blocking(client.set_torrent_location, **kwargs)


async def _torrents_set_torrent_name(client, **kwargs):
    return await run_blocking(client.set_torrent_name, **kwargs)


async def _torrents_set_torrent_category(client, **kwargs):
    return await run_blocking(client.set_torrent_category, **kwargs)


async def _torrents_get_all_categories(client, **kwargs):
    return await run_blocking(client.get_categories, **kwargs)


async def _torrents_add_new_category(client, **kwargs):
    return await run_blocking(client.create_category, **kwargs)


async def _torrents_edit_category(client, **kwargs):
    return await run_blocking(client.edit_category, **kwargs)


async def _torrents_remove_categories(client, **kwargs):
    return await run_blocking(client.remove_categories, **kwargs)


async def _torrents_add_torrent_tags(client, **kwargs):
    return await run_blocking(client.add_torrent_tags, **kwargs)


async def _torrents_remove_torrent_tags(client, **kwargs):
    return await run_blocking(client.remove_torrent_tags, **kwargs)


async def _torrents_get_all_tags(client, **kwargs):
    return await run_blocking(client.get_tags, **kwargs)


async def _torrents_create_tags(client, **kwargs):
    return await run_blocking(client.create_tags, **kwargs)


async def _torrents_delete_tags(client, **kwargs):
    return await run_blocking(client.delete_tags, **kwargs)


async def _torrents_set_auto_management(client, **kwargs):
    return await run_blocking(client.set_auto_management, **kwargs)


async def _torrents_toggle_sequential_download(client, **kwargs):
    return await run_blocking(client.toggle_sequential_download, **kwargs)


async def _torrents_toggle_first_last_piece_priority(client, **kwargs):
    return await run_blocking(client.toggle_first_last_piece_priority, **kwargs)


async def _torrents_set_force_start(client, **kwargs):
    return await run_blocking(client.set_force_start, **kwargs)


async def _torrents_set_super_seeding(client, **kwargs):
    return await run_blocking(client.set_super_seeding, **kwargs)


async def _torrents_rename_file(client, **kwargs):
    return await run_blocking(client.rename_file, **kwargs)


async def _torrents_rename_folder(client, **kwargs):
    return await run_blocking(client.rename_folder, **kwargs)


_TORRENTS_ACTION_HANDLERS: dict[str, Any] = {
    "get_torrent_list": _torrents_get_torrent_list,
    "get_torrent_properties": _torrents_get_torrent_properties,
    "get_torrent_trackers": _torrents_get_torrent_trackers,
    "get_torrent_webseeds": _torrents_get_torrent_webseeds,
    "get_torrent_contents": _torrents_get_torrent_contents,
    "get_torrent_piece_states": _torrents_get_torrent_piece_states,
    "get_torrent_piece_hashes": _torrents_get_torrent_piece_hashes,
    "pause_torrents": _torrents_pause_torrents,
    "resume_torrents": _torrents_resume_torrents,
    "delete_torrents": _torrents_delete_torrents,
    "recheck_torrents": _torrents_recheck_torrents,
    "reannounce_torrents": _torrents_reannounce_torrents,
    "edit_tracker": _torrents_edit_tracker,
    "remove_trackers": _torrents_remove_trackers,
    "add_peers": _torrents_add_peers,
    "add_new_torrent": _torrents_add_new_torrent,
    "add_trackers_to_torrent": _torrents_add_trackers_to_torrent,
    "increase_torrent_priority": _torrents_increase_torrent_priority,
    "decrease_torrent_priority": _torrents_decrease_torrent_priority,
    "top_torrent_priority": _torrents_top_torrent_priority,
    "bottom_torrent_priority": _torrents_bottom_torrent_priority,
    "set_file_priority": _torrents_set_file_priority,
    "get_torrent_download_limit": _torrents_get_torrent_download_limit,
    "set_torrent_download_limit": _torrents_set_torrent_download_limit,
    "set_torrent_share_limit": _torrents_set_torrent_share_limit,
    "get_torrent_upload_limit": _torrents_get_torrent_upload_limit,
    "set_torrent_upload_limit": _torrents_set_torrent_upload_limit,
    "set_torrent_location": _torrents_set_torrent_location,
    "set_torrent_name": _torrents_set_torrent_name,
    "set_torrent_category": _torrents_set_torrent_category,
    "get_all_categories": _torrents_get_all_categories,
    "add_new_category": _torrents_add_new_category,
    "edit_category": _torrents_edit_category,
    "remove_categories": _torrents_remove_categories,
    "add_torrent_tags": _torrents_add_torrent_tags,
    "remove_torrent_tags": _torrents_remove_torrent_tags,
    "get_all_tags": _torrents_get_all_tags,
    "create_tags": _torrents_create_tags,
    "delete_tags": _torrents_delete_tags,
    "set_auto_management": _torrents_set_auto_management,
    "toggle_sequential_download": _torrents_toggle_sequential_download,
    "toggle_first_last_piece_priority": _torrents_toggle_first_last_piece_priority,
    "set_force_start": _torrents_set_force_start,
    "set_super_seeding": _torrents_set_super_seeding,
    "rename_file": _torrents_rename_file,
    "rename_folder": _torrents_rename_folder,
}


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
        except Exception:
            return {"error": "Operation failed"}

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

        handler = _TORRENTS_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        raise ValueError(f"Unknown action: {action}")
