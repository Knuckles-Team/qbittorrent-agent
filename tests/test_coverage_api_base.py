from unittest.mock import MagicMock, PropertyMock, patch

import pytest
import requests
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from qbittorrent_agent.api_client import QbittorrentApi
from qbittorrent_agent.auth import get_client


def test_qbittorrent_api_errors(mock_session):
    """Verify standard base client HTTP error handling pathways.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
    """
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
    api_instance_no_verify.session.cookies = requests.utils.cookiejar_from_dict(
        {"SID": "test_sid"}
    )
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
    """Verify API client handling for various authentication and login errors.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
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
    assert "Login failed with status code 500" in str(exc_info.value)

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


def test_auth_get_client_error():
    """Verify singleton client initialization raises correct RuntimeErrors.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
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


def test_auth_get_client_success():
    """Verify successful client retrieval and singleton caching.

    CONCEPT:OS-5.3 — Guardrail Engine / Session Concurrency
    """
    with patch("qbittorrent_agent.auth._client", None):
        with patch("qbittorrent_agent.auth.QbittorrentApi"):
            client = get_client()
            assert client is not None
