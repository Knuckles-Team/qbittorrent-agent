"""MCP tools for rss operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


def register_rss_tools(mcp: FastMCP):
    @mcp.tool(tags={"rss"})
    async def qbittorrent_rss(
        action: str = Field(
            description="Action to perform. Must be one of: 'add_rss_folder', 'add_rss_feed', 'remove_rss_item', 'move_rss_item', 'get_all_rss_items', 'mark_rss_as_read', 'refresh_rss_item', 'set_rss_auto_downloading_rule', 'rename_rss_auto_downloading_rule', 'remove_rss_auto_downloading_rule', 'get_all_rss_auto_downloading_rules', 'get_all_rss_articles_matching_rule'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage qbittorrent rss operations."""
        if ctx:
            import inspect

            res = ctx.info("Executing tool...")
            if inspect.isawaitable(res):
                await res
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "add_rss_folder",
            "add_rss_feed",
            "remove_rss_item",
            "move_rss_item",
            "get_all_rss_items",
            "mark_rss_as_read",
            "refresh_rss_item",
            "set_rss_auto_downloading_rule",
            "rename_rss_auto_downloading_rule",
            "remove_rss_auto_downloading_rule",
            "get_all_rss_auto_downloading_rules",
            "get_all_rss_articles_matching_rule",
        )
        resolved = resolve_action(action, valid_actions, service="qbittorrent-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "add_rss_folder":
            return client.add_rss_folder(**kwargs)
        if action == "add_rss_feed":
            return client.add_rss_feed(**kwargs)
        if action == "remove_rss_item":
            return client.remove_rss_item(**kwargs)
        if action == "move_rss_item":
            return client.move_rss_item(**kwargs)
        if action == "get_all_rss_items":
            return client.get_rss_items(**kwargs)
        if action == "mark_rss_as_read":
            return client.mark_rss_as_read(**kwargs)
        if action == "refresh_rss_item":
            return client.refresh_rss_item(**kwargs)
        if action == "set_rss_auto_downloading_rule":
            return client.set_rss_rule(**kwargs)
        if action == "rename_rss_auto_downloading_rule":
            return client.rename_rss_rule(**kwargs)
        if action == "remove_rss_auto_downloading_rule":
            return client.remove_rss_rule(**kwargs)
        if action == "get_all_rss_auto_downloading_rules":
            return client.get_rss_rules(**kwargs)
        if action == "get_all_rss_articles_matching_rule":
            return client.get_rss_matching_articles(**kwargs)
        raise ValueError(f"Unknown action: {action}")
