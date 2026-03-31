import os
import logging
import requests
import urllib3
from typing import Optional, List, Dict, Any

from agent_utilities.exceptions import (
    AuthError,
    UnauthorizedError,
)
from agent_utilities.decorators import require_auth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class QbittorrentApi:
    """REST API wrapper for qBittorrent WebUI."""

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        username: Optional[str] = None,
        password: Optional[str] = None,
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

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.api_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        self._handle_errors(response)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _post(
        self, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None
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

    @require_auth
    def get_version(self) -> str:
        """Get application version."""
        return self._get("app/version")

    @require_auth
    def get_preferences(self) -> Dict:
        """Get application preferences."""
        return self._get("app/preferences")

    @require_auth
    def get_torrents(
        self,
        filter: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Dict]:
        """Get torrent list."""
        params = {}
        if filter:
            params["filter"] = filter
        if category:
            params["category"] = category
        if tag:
            params["tag"] = tag
        return self._get("torrents/info", params=params)

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
    def add_torrent(
        self,
        urls: Optional[str] = None,
        torrent_files: Optional[List[str]] = None,
        **kwargs,
    ):
        """Add new torrent."""
        data = {}
        if urls:
            data["urls"] = urls

        for k, v in kwargs.items():
            data[k] = str(v).lower() if isinstance(v, bool) else v

        files = {}
        if torrent_files:

            pass

        return self._post("torrents/add", data=data, files=files)

    @require_auth
    def get_transfer_info(self) -> Dict:
        """Get global transfer info."""
        return self._get("transfer/info")

    @require_auth
    def get_log(self, last_known_id: int = -1) -> List[Dict]:
        """Get main log."""
        return self._get("log/main", params={"last_known_id": last_known_id})

    @require_auth
    def search_start(
        self, pattern: str, plugins: str = "all", category: str = "all"
    ) -> Dict:
        """Start search."""
        return self._post(
            "search/start",
            data={"pattern": pattern, "plugins": plugins, "category": category},
        )

    @require_auth
    def search_status(self, search_id: Optional[int] = None) -> List[Dict]:
        """Get search status."""
        params = {}
        if search_id is not None:
            params["id"] = search_id
        return self._get("search/status", params=params)

    @require_auth
    def search_results(self, search_id: int, limit: int = 10, offset: int = 0) -> Dict:
        """Get search results."""
        return self._get(
            "search/results", params={"id": search_id, "limit": limit, "offset": offset}
        )

    @require_auth
    def get_rss_items(self, with_data: bool = False) -> Dict:
        """Get all RSS items."""
        return self._get("rss/items", params={"withData": str(with_data).lower()})

    @require_auth
    def get_rss_rules(self) -> Dict:
        """Get all auto-downloading rules."""
        return self._get("rss/rules")
