import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, MagicMock, patch


pulsar_provider_mock = MagicMock()
producer_mock = MagicMock()
pulsar_provider_mock.return_value.create_producer.return_value = producer_mock

with patch("pulsar_provider.PulsarProvider", pulsar_provider_mock):
    from tts_api.routers.text import router


@pytest.fixture
def client():
    return TestClient(router)


@patch("pulsar_provider.PulsarProvider")
def test_send_text_success(mock_pulsar_provider, client):
    mock_producer = Mock()
    mock_pulsar_provider.return_value.create_producer.return_value = mock_producer

    response = client.post("/text/", json={"text": "You are awesome !"})
    assert response.status_code == 201
    assert response.json() == "You are awesome !"
