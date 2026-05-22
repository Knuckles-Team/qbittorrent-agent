from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def get_main_data(self, rid: int = 0) -> dict:
        """Get main data."""
        return self._get("sync/maindata", params={"rid": rid})

    @require_auth
    def get_torrent_peers_data(self, hash: str, rid: int = 0) -> dict:
        """Get torrent peers data."""
        return self._get("sync/torrentPeers", params={"hash": hash, "rid": rid})
