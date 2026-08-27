"""Characterization tests for ``register_torrents_tools.qbittorrent_torrents``.

Lane: CXA-FL-QBITTORRENTAGENT-01 (Phase A, CCN 53).

There are TWO independently-defined copies of this function in this repo:

* ``qbittorrent_agent.mcp_server.register_torrents_tools`` — the live copy,
  wired into the production server (``get_mcp_instance`` / ``create_mcp_server``)
  and already exercised by ``tests/test_action_discovery.py`` and
  ``tests/test_coverage_mcp_server.py``.
* ``qbittorrent_agent.mcp.mcp_torrents.register_torrents_tools`` — a byte-for-byte
  duplicate (differs only in a return-type annotation, ``-> Any`` vs ``-> dict``)
  that lives in the ``qbittorrent_agent.mcp`` sub-package. That sub-package is
  NOT imported by ``mcp_server.py``, any other module in this repo, any test in
  this repo, or (per a workspace-wide grep) any other repo — it appears to be an
  orphaned artifact of an "ecosystem standardization" auto-split that was never
  wired in. See the lane report for full evidence.

Because the second copy has ZERO existing test coverage anywhere, every
assertion here is written generically and parametrized over BOTH
implementations so it pins both independently.

These tests target the UNMODIFIED, pre-refactor functions and must stay
byte-identical across commit 2 (the refactor commit).
"""

from __future__ import annotations

import asyncio
import json
from unittest.mock import MagicMock

import pytest
from fastmcp import FastMCP

import qbittorrent_agent.mcp.mcp_torrents as mcp_torrents_module
import qbittorrent_agent.mcp_server as mcp_server_module

# (action, expected client-method name) for every one of the 46 branches,
# extracted mechanically from the source (both copies are identical here).
ACTION_CLIENT_PAIRS = [
    ("get_torrent_list", "get_torrents"),
    ("get_torrent_properties", "get_torrent_properties"),
    ("get_torrent_trackers", "get_torrent_trackers"),
    ("get_torrent_webseeds", "get_torrent_webseeds"),
    ("get_torrent_contents", "get_torrent_contents"),
    ("get_torrent_piece_states", "get_torrent_piece_states"),
    ("get_torrent_piece_hashes", "get_torrent_piece_hashes"),
    ("pause_torrents", "pause_torrents"),
    ("resume_torrents", "resume_torrents"),
    ("delete_torrents", "delete_torrents"),
    ("recheck_torrents", "recheck_torrents"),
    ("reannounce_torrents", "reannounce_torrents"),
    ("edit_tracker", "edit_tracker"),
    ("remove_trackers", "remove_trackers"),
    ("add_peers", "add_peers"),
    ("add_new_torrent", "add_torrent"),
    ("add_trackers_to_torrent", "add_trackers"),
    ("increase_torrent_priority", "increase_priority"),
    ("decrease_torrent_priority", "decrease_priority"),
    ("top_torrent_priority", "top_priority"),
    ("bottom_torrent_priority", "bottom_priority"),
    ("set_file_priority", "set_file_priority"),
    ("get_torrent_download_limit", "get_torrent_download_limit"),
    ("set_torrent_download_limit", "set_torrent_download_limit"),
    ("set_torrent_share_limit", "set_torrent_share_limit"),
    ("get_torrent_upload_limit", "get_torrent_upload_limit"),
    ("set_torrent_upload_limit", "set_torrent_upload_limit"),
    ("set_torrent_location", "set_torrent_location"),
    ("set_torrent_name", "set_torrent_name"),
    ("set_torrent_category", "set_torrent_category"),
    ("get_all_categories", "get_categories"),
    ("add_new_category", "create_category"),
    ("edit_category", "edit_category"),
    ("remove_categories", "remove_categories"),
    ("add_torrent_tags", "add_torrent_tags"),
    ("remove_torrent_tags", "remove_torrent_tags"),
    ("get_all_tags", "get_tags"),
    ("create_tags", "create_tags"),
    ("delete_tags", "delete_tags"),
    ("set_auto_management", "set_auto_management"),
    ("toggle_sequential_download", "toggle_sequential_download"),
    ("toggle_first_last_piece_priority", "toggle_first_last_piece_priority"),
    ("set_force_start", "set_force_start"),
    ("set_super_seeding", "set_super_seeding"),
    ("rename_file", "rename_file"),
    ("rename_folder", "rename_folder"),
]

MODULES = {
    "mcp_server": mcp_server_module,
    "mcp_torrents": mcp_torrents_module,
}


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


def _get_torrents_tool(module):
    mcp = _CapturingMCP("test")
    module.register_torrents_tools(mcp)
    return mcp.captured["qbittorrent_torrents"]


@pytest.mark.parametrize("module_name", list(MODULES))
@pytest.mark.parametrize("action,client_attr", ACTION_CLIENT_PAIRS)
def test_action_dispatches_to_expected_client_method(module_name, action, client_attr):
    """Every valid action must call exactly the mapped client method, once,
    with the parsed params_json kwargs passed straight through, and return
    that call's result unchanged."""
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()
    sentinel = {"sentinel": f"{action}-result"}
    getattr(client, client_attr).return_value = sentinel

    result = asyncio.run(
        fn(
            action=action,
            params_json=json.dumps({"hashes": "abc123", "extra": 7}),
            client=client,
            ctx=None,
        )
    )

    getattr(client, client_attr).assert_called_once_with(hashes="abc123", extra=7)
    assert result == sentinel

    # No other client method should have been touched.
    for other_action, other_attr in ACTION_CLIENT_PAIRS:
        if other_attr == client_attr:
            continue
        assert not getattr(client, other_attr).called, (
            f"action={action!r} unexpectedly touched client.{other_attr}"
        )


@pytest.mark.parametrize("module_name", list(MODULES))
def test_none_valued_params_are_dropped_before_dispatch(module_name):
    """kwargs with a JSON null value are filtered out (``if v is not None``)
    before being passed to the client method; falsy-but-not-None values
    (0, "", False) survive."""
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()
    client.get_torrents.return_value = {"ok": True}

    asyncio.run(
        fn(
            action="get_torrent_list",
            params_json=json.dumps({"filter": None, "limit": 0, "reverse": False, "tag": ""}),
            client=client,
            ctx=None,
        )
    )

    client.get_torrents.assert_called_once_with(limit=0, reverse=False, tag="")


@pytest.mark.parametrize("module_name", list(MODULES))
def test_invalid_json_params_returns_generic_error(module_name):
    """Malformed params_json is swallowed and reported as a generic error dict
    -- pinning the (unhelpful) copy-paste error message as current behavior."""
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()

    result = asyncio.run(
        fn(action="get_torrent_list", params_json="{not valid json", client=client, ctx=None)
    )

    assert result == {"error": "Operation failed"}
    assert not client.get_torrents.called


@pytest.mark.parametrize("module_name", list(MODULES))
def test_unknown_action_raises_with_did_you_mean_hint(module_name):
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()

    with pytest.raises(ValueError) as exc_info:
        asyncio.run(
            fn(action="get_torrent_lst", params_json="{}", client=client, ctx=None)
        )

    message = str(exc_info.value)
    assert "list_actions" in message
    assert "Did you mean" in message


@pytest.mark.parametrize("module_name", list(MODULES))
def test_list_actions_returns_all_46_action_names(module_name):
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()

    result = asyncio.run(
        fn(action="list_actions", params_json="{}", client=client, ctx=None)
    )

    assert isinstance(result, dict)
    assert result["service"] == "qbittorrent-agent"
    expected = {a for a, _ in ACTION_CLIENT_PAIRS}
    assert expected.issubset(set(result["actions"]))


@pytest.mark.parametrize("module_name", list(MODULES))
def test_ctx_info_awaited_when_context_provided(module_name):
    """When ``ctx`` is supplied, ``ctx.info("Executing tool...")`` is invoked
    (and awaited if awaitable) before dispatch."""
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()
    client.get_torrents.return_value = {"ok": True}

    async def _info(msg):
        return None

    ctx = MagicMock()
    ctx.info = MagicMock(side_effect=_info)

    asyncio.run(
        fn(action="get_torrent_list", params_json="{}", client=client, ctx=ctx)
    )

    ctx.info.assert_called_once_with("Executing tool...")


@pytest.mark.parametrize("module_name", list(MODULES))
def test_ctx_info_not_called_when_ctx_is_none(module_name):
    fn = _get_torrents_tool(MODULES[module_name])
    client = MagicMock()
    client.get_torrents.return_value = {"ok": True}

    # Should simply not raise, and should not attempt to touch a None ctx.
    result = asyncio.run(
        fn(action="get_torrent_list", params_json="{}", client=client, ctx=None)
    )
    assert result == {"ok": True}
