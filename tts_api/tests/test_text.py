import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from unittest.mock import MagicMock, patch

# Mock Pulsar before importing routes
pulsar_provider_mock = MagicMock()
producer_mock = MagicMock()
pulsar_provider_mock.return_value.create_producer.return_value = producer_mock

# Patch the PulsarProvider in the module where routes are defined
with patch('pulsar_provider.PulsarProvider', pulsar_provider_mock):
    # Now import the routes module after patching
    from tts_api.routers.text import router, TextRequest, send_text


@pytest.fixture
def client():
    return TestClient(router)


@patch('pulsar_provider.PulsarProvider')
def test_send_text_success(mock_pulsar_provider, client):
    mock_producer = Mock()
    mock_pulsar_provider.return_value.create_producer.return_value = mock_producer

    response = client.post("/text/", json={"text": "You are awesome !"})
    assert response.status_code == 201
    assert response.json() == "You are awesome !"
