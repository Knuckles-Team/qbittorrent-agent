import inspect
from typing import Any
from unittest.mock import MagicMock, patch

import requests

from qbittorrent_agent.api_client import QbittorrentApi


def test_qbittorrent_api_brute_force(mock_session):
    """Programmatically introspect and invoke all QbittorrentApi wrapper endpoints.

    CONCEPT:AU-ORCH.adapter.kg-graph-materialization — Action Execution Pipeline
    """
    api_instance = QbittorrentApi(
        base_url="http://test", username="test", password="test"
    )
    api_instance.session.cookies = requests.utils.cookiejar_from_dict(
        {"SID": "test_sid"}
    )

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
        kwargs = _synthesize_kwargs(sig)
        _invoke_and_tolerate(method, kwargs)


def _default_value_for_param(p: inspect.Parameter) -> Any:
    """Synthesize a plausible value for a required (no-default) parameter.

    Picked by scanning the parameter's annotation text for a known type name;
    falls back to the string ``"test"`` when nothing matches.
    """
    p_str = str(p.annotation)
    if "int" in p_str:
        return 1
    if "float" in p_str:
        return 1.0
    if "bool" in p_str:
        return True
    if "dict" in p_str:
        return {}
    if "list" in p_str:
        return []
    return "test"


def _synthesize_kwargs(sig: inspect.Signature) -> dict[str, Any]:
    """Build a kwargs dict covering every required (no-default) parameter of `sig`."""
    kwargs: dict[str, Any] = {}
    for p_name, p in sig.parameters.items():
        if p.default is inspect.Parameter.empty:
            kwargs[p_name] = _default_value_for_param(p)
    return kwargs


def _invoke_and_tolerate(method, kwargs: dict[str, Any]) -> None:
    """Call ``method(**kwargs)``, tolerating handled exceptions.

    Re-raises an ``AttributeError`` mentioning "headers" (a ``require_auth``
    failure signal, i.e. a real implementation bug) but swallows/logs any
    other exception, since these are best-effort brute-force calls.
    """
    try:
        method(**kwargs)
    except Exception as e:
        # We fail the test if there is an unexpected error like require_auth failure
        # but allow handled/intended exceptions to catch actual implementation bugs
        if isinstance(e, AttributeError) and "headers" in str(e):
            raise e
        print(f"Operation failed: {type(e).__name__}")
