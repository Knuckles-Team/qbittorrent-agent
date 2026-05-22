import json

from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def get_version(self) -> str:
        """Get application version."""
        return self._get("app/version")

    @require_auth
    def get_api_version(self) -> str:
        """Get API version."""
        return self._get("app/webapiVersion")

    @require_auth
    def get_build_info(self) -> dict:
        """Get build info."""
        return self._get("app/buildInfo")

    @require_auth
    def shutdown_application(self):
        """Shutdown application."""
        return self._post("app/shutdown")

    @require_auth
    def get_preferences(self) -> dict:
        """Get application preferences."""
        return self._get("app/preferences")

    @require_auth
    def set_preferences(self, preferences: dict):
        """Set application preferences."""
        return self._post("app/setPreferences", data={"json": json.dumps(preferences)})

    @require_auth
    def get_default_save_path(self) -> str:
        """Get default save path."""
        return self._get("app/defaultSavePath")
