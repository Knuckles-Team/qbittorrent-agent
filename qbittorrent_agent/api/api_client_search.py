from typing import Any

from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def search_start(
        self, pattern: str, plugins: str = "all", category: str = "all"
    ) -> dict:
        """Start search."""
        return self._post(
            "search/start",
            data={"pattern": pattern, "plugins": plugins, "category": category},
        )

    @require_auth
    def search_stop(self, search_id: int):
        """Stop search."""
        return self._post("search/stop", data={"id": search_id})

    @require_auth
    def search_status(self, search_id: int | None = None) -> list[dict]:
        """Get search status."""
        params: dict[str, Any] = {}
        if search_id is not None:
            params["id"] = search_id
        return self._get("search/status", params=params)

    @require_auth
    def search_results(self, search_id: int, limit: int = 10, offset: int = 0) -> dict:
        """Get search results."""
        return self._get(
            "search/results", params={"id": search_id, "limit": limit, "offset": offset}
        )

    @require_auth
    def search_delete(self, search_id: int):
        """Delete search."""
        return self._post("search/delete", data={"id": search_id})

    @require_auth
    def get_search_plugins(self) -> list[dict]:
        """Get search plugins."""
        return self._get("search/plugins")

    @require_auth
    def install_search_plugin(self, sources: str):
        """Install search plugin."""
        return self._post("search/installPlugin", data={"sources": sources})

    @require_auth
    def uninstall_search_plugin(self, names: str):
        """Uninstall search plugin."""
        return self._post("search/uninstallPlugin", data={"names": names})

    @require_auth
    def enable_search_plugin(self, names: str, enable: bool = True):
        """Enable/disable search plugin."""
        return self._post(
            "search/enablePlugin", data={"names": names, "enable": str(enable).lower()}
        )

    @require_auth
    def update_search_plugins(self):
        """Update search plugins."""
        return self._post("search/updatePlugins")
