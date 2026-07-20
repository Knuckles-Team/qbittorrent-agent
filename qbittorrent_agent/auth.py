#!/usr/bin/python

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from qbittorrent_agent.api_client import QbittorrentApi

_client = None


def get_client(tls_profile: ResolvedTLSProfile | None = None):
    """Get or create a singleton API client instance.

    CONCEPT:AU-OS.governance.reactive-multi-axis-budget — Guardrail Engine / Session Concurrency
    """
    global _client
    if _client is None:
        base_url = setting("QBITTORRENT_URL", "")
        username = setting("QBITTORRENT_USERNAME", "")
        password = setting("QBITTORRENT_PASSWORD", "")
        if not base_url:
            raise RuntimeError("QBITTORRENT_URL is required")
        if not username or not password:
            raise RuntimeError("qBittorrent credentials are required")

        try:
            _client = QbittorrentApi(
                base_url=base_url,
                username=username,
                password=password,
                tls_profile=tls_profile
                or resolve_configured_tls_profile("qbittorrent"),
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The configured credentials were rejected. "
                f"Please check your QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD and QBITTORRENT_URL environment variables. "
                f"Error details: {type(e).__name__}"
            ) from e

    return _client
