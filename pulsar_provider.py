import logging
from pulsar import Client
from pulsar.schema import BytesSchema, Schema
from pulsar import Producer, Consumer


class PulsarProvider:
    def __init__(self, host: str = "pulsar://localhost:6650") -> None:
        """
        Initialize PulsarProvider with a Pulsar client.

        :param host: Pulsar service URL (default: pulsar://localhost:6650)
        """
        self.client = Client(host)

    def create_producer(
        self, topic: str, schema: Schema = BytesSchema(), batching_enabled: bool = False
    ) -> Producer:
        """
        Create a Pulsar producer for the given topic.

        :param topic: Name of the topic to produce messages to.
        :param schema: Schema used for serializing messages (default: BytesSchema).
        :param batching_enabled: Enable message batching (default: False).
        :return: Pulsar producer instance.
        """
        producer = self.client.create_producer(
            topic, schema=schema, batching_enabled=batching_enabled
        )
        return producer

    def create_consumer(
        self, topic: str, subscription_name: str = "my-sub"
    ) -> Consumer:
        """
        Create a Pulsar consumer for the given topic.

        :param topic: Name of the topic to consume messages from.
        :param subscription_name: Name of the subscription (default: 'my-sub').
        :return: Pulsar consumer instance.
        """
        consumer = self.client.subscribe(topic, subscription_name=subscription_name)
        return consumer

    def __del__(self) -> None:
        """
        Destructor to close the Pulsar client when the instance is deleted.
        """
        self.client.close()

    @staticmethod
    def send_callback(res, msg_id: str, *args: tuple):  # pylint: disable=unused-argument
        """
        Placeholder for a send callback function.

        :param res: Result of the send operation.
        :param msg_id: Message ID of the sent message.
        :param args: Additional arguments.
        """
        logging.debug(f"Message result -> {res}")
