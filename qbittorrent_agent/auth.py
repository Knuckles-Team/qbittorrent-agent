#!/usr/bin/python
               

import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.exceptions import AuthError, UnauthorizedError

from qbittorrent_agent.qbittorrent_api import QbittorrentApi

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = os.getenv("QBITTORRENT_URL", "http://localhost:8080")
        username = os.getenv("QBITTORRENT_USERNAME", "admin")
        password = os.getenv("QBITTORRENT_PASSWORD", "adminadmin")
        verify = os.getenv("QBITTORRENT_AGENT_VERIFY", "True").lower() in ("true", "1", "yes")

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
