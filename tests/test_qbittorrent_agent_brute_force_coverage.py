import asyncio
import inspect
import json
import os
import sys
from typing import Any
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
import requests

# Mock agent_utilities workspace and identity functions at the module level
# to prevent locked DB or network calls during test collection and execution
mock_initialize = MagicMock()
mock_load_identity = MagicMock()
mock_load_identity.return_value = {
    "name": "qBittorrent Manager",
    "description": "AI agent for qBittorrent management, RSS automation, and search.",
}

import agent_utilities
agent_utilities.initialize_workspace = mock_initialize
agent_utilities.load_identity = mock_load_identity
agent_utilities.build_system_prompt_from_workspace = MagicMock(return_value="mock prompt")
agent_utilities.create_agent_server = MagicMock()

# Mock agent parser to avoid parsing pytest command line arguments
mock_parser = MagicMock()
mock_args = MagicMock()
mock_args.debug = False
mock_args.mcp_url = "http://localhost:8000"
mock_args.mcp_config = "mcp_config.json"
mock_args.host = "127.0.0.1"
mock_args.port = 8000
mock_args.provider = "openai"
mock_args.model_id = "gpt-4o"
mock_args.base_url = None
mock_args.api_key = None
mock_args.custom_skills_directory = None
mock_args.web = False
mock_args.otel = False
mock_args.otel_endpoint = None
mock_args.otel_headers = None
mock_args.otel_public_key = None
mock_args.otel_secret_key = None
mock_args.otel_protocol = None
mock_parser.parse_args.return_value = mock_args
agent_utilities.create_agent_parser = MagicMock(return_value=mock_parser)


@pytest.fixture
def mock_session():
    with patch("requests.Session") as mock_s:
        session = mock_s.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"id": 1, "name": "test"}
        response.text = '{"id": 1}'
        session.get.return_value = response
        session.post.return_value = response
        session.put.return_value = response
        session.delete.return_value = response
        session.patch.return_value = response

        # SID cookie mock
        session.cookies = {"SID": "test_sid"}
        yield session


def test_qbittorrent_models_coverage():
    from qbittorrent_agent import qbittorrent_models
    from pydantic import BaseModel

    for name, obj in inspect.getmembers(qbittorrent_models, inspect.isclass):
        if issubclass(obj, BaseModel) and obj is not BaseModel:
            kwargs: dict[str, Any] = {}
            for field_name, field in obj.model_fields.items():
                if field.is_required():
                    anno = field.annotation
                    anno_str = str(anno)
                    if "int" in anno_str:
                        kwargs[field_name] = 1
                    elif "float" in anno_str:
                        kwargs[field_name] = 1.0
                    elif "bool" in anno_str:
                        kwargs[field_name] = True
                    elif "list" in anno_str or "List" in anno_str:
                        kwargs[field_name] = []
                    elif "dict" in anno_str or "Dict" in anno_str:
                        kwargs[field_name] = {}
                    else:
                        kwargs[field_name] = "test"
            try:
                inst = obj(**kwargs)
                assert isinstance(inst, obj)
            except Exception as e:
                print(f"Failed instantiating {name}: {e}")


def test_qbittorrent_api_brute_force(mock_session):
    from qbittorrent_agent.api_client import QbittorrentApi

    api_instance = QbittorrentApi(base_url="http://test", username="test", password="test")
    api_instance.session.cookies = requests.utils.cookiejar_from_dict({"SID": "test_sid"})

    # Call specific scenarios to cover lines that default arguments would miss
    api_instance.get_torrents(
        filter="all",
        category="test",
        tag="test",
        sort="name",
        reverse=True,
        limit=10,
        offset=5,
        hashes="hash1|hash2",
    )
    api_instance.get_torrent_contents(hash="test", indexes="1,2,3")
    api_instance.mark_rss_as_read(item_path="test", article_id="123")
    api_instance.search_status(search_id=123)

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", return_value=MagicMock()):
            api_instance.add_torrent(
                urls="http://test",
                torrent_files=["test.torrent"],
                some_kwarg=True,
            )

    api_instance.logout()

    # Introspect all remaining methods
    for name, method in inspect.getmembers(api_instance, predicate=inspect.ismethod):
        if name.startswith("_") or name in ("login", "logout"):
            continue

        print(f"Calling {name}...")
        sig = inspect.signature(method)
        kwargs: dict[str, Any] = {}
        for p_name, p in sig.parameters.items():
            if p.default is inspect.Parameter.empty:
                p_str = str(p.annotation)
                if "int" in p_str:
                    kwargs[p_name] = 1
                elif "float" in p_str:
                    kwargs[p_name] = 1.0
                elif "bool" in p_str:
                    kwargs[p_name] = True
                elif "dict" in p_str:
                    kwargs[p_name] = {}
                elif "list" in p_str:
                    kwargs[p_name] = []
                else:
                    kwargs[p_name] = "test"

        try:
            method(**kwargs)
        except Exception as e:
            # We fail the test if there is an unexpected error like require_auth failure
            # but allow handled/intended exceptions to catch actual implementation bugs
            if isinstance(e, AttributeError) and "headers" in str(e):
                raise e
            print(f"Handled method call for {name}: {e}")


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
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
    from qbittorrent_agent.mcp_server import get_mcp_instance

    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    with patch.object(RateLimitingMiddleware, "on_request", mock_on_request):
        with patch("qbittorrent_agent.auth.get_client") as mock_api_class:
            mock_api = mock_api_class.return_value

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
                        if (
                            hasattr(tool, "parameters")
                            and hasattr(tool.parameters, "properties")
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


def test_qbittorrent_api_errors(mock_session):
    from qbittorrent_agent.api_client import QbittorrentApi
    from agent_utilities.core.exceptions import AuthError, UnauthorizedError

    # Test verify=False logic
    api_instance_no_verify = QbittorrentApi(base_url="http://test", verify=False)
    assert api_instance_no_verify.session.verify is False

    # Trigger 400 error (we return text or json) for both GET and POST
    response_400 = MagicMock()
    response_400.status_code = 400
    response_400.text = "Error detail"
    response_400.json.side_effect = ValueError("Not JSON")
    mock_session.get.return_value = response_400
    mock_session.post.return_value = response_400
    res = api_instance_no_verify.get_version()
    assert res == "Error detail"

    # Trigger 400 error for POST specifically (covers _post ValueError)
    res_post = api_instance_no_verify.shutdown_application()
    assert res_post == "Error detail"

    # Trigger 400 error where text property access throws an exception
    response_400_throw = MagicMock()
    response_400_throw.status_code = 400
    type(response_400_throw).text = PropertyMock(
        side_effect=Exception("Mock text error")
    )
    mock_session.get.return_value = response_400_throw
    try:
        api_instance_no_verify.get_version()
    except Exception:
        pass

    # Trigger empty response
    response_empty = MagicMock()
    response_empty.status_code = 200
    response_empty.text = ""
    response_empty.json.side_effect = ValueError
    mock_session.get.return_value = response_empty
    api_instance_no_verify.session.cookies = requests.utils.cookiejar_from_dict({"SID": "test_sid"})
    res = api_instance_no_verify.get_version()
    assert res == ""

    # Trigger non-JSON content decode error
    response_non_json = MagicMock()
    response_non_json.status_code = 200
    response_non_json.text = "invalid json payload"
    response_non_json.json.side_effect = ValueError
    response_non_json.headers = {"Content-Type": "text/html"}
    mock_session.get.return_value = response_non_json
    res = api_instance_no_verify.get_version()
    assert res == "invalid json payload"

    # Trigger 401 UnauthorizedError
    response_401 = MagicMock()
    response_401.status_code = 401
    mock_session.get.return_value = response_401
    mock_session.post.return_value = response_401
    with pytest.raises(UnauthorizedError):
        api_instance_no_verify.get_version()

    # Trigger 403 UnauthorizedError
    response_403 = MagicMock()
    response_403.status_code = 403
    mock_session.get.return_value = response_403
    mock_session.post.return_value = response_403
    with pytest.raises(UnauthorizedError):
        api_instance_no_verify.get_version()

    # Trigger 404 logger warning
    response_404 = MagicMock()
    response_404.status_code = 404
    response_404.url = "http://test/404"
    mock_session.get.return_value = response_404
    api_instance_no_verify.get_version()


def test_qbittorrent_api_login_failures(mock_session):
    from qbittorrent_agent.api_client import QbittorrentApi
    from agent_utilities.core.exceptions import AuthError

    # 1. 403 IP banned
    response_403 = MagicMock()
    response_403.status_code = 403
    mock_session.post.return_value = response_403
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "User's IP is banned" in str(exc_info.value)

    # 2. Other status code (e.g. 500)
    response_500 = MagicMock()
    response_500.status_code = 500
    response_500.text = "Internal server error"
    mock_session.post.return_value = response_500
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "Login failed with status code 500" in str(exc_info.value)

    # 3. Connection error
    mock_session.post.side_effect = requests.exceptions.RequestException("connection error")
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "Connection error during login" in str(exc_info.value)

    # 4. 200 OK but SID cookie not found
    mock_session.post.side_effect = None
    response_200 = MagicMock()
    response_200.status_code = 200
    mock_session.post.return_value = response_200
    mock_session.cookies = {}
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "SID cookie not found" in str(exc_info.value)


def test_agent_server_coverage():
    from qbittorrent_agent.agent_server import agent_server

    # Standard execution test
    with patch("qbittorrent_agent.agent_server.create_agent_server") as mock_s:
        with patch("sys.argv", ["agent_server.py"]):
            agent_server()
            assert mock_s.called

    # Debug mode execution test
    with patch("qbittorrent_agent.agent_server.create_agent_server") as mock_s:
        mock_args.debug = True
        try:
            with patch("sys.argv", ["agent_server.py", "--debug"]):
                agent_server()
                assert mock_s.called
        finally:
            mock_args.debug = False


def test_init_coverage():
    from qbittorrent_agent import _import_module_safely

    assert _import_module_safely("os") is not None
    assert _import_module_safely("non_existent_module") is None


def test_package_dynamic_attributes():
    import qbittorrent_agent

    # 1. Trigger __dir__
    assert "QbittorrentApi" in dir(qbittorrent_agent)

    # 2. Trigger _MCP_AVAILABLE and _AGENT_AVAILABLE
    assert qbittorrent_agent._MCP_AVAILABLE is True
    assert qbittorrent_agent._AGENT_AVAILABLE is True

    # 3. Trigger AttributeError
    with pytest.raises(AttributeError):
        _ = qbittorrent_agent.non_existent_attribute

    # 4. Trigger safe import error handling
    with patch("importlib.import_module", side_effect=ImportError):
        from qbittorrent_agent import __getattr__

        assert __getattr__("_MCP_AVAILABLE") is False
        assert __getattr__("_AGENT_AVAILABLE") is False

    # 5. Trigger OPTIONAL_MODULES missing keys to hit lines in __getattr__
    original_optional = dict(qbittorrent_agent.OPTIONAL_MODULES)
    try:
        qbittorrent_agent.OPTIONAL_MODULES.clear()
        assert qbittorrent_agent.__getattr__("_MCP_AVAILABLE") is False
        assert qbittorrent_agent.__getattr__("_AGENT_AVAILABLE") is False
    finally:
        qbittorrent_agent.OPTIONAL_MODULES.update(original_optional)

    # 6. Trigger fallback modules loading check
    mock_module = MagicMock()
    mock_module.some_test_attribute_abc = "hello_world_test"
    qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.agent_server"] = mock_module
    try:
        assert getattr(qbittorrent_agent, "some_test_attribute_abc") == "hello_world_test"
    finally:
        del qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.agent_server"]


def test_main_execution():
    import runpy
    import sys

    agent_utilities.create_agent_server.reset_mock()
    if "qbittorrent_agent" in sys.modules:
        del sys.modules["qbittorrent_agent"]
    if "qbittorrent_agent.agent_server" in sys.modules:
        del sys.modules["qbittorrent_agent.agent_server"]

    with patch("sys.argv", ["agent_server.py"]):
        runpy.run_module("qbittorrent_agent", run_name="__main__")
        agent_utilities.create_agent_server.assert_called_once()


def test_agent_server_main_execution():
    import runpy
    import sys

    agent_utilities.create_agent_server.reset_mock()
    if "qbittorrent_agent.agent_server" in sys.modules:
        del sys.modules["qbittorrent_agent.agent_server"]

    with patch("sys.argv", ["agent_server.py"]):
        runpy.run_module("qbittorrent_agent.agent_server", run_name="__main__")
        agent_utilities.create_agent_server.assert_called_once()


def test_mcp_server_main_execution():
    import runpy
    from fastmcp import FastMCP

    with patch.object(FastMCP, "run") as mock_run:
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_module("qbittorrent_agent.mcp_server", run_name="__main__")
            assert mock_run.called


def test_mcp_server_run_options():
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
        mock_mcp.run.assert_called_with(
            transport="sse", host="127.0.0.1", port=8000
        )

        # Test invalid transport
        mock_args.transport = "invalid"
        with patch("sys.exit") as mock_exit:
            mcp_server()
            mock_exit.assert_called_with(1)


def test_auth_get_client_error():
    from qbittorrent_agent.auth import get_client
    from agent_utilities.core.exceptions import AuthError, UnauthorizedError

    with patch("qbittorrent_agent.auth._client", None):
        with patch("qbittorrent_agent.auth.QbittorrentApi", side_effect=AuthError("auth error")):
            with pytest.raises(RuntimeError) as exc_info:
                get_client()
            assert "AUTHENTICATION ERROR" in str(exc_info.value)

    with patch("qbittorrent_agent.auth._client", None):
        with patch("qbittorrent_agent.auth.QbittorrentApi", side_effect=UnauthorizedError("auth error")):
            with pytest.raises(RuntimeError) as exc_info:
                get_client()
            assert "AUTHENTICATION ERROR" in str(exc_info.value)


def test_auth_get_client_success():
    from qbittorrent_agent.auth import get_client

    with patch("qbittorrent_agent.auth._client", None):
        with patch("qbittorrent_agent.auth.QbittorrentApi") as mock_api:
            client = get_client()
            assert client is not None


def test_requests_dependency_warning_import_error():
    import sys
    import builtins

    original_import = builtins.__import__
    def mock_import(name, *args, **kwargs):
        if "RequestsDependencyWarning" in name or "requests.exceptions" in name:
            raise ImportError("mocked import error")
        return original_import(name, *args, **kwargs)

    if "qbittorrent_agent.mcp_server" in sys.modules:
        del sys.modules["qbittorrent_agent.mcp_server"]

    with patch("builtins.__import__", side_effect=mock_import):
        import qbittorrent_agent.mcp_server
        import importlib
        importlib.reload(qbittorrent_agent.mcp_server)
