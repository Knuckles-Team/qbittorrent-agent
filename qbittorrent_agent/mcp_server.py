import os
import sys
import logging
import json
import inspect
from pathlib import Path
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from pydantic import Field
from agent_utilities import get_logger, to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from qbittorrent_agent.auth import get_client
from qbittorrent_agent.qbittorrent_api import QbittorrentApi

__version__ = "0.1.5"


logger = get_logger(name="QBittorrent_MCP")
logger.setLevel(logging.INFO)

API_CLASSES = {
    "qbittorrent": QbittorrentApi,
}


def load_tool_config() -> Dict[str, Dict[str, str]]:
    """Load the tool methods to tag mapping."""
    config_path = Path(__file__).parent / "tool_tags.json"
    if not config_path.exists():
        logger.error(f"Missing {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_dynamic_tool(
    service: str, method_name: str, tag: str, api_class: type
) -> Optional[Any]:
    """Dynamically compile a wrapper function for an API method."""
    method = getattr(api_class, method_name)
    sig = inspect.signature(method)
    docstring = method.__doc__ or f"Call {service} {method_name}"

    params_code = []
    call_args = []

    for name, param in list(sig.parameters.items())[1:]:
        if param.annotation is inspect.Parameter.empty:
            type_str = "Any"
        else:
            try:
                type_str = str(param.annotation).replace("typing.", "")
                if "class" in type_str:
                    type_str = param.annotation.__name__
            except Exception:
                type_str = "Any"

        if param.default is inspect.Parameter.empty:
            field_def = f"Field(..., description='{name}')"
        else:
            field_def = f"Field(default={repr(param.default)}, description='{name}')"

        params_code.append(f"    {name}: {type_str} = {field_def}")
        call_args.append(f"{name}={name}")

    params_str = ",\n".join(params_code)
    call_args_str = ", ".join(call_args)
    if params_str:
        params_str += ",\n"

    tool_name = f"{method_name}"

    func_source = f'''
async def {tool_name}(
{params_str}
) -> Any:
    """{docstring}"""
    client = get_client()
    # Execute the underlying method
    return client.{method_name}({call_args_str})
'''

    local_env = {}
    global_env = {
        "os": os,
        "Field": Field,
        "Optional": Optional,
        "Dict": Dict,
        "List": List,
        "Any": Any,
        "to_boolean": to_boolean,
        "get_client": get_client,
    }

    try:
        exec(func_source, global_env, local_env)
        return local_env[tool_name]
    except Exception as e:
        logger.error(f"Failed to compile dynamic tool {service}.{method_name}: {e}")
        return None


def register_dynamic_tools(
    mcp: FastMCP, filter_tags: Optional[List[str]] = None
) -> List[str]:
    """Read configuration and dynamically register allowed tools."""
    tool_config = load_tool_config()
    registered_tags = set()

    for service, methods in tool_config.items():
        if service not in API_CLASSES:
            continue

        api_class = API_CLASSES[service]

        for method_name, tag in methods.items():
            if filter_tags and tag not in filter_tags:
                continue

            wrapper_func = _generate_dynamic_tool(service, method_name, tag, api_class)
            if wrapper_func:
                mcp.add_tool(wrapper_func)
                registered_tags.add(tag)

    return sorted(list(registered_tags))


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the qBittorrent Manager MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="qBittorrent Manager MCP",
        version=__version__,
        instructions="qBittorrent Manager MCP Server",
    )

    toggles = {
        "app": "APPTOOL",
        "torrents": "TORRENTSTOOL",
        "transfer": "TRANSFERTOOL",
        "rss": "RSSTOOL",
        "search": "SEARCHTOOL",
        "log": "LOGTOOL",
    }

    registered_tags = []
    for tag, env_var in toggles.items():
        if to_boolean(os.getenv(env_var, "True")):
            registered_tags.extend(register_dynamic_tools(mcp, filter_tags=[tag]))

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"qBittorrent Manager MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(set(registered_tags))}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
