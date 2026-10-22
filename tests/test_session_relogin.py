"""Session re-login behavior with a faked transport (no network)."""

import pytest
import requests
from agent_connector_sdk.exceptions import UnauthorizedError

from qbittorrent_agent.api.api_client_base import BaseApiClient


class FakeResponse:
    def __init__(self, status_code: int, body=None):
        self.status_code = status_code
        self._body = body
        self.text = ""

    def json(self):
        if self._body is None:
            raise ValueError("no body")
        return self._body


class FakeSession:
    """Scripted transport: login calls and API calls are recorded separately."""

    def __init__(self, api_statuses):
        self.cookies = requests.cookies.RequestsCookieJar()
        self.api_statuses = list(api_statuses)
        self.logins = 0
        self.api_calls = 0

    def post(self, url, **kwargs):
        if url.endswith("/auth/login"):
            self.logins += 1
            self.cookies.set("SID", "fake-session")
            return FakeResponse(200)
        return self._api()

    def get(self, url, **kwargs):
        return self._api()

    def _api(self):
        self.api_calls += 1
        status = self.api_statuses.pop(0)
        return FakeResponse(status, {"ok": True} if status == 200 else None)

    def close(self):
        pass


class FakeProfile:
    def __init__(self, session):
        self.session = session

    def configure_requests_session(self, _session):
        return self.session

    def cleanup(self):
        pass


def make_client(api_statuses):
    session = FakeSession(api_statuses)
    client = BaseApiClient(
        "https://qbit.invalid",
        username="user",
        password="pw",
        tls_profile=FakeProfile(session),
    )
    return client, session


@pytest.mark.spec("CONN-QBITTORRENT-AGENT-R001")
def test_expired_session_logs_in_again_and_retries_once():
    client, session = make_client([403, 200])
    assert session.logins == 1
    assert client._get("app/version") == {"ok": True}
    assert session.logins == 2
    assert session.api_calls == 2


@pytest.mark.spec("CONN-QBITTORRENT-AGENT-R001")
def test_second_consecutive_rejection_raises_without_looping():
    client, session = make_client([403, 403, 200])
    with pytest.raises(UnauthorizedError):
        client._get("app/version")
    assert session.logins == 2
    assert session.api_calls == 2


@pytest.mark.spec("CONN-QBITTORRENT-AGENT-R001")
def test_post_also_retries_on_401():
    client, session = make_client([401, 200])
    assert client._post("torrents/pause", data={"hashes": "all"}) == {"ok": True}
    assert session.logins == 2


@pytest.mark.spec("CONN-QBITTORRENT-AGENT-R003")
def test_public_operation_recovers_from_expired_session():
    from qbittorrent_agent.api_client import QbittorrentApi

    session = FakeSession([403, 200])
    api = QbittorrentApi(
        "https://qbit.invalid",
        username="user",
        password="pw",
        tls_profile=FakeProfile(session),
    )
    assert api.get_version() == {"ok": True}
    assert session.logins == 2
