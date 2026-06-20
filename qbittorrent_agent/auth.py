#!/usr/bin/python
import urllib3

from qbittorrent_agent.api_client import QbittorrentApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

_client = None


def get_client():
    """Get or create a singleton API client instance.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
    """
    global _client
    if _client is None:
        base_url = setting("QBITTORRENT_URL", "http://localhost:8080")
        username = setting("QBITTORRENT_USERNAME", "admin")
        password = setting("QBITTORRENT_PASSWORD", "adminadmin")
        verify_env = setting("QBITTORRENT_SSL_VERIFY")
        if verify_env is None:
            verify_env = setting("QBITTORRENT_AGENT_VERIFY") or "True"
        verify: bool = verify_env.lower() in ("true", "1", "yes")

        try:
            _client = QbittorrentApi(
                base_url=base_url,
                username=username,
                password=password,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD and QBITTORRENT_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client
