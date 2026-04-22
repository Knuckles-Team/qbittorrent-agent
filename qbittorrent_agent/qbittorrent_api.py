import json
import logging
import os
from typing import Any

import requests
import urllib3
from agent_utilities.decorators import require_auth
from agent_utilities.exceptions import (
    AuthError,
    UnauthorizedError,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class QbittorrentApi:
    """REST API wrapper for qBittorrent WebUI."""

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        username: str | None = None,
        password: str | None = None,
        verify: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v2"
        self.username = username or os.getenv("QBITTORRENT_USERNAME", "admin")
        self.password = password or os.getenv("QBITTORRENT_PASSWORD", "adminadmin")
        self.verify = verify
        self.session = requests.Session()
        self.session.verify = self.verify
        self._authenticated = False

        self.login()

    def login(self):
        """Authenticate with qBittorrent and get SID cookie."""
        url = f"{self.api_url}/auth/login"
        data = {"username": self.username, "password": self.password}

        headers = {"Referer": self.base_url}

        try:
            response = self.session.post(url, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                if "SID" in self.session.cookies:
                    self._authenticated = True
                    logger.info(
                        f"Successfully logged in to qBittorrent at {self.base_url}"
                    )
                else:
                    raise AuthError(
                        "Login successful but SID cookie not found in response."
                    )
            elif response.status_code == 403:
                raise AuthError(
                    "User's IP is banned for too many failed login attempts."
                )
            else:
                raise AuthError(
                    f"Login failed with status code {response.status_code}: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise AuthError(f"Connection error during login: {str(e)}")

    def logout(self):
        """Log out from qBittorrent."""
        url = f"{self.api_url}/auth/logout"
        self.session.post(url, timeout=10)
        self._authenticated = False

    def _get(self, endpoint: str, params: dict | None = None) -> Any:
        url = f"{self.api_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        self._handle_errors(response)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _post(
        self, endpoint: str, data: dict | None = None, files: dict | None = None
    ) -> Any:
        url = f"{self.api_url}/{endpoint}"
        response = self.session.post(url, data=data, files=files, timeout=30)
        self._handle_errors(response)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _handle_errors(self, response: requests.Response):
        if response.status_code == 401:
            raise UnauthorizedError("Not authenticated or session expired.")
        elif response.status_code == 403:
            raise UnauthorizedError(
                "Forbidden: You don't have permission to access this resource."
            )
        elif response.status_code == 404:
            logger.warning(f"Resource not found: {response.url}")
        elif response.status_code >= 400:
            logger.error(f"API Error {response.status_code}: {response.text}")

    # --- Application ---

    @require_auth
    def get_version(self) -> str:
        """Get application version."""
        return self._get("app/version")

    @require_auth
    def get_api_version(self) -> str:
        """Get API version."""
        return self._get("app/webapiVersion")

    @require_auth
    def get_build_info(self) -> dict:
        """Get build info."""
        return self._get("app/buildInfo")

    @require_auth
    def shutdown_application(self):
        """Shutdown application."""
        return self._post("app/shutdown")

    @require_auth
    def get_preferences(self) -> dict:
        """Get application preferences."""
        return self._get("app/preferences")

    @require_auth
    def set_preferences(self, preferences: dict):
        """Set application preferences."""
        return self._post("app/setPreferences", data={"json": json.dumps(preferences)})

    @require_auth
    def get_default_save_path(self) -> str:
        """Get default save path."""
        return self._get("app/defaultSavePath")

    # --- Log ---

    @require_auth
    def get_log(
        self,
        normal: bool = True,
        info: bool = True,
        warning: bool = True,
        critical: bool = True,
        last_known_id: int = -1,
    ) -> list[dict]:
        """Get main log."""
        params = {
            "normal": str(normal).lower(),
            "info": str(info).lower(),
            "warning": str(warning).lower(),
            "critical": str(critical).lower(),
            "last_known_id": last_known_id,
        }
        return self._get("log/main", params=params)

    @require_auth
    def get_peer_log(self, last_known_id: int = -1) -> list[dict]:
        """Get peer log."""
        return self._get("log/peers", params={"last_known_id": last_known_id})

    # --- Sync ---

    @require_auth
    def get_main_data(self, rid: int = 0) -> dict:
        """Get main data."""
        return self._get("sync/maindata", params={"rid": rid})

    @require_auth
    def get_torrent_peers_data(self, hash: str, rid: int = 0) -> dict:
        """Get torrent peers data."""
        return self._get("sync/torrentPeers", params={"hash": hash, "rid": rid})

    # --- Transfer ---

    @require_auth
    def get_transfer_info(self) -> dict:
        """Get global transfer info."""
        return self._get("transfer/info")

    @require_auth
    def get_speed_limits_mode(self) -> int:
        """Get alternative speed limits state (1 if enabled, 0 otherwise)."""
        return int(self._get("transfer/speedLimitsMode"))

    @require_auth
    def toggle_speed_limits_mode(self):
        """Toggle alternative speed limits."""
        return self._post("transfer/toggleSpeedLimitsMode")

    @require_auth
    def get_global_download_limit(self) -> int:
        """Get global download limit in bytes/second."""
        return int(self._get("transfer/downloadLimit"))

    @require_auth
    def set_global_download_limit(self, limit: int):
        """Set global download limit in bytes/second."""
        return self._post("transfer/setDownloadLimit", data={"limit": limit})

    @require_auth
    def get_global_upload_limit(self) -> int:
        """Get global upload limit in bytes/second."""
        return int(self._get("transfer/uploadLimit"))

    @require_auth
    def set_global_upload_limit(self, limit: int):
        """Set global upload limit in bytes/second."""
        return self._post("transfer/setUploadLimit", data={"limit": limit})

    @require_auth
    def ban_peers(self, peers: str):
        """Ban peers. 'peers' is a string of peers separated by | (host:port)."""
        return self._post("transfer/banPeers", data={"peers": peers})

    # --- Torrents ---

    @require_auth
    def get_torrents(
        self,
        filter: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        sort: str | None = None,
        reverse: bool = False,
        limit: int | None = None,
        offset: int | None = None,
        hashes: str | None = None,
    ) -> list[dict]:
        """Get torrent list."""
        params: dict[str, Any] = {}
        if filter:
            params["filter"] = filter
        if category:
            params["category"] = category
        if tag:
            params["tag"] = tag
        if sort:
            params["sort"] = sort
        if reverse:
            params["reverse"] = str(reverse).lower()
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if hashes:
            params["hashes"] = hashes
        return self._get("torrents/info", params=params)

    @require_auth
    def get_torrent_properties(self, hash: str) -> dict:
        """Get torrent generic properties."""
        return self._get("torrents/properties", params={"hash": hash})

    @require_auth
    def get_torrent_trackers(self, hash: str) -> list[dict]:
        """Get torrent trackers."""
        return self._get("torrents/trackers", params={"hash": hash})

    @require_auth
    def get_torrent_webseeds(self, hash: str) -> list[dict]:
        """Get torrent web seeds."""
        return self._get("torrents/webseeds", params={"hash": hash})

    @require_auth
    def get_torrent_contents(self, hash: str, indexes: str | None = None) -> list[dict]:
        """Get torrent contents."""
        params = {"hash": hash}
        if indexes:
            params["indexes"] = indexes
        return self._get("torrents/files", params=params)

    @require_auth
    def get_torrent_piece_states(self, hash: str) -> list[int]:
        """Get torrent pieces' states."""
        return self._get("torrents/pieceStates", params={"hash": hash})

    @require_auth
    def get_torrent_piece_hashes(self, hash: str) -> list[str]:
        """Get torrent pieces' hashes."""
        return self._get("torrents/pieceHashes", params={"hash": hash})

    @require_auth
    def pause_torrents(self, hashes: str = "all"):
        """Pause torrents."""
        return self._post("torrents/pause", data={"hashes": hashes})

    @require_auth
    def resume_torrents(self, hashes: str = "all"):
        """Resume torrents."""
        return self._post("torrents/resume", data={"hashes": hashes})

    @require_auth
    def delete_torrents(self, hashes: str, delete_files: bool = False):
        """Delete torrents."""
        return self._post(
            "torrents/delete",
            data={"hashes": hashes, "deleteFiles": str(delete_files).lower()},
        )

    @require_auth
    def recheck_torrents(self, hashes: str = "all"):
        """Recheck torrents."""
        return self._post("torrents/recheck", data={"hashes": hashes})

    @require_auth
    def reannounce_torrents(self, hashes: str = "all"):
        """Reannounce torrents."""
        return self._post("torrents/reannounce", data={"hashes": hashes})

    @require_auth
    def edit_tracker(self, hash: str, orig_url: str, new_url: str):
        """Edit tracker."""
        return self._post(
            "torrents/editTracker",
            data={"hash": hash, "origUrl": orig_url, "newUrl": new_url},
        )

    @require_auth
    def remove_trackers(self, hash: str, urls: str):
        """Remove trackers."""
        return self._post("torrents/removeTrackers", data={"hash": hash, "urls": urls})

    @require_auth
    def add_peers(self, hashes: str, peers: str):
        """Add peers."""
        return self._post("torrents/addPeers", data={"hashes": hashes, "peers": peers})

    @require_auth
    def add_torrent(
        self,
        urls: str | None = None,
        torrent_files: list[str] | None = None,
        **kwargs,
    ):
        """Add new torrent."""
        data: dict[str, Any] = {}
        if urls:
            data["urls"] = urls

        for k, v in kwargs.items():
            if v is not None:
                data[k] = str(v).lower() if isinstance(v, bool) else v

        files = []
        if torrent_files:
            for file_path in torrent_files:
                if os.path.exists(file_path):
                    files.append(
                        (
                            "torrents",
                            (os.path.basename(file_path), open(file_path, "rb")),
                        )
                    )

        # multipart/form-data is handled by requests when 'files' is provided
        return self._post("torrents/add", data=data, files=files)

    @require_auth
    def add_trackers(self, hash: str, urls: str):
        """Add trackers to torrent."""
        return self._post("torrents/addTrackers", data={"hash": hash, "urls": urls})

    @require_auth
    def increase_priority(self, hashes: str = "all"):
        """Increase torrent priority."""
        return self._post("torrents/increasePrio", data={"hashes": hashes})

    @require_auth
    def decrease_priority(self, hashes: str = "all"):
        """Decrease torrent priority."""
        return self._post("torrents/decreasePrio", data={"hashes": hashes})

    @require_auth
    def top_priority(self, hashes: str = "all"):
        """Maximal torrent priority."""
        return self._post("torrents/topPrio", data={"hashes": hashes})

    @require_auth
    def bottom_priority(self, hashes: str = "all"):
        """Minimal torrent priority."""
        return self._post("torrents/bottomPrio", data={"hashes": hashes})

    @require_auth
    def set_file_priority(self, hash: str, id: str, priority: int):
        """Set file priority."""
        return self._post(
            "torrents/filePrio", data={"hash": hash, "id": id, "priority": priority}
        )

    @require_auth
    def get_torrent_download_limit(self, hashes: str = "all") -> dict:
        """Get torrent download limit."""
        return self._post("torrents/downloadLimit", data={"hashes": hashes})

    @require_auth
    def set_torrent_download_limit(self, hashes: str, limit: int):
        """Set torrent download limit."""
        return self._post(
            "torrents/setDownloadLimit", data={"hashes": hashes, "limit": limit}
        )

    @require_auth
    def set_torrent_share_limit(
        self,
        hashes: str,
        ratio_limit: float,
        seeding_time_limit: int,
        inactive_seeding_time_limit: int = -2,
    ):
        """Set torrent share limit."""
        data = {
            "hashes": hashes,
            "ratioLimit": ratio_limit,
            "seedingTimeLimit": seeding_time_limit,
            "inactiveSeedingTimeLimit": inactive_seeding_time_limit,
        }
        return self._post("torrents/setShareLimits", data=data)

    @require_auth
    def get_torrent_upload_limit(self, hashes: str = "all") -> dict:
        """Get torrent upload limit."""
        return self._post("torrents/uploadLimit", data={"hashes": hashes})

    @require_auth
    def set_torrent_upload_limit(self, hashes: str, limit: int):
        """Set torrent upload limit."""
        return self._post(
            "torrents/setUploadLimit", data={"hashes": hashes, "limit": limit}
        )

    @require_auth
    def set_torrent_location(self, hashes: str, location: str):
        """Set torrent location."""
        return self._post(
            "torrents/setLocation", data={"hashes": hashes, "location": location}
        )

    @require_auth
    def set_torrent_name(self, hash: str, name: str):
        """Set torrent name."""
        return self._post("torrents/rename", data={"hash": hash, "name": name})

    @require_auth
    def set_torrent_category(self, hashes: str, category: str):
        """Set torrent category."""
        return self._post(
            "torrents/setCategory", data={"hashes": hashes, "category": category}
        )

    @require_auth
    def get_categories(self) -> dict:
        """Get all categories."""
        return self._get("torrents/categories")

    @require_auth
    def create_category(self, category: str, save_path: str = ""):
        """Add new category."""
        return self._post(
            "torrents/createCategory",
            data={"category": category, "savePath": save_path},
        )

    @require_auth
    def edit_category(self, category: str, save_path: str = ""):
        """Edit category."""
        return self._post(
            "torrents/editCategory", data={"category": category, "savePath": save_path}
        )

    @require_auth
    def remove_categories(self, categories: str):
        """Remove categories. 'categories' is \n separated list."""
        return self._post("torrents/removeCategories", data={"categories": categories})

    @require_auth
    def add_torrent_tags(self, hashes: str, tags: str):
        """Add torrent tags."""
        return self._post("torrents/addTags", data={"hashes": hashes, "tags": tags})

    @require_auth
    def remove_torrent_tags(self, hashes: str, tags: str = ""):
        """Remove torrent tags."""
        return self._post("torrents/removeTags", data={"hashes": hashes, "tags": tags})

    @require_auth
    def get_tags(self) -> list[str]:
        """Get all tags."""
        return self._get("torrents/tags")

    @require_auth
    def create_tags(self, tags: str):
        """Create tags."""
        return self._post("torrents/createTags", data={"tags": tags})

    @require_auth
    def delete_tags(self, tags: str):
        """Delete tags."""
        return self._post("torrents/deleteTags", data={"tags": tags})

    @require_auth
    def set_auto_management(self, hashes: str, enable: bool = True):
        """Set automatic torrent management."""
        return self._post(
            "torrents/setAutoManagement",
            data={"hashes": hashes, "enable": str(enable).lower()},
        )

    @require_auth
    def toggle_sequential_download(self, hashes: str):
        """Toggle sequential download."""
        return self._post("torrents/toggleSequentialDownload", data={"hashes": hashes})

    @require_auth
    def toggle_first_last_piece_priority(self, hashes: str):
        """Set first/last piece priority."""
        return self._post("torrents/toggleFirstLastPiecePrio", data={"hashes": hashes})

    @require_auth
    def set_force_start(self, hashes: str, value: bool = True):
        """Set force start."""
        return self._post(
            "torrents/setForceStart",
            data={"hashes": hashes, "value": str(value).lower()},
        )

    @require_auth
    def set_super_seeding(self, hashes: str, value: bool = True):
        """Set super seeding."""
        return self._post(
            "torrents/setSuperSeeding",
            data={"hashes": hashes, "value": str(value).lower()},
        )

    @require_auth
    def rename_file(self, hash: str, old_path: str, new_path: str):
        """Rename file."""
        return self._post(
            "torrents/renameFile",
            data={"hash": hash, "oldPath": old_path, "newPath": new_path},
        )

    @require_auth
    def rename_folder(self, hash: str, old_path: str, new_path: str):
        """Rename folder."""
        return self._post(
            "torrents/renameFolder",
            data={"hash": hash, "oldPath": old_path, "newPath": new_path},
        )

    # --- RSS ---

    @require_auth
    def add_rss_folder(self, path: str):
        """Add RSS folder."""
        return self._post("rss/addFolder", data={"path": path})

    @require_auth
    def add_rss_feed(self, url: str, path: str = ""):
        """Add RSS feed."""
        return self._post("rss/addFeed", data={"url": url, "path": path})

    @require_auth
    def remove_rss_item(self, path: str):
        """Remove RSS item."""
        return self._post("rss/removeItem", data={"path": path})

    @require_auth
    def move_rss_item(self, item_path: str, dest_path: str):
        """Move RSS item."""
        return self._post(
            "rss/moveItem", data={"itemPath": item_path, "destPath": dest_path}
        )

    @require_auth
    def get_rss_items(self, with_data: bool = False) -> dict:
        """Get all RSS items."""
        return self._get("rss/items", params={"withData": str(with_data).lower()})

    @require_auth
    def mark_rss_as_read(self, item_path: str, article_id: str | None = None):
        """Mark RSS as read."""
        params = {"itemPath": item_path}
        if article_id:
            params["articleId"] = article_id
        return self._post("rss/markAsRead", data=params)

    @require_auth
    def refresh_rss_item(self, item_path: str):
        """Refresh RSS item."""
        return self._post("rss/refreshItem", data={"itemPath": item_path})

    @require_auth
    def set_rss_rule(self, rule_name: str, rule_def: dict):
        """Set auto-downloading rule."""
        return self._post(
            "rss/setRule", data={"ruleName": rule_name, "ruleDef": json.dumps(rule_def)}
        )

    @require_auth
    def rename_rss_rule(self, rule_name: str, new_rule_name: str):
        """Rename auto-downloading rule."""
        return self._post(
            "rss/renameRule", data={"ruleName": rule_name, "newRuleName": new_rule_name}
        )

    @require_auth
    def remove_rss_rule(self, rule_name: str):
        """Remove auto-downloading rule."""
        return self._post("rss/removeRule", data={"ruleName": rule_name})

    @require_auth
    def get_rss_rules(self) -> dict:
        """Get all auto-downloading rules."""
        return self._get("rss/rules")

    @require_auth
    def get_rss_matching_articles(self, rule_name: str) -> dict:
        """Get all articles matching a rule."""
        return self._get("rss/matchingArticles", params={"ruleName": rule_name})

    # --- Search ---

    @require_auth
    def search_start(
        self, pattern: str, plugins: str = "all", category: str = "all"
    ) -> dict:
        """Start search."""
        return self._post(
            "search/start",
            data={"pattern": pattern, "plugins": plugins, "category": category},
        )

    @require_auth
    def search_stop(self, search_id: int):
        """Stop search."""
        return self._post("search/stop", data={"id": search_id})

    @require_auth
    def search_status(self, search_id: int | None = None) -> list[dict]:
        """Get search status."""
        params: dict[str, Any] = {}
        if search_id is not None:
            params["id"] = search_id
        return self._get("search/status", params=params)

    @require_auth
    def search_results(self, search_id: int, limit: int = 10, offset: int = 0) -> dict:
        """Get search results."""
        return self._get(
            "search/results", params={"id": search_id, "limit": limit, "offset": offset}
        )

    @require_auth
    def search_delete(self, search_id: int):
        """Delete search."""
        return self._post("search/delete", data={"id": search_id})

    @require_auth
    def get_search_plugins(self) -> list[dict]:
        """Get search plugins."""
        return self._get("search/plugins")

    @require_auth
    def install_search_plugin(self, sources: str):
        """Install search plugin."""
        return self._post("search/installPlugin", data={"sources": sources})

    @require_auth
    def uninstall_search_plugin(self, names: str):
        """Uninstall search plugin."""
        return self._post("search/uninstallPlugin", data={"names": names})

    @require_auth
    def enable_search_plugin(self, names: str, enable: bool = True):
        """Enable/disable search plugin."""
        return self._post(
            "search/enablePlugin", data={"names": names, "enable": str(enable).lower()}
        )

    @require_auth
    def update_search_plugins(self):
        """Update search plugins."""
        return self._post("search/updatePlugins")
