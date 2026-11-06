from unittest.mock import MagicMock, PropertyMock, patch

import pytest
import requests
from scion_sdk.exceptions import AuthError, UnauthorizedError

from qbittorrent_agent.api_client import QbittorrentApi
from qbittorrent_agent.auth import get_client




def test_qbittorrent_api_login_failures(mock_session):
    """Verify API client handling for various authentication and login errors.

    CONCEPT:AU-OS.governance.reactive-multi-axis-budget — Guardrail Engine / Session Concurrency
    """
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
    assert "Login failed with HTTP 500" in str(exc_info.value)

    # 3. Connection error
    mock_session.post.side_effect = requests.exceptions.RequestException(
        "connection error"
    )
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "Connection error during login" in str(exc_info.value)

    # 4. 200 OK but session cookie not set
    mock_session.post.side_effect = None
    response_200 = MagicMock()
    response_200.status_code = 200
    mock_session.post.return_value = response_200
    mock_session.cookies = {}
    with pytest.raises(AuthError) as exc_info:
        QbittorrentApi(base_url="http://test")
    assert "no session cookie set" in str(exc_info.value)


@patch.dict(
    "os.environ",
    {
        "QBITTORRENT_URL": "https://service.invalid",
        "QBITTORRENT_USERNAME": "user",
        "QBITTORRENT_PASSWORD": "secret",
    },
)
def test_auth_get_client_error():
    """Verify singleton client initialization raises correct RuntimeErrors.

    CONCEPT:AU-OS.governance.reactive-multi-axis-budget — Guardrail Engine / Session Concurrency
    """
    with patch("qbittorrent_agent.auth._client", None):
        with patch(
            "qbittorrent_agent.auth.QbittorrentApi", side_effect=AuthError("auth error")
        ):
            with pytest.raises(RuntimeError) as exc_info:
                get_client()
            assert "AUTHENTICATION ERROR" in str(exc_info.value)

    with patch("qbittorrent_agent.auth._client", None):
        with patch(
            "qbittorrent_agent.auth.QbittorrentApi",
            side_effect=UnauthorizedError("auth error"),
        ):
            with pytest.raises(RuntimeError) as exc_info:
                get_client()
            assert "AUTHENTICATION ERROR" in str(exc_info.value)


@patch.dict(
    "os.environ",
    {
        "QBITTORRENT_URL": "https://service.invalid",
        "QBITTORRENT_USERNAME": "user",
        "QBITTORRENT_PASSWORD": "secret",
    },
)
def test_auth_get_client_success():
    """Verify successful client retrieval and singleton caching.

    CONCEPT:AU-OS.governance.reactive-multi-axis-budget — Guardrail Engine / Session Concurrency
    """
    with patch("qbittorrent_agent.auth._client", None):
        with patch("qbittorrent_agent.auth.QbittorrentApi"):
            client = get_client()
            assert client is not None
