import logging
import os
from typing import Any

import requests
import urllib3
from agent_utilities.core.exceptions import (
    AuthError,
    UnauthorizedError,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class BaseApiClient:
    """REST API wrapper for qBittorrent WebUI.

    CONCEPT:ORCH-1.4 — Action Execution Pipeline
    """

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
        self.headers = {"Referer": self.base_url}

        self.login()

    def login(self):
        """Authenticate with qBittorrent and get SID cookie."""
        url = f"{self.api_url}/auth/login"
        data = {"username": self.username, "password": self.password}

        headers = {"Referer": self.base_url}

        try:
            response = self.session.post(url, data=data, headers=headers, timeout=10)
            # qBittorrent success: <5.1 returns 200 "Ok." + cookie "SID";
            # 5.1/5.2+ returns 204 No Content + cookie "QBT_SID_<port>".
            if response.status_code in (200, 204):
                cookie_names = list(self.session.cookies.keys())
                if any(n == "SID" or n.startswith("QBT_SID") for n in cookie_names):
                    self._authenticated = True
                    logger.info(
                        f"Successfully logged in to qBittorrent at {self.base_url}"
                    )
                else:
                    raise AuthError(
                        "Login response received but no session cookie set "
                        "(check QBITTORRENT_USERNAME/PASSWORD)."
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
            raise AuthError(f"Connection error during login: {str(e)}") from e

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
