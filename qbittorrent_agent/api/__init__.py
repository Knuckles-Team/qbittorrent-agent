"""qBittorrent WebUI API client (one method per upstream operation)."""

from qbittorrent_agent.api.api_client_base import (
    BaseApiClient,
    QbittorrentApiError,
    QbittorrentUnsupportedError,
)
from qbittorrent_agent.api.client import Api

__all__ = ["Api", "BaseApiClient", "QbittorrentApiError", "QbittorrentUnsupportedError"]
