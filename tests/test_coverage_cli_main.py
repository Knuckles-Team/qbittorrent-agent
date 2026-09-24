import builtins
import sys
from unittest.mock import MagicMock, patch

import pytest


def test_init_coverage():
    """Verify package level safe import functionality.

    CONCEPT:AU-OS.state.cognitive-scheduler-preemption — Resource Scheduling
    """
    from qbittorrent_agent import _import_module_safely

    assert _import_module_safely("os") is not None
    assert _import_module_safely("non_existent_module") is None


def test_package_dynamic_attributes():
    """Verify lazy-loading fallback proxies inside package initializers.

    CONCEPT:AU-OS.state.cognitive-scheduler-preemption — Resource Scheduling
    """
    import qbittorrent_agent

    # 1. Trigger __dir__
    assert "QbittorrentApi" in dir(qbittorrent_agent)

    # 2. Trigger _MCP_AVAILABLE; agent_server was retired fleet-wide, so
    # _AGENT_AVAILABLE is a permanent False (no such optional module exists).
    assert qbittorrent_agent._MCP_AVAILABLE is True
    assert qbittorrent_agent._AGENT_AVAILABLE is False

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
    qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.mcp_server"] = (
        mock_module
    )
    try:
        assert qbittorrent_agent.some_test_attribute_abc == "hello_world_test"
    finally:
        del qbittorrent_agent._loaded_optional_modules["qbittorrent_agent.mcp_server"]


def test_main_execution():
    """Verify __main__ package entrypoint runs the MCP server.

    CONCEPT:AU-OS.state.cognitive-scheduler-preemption — Resource Scheduling
    """
    import runpy

    if "qbittorrent_agent" in sys.modules:
        del sys.modules["qbittorrent_agent"]
    if "qbittorrent_agent.__main__" in sys.modules:
        del sys.modules["qbittorrent_agent.__main__"]

    with patch("qbittorrent_agent.mcp_server.mcp_server") as mock_mcp_server:
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_module("qbittorrent_agent", run_name="__main__")
            mock_mcp_server.assert_called_once()


def test_mcp_server_main_execution():
    """Verify mcp_server direct run executes server loops.

    CONCEPT:AU-OS.state.cognitive-scheduler-preemption — Resource Scheduling
    """
    import runpy

    with patch("fastmcp.server.mixins.transport.TransportMixin.run") as mock_run:
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_module("qbittorrent_agent.mcp_server", run_name="__main__")
            assert mock_run.called


def test_requests_dependency_warning_import_error():
    """Verify mcp_server safe import exception handling.

    CONCEPT:AU-OS.state.cognitive-scheduler-preemption — Resource Scheduling
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
