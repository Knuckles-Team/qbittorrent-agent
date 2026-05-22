from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def get_log(
        self,
        normal: bool = True,
        info: bool = True,
        warning: bool = True,
        critical: bool = True,
        last_known_id: int = -1,
    ) -> list[dict]:
        """Get main log."""
        params = {
            "normal": str(normal).lower(),
            "info": str(info).lower(),
            "warning": str(warning).lower(),
            "critical": str(critical).lower(),
            "last_known_id": last_known_id,
        }
        return self._get("log/main", params=params)

    @require_auth
    def get_peer_log(self, last_known_id: int = -1) -> list[dict]:
        """Get peer log."""
        return self._get("log/peers", params={"last_known_id": last_known_id})
