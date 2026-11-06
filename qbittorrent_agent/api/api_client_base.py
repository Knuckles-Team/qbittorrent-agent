import base64
import json
import logging
from typing import Any

import requests
from scion_sdk.exceptions import (
    AuthError,
    UnauthorizedError,
)
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile

logger = logging.getLogger(__name__)


def is_api_key(value: str | None) -> bool:
    """A qBittorrent WebUI API key is ``qbt_`` plus 28 characters (5.2+).

    Anything else (an unset or placeholder setting) falls back to the
    username and password session, so a placeholder never locks the client out.
    """
    return bool(value) and value.startswith("qbt_") and len(value) == 32


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
        api_key: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v2"
        self.username = username
        self.password = password
        self.tls_profile = tls_profile or resolve_tls_profile("qbittorrent")
        self.session = self.tls_profile.configure_requests_session(requests.Session())
        self._authenticated = False
        self.headers = {"Referer": self.base_url}
        # qBittorrent 5.2 accepts a WebUI API key as a bearer token: no login,
        # no session cookie, and no IP ban after failed logins.
        self.api_key = api_key if is_api_key(api_key) else None
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
            self._authenticated = True
        else:
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

    def _send(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send one API call; on 401/403 re-login and retry exactly once."""
        url = f"{self.api_url}/{endpoint}"
        send = getattr(self.session, method)
        response = send(url, timeout=30, **kwargs)
        if response.status_code in (401, 403) and not self.api_key:
            logger.info("qBittorrent session rejected; logging in again")
            self._authenticated = False
            try:
                self.login()
            except UnauthorizedError:
                raise
            except AuthError as exc:
                raise UnauthorizedError("Session expired and re-login failed.") from exc
            response = send(url, timeout=30, **kwargs)
        self._handle_errors(response)
        return response

    def _get(self, endpoint: str, params: dict | None = None) -> Any:
        response = self._send("get", endpoint, params=params)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _post(
        self, endpoint: str, data: dict | None = None, files: dict | None = None
    ) -> Any:
        response = self._send("post", endpoint, data=data, files=files)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _handle_errors(self, response: requests.Response):
        """Raise on every failed call, carrying qBittorrent's own reason.

        qBittorrent answers a failed call with a status and a short plain-text
        reason (for example ``Torrent hash(es) not found`` or ``Category name
        is invalid``). Before CONN-QBITTORRENT-AGENT-SURFACE-R003 a 404 or 409
        was only logged and the tool reported success.
        """
        if response.status_code < 400:
            return
        reason = _reason(response)
        suffix = f": {reason}" if reason else ""
        if response.status_code == 401:
            raise UnauthorizedError(f"Not authenticated or session expired{suffix}")
        if response.status_code == 403:
            raise UnauthorizedError(f"Forbidden (banned IP or refused API key){suffix}")
        raise QbittorrentApiError(response.status_code, reason)

    def _call(
        self,
        verb: str,
        route: str,
        params: dict[str, Any] | None = None,
        files: dict[str, str] | None = None,
    ) -> Any:
        """Send one WebUI API operation and shape its answer for a tool.

        ``params`` travel as the query of a GET and as the form of a POST;
        booleans become ``true``/``false`` and ``None`` values are dropped.
        ``files`` maps an uploaded file name to its base64 content.
        """
        clean = {
            key: _wire(value)
            for key, value in (params or {}).items()
            if value is not None
        }
        if verb == "GET":
            response = self._send("get", route, params=clean)
        else:
            upload = None
            if files:
                upload = [
                    ("torrents", (name, base64.b64decode(content)))
                    for name, content in files.items()
                ]
            response = self._send("post", route, data=clean, files=upload)
        return _shape(response)


class QbittorrentApiError(RuntimeError):
    """A failed WebUI API call: the HTTP status and qBittorrent's reason."""

    def __init__(self, status_code: int, reason: str = ""):
        self.status_code = status_code
        self.reason = reason
        super().__init__(
            f"qBittorrent API error: HTTP {status_code}"
            + (f": {reason}" if reason else "")
        )


_MAX_REASON_CHARS = 1000


def _wire(value: Any) -> Any:
    """Booleans travel as ``true``/``false``; objects and lists as JSON text."""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict | list):
        return json.dumps(value)
    return value


def _reason(response: requests.Response) -> str:
    try:
        text = str(response.text or "")
    except Exception:  # noqa: BLE001 - an unreadable body still raises the status
        return ""
    text = " ".join(text.split())
    if text.startswith("<"):
        return "qBittorrent answered with a web page (wrong route or proxy error)"
    return text[:_MAX_REASON_CHARS]


def _shape(response: requests.Response) -> Any:
    """Every tool returns a JSON object: lists and scalars sit under ``result``."""
    if response.status_code == 204 or not response.content:
        return {"status": "success"}
    kind = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if kind in {"application/x-bittorrent", "application/octet-stream"}:
        disposition = response.headers.get("content-disposition", "")
        name = (
            disposition.split("filename=", 1)[-1].strip('"')
            if "filename=" in disposition
            else ""
        )
        return {
            "filename": name,
            "content_base64": base64.b64encode(response.content).decode("ascii"),
        }
    try:
        body = response.json()
    except (ValueError, json.JSONDecodeError):
        return {"result": response.text}
    return body if isinstance(body, dict) else {"result": body}
