"""Action-discovery behavior for the qbittorrent-agent action-routed tools.

Verifies the shared ``agent_utilities.mcp_utilities.resolve_action`` wiring:
``list_actions`` discovery, real-action dispatch, and a rich did-you-mean
error on an unknown action.
"""

import asyncio
from unittest.mock import MagicMock

from fastmcp import FastMCP

import qbittorrent_agent.mcp_server as mcp_server


class _CapturingMCP(FastMCP):
    """FastMCP that also captures the undecorated tool callables by name."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured: dict = {}

    def tool(self, *args, **kwargs):
        decorator = super().tool(*args, **kwargs)

        def wrapper(func):
            self.captured[func.__name__] = func
            return decorator(func)

        return wrapper


def _get_torrents_tool():
    mcp = _CapturingMCP("test")
    mcp_server.register_torrents_tools(mcp)
    return mcp.captured["qbittorrent_torrents"]


def test_list_actions_returns_names():
    fn = _get_torrents_tool()
    client = MagicMock()
    result = asyncio.run(
        fn(action="list_actions", params_json="{}", client=client, ctx=None)
    )
    assert isinstance(result, dict)
    assert result["service"] == "qbittorrent-agent"
    assert "get_torrent_list" in result["actions"]
    assert len(result["actions"]) > 1


def test_real_action_dispatches():
    fn = _get_torrents_tool()
    client = MagicMock()
    client.get_torrents.return_value = {"ok": True}
    result = asyncio.run(
        fn(action="get_torrent_list", params_json="{}", client=client, ctx=None)
    )
    assert result == {"ok": True}
    client.get_torrents.assert_called_once()


def test_bogus_action_raises_with_list_actions_hint():
    fn = _get_torrents_tool()
    client = MagicMock()
    try:
        asyncio.run(
            fn(action="get_torrent_lst", params_json="{}", client=client, ctx=None)
        )
    except ValueError as exc:
        message = str(exc)
        assert "list_actions" in message
        assert "Did you mean" in message
    else:
        raise AssertionError("expected ValueError for unknown action")
