import builtins
import sys
from unittest.mock import MagicMock, patch
import pytest

# Setup standard agent_utilities and parser mocks to isolate execution
mock_initialize = MagicMock()
mock_load_identity = MagicMock()
mock_load_identity.return_value = {
    "name": "qBittorrent Manager",
    "description": "AI agent for qBittorrent management, RSS automation, and search.",
}

import agent_utilities

agent_utilities.initialize_workspace = mock_initialize
agent_utilities.load_identity = mock_load_identity
agent_utilities.build_system_prompt_from_workspace = MagicMock(
    return_value="mock prompt"
)
agent_utilities.create_agent_server = MagicMock()

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


def test_agent_server_coverage():
    """Verify agent server parses command line arguments and invokes backend server.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
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
    """Verify package level safe import functionality.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
    from qbittorrent_agent import _import_module_safely

    assert _import_module_safely("os") is not None
    assert _import_module_safely("non_existent_module") is None


def test_package_dynamic_attributes():
    """Verify lazy-loading fallback proxies inside package initializers.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
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
    qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.agent_server"] = (
        mock_module
    )
    try:
        assert qbittorrent_agent.some_test_attribute_abc == "hello_world_test"
    finally:
        del qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.agent_server"]


def test_main_execution():
    """Verify __main__ package entrypoint invokes backend initialization.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
    import runpy

    agent_utilities.create_agent_server.reset_mock()
    if "qbittorrent_agent" in sys.modules:
        del sys.modules["qbittorrent_agent"]
    if "qbittorrent_agent.agent_server" in sys.modules:
        del sys.modules["qbittorrent_agent.agent_server"]

    with patch("sys.argv", ["agent_server.py"]):
        runpy.run_module("qbittorrent_agent", run_name="__main__")
        agent_utilities.create_agent_server.assert_called_once()


def test_agent_server_main_execution():
    """Verify agent_server direct execution runs setup routines.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
    import runpy

    agent_utilities.create_agent_server.reset_mock()
    if "qbittorrent_agent.agent_server" in sys.modules:
        del sys.modules["qbittorrent_agent.agent_server"]

    with patch("sys.argv", ["agent_server.py"]):
        runpy.run_module("qbittorrent_agent.agent_server", run_name="__main__")
        agent_utilities.create_agent_server.assert_called_once()


def test_mcp_server_main_execution():
    """Verify mcp_server direct run executes server loops.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
    import runpy

    with patch("fastmcp.server.mixins.transport.TransportMixin.run") as mock_run:
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_module("qbittorrent_agent.mcp_server", run_name="__main__")
            assert mock_run.called


def test_requests_dependency_warning_import_error():
    """Verify mcp_server safe import exception handling.

    CONCEPT:OS-5.2 — Resource Scheduling
    """
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "RequestsDependencyWarning" in name or "requests.exceptions" in name:
            raise ImportError("mocked import error")
        return original_import(name, *args, **kwargs)

    if "qbittorrent_agent.mcp_server" in sys.modules:
        del sys.modules["qbittorrent_agent.mcp_server"]

    with patch("builtins.__import__", side_effect=mock_import):
        import importlib
        import qbittorrent_agent.mcp_server

        importlib.reload(qbittorrent_agent.mcp_server)
