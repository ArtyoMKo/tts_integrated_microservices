import unittest
from unittest.mock import Mock, patch
from pulsar_provider import PulsarProvider, Producer, Consumer


class TestPulsarProvider(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.provider = PulsarProvider()
        self.provider.client = self.mock_client

    def test_create_producer(self):
        mock_producer = Mock(spec=Producer)
        self.mock_client.create_producer.return_value = mock_producer

        topic = "test-topic"
        schema = Mock()
        batching_enabled = True

        producer = self.provider.create_producer(topic, schema, batching_enabled)

        self.mock_client.create_producer.assert_called_once_with(
            topic, schema=schema, batching_enabled=batching_enabled
        )
        self.assertEqual(producer, mock_producer)

    def test_create_consumer(self):
        mock_consumer = Mock(spec=Consumer)
        self.mock_client.subscribe.return_value = mock_consumer

        topic = "test-topic"
        subscription_name = "test-subscription"

        consumer = self.provider.create_consumer(topic, subscription_name)

        self.mock_client.subscribe.assert_called_once_with(
            topic, subscription_name=subscription_name
        )
        self.assertEqual(consumer, mock_consumer)

    def test_send_callback(self):
        pass

    @patch.object(PulsarProvider, "__del__")
    def test_destructor(self, mock_del):
        self.provider.__del__()
        mock_del.assert_called_once()
