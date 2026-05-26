import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_session():
    """Mock the requests.Session to return deterministic, successful HTTP responses."""
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
