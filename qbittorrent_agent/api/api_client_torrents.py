import os
from typing import Any

from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
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
        """Pause (stop) torrents. qBittorrent 5.x renamed the endpoint to torrents/stop."""
        return self._post("torrents/stop", data={"hashes": hashes})

    @require_auth
    def resume_torrents(self, hashes: str = "all"):
        """Resume (start) torrents. qBittorrent 5.x renamed the endpoint to torrents/start."""
        return self._post("torrents/start", data={"hashes": hashes})

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
        return self._post("torrents/add", data=data, files=files)  # type: ignore[arg-type]

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
