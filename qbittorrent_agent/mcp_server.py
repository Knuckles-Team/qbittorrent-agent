#!/usr/bin/python
import warnings

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
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from qbittorrent_agent.auth import get_client

__version__ = "0.10.0"

logger = get_logger(name="qbittorrent-agent")
logger.setLevel(logging.INFO)


def register_app_tools(mcp: FastMCP):
    @mcp.tool(tags={"app"})
    async def qbittorrent_app(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_application_version', 'get_api_version', 'get_build_info', 'shutdown_application', 'get_preferences', 'set_preferences', 'get_default_save_path'"
        ),
        preferences: dict | None = Field(default=None, description="preferences"),
        client=Depends(get_client),
    ) -> dict:
        """Manage app operations.

        Actions:
          - 'get_application_version': Call get_application_version
          - 'get_api_version': Get API version.
          - 'get_build_info': Get build info.
          - 'shutdown_application': Shutdown application.
          - 'get_preferences': Get application preferences.
          - 'set_preferences': Set application preferences.
          - 'get_default_save_path': Get default save path.
        """
        kwargs: dict[str, Any]
        if action == "get_application_version":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_application_version(**kwargs)
        if action == "get_api_version":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_api_version(**kwargs)
        if action == "get_build_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_build_info(**kwargs)
        if action == "shutdown_application":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.shutdown_application(**kwargs)
        if action == "get_preferences":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_preferences(**kwargs)
        if action == "set_preferences":
            kwargs = {"preferences": preferences}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_preferences(**kwargs)
        if action == "get_default_save_path":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_default_save_path(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_application_version', 'get_api_version', 'get_build_info', 'shutdown_application', 'get_preferences', 'set_preferences', 'get_default_save_path"
        )


def register_log_tools(mcp: FastMCP):
    @mcp.tool(tags={"log"})
    async def qbittorrent_log(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_main_log', 'get_peer_log'"
        ),
        last_known_id: int | None = Field(default=None, description="last known id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage log operations.

        Actions:
          - 'get_main_log': Call get_main_log
          - 'get_peer_log': Get peer log.
        """
        kwargs: dict[str, Any]
        if action == "get_main_log":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_main_log(**kwargs)
        if action == "get_peer_log":
            kwargs = {"last_known_id": last_known_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_peer_log(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_main_log', 'get_peer_log"
        )


def register_sync_tools(mcp: FastMCP):
    @mcp.tool(tags={"sync"})
    async def qbittorrent_sync(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_main_data', 'get_torrent_peers_data'"
        ),
        rid: int | None = Field(default=None, description="rid"),
        hash: str | None = Field(default=None, description="hash"),
        client=Depends(get_client),
    ) -> dict:
        """Manage sync operations.

        Actions:
          - 'get_main_data': Get main data.
          - 'get_torrent_peers_data': Get torrent peers data.
        """
        kwargs: dict[str, Any]
        if action == "get_main_data":
            kwargs = {"rid": rid}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_main_data(**kwargs)
        if action == "get_torrent_peers_data":
            kwargs = {"hash": hash, "rid": rid}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_peers_data(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_main_data', 'get_torrent_peers_data"
        )


def register_transfer_tools(mcp: FastMCP):
    @mcp.tool(tags={"transfer"})
    async def qbittorrent_transfer(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_global_transfer_info', 'get_speed_limits_mode', 'toggle_speed_limits_mode', 'get_global_download_limit', 'set_global_download_limit', 'get_global_upload_limit', 'set_global_upload_limit', 'ban_peers'"
        ),
        limit: int | None = Field(default=None, description="limit"),
        peers: str | None = Field(default=None, description="peers"),
        client=Depends(get_client),
    ) -> dict:
        """Manage transfer operations.

        Actions:
          - 'get_global_transfer_info': Call get_global_transfer_info
          - 'get_speed_limits_mode': Get alternative speed limits state (1 if enabled, 0 otherwise).
          - 'toggle_speed_limits_mode': Toggle alternative speed limits.
          - 'get_global_download_limit': Get global download limit in bytes/second.
          - 'set_global_download_limit': Set global download limit in bytes/second.
          - 'get_global_upload_limit': Get global upload limit in bytes/second.
          - 'set_global_upload_limit': Set global upload limit in bytes/second.
          - 'ban_peers': Ban peers. 'peers' is a string of peers separated by | (host:port).
        """
        kwargs: dict[str, Any]
        if action == "get_global_transfer_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_global_transfer_info(**kwargs)
        if action == "get_speed_limits_mode":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_speed_limits_mode(**kwargs)
        if action == "toggle_speed_limits_mode":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.toggle_speed_limits_mode(**kwargs)
        if action == "get_global_download_limit":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_global_download_limit(**kwargs)
        if action == "set_global_download_limit":
            kwargs = {"limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_global_download_limit(**kwargs)
        if action == "get_global_upload_limit":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_global_upload_limit(**kwargs)
        if action == "set_global_upload_limit":
            kwargs = {"limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_global_upload_limit(**kwargs)
        if action == "ban_peers":
            kwargs = {"peers": peers}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.ban_peers(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_global_transfer_info', 'get_speed_limits_mode', 'toggle_speed_limits_mode', 'get_global_download_limit', 'set_global_download_limit', 'get_global_upload_limit', 'set_global_upload_limit', 'ban_peers"
        )


def register_torrents_tools(mcp: FastMCP):
    @mcp.tool(tags={"torrents"})
    async def qbittorrent_torrents(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_torrent_list', 'get_torrent_properties', 'get_torrent_trackers', 'get_torrent_webseeds', 'get_torrent_contents', 'get_torrent_piece_states', 'get_torrent_piece_hashes', 'pause_torrents', 'resume_torrents', 'delete_torrents', 'recheck_torrents', 'reannounce_torrents', 'edit_tracker', 'remove_trackers', 'add_peers', 'add_new_torrent', 'add_trackers_to_torrent', 'increase_torrent_priority', 'decrease_torrent_priority', 'top_torrent_priority', 'bottom_torrent_priority', 'set_file_priority', 'get_torrent_download_limit', 'set_torrent_download_limit', 'set_torrent_share_limit', 'get_torrent_upload_limit', 'set_torrent_upload_limit', 'set_torrent_location', 'set_torrent_name', 'set_torrent_category', 'get_all_categories', 'add_new_category', 'edit_category', 'remove_categories', 'add_torrent_tags', 'remove_torrent_tags', 'get_all_tags', 'create_tags', 'delete_tags', 'set_auto_management', 'toggle_sequential_download', 'toggle_first_last_piece_priority', 'set_force_start', 'set_super_seeding', 'rename_file', 'rename_folder'"
        ),
        hash: str | None = Field(default=None, description="hash"),
        indexes: str | None = Field(default=None, description="indexes"),
        hashes: str | None = Field(default=None, description="hashes"),
        delete_files: bool | None = Field(default=None, description="delete files"),
        orig_url: str | None = Field(default=None, description="orig url"),
        new_url: str | None = Field(default=None, description="new url"),
        urls: str | None = Field(default=None, description="urls"),
        peers: str | None = Field(default=None, description="peers"),
        id: str | None = Field(default=None, description="id"),
        priority: int | None = Field(default=None, description="priority"),
        limit: int | None = Field(default=None, description="limit"),
        ratio_limit: float | None = Field(default=None, description="ratio limit"),
        seeding_time_limit: int | None = Field(
            default=None, description="seeding time limit"
        ),
        inactive_seeding_time_limit: int | None = Field(
            default=None, description="inactive seeding time limit"
        ),
        location: str | None = Field(default=None, description="location"),
        name: str | None = Field(default=None, description="name"),
        category: str | None = Field(default=None, description="category"),
        save_path: str | None = Field(default=None, description="save path"),
        categories: str | None = Field(default=None, description="categories"),
        tags: str | None = Field(default=None, description="tags"),
        enable: bool | None = Field(default=None, description="enable"),
        value: bool | None = Field(default=None, description="value"),
        old_path: str | None = Field(default=None, description="old path"),
        new_path: str | None = Field(default=None, description="new path"),
        client=Depends(get_client),
    ) -> dict:
        """Manage torrents operations.

        Actions:
          - 'get_torrent_list': Call get_torrent_list
          - 'get_torrent_properties': Get torrent generic properties.
          - 'get_torrent_trackers': Get torrent trackers.
          - 'get_torrent_webseeds': Get torrent web seeds.
          - 'get_torrent_contents': Get torrent contents.
          - 'get_torrent_piece_states': Get torrent pieces' states.
          - 'get_torrent_piece_hashes': Get torrent pieces' hashes.
          - 'pause_torrents': Pause torrents.
          - 'resume_torrents': Resume torrents.
          - 'delete_torrents': Delete torrents.
          - 'recheck_torrents': Recheck torrents.
          - 'reannounce_torrents': Reannounce torrents.
          - 'edit_tracker': Edit tracker.
          - 'remove_trackers': Remove trackers.
          - 'add_peers': Add peers.
          - 'add_new_torrent': Call add_new_torrent
          - 'add_trackers_to_torrent': Call add_trackers_to_torrent
          - 'increase_torrent_priority': Call increase_torrent_priority
          - 'decrease_torrent_priority': Call decrease_torrent_priority
          - 'top_torrent_priority': Call top_torrent_priority
          - 'bottom_torrent_priority': Call bottom_torrent_priority
          - 'set_file_priority': Set file priority.
          - 'get_torrent_download_limit': Get torrent download limit.
          - 'set_torrent_download_limit': Set torrent download limit.
          - 'set_torrent_share_limit': Set torrent share limit.
          - 'get_torrent_upload_limit': Get torrent upload limit.
          - 'set_torrent_upload_limit': Set torrent upload limit.
          - 'set_torrent_location': Set torrent location.
          - 'set_torrent_name': Set torrent name.
          - 'set_torrent_category': Set torrent category.
          - 'get_all_categories': Call get_all_categories
          - 'add_new_category': Call add_new_category
          - 'edit_category': Edit category.
          - 'remove_categories': Remove categories. 'categories' is
          - 'add_torrent_tags': Add torrent tags.
          - 'remove_torrent_tags': Remove torrent tags.
          - 'get_all_tags': Call get_all_tags
          - 'create_tags': Create tags.
          - 'delete_tags': Delete tags.
          - 'set_auto_management': Set automatic torrent management.
          - 'toggle_sequential_download': Toggle sequential download.
          - 'toggle_first_last_piece_priority': Set first/last piece priority.
          - 'set_force_start': Set force start.
          - 'set_super_seeding': Set super seeding.
          - 'rename_file': Rename file.
          - 'rename_folder': Rename folder.
        """
        kwargs: dict[str, Any]
        if action == "get_torrent_list":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_list(**kwargs)
        if action == "get_torrent_properties":
            kwargs = {"hash": hash}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_properties(**kwargs)
        if action == "get_torrent_trackers":
            kwargs = {"hash": hash}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_trackers(**kwargs)
        if action == "get_torrent_webseeds":
            kwargs = {"hash": hash}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_webseeds(**kwargs)
        if action == "get_torrent_contents":
            kwargs = {"hash": hash, "indexes": indexes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_contents(**kwargs)
        if action == "get_torrent_piece_states":
            kwargs = {"hash": hash}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_piece_states(**kwargs)
        if action == "get_torrent_piece_hashes":
            kwargs = {"hash": hash}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_piece_hashes(**kwargs)
        if action == "pause_torrents":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.pause_torrents(**kwargs)
        if action == "resume_torrents":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.resume_torrents(**kwargs)
        if action == "delete_torrents":
            kwargs = {"hashes": hashes, "delete_files": delete_files}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_torrents(**kwargs)
        if action == "recheck_torrents":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.recheck_torrents(**kwargs)
        if action == "reannounce_torrents":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.reannounce_torrents(**kwargs)
        if action == "edit_tracker":
            kwargs = {
                "hash": hash,
                "orig_url": orig_url,
                "new_url": new_url,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.edit_tracker(**kwargs)
        if action == "remove_trackers":
            kwargs = {"hash": hash, "urls": urls}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_trackers(**kwargs)
        if action == "add_peers":
            kwargs = {"hashes": hashes, "peers": peers}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_peers(**kwargs)
        if action == "add_new_torrent":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_new_torrent(**kwargs)
        if action == "add_trackers_to_torrent":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_trackers_to_torrent(**kwargs)
        if action == "increase_torrent_priority":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.increase_torrent_priority(**kwargs)
        if action == "decrease_torrent_priority":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.decrease_torrent_priority(**kwargs)
        if action == "top_torrent_priority":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.top_torrent_priority(**kwargs)
        if action == "bottom_torrent_priority":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bottom_torrent_priority(**kwargs)
        if action == "set_file_priority":
            kwargs = {"hash": hash, "id": id, "priority": priority}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_file_priority(**kwargs)
        if action == "get_torrent_download_limit":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_download_limit(**kwargs)
        if action == "set_torrent_download_limit":
            kwargs = {"hashes": hashes, "limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_download_limit(**kwargs)
        if action == "set_torrent_share_limit":
            kwargs = {
                "hashes": hashes,
                "ratio_limit": ratio_limit,
                "seeding_time_limit": seeding_time_limit,
                "inactive_seeding_time_limit": inactive_seeding_time_limit,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_share_limit(**kwargs)
        if action == "get_torrent_upload_limit":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_torrent_upload_limit(**kwargs)
        if action == "set_torrent_upload_limit":
            kwargs = {"hashes": hashes, "limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_upload_limit(**kwargs)
        if action == "set_torrent_location":
            kwargs = {"hashes": hashes, "location": location}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_location(**kwargs)
        if action == "set_torrent_name":
            kwargs = {"hash": hash, "name": name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_name(**kwargs)
        if action == "set_torrent_category":
            kwargs = {"hashes": hashes, "category": category}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_torrent_category(**kwargs)
        if action == "get_all_categories":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_categories(**kwargs)
        if action == "add_new_category":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_new_category(**kwargs)
        if action == "edit_category":
            kwargs = {"category": category, "save_path": save_path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.edit_category(**kwargs)
        if action == "remove_categories":
            kwargs = {"categories": categories}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_categories(**kwargs)
        if action == "add_torrent_tags":
            kwargs = {"hashes": hashes, "tags": tags}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_torrent_tags(**kwargs)
        if action == "remove_torrent_tags":
            kwargs = {"hashes": hashes, "tags": tags}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_torrent_tags(**kwargs)
        if action == "get_all_tags":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_tags(**kwargs)
        if action == "create_tags":
            kwargs = {"tags": tags}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_tags(**kwargs)
        if action == "delete_tags":
            kwargs = {"tags": tags}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_tags(**kwargs)
        if action == "set_auto_management":
            kwargs = {"hashes": hashes, "enable": enable}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_auto_management(**kwargs)
        if action == "toggle_sequential_download":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.toggle_sequential_download(**kwargs)
        if action == "toggle_first_last_piece_priority":
            kwargs = {"hashes": hashes}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.toggle_first_last_piece_priority(**kwargs)
        if action == "set_force_start":
            kwargs = {"hashes": hashes, "value": value}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_force_start(**kwargs)
        if action == "set_super_seeding":
            kwargs = {"hashes": hashes, "value": value}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_super_seeding(**kwargs)
        if action == "rename_file":
            kwargs = {
                "hash": hash,
                "old_path": old_path,
                "new_path": new_path,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.rename_file(**kwargs)
        if action == "rename_folder":
            kwargs = {
                "hash": hash,
                "old_path": old_path,
                "new_path": new_path,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.rename_folder(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_torrent_list', 'get_torrent_properties', 'get_torrent_trackers', 'get_torrent_webseeds', 'get_torrent_contents', 'get_torrent_piece_states', 'get_torrent_piece_hashes', 'pause_torrents', 'resume_torrents', 'delete_torrents', 'recheck_torrents', 'reannounce_torrents', 'edit_tracker', 'remove_trackers', 'add_peers', 'add_new_torrent', 'add_trackers_to_torrent', 'increase_torrent_priority', 'decrease_torrent_priority', 'top_torrent_priority', 'bottom_torrent_priority', 'set_file_priority', 'get_torrent_download_limit', 'set_torrent_download_limit', 'set_torrent_share_limit', 'get_torrent_upload_limit', 'set_torrent_upload_limit', 'set_torrent_location', 'set_torrent_name', 'set_torrent_category', 'get_all_categories', 'add_new_category', 'edit_category', 'remove_categories', 'add_torrent_tags', 'remove_torrent_tags', 'get_all_tags', 'create_tags', 'delete_tags', 'set_auto_management', 'toggle_sequential_download', 'toggle_first_last_piece_priority', 'set_force_start', 'set_super_seeding', 'rename_file', 'rename_folder"
        )


def register_rss_tools(mcp: FastMCP):
    @mcp.tool(tags={"rss"})
    async def qbittorrent_rss(
        action: str = Field(
            description="Action to perform. Must be one of: 'add_rss_folder', 'add_rss_feed', 'remove_rss_item', 'move_rss_item', 'get_all_rss_items', 'mark_rss_as_read', 'refresh_rss_item', 'set_rss_auto_downloading_rule', 'rename_rss_auto_downloading_rule', 'remove_rss_auto_downloading_rule', 'get_all_rss_auto_downloading_rules', 'get_all_rss_articles_matching_rule'"
        ),
        path: str | None = Field(default=None, description="path"),
        url: str | None = Field(default=None, description="url"),
        item_path: str | None = Field(default=None, description="item path"),
        dest_path: str | None = Field(default=None, description="dest path"),
        article_id: str | None = Field(default=None, description="article id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage rss operations.

        Actions:
          - 'add_rss_folder': Add RSS folder.
          - 'add_rss_feed': Add RSS feed.
          - 'remove_rss_item': Remove RSS item.
          - 'move_rss_item': Move RSS item.
          - 'get_all_rss_items': Call get_all_rss_items
          - 'mark_rss_as_read': Mark RSS as read.
          - 'refresh_rss_item': Refresh RSS item.
          - 'set_rss_auto_downloading_rule': Call set_rss_auto_downloading_rule
          - 'rename_rss_auto_downloading_rule': Call rename_rss_auto_downloading_rule
          - 'remove_rss_auto_downloading_rule': Call remove_rss_auto_downloading_rule
          - 'get_all_rss_auto_downloading_rules': Call get_all_rss_auto_downloading_rules
          - 'get_all_rss_articles_matching_rule': Call get_all_rss_articles_matching_rule
        """
        kwargs: dict[str, Any]
        if action == "add_rss_folder":
            kwargs = {"path": path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_rss_folder(**kwargs)
        if action == "add_rss_feed":
            kwargs = {"url": url, "path": path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_rss_feed(**kwargs)
        if action == "remove_rss_item":
            kwargs = {"path": path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_rss_item(**kwargs)
        if action == "move_rss_item":
            kwargs = {"item_path": item_path, "dest_path": dest_path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.move_rss_item(**kwargs)
        if action == "get_all_rss_items":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_rss_items(**kwargs)
        if action == "mark_rss_as_read":
            kwargs = {"item_path": item_path, "article_id": article_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.mark_rss_as_read(**kwargs)
        if action == "refresh_rss_item":
            kwargs = {"item_path": item_path}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.refresh_rss_item(**kwargs)
        if action == "set_rss_auto_downloading_rule":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_rss_auto_downloading_rule(**kwargs)
        if action == "rename_rss_auto_downloading_rule":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.rename_rss_auto_downloading_rule(**kwargs)
        if action == "remove_rss_auto_downloading_rule":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_rss_auto_downloading_rule(**kwargs)
        if action == "get_all_rss_auto_downloading_rules":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_rss_auto_downloading_rules(**kwargs)
        if action == "get_all_rss_articles_matching_rule":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_rss_articles_matching_rule(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: add_rss_folder', 'add_rss_feed', 'remove_rss_item', 'move_rss_item', 'get_all_rss_items', 'mark_rss_as_read', 'refresh_rss_item', 'set_rss_auto_downloading_rule', 'rename_rss_auto_downloading_rule', 'remove_rss_auto_downloading_rule', 'get_all_rss_auto_downloading_rules', 'get_all_rss_articles_matching_rule"
        )


def register_search_tools(mcp: FastMCP):
    @mcp.tool(tags={"search"})
    async def qbittorrent_search(
        action: str = Field(
            description="Action to perform. Must be one of: 'start_search', 'stop_search', 'get_search_status', 'get_search_results', 'delete_search', 'get_search_plugins', 'install_search_plugin', 'uninstall_search_plugin', 'enable_search_plugin', 'update_search_plugins'"
        ),
        sources: str | None = Field(default=None, description="sources"),
        names: str | None = Field(default=None, description="names"),
        enable: bool | None = Field(default=None, description="enable"),
        client=Depends(get_client),
    ) -> dict:
        """Manage search operations.

        Actions:
          - 'start_search': Call start_search
          - 'stop_search': Call stop_search
          - 'get_search_status': Call get_search_status
          - 'get_search_results': Call get_search_results
          - 'delete_search': Call delete_search
          - 'get_search_plugins': Get search plugins.
          - 'install_search_plugin': Install search plugin.
          - 'uninstall_search_plugin': Uninstall search plugin.
          - 'enable_search_plugin': Enable/disable search plugin.
          - 'update_search_plugins': Update search plugins.
        """
        kwargs: dict[str, Any]
        if action == "start_search":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.start_search(**kwargs)
        if action == "stop_search":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.stop_search(**kwargs)
        if action == "get_search_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_search_status(**kwargs)
        if action == "get_search_results":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_search_results(**kwargs)
        if action == "delete_search":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_search(**kwargs)
        if action == "get_search_plugins":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_search_plugins(**kwargs)
        if action == "install_search_plugin":
            kwargs = {"sources": sources}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.install_search_plugin(**kwargs)
        if action == "uninstall_search_plugin":
            kwargs = {"names": names}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.uninstall_search_plugin(**kwargs)
        if action == "enable_search_plugin":
            kwargs = {"names": names, "enable": enable}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.enable_search_plugin(**kwargs)
        if action == "update_search_plugins":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_search_plugins(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: start_search', 'stop_search', 'get_search_status', 'get_search_results', 'delete_search', 'get_search_plugins', 'install_search_plugin', 'uninstall_search_plugin', 'enable_search_plugin', 'update_search_plugins"
        )


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
