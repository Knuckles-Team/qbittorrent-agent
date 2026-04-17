import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import os
import sys
import logging
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from pydantic import Field
from agent_utilities import get_logger, to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from qbittorrent_agent.auth import get_client

__version__ = "0.1.7"

logger = get_logger(name="QBittorrent_MCP")
logger.setLevel(logging.INFO)


def register_app_tools(mcp: FastMCP):
    @mcp.tool(tags={"app"})
    def get_application_version() -> str:
        """Get qBittorrent application version."""
        client = get_client()
        return client.get_version()

    @mcp.tool(tags={"app"})
    def get_api_version() -> str:
        """Get qBittorrent WebAPI version."""
        client = get_client()
        return client.get_api_version()

    @mcp.tool(tags={"app"})
    def get_build_info() -> Dict:
        """Get qBittorrent build information (QT, libtorrent, boost, openssl versions, etc.)."""
        client = get_client()
        return client.get_build_info()

    @mcp.tool(tags={"app"})
    def shutdown_application() -> str:
        """Shutdown the qBittorrent application."""
        client = get_client()
        return client.shutdown_application()

    @mcp.tool(tags={"app"})
    def get_preferences() -> Dict:
        """Get all application preferences/settings."""
        client = get_client()
        return client.get_preferences()

    @mcp.tool(tags={"app"})
    def set_preferences(
        preferences: Dict = Field(
            description="JSON object with key-value pairs of settings to change."
        ),
    ) -> str:
        """Set application preferences/settings."""
        client = get_client()
        return client.set_preferences(preferences)

    @mcp.tool(tags={"app"})
    def get_default_save_path() -> str:
        """Get the default save path for torrents."""
        client = get_client()
        return client.get_default_save_path()


def register_log_tools(mcp: FastMCP):
    @mcp.tool(tags={"log"})
    def get_main_log(
        normal: bool = Field(default=True, description="Include normal messages"),
        info: bool = Field(default=True, description="Include info messages"),
        warning: bool = Field(default=True, description="Include warning messages"),
        critical: bool = Field(default=True, description="Include critical messages"),
        last_known_id: int = Field(
            default=-1, description="Exclude messages with ID <= last_known_id"
        ),
    ) -> List[Dict]:
        """Get the main qBittorrent log."""
        client = get_client()
        return client.get_log(normal, info, warning, critical, last_known_id)

    @mcp.tool(tags={"log"})
    def get_peer_log(
        last_known_id: int = Field(
            default=-1, description="Exclude messages with ID <= last_known_id"
        )
    ) -> List[Dict]:
        """Get the peer log."""
        client = get_client()
        return client.get_peer_log(last_known_id)


def register_sync_tools(mcp: FastMCP):
    @mcp.tool(tags={"sync"})
    def get_main_data(
        rid: int = Field(default=0, description="Response ID for incremental updates")
    ) -> Dict:
        """Get main sync data (torrents, categories, tags, server state)."""
        client = get_client()
        return client.get_main_data(rid)

    @mcp.tool(tags={"sync"})
    def get_torrent_peers_data(
        hash: str = Field(description="Torrent hash"),
        rid: int = Field(default=0, description="Response ID for incremental updates"),
    ) -> Dict:
        """Get sync data for torrent peers."""
        client = get_client()
        return client.get_torrent_peers_data(hash, rid)


def register_transfer_tools(mcp: FastMCP):
    @mcp.tool(tags={"transfer"})
    def get_global_transfer_info() -> Dict:
        """Get global transfer info (speeds, total data, DHT nodes, connection status)."""
        client = get_client()
        return client.get_transfer_info()

    @mcp.tool(tags={"transfer"})
    def get_speed_limits_mode() -> int:
        """Get alternative speed limits state (1 if enabled, 0 otherwise)."""
        client = get_client()
        return client.get_speed_limits_mode()

    @mcp.tool(tags={"transfer"})
    def toggle_speed_limits_mode() -> str:
        """Toggle alternative speed limits."""
        client = get_client()
        return client.toggle_speed_limits_mode()

    @mcp.tool(tags={"transfer"})
    def get_global_download_limit() -> int:
        """Get global download limit in bytes/second."""
        client = get_client()
        return client.get_global_download_limit()

    @mcp.tool(tags={"transfer"})
    def set_global_download_limit(
        limit: int = Field(description="Limit in bytes/second"),
    ) -> str:
        """Set global download limit in bytes/second."""
        client = get_client()
        return client.set_global_download_limit(limit)

    @mcp.tool(tags={"transfer"})
    def get_global_upload_limit() -> int:
        """Get global upload limit in bytes/second."""
        client = get_client()
        return client.get_global_upload_limit()

    @mcp.tool(tags={"transfer"})
    def set_global_upload_limit(
        limit: int = Field(description="Limit in bytes/second"),
    ) -> str:
        """Set global upload limit in bytes/second."""
        client = get_client()
        return client.set_global_upload_limit(limit)

    @mcp.tool(tags={"transfer"})
    def ban_peers(
        peers: str = Field(description="Peers to ban, separated by | (host:port)"),
    ) -> str:
        """Ban specific peers."""
        client = get_client()
        return client.ban_peers(peers)


def register_torrents_tools(mcp: FastMCP):
    @mcp.tool(tags={"torrents"})
    def get_torrent_list(
        filter: Optional[str] = Field(
            default=None,
            description="Filter by state (all, downloading, seeding, completed, etc.)",
        ),
        category: Optional[str] = Field(default=None, description="Filter by category"),
        tag: Optional[str] = Field(default=None, description="Filter by tag"),
        sort: Optional[str] = Field(default=None, description="Sort by field"),
        reverse: bool = Field(default=False, description="Reverse sort order"),
        limit: Optional[int] = Field(default=None, description="Limit results"),
        offset: Optional[int] = Field(default=None, description="Result offset"),
        hashes: Optional[str] = Field(
            default=None, description="Filter by hashes separated by |"
        ),
    ) -> List[Dict]:
        """Get list of torrents and their information."""
        client = get_client()
        return client.get_torrents(
            filter=filter,
            category=category,
            tag=tag,
            sort=sort,
            reverse=reverse,
            limit=limit,
            offset=offset,
            hashes=hashes,
        )

    @mcp.tool(tags={"torrents"})
    def get_torrent_properties(hash: str = Field(description="Torrent hash")) -> Dict:
        """Get generic properties of a torrent."""
        client = get_client()
        return client.get_torrent_properties(hash)

    @mcp.tool(tags={"torrents"})
    def get_torrent_trackers(
        hash: str = Field(description="Torrent hash"),
    ) -> List[Dict]:
        """Get trackers for a torrent."""
        client = get_client()
        return client.get_torrent_trackers(hash)

    @mcp.tool(tags={"torrents"})
    def get_torrent_webseeds(
        hash: str = Field(description="Torrent hash"),
    ) -> List[Dict]:
        """Get web seeds for a torrent."""
        client = get_client()
        return client.get_torrent_webseeds(hash)

    @mcp.tool(tags={"torrents"})
    def get_torrent_contents(
        hash: str = Field(description="Torrent hash"),
        indexes: Optional[str] = Field(
            default=None, description="File indexes separated by |"
        ),
    ) -> List[Dict]:
        """Get contents (files) of a torrent."""
        client = get_client()
        return client.get_torrent_contents(hash, indexes)

    @mcp.tool(tags={"torrents"})
    def get_torrent_piece_states(
        hash: str = Field(description="Torrent hash"),
    ) -> List[int]:
        """Get states of all pieces of a torrent (0:not downloaded, 1:downloading, 2:downloaded)."""
        client = get_client()
        return client.get_torrent_piece_states(hash)

    @mcp.tool(tags={"torrents"})
    def get_torrent_piece_hashes(
        hash: str = Field(description="Torrent hash"),
    ) -> List[str]:
        """Get hashes of all pieces of a torrent."""
        client = get_client()
        return client.get_torrent_piece_hashes(hash)

    @mcp.tool(tags={"torrents"})
    def pause_torrents(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Pause one or more torrents."""
        client = get_client()
        return client.pause_torrents(hashes)

    @mcp.tool(tags={"torrents"})
    def resume_torrents(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Resume one or more torrents."""
        client = get_client()
        return client.resume_torrents(hashes)

    @mcp.tool(tags={"torrents"})
    def delete_torrents(
        hashes: str = Field(description="Torrent hashes separated by |"),
        delete_files: bool = Field(
            default=False, description="Delete downloaded data from disk"
        ),
    ) -> str:
        """Delete one or more torrents."""
        client = get_client()
        return client.delete_torrents(hashes, delete_files)

    @mcp.tool(tags={"torrents"})
    def recheck_torrents(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Recheck one or more torrents."""
        client = get_client()
        return client.recheck_torrents(hashes)

    @mcp.tool(tags={"torrents"})
    def reannounce_torrents(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Reannounce one or more torrents."""
        client = get_client()
        return client.reannounce_torrents(hashes)

    @mcp.tool(tags={"torrents"})
    def edit_tracker(
        hash: str = Field(description="Torrent hash"),
        orig_url: str = Field(description="Original tracker URL"),
        new_url: str = Field(description="New tracker URL"),
    ) -> str:
        """Edit a tracker URL for a torrent."""
        client = get_client()
        return client.edit_tracker(hash, orig_url, new_url)

    @mcp.tool(tags={"torrents"})
    def remove_trackers(
        hash: str = Field(description="Torrent hash"),
        urls: str = Field(description="Tracker URLs to remove, separated by |"),
    ) -> str:
        """Remove trackers from a torrent."""
        client = get_client()
        return client.remove_trackers(hash, urls)

    @mcp.tool(tags={"torrents"})
    def add_peers(
        hashes: str = Field(description="Torrent hashes separated by |"),
        peers: str = Field(description="Peers to add, separated by | (host:port)"),
    ) -> str:
        """Add peers to one or more torrents."""
        client = get_client()
        return client.add_peers(hashes, peers)

    @mcp.tool(tags={"torrents"})
    def add_new_torrent(
        urls: Optional[str] = Field(
            default=None, description="URLs separated by newline"
        ),
        savepath: Optional[str] = Field(default=None, description="Download folder"),
        cookie: Optional[str] = Field(
            default=None, description="Cookie for downloading .torrent"
        ),
        category: Optional[str] = Field(default=None, description="Category"),
        tags: Optional[str] = Field(default=None, description="Tags separated by ,"),
        skip_checking: Optional[bool] = Field(
            default=False, description="Skip hash check"
        ),
        paused: Optional[bool] = Field(
            default=False, description="Add in paused state"
        ),
        root_folder: Optional[bool] = Field(
            default=None, description="Create root folder"
        ),
        rename: Optional[str] = Field(default=None, description="Rename torrent"),
        upLimit: Optional[int] = Field(
            default=None, description="Upload limit (bytes/s)"
        ),
        dlLimit: Optional[int] = Field(
            default=None, description="Download limit (bytes/s)"
        ),
        ratioLimit: Optional[float] = Field(
            default=None, description="Share ratio limit"
        ),
        seedingTimeLimit: Optional[int] = Field(
            default=None, description="Seeding time limit (minutes)"
        ),
        autoTMM: Optional[bool] = Field(
            default=None, description="Use automatic torrent management"
        ),
        sequentialDownload: Optional[bool] = Field(
            default=False, description="Enable sequential download"
        ),
        firstLastPiecePrio: Optional[bool] = Field(
            default=False, description="Prioritize first/last pieces"
        ),
    ) -> str:
        """Add a new torrent from URLs."""
        client = get_client()
        return client.add_torrent(
            urls=urls,
            savepath=savepath,
            cookie=cookie,
            category=category,
            tags=tags,
            skip_checking=skip_checking,
            paused=paused,
            root_folder=root_folder,
            rename=rename,
            upLimit=upLimit,
            dlLimit=dlLimit,
            ratioLimit=ratioLimit,
            seedingTimeLimit=seedingTimeLimit,
            autoTMM=autoTMM,
            sequentialDownload=sequentialDownload,
            firstLastPiecePrio=firstLastPiecePrio,
        )

    @mcp.tool(tags={"torrents"})
    def add_trackers_to_torrent(
        hash: str = Field(description="Torrent hash"),
        urls: str = Field(description="Tracker URLs separated by newline"),
    ) -> str:
        """Add trackers to a torrent."""
        client = get_client()
        return client.add_trackers(hash, urls)

    @mcp.tool(tags={"torrents"})
    def increase_torrent_priority(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Increase priority of one or more torrents."""
        client = get_client()
        return client.increase_priority(hashes)

    @mcp.tool(tags={"torrents"})
    def decrease_torrent_priority(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Decrease priority of one or more torrents."""
        client = get_client()
        return client.decrease_priority(hashes)

    @mcp.tool(tags={"torrents"})
    def top_torrent_priority(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Set one or more torrents to maximum priority."""
        client = get_client()
        return client.top_priority(hashes)

    @mcp.tool(tags={"torrents"})
    def bottom_torrent_priority(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> str:
        """Set one or more torrents to minimum priority."""
        client = get_client()
        return client.bottom_priority(hashes)

    @mcp.tool(tags={"torrents"})
    def set_file_priority(
        hash: str = Field(description="Torrent hash"),
        id: str = Field(description="File IDs separated by |"),
        priority: int = Field(
            description="Priority (0:Don't download, 1:Normal, 6:High, 7:Maximum)"
        ),
    ) -> str:
        """Set priority for one or more files in a torrent."""
        client = get_client()
        return client.set_file_priority(hash, id, priority)

    @mcp.tool(tags={"torrents"})
    def get_torrent_download_limit(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> Dict:
        """Get download limit for one or more torrents."""
        client = get_client()
        return client.get_torrent_download_limit(hashes)

    @mcp.tool(tags={"torrents"})
    def set_torrent_download_limit(
        hashes: str = Field(description="Torrent hashes separated by |"),
        limit: int = Field(description="Limit in bytes/second"),
    ) -> str:
        """Set download limit for one or more torrents."""
        client = get_client()
        return client.set_torrent_download_limit(hashes, limit)

    @mcp.tool(tags={"torrents"})
    def set_torrent_share_limit(
        hashes: str = Field(description="Torrent hashes separated by |"),
        ratio_limit: float = Field(
            description="Max share ratio (-2:Global, -1:No limit)"
        ),
        seeding_time_limit: int = Field(
            description="Max seeding time in minutes (-2:Global, -1:No limit)"
        ),
        inactive_seeding_time_limit: int = Field(
            default=-2,
            description="Max inactive seeding time in minutes (-2:Global, -1:No limit)",
        ),
    ) -> str:
        """Set share limits for one or more torrents."""
        client = get_client()
        return client.set_torrent_share_limit(
            hashes, ratio_limit, seeding_time_limit, inactive_seeding_time_limit
        )

    @mcp.tool(tags={"torrents"})
    def get_torrent_upload_limit(
        hashes: str = Field(default="all", description="Torrent hashes separated by |")
    ) -> Dict:
        """Get upload limit for one or more torrents."""
        client = get_client()
        return client.get_torrent_upload_limit(hashes)

    @mcp.tool(tags={"torrents"})
    def set_torrent_upload_limit(
        hashes: str = Field(description="Torrent hashes separated by |"),
        limit: int = Field(description="Limit in bytes/second"),
    ) -> str:
        """Set upload limit for one or more torrents."""
        client = get_client()
        return client.set_torrent_upload_limit(hashes, limit)

    @mcp.tool(tags={"torrents"})
    def set_torrent_location(
        hashes: str = Field(description="Torrent hashes separated by |"),
        location: str = Field(description="New location path"),
    ) -> str:
        """Set download location for one or more torrents."""
        client = get_client()
        return client.set_torrent_location(hashes, location)

    @mcp.tool(tags={"torrents"})
    def set_torrent_name(
        hash: str = Field(description="Torrent hash"),
        name: str = Field(description="New torrent name"),
    ) -> str:
        """Rename a torrent."""
        client = get_client()
        return client.set_torrent_name(hash, name)

    @mcp.tool(tags={"torrents"})
    def set_torrent_category(
        hashes: str = Field(description="Torrent hashes separated by |"),
        category: str = Field(description="Category name"),
    ) -> str:
        """Assign a category to one or more torrents."""
        client = get_client()
        return client.set_torrent_category(hashes, category)

    @mcp.tool(tags={"torrents"})
    def get_all_categories() -> Dict:
        """Get all defined categories."""
        client = get_client()
        return client.get_categories()

    @mcp.tool(tags={"torrents"})
    def add_new_category(
        category: str = Field(description="Category name"),
        save_path: str = Field(default="", description="Save path for this category"),
    ) -> str:
        """Add a new category."""
        client = get_client()
        return client.create_category(category, save_path)

    @mcp.tool(tags={"torrents"})
    def edit_category(
        category: str = Field(description="Category name"),
        save_path: str = Field(
            default="", description="New save path for this category"
        ),
    ) -> str:
        """Edit an existing category."""
        client = get_client()
        return client.edit_category(category, save_path)

    @mcp.tool(tags={"torrents"})
    def remove_categories(
        categories: str = Field(description="Category names separated by newline"),
    ) -> str:
        """Remove one or more categories."""
        client = get_client()
        return client.remove_categories(categories)

    @mcp.tool(tags={"torrents"})
    def add_torrent_tags(
        hashes: str = Field(description="Torrent hashes separated by |"),
        tags: str = Field(description="Tags separated by ,"),
    ) -> str:
        """Add tags to one or more torrents."""
        client = get_client()
        return client.add_torrent_tags(hashes, tags)

    @mcp.tool(tags={"torrents"})
    def remove_torrent_tags(
        hashes: str = Field(description="Torrent hashes separated by |"),
        tags: str = Field(default="", description="Tags to remove separated by ,"),
    ) -> str:
        """Remove tags from one or more torrents. Empty list removes all tags."""
        client = get_client()
        return client.remove_torrent_tags(hashes, tags)

    @mcp.tool(tags={"torrents"})
    def get_all_tags() -> List[str]:
        """Get all defined tags."""
        client = get_client()
        return client.get_tags()

    @mcp.tool(tags={"torrents"})
    def create_tags(
        tags: str = Field(description="Tags to create, separated by ,"),
    ) -> str:
        """Create new tags."""
        client = get_client()
        return client.create_tags(tags)

    @mcp.tool(tags={"torrents"})
    def delete_tags(
        tags: str = Field(description="Tags to delete, separated by ,"),
    ) -> str:
        """Delete tags."""
        client = get_client()
        return client.delete_tags(tags)

    @mcp.tool(tags={"torrents"})
    def set_auto_management(
        hashes: str = Field(description="Torrent hashes separated by |"),
        enable: bool = Field(default=True, description="Enable automatic management"),
    ) -> str:
        """Set automatic torrent management for one or more torrents."""
        client = get_client()
        return client.set_auto_management(hashes, enable)

    @mcp.tool(tags={"torrents"})
    def toggle_sequential_download(
        hashes: str = Field(description="Torrent hashes separated by |"),
    ) -> str:
        """Toggle sequential download for one or more torrents."""
        client = get_client()
        return client.toggle_sequential_download(hashes)

    @mcp.tool(tags={"torrents"})
    def toggle_first_last_piece_priority(
        hashes: str = Field(description="Torrent hashes separated by |"),
    ) -> str:
        """Toggle prioritization of first/last pieces for one or more torrents."""
        client = get_client()
        return client.toggle_first_last_piece_priority(hashes)

    @mcp.tool(tags={"torrents"})
    def set_force_start(
        hashes: str = Field(description="Torrent hashes separated by |"),
        value: bool = Field(default=True, description="Force start value"),
    ) -> str:
        """Set force start for one or more torrents."""
        client = get_client()
        return client.set_force_start(hashes, value)

    @mcp.tool(tags={"torrents"})
    def set_super_seeding(
        hashes: str = Field(description="Torrent hashes separated by |"),
        value: bool = Field(default=True, description="Super seeding value"),
    ) -> str:
        """Set super seeding for one or more torrents."""
        client = get_client()
        return client.set_super_seeding(hashes, value)

    @mcp.tool(tags={"torrents"})
    def rename_file(
        hash: str = Field(description="Torrent hash"),
        old_path: str = Field(description="Old file path"),
        new_path: str = Field(description="New file path"),
    ) -> str:
        """Rename a file within a torrent."""
        client = get_client()
        return client.rename_file(hash, old_path, new_path)

    @mcp.tool(tags={"torrents"})
    def rename_folder(
        hash: str = Field(description="Torrent hash"),
        old_path: str = Field(description="Old folder path"),
        new_path: str = Field(description="New folder path"),
    ) -> str:
        """Rename a folder within a torrent."""
        client = get_client()
        return client.rename_folder(hash, old_path, new_path)


def register_rss_tools(mcp: FastMCP):
    @mcp.tool(tags={"rss"})
    def add_rss_folder(
        path: str = Field(description="Full path of folder to add"),
    ) -> str:
        """Add an RSS folder."""
        client = get_client()
        return client.add_rss_folder(path)

    @mcp.tool(tags={"rss"})
    def add_rss_feed(
        url: str = Field(description="URL of RSS feed"),
        path: str = Field(default="", description="Full path of folder to add feed to"),
    ) -> str:
        """Add an RSS feed."""
        client = get_client()
        return client.add_rss_feed(url, path)

    @mcp.tool(tags={"rss"})
    def remove_rss_item(
        path: str = Field(description="Full path of item (folder or feed) to remove"),
    ) -> str:
        """Remove an RSS item (folder or feed)."""
        client = get_client()
        return client.remove_rss_item(path)

    @mcp.tool(tags={"rss"})
    def move_rss_item(
        item_path: str = Field(description="Current full path of item"),
        dest_path: str = Field(description="New full path of item"),
    ) -> str:
        """Move or rename an RSS item."""
        client = get_client()
        return client.move_rss_item(item_path, dest_path)

    @mcp.tool(tags={"rss"})
    def get_all_rss_items(
        with_data: bool = Field(
            default=False, description="Include current feed articles"
        )
    ) -> Dict:
        """Get all RSS items (folders and feeds)."""
        client = get_client()
        return client.get_rss_items(with_data)

    @mcp.tool(tags={"rss"})
    def mark_rss_as_read(
        item_path: str = Field(description="Full path of feed"),
        article_id: Optional[str] = Field(
            default=None,
            description="Article ID. If omitted, marks whole feed as read.",
        ),
    ) -> str:
        """Mark RSS articles or feeds as read."""
        client = get_client()
        return client.mark_rss_as_read(item_path, article_id)

    @mcp.tool(tags={"rss"})
    def refresh_rss_item(
        item_path: str = Field(description="Full path of item to refresh"),
    ) -> str:
        """Refresh an RSS item (folder or feed)."""
        client = get_client()
        return client.refresh_rss_item(item_path)

    @mcp.tool(tags={"rss"})
    def set_rss_auto_downloading_rule(
        rule_name: str = Field(description="Rule name"),
        rule_def: Dict = Field(description="JSON rule definition object"),
    ) -> str:
        """Set or update an RSS auto-downloading rule."""
        client = get_client()
        return client.set_rss_rule(rule_name, rule_def)

    @mcp.tool(tags={"rss"})
    def rename_rss_auto_downloading_rule(
        rule_name: str = Field(description="Current rule name"),
        new_rule_name: str = Field(description="New rule name"),
    ) -> str:
        """Rename an RSS auto-downloading rule."""
        client = get_client()
        return client.rename_rss_rule(rule_name, new_rule_name)

    @mcp.tool(tags={"rss"})
    def remove_rss_auto_downloading_rule(
        rule_name: str = Field(description="Rule name to remove"),
    ) -> str:
        """Remove an RSS auto-downloading rule."""
        client = get_client()
        return client.remove_rss_rule(rule_name)

    @mcp.tool(tags={"rss"})
    def get_all_rss_auto_downloading_rules() -> Dict:
        """Get all RSS auto-downloading rules."""
        client = get_client()
        return client.get_rss_rules()

    @mcp.tool(tags={"rss"})
    def get_all_rss_articles_matching_rule(
        rule_name: str = Field(description="Rule name"),
    ) -> Dict:
        """Get all articles matching an RSS rule."""
        client = get_client()
        return client.get_rss_matching_articles(rule_name)


def register_search_tools(mcp: FastMCP):
    @mcp.tool(tags={"search"})
    def start_search(
        pattern: str = Field(description="Search pattern"),
        plugins: str = Field(
            default="all", description="Plugins to use separated by |"
        ),
        category: str = Field(default="all", description="Category for search"),
    ) -> Dict:
        """Start a search job."""
        client = get_client()
        return client.search_start(pattern, plugins, category)

    @mcp.tool(tags={"search"})
    def stop_search(search_id: int = Field(description="Search job ID")) -> str:
        """Stop a running search job."""
        client = get_client()
        return client.search_stop(search_id)

    @mcp.tool(tags={"search"})
    def get_search_status(
        search_id: Optional[int] = Field(
            default=None, description="Search job ID. If omitted, returns all."
        )
    ) -> List[Dict]:
        """Get status of search jobs."""
        client = get_client()
        return client.search_status(search_id)

    @mcp.tool(tags={"search"})
    def get_search_results(
        search_id: int = Field(description="Search job ID"),
        limit: int = Field(default=10, description="Max results to return"),
        offset: int = Field(default=0, description="Result offset"),
    ) -> Dict:
        """Get results of a search job."""
        client = get_client()
        return client.search_results(search_id, limit, offset)

    @mcp.tool(tags={"search"})
    def delete_search(search_id: int = Field(description="Search job ID")) -> str:
        """Delete a search job."""
        client = get_client()
        return client.search_delete(search_id)

    @mcp.tool(tags={"search"})
    def get_search_plugins() -> List[Dict]:
        """Get all search plugins."""
        client = get_client()
        return client.get_search_plugins()

    @mcp.tool(tags={"search"})
    def install_search_plugin(
        sources: str = Field(description="URLs or paths separated by |"),
    ) -> str:
        """Install one or more search plugins."""
        client = get_client()
        return client.install_search_plugin(sources)

    @mcp.tool(tags={"search"})
    def uninstall_search_plugin(
        names: str = Field(description="Plugin names separated by |"),
    ) -> str:
        """Uninstall one or more search plugins."""
        client = get_client()
        return client.uninstall_search_plugin(names)

    @mcp.tool(tags={"search"})
    def enable_search_plugin(
        names: str = Field(description="Plugin names separated by |"),
        enable: bool = Field(default=True, description="Enable or disable"),
    ) -> str:
        """Enable or disable one or more search plugins."""
        client = get_client()
        return client.enable_search_plugin(names, enable)

    @mcp.tool(tags={"search"})
    def update_search_plugins() -> str:
        """Update all installed search plugins."""
        client = get_client()
        return client.update_search_plugins()


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the qBittorrent Manager MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="qBittorrent Manager MCP",
        version=__version__,
        instructions="qBittorrent Manager MCP Server. Direct tool usage for qBittorrent WebUI API.",
    )

    toggles = {
        "app": (register_app_tools, "APPTOOL"),
        "torrents": (register_torrents_tools, "TORRENTSTOOL"),
        "transfer": (register_transfer_tools, "TRANSFERTOOL"),
        "rss": (register_rss_tools, "RSSTOOL"),
        "search": (register_search_tools, "SEARCHTOOL"),
        "log": (register_log_tools, "LOGTOOL"),
        "sync": (register_sync_tools, "SYNCTOOL"),
    }

    registered_tags = []
    for tag, (reg_func, env_var) in toggles.items():
        if to_boolean(os.getenv(env_var, "True")):
            reg_func(mcp)
            registered_tags.append(tag)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"qBittorrent Manager MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Tags Loaded: {', '.join(registered_tags)}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
