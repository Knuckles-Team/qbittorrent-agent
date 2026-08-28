"""MCP tools for rss operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from qbittorrent_agent.auth import get_client


# One tiny extracted handler per action -- each preserves the exact
# client-method call and kwargs passthrough the if/elif chain used to
# perform inline. Kept module-level (not nested) so each has CCN 1 and
# is independently addressable/testable.
async def _rss_add_rss_folder(client, **kwargs):
    return await run_blocking(client.add_rss_folder, **kwargs)


async def _rss_add_rss_feed(client, **kwargs):
    return await run_blocking(client.add_rss_feed, **kwargs)


async def _rss_remove_rss_item(client, **kwargs):
    return await run_blocking(client.remove_rss_item, **kwargs)


async def _rss_move_rss_item(client, **kwargs):
    return await run_blocking(client.move_rss_item, **kwargs)


async def _rss_get_all_rss_items(client, **kwargs):
    return await run_blocking(client.get_rss_items, **kwargs)


async def _rss_mark_rss_as_read(client, **kwargs):
    return await run_blocking(client.mark_rss_as_read, **kwargs)


async def _rss_refresh_rss_item(client, **kwargs):
    return await run_blocking(client.refresh_rss_item, **kwargs)


async def _rss_set_rss_auto_downloading_rule(client, **kwargs):
    return await run_blocking(client.set_rss_rule, **kwargs)


async def _rss_rename_rss_auto_downloading_rule(client, **kwargs):
    return await run_blocking(client.rename_rss_rule, **kwargs)


async def _rss_remove_rss_auto_downloading_rule(client, **kwargs):
    return await run_blocking(client.remove_rss_rule, **kwargs)


async def _rss_get_all_rss_auto_downloading_rules(client, **kwargs):
    return await run_blocking(client.get_rss_rules, **kwargs)


async def _rss_get_all_rss_articles_matching_rule(client, **kwargs):
    return await run_blocking(client.get_rss_matching_articles, **kwargs)


_RSS_ACTION_HANDLERS: dict[str, Any] = {
    "add_rss_folder": _rss_add_rss_folder,
    "add_rss_feed": _rss_add_rss_feed,
    "remove_rss_item": _rss_remove_rss_item,
    "move_rss_item": _rss_move_rss_item,
    "get_all_rss_items": _rss_get_all_rss_items,
    "mark_rss_as_read": _rss_mark_rss_as_read,
    "refresh_rss_item": _rss_refresh_rss_item,
    "set_rss_auto_downloading_rule": _rss_set_rss_auto_downloading_rule,
    "rename_rss_auto_downloading_rule": _rss_rename_rss_auto_downloading_rule,
    "remove_rss_auto_downloading_rule": _rss_remove_rss_auto_downloading_rule,
    "get_all_rss_auto_downloading_rules": _rss_get_all_rss_auto_downloading_rules,
    "get_all_rss_articles_matching_rule": _rss_get_all_rss_articles_matching_rule,
}


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
        except Exception:
            return {"error": "Operation failed"}

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

        handler = _RSS_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        raise ValueError(f"Unknown action: {action}")
