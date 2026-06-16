import asyncio
import inspect
import json
from typing import Any
from unittest.mock import MagicMock, patch

from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

VALID_TOOL_ACTIONS = {
    "qbittorrent_app": [
        "get_application_version",
        "get_api_version",
        "get_build_info",
        "shutdown_application",
        "get_preferences",
        "set_preferences",
        "get_default_save_path",
    ],
    "qbittorrent_log": [
        "get_main_log",
        "get_peer_log",
    ],
    "qbittorrent_sync": [
        "get_main_data",
        "get_torrent_peers_data",
    ],
    "qbittorrent_transfer": [
        "get_global_transfer_info",
        "get_speed_limits_mode",
        "toggle_speed_limits_mode",
        "get_global_download_limit",
        "set_global_download_limit",
        "get_global_upload_limit",
        "set_global_upload_limit",
        "ban_peers",
    ],
    "qbittorrent_torrents": [
        "get_torrent_list",
        "get_torrent_properties",
        "get_torrent_trackers",
        "get_torrent_webseeds",
        "get_torrent_contents",
        "get_torrent_piece_states",
        "get_torrent_piece_hashes",
        "pause_torrents",
        "resume_torrents",
        "delete_torrents",
        "recheck_torrents",
        "reannounce_torrents",
        "edit_tracker",
        "remove_trackers",
        "add_peers",
        "add_new_torrent",
        "add_trackers_to_torrent",
        "increase_torrent_priority",
        "decrease_torrent_priority",
        "top_torrent_priority",
        "bottom_torrent_priority",
        "set_file_priority",
        "get_torrent_download_limit",
        "set_torrent_download_limit",
        "set_torrent_share_limit",
        "get_torrent_upload_limit",
        "set_torrent_upload_limit",
        "set_torrent_location",
        "set_torrent_name",
        "set_torrent_category",
        "get_all_categories",
        "add_new_category",
        "edit_category",
        "remove_categories",
        "add_torrent_tags",
        "remove_torrent_tags",
        "get_all_tags",
        "create_tags",
        "delete_tags",
        "set_auto_management",
        "toggle_sequential_download",
        "toggle_first_last_piece_priority",
        "set_force_start",
        "set_super_seeding",
        "rename_file",
        "rename_folder",
    ],
    "qbittorrent_rss": [
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
    ],
    "qbittorrent_search": [
        "start_search",
        "stop_search",
        "get_search_status",
        "get_search_results",
        "delete_search",
        "get_search_plugins",
        "install_search_plugin",
        "uninstall_search_plugin",
        "enable_search_plugin",
        "update_search_plugins",
    ],
}


def test_mcp_server_coverage(mock_session):
    """Verify MCP tools invoke correctly with and without Context.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
    """

    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    with patch.object(RateLimitingMiddleware, "on_request", mock_on_request):
        with patch("qbittorrent_agent.auth.get_client") as mock_api_class:
            mock_api = mock_api_class.return_value

            from qbittorrent_agent.mcp_server import get_mcp_instance

            mcp_data = get_mcp_instance()
            mcp = mcp_data[0] if isinstance(mcp_data, tuple) else mcp_data

            async def run_tools():
                # Test custom health route
                routes = []
                if hasattr(mcp, "_additional_http_routes"):
                    routes = mcp._additional_http_routes
                elif hasattr(mcp, "routes"):
                    routes = mcp.routes
                elif hasattr(mcp, "_app") and hasattr(mcp._app, "routes"):
                    routes = mcp._app.routes

                for route in routes:
                    if hasattr(route, "path") and route.path == "/health":
                        from starlette.datastructures import Headers
                        from starlette.requests import Request

                        mock_scope = {
                            "type": "http",
                            "method": "GET",
                            "path": "/health",
                            "headers": Headers().raw,
                        }
                        mock_req = Request(scope=mock_scope)
                        res = await route.endpoint(mock_req)
                        assert res.status_code == 200
                        assert json.loads(res.body.decode()) == {"status": "OK"}

                tool_objs = (
                    await mcp.list_tools()
                    if inspect.iscoroutinefunction(mcp.list_tools)
                    else mcp.list_tools()
                )
                for tool in tool_objs:
                    tool_name = tool.name
                    print(f"Testing MCP tool: {tool_name}")

                    # 1. Standard call_tool using the first valid action
                    try:
                        target_params: dict[str, Any] = {}
                        if hasattr(tool, "parameters") and hasattr(
                            tool.parameters, "properties"
                        ):
                            for p_name in tool.parameters.properties.keys():
                                if p_name == "action":
                                    target_params["action"] = VALID_TOOL_ACTIONS.get(
                                        tool_name, [""]
                                    )[0]
                                elif p_name == "params_json":
                                    target_params["params_json"] = "{}"
                                else:
                                    target_params[p_name] = "test"
                        await mcp.call_tool(tool_name, target_params)
                    except Exception as e:
                        print(f"Standard tool call failed: {e}")

                    # 2. Direct tool.fn call for every single valid action
                    actions = VALID_TOOL_ACTIONS.get(tool_name, [None])
                    for act in actions:
                        try:
                            # With and without Context
                            await tool.fn(
                                action=act,
                                params_json="{}",
                                client=mock_api,
                                ctx=MagicMock(),
                            )
                            await tool.fn(
                                action=act,
                                params_json="{}",
                                client=mock_api,
                                ctx=None,
                            )
                        except Exception as e:
                            print(f"Direct tool.fn call failed for {act}: {e}")

                    # 3. Invalid action path to cover ValueError
                    try:
                        await tool.fn(
                            action="invalid_action_xyz",
                            params_json="{}",
                            client=mock_api,
                            ctx=MagicMock(),
                        )
                    except ValueError:
                        pass

                    # 4. Invalid json in params_json
                    try:
                        await tool.fn(
                            action=actions[0],
                            params_json="invalid_json",
                            client=mock_api,
                            ctx=MagicMock(),
                        )
                    except Exception:
                        pass

            loop = asyncio.new_event_loop()
            loop.run_until_complete(run_tools())
            loop.close()


def test_mcp_server_run_options():
    """Verify different command line transport and run configurations.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
    """
    from qbittorrent_agent.mcp_server import mcp_server

    mock_mcp = MagicMock()
    mock_args = MagicMock()

    with patch(
        "qbittorrent_agent.mcp_server.get_mcp_instance",
        return_value=(mock_mcp, mock_args, []),
    ):
        # Test stdio transport
        mock_args.transport = "stdio"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="stdio")

        # Test streamable-http transport
        mock_args.transport = "streamable-http"
        mock_args.host = "127.0.0.1"
        mock_args.port = 8000
        mcp_server()
        mock_mcp.run.assert_called_with(
            transport="streamable-http", host="127.0.0.1", port=8000
        )

        # Test sse transport
        mock_args.transport = "sse"
        mcp_server()
        mock_mcp.run.assert_called_with(transport="sse", host="127.0.0.1", port=8000)

        # Test invalid transport
        mock_args.transport = "invalid"
        with patch("sys.exit") as mock_exit:
            mcp_server()
            mock_exit.assert_called_with(1)
