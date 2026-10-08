#!/usr/bin/env python

import importlib
import inspect
from typing import Any

__all__: list[str] = []

CORE_MODULES: list[str] = ["qbittorrent_agent.api_client"]

OPTIONAL_MODULES = {
    "qbittorrent_agent.agent_server": "agent",
    "qbittorrent_agent.mcp_server": "mcp",
}


def _expose_members(module):
    """Expose public classes and functions from a module into globals and __all__."""
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
            globals()[name] = obj
            if name not in __all__:
                __all__.append(name)


# Eagerly import core modules (keeps API wrappers fast & light)
for module_name in CORE_MODULES:
    if module_name:
        module = importlib.import_module(module_name)
        _expose_members(module)

# Dynamic/lazy loading of optional modules (agent_server, mcp_server)
_loaded_optional_modules: dict[str, Any] = {}


def _import_module_safely(module_name: str):
    """Try to import a module and return it, or None if not available."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


# Maps a synthetic availability-flag attribute to the substring identifying
# which entry in OPTIONAL_MODULES it reports on.
_AVAILABILITY_FLAGS = {
    "_MCP_AVAILABLE": "mcp_server",
    "_AGENT_AVAILABLE": "agent_server",
}


def _optional_module_available(module_substring: str) -> bool:
    """Report whether the optional module matching ``module_substring`` imports."""
    module_name = next((k for k in OPTIONAL_MODULES if module_substring in k), None)
    if module_name is None:
        return False
    return _import_module_safely(module_name) is not None


def _resolve_from_optional_modules(name: str) -> Any:
    """Lazily import each optional module in turn until one exposes ``name``."""
    for module_name in OPTIONAL_MODULES:
        if module_name not in _loaded_optional_modules:
            module = _import_module_safely(module_name)
            if module is not None:
                _loaded_optional_modules[module_name] = module
                _expose_members(module)

        module = _loaded_optional_modules.get(module_name)
        if module is not None and hasattr(module, name):
            return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    # Handle availability flags dynamically without eager imports
    if name in _AVAILABILITY_FLAGS:
        return _optional_module_available(_AVAILABILITY_FLAGS[name])

    return _resolve_from_optional_modules(name)


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)
