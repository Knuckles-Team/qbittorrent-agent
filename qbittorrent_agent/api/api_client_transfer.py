from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def get_transfer_info(self) -> dict:
        """Get global transfer info."""
        return self._get("transfer/info")

    @require_auth
    def get_speed_limits_mode(self) -> int:
        """Get alternative speed limits state (1 if enabled, 0 otherwise)."""
        return int(self._get("transfer/speedLimitsMode"))

    @require_auth
    def toggle_speed_limits_mode(self):
        """Toggle alternative speed limits."""
        return self._post("transfer/toggleSpeedLimitsMode")

    @require_auth
    def get_global_download_limit(self) -> int:
        """Get global download limit in bytes/second."""
        return int(self._get("transfer/downloadLimit"))

    @require_auth
    def set_global_download_limit(self, limit: int):
        """Set global download limit in bytes/second."""
        return self._post("transfer/setDownloadLimit", data={"limit": limit})

    @require_auth
    def get_global_upload_limit(self) -> int:
        """Get global upload limit in bytes/second."""
        return int(self._get("transfer/uploadLimit"))

    @require_auth
    def set_global_upload_limit(self, limit: int):
        """Set global upload limit in bytes/second."""
        return self._post("transfer/setUploadLimit", data={"limit": limit})

    @require_auth
    def ban_peers(self, peers: str):
        """Ban peers. 'peers' is a string of peers separated by | (host:port)."""
        return self._post("transfer/banPeers", data={"peers": peers})
