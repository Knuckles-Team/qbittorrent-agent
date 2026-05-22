from qbittorrent_agent.api.api_client_app import Api as AppApi
from qbittorrent_agent.api.api_client_log import Api as LogApi
from qbittorrent_agent.api.api_client_rss import Api as RssApi
from qbittorrent_agent.api.api_client_search import Api as SearchApi
from qbittorrent_agent.api.api_client_sync import Api as SyncApi
from qbittorrent_agent.api.api_client_torrents import Api as TorrentsApi
from qbittorrent_agent.api.api_client_transfer import Api as TransferApi


class Api(
    AppApi,
    LogApi,
    SyncApi,
    TransferApi,
    RssApi,
    SearchApi,
    TorrentsApi,
):
    """Unified API Client for qBittorrent, combining decomposed sub-clients."""
