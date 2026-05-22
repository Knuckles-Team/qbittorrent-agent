import json

from agent_utilities.core.decorators import require_auth

from qbittorrent_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    @require_auth
    def add_rss_folder(self, path: str):
        """Add RSS folder."""
        return self._post("rss/addFolder", data={"path": path})

    @require_auth
    def add_rss_feed(self, url: str, path: str = ""):
        """Add RSS feed."""
        return self._post("rss/addFeed", data={"url": url, "path": path})

    @require_auth
    def remove_rss_item(self, path: str):
        """Remove RSS item."""
        return self._post("rss/removeItem", data={"path": path})

    @require_auth
    def move_rss_item(self, item_path: str, dest_path: str):
        """Move RSS item."""
        return self._post(
            "rss/moveItem", data={"itemPath": item_path, "destPath": dest_path}
        )

    @require_auth
    def get_rss_items(self, with_data: bool = False) -> dict:
        """Get all RSS items."""
        return self._get("rss/items", params={"withData": str(with_data).lower()})

    @require_auth
    def mark_rss_as_read(self, item_path: str, article_id: str | None = None):
        """Mark RSS as read."""
        params = {"itemPath": item_path}
        if article_id:
            params["articleId"] = article_id
        return self._post("rss/markAsRead", data=params)

    @require_auth
    def refresh_rss_item(self, item_path: str):
        """Refresh RSS item."""
        return self._post("rss/refreshItem", data={"itemPath": item_path})

    @require_auth
    def set_rss_rule(self, rule_name: str, rule_def: dict):
        """Set auto-downloading rule."""
        return self._post(
            "rss/setRule", data={"ruleName": rule_name, "ruleDef": json.dumps(rule_def)}
        )

    @require_auth
    def rename_rss_rule(self, rule_name: str, new_rule_name: str):
        """Rename auto-downloading rule."""
        return self._post(
            "rss/renameRule", data={"ruleName": rule_name, "newRuleName": new_rule_name}
        )

    @require_auth
    def remove_rss_rule(self, rule_name: str):
        """Remove auto-downloading rule."""
        return self._post("rss/removeRule", data={"ruleName": rule_name})

    @require_auth
    def get_rss_rules(self) -> dict:
        """Get all auto-downloading rules."""
        return self._get("rss/rules")

    @require_auth
    def get_rss_matching_articles(self, rule_name: str) -> dict:
        """Get all articles matching a rule."""
        return self._get("rss/matchingArticles", params={"ruleName": rule_name})
