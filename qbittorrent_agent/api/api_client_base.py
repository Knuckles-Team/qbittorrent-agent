import logging
from typing import Any

import requests
from agent_utilities.core.exceptions import (
    AuthError,
    UnauthorizedError,
)
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

logger = logging.getLogger(__name__)


class BaseApiClient:
    """REST API wrapper for qBittorrent WebUI.

    CONCEPT:AU-ORCH.adapter.kg-graph-materialization — Action Execution Pipeline
    """

    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v2"
        self.username = username
        self.password = password
        self.tls_profile = tls_profile or resolve_configured_tls_profile("qbittorrent")
        self.session = self.tls_profile.configure_requests_session(requests.Session())
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
                    logger.info("Successfully logged in to qBittorrent")
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
                raise AuthError(f"Login failed with HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise AuthError(f"Connection error during login: {type(e).__name__}") from e

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self.session.close()
        self.tls_profile.cleanup()

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
            logger.warning("qBittorrent resource lookup failed")
        elif response.status_code >= 400:
            logger.error(
                "qBittorrent API request failed: status_code=%s",
                response.status_code,
            )
