from pulsar import Client
from pulsar.schema import BytesSchema


class PulsarProvider:
    def __init__(self, host='pulsar://localhost:6650'):
        self.client = Client(host)

    def create_producer(self, topic, schema=BytesSchema(), batching_enabled=False):
        """

        :param topic: topic name
        :param schema: pulsar topic schema
        :param batching_enabled: messages batching enabled
        :return pulsar.Client.producer
        """
        producer = self.client.create_producer(
            topic,
            schema=schema,
            batching_enabled=batching_enabled
        )
        return producer

    def create_consumer(self, topic, subscription_name='my-sub'):
        """

        :param topic: topic name
        :param subscription_name: subscription name
        :return pulsar.Client.subscribe
        """
        consumer = self.client.subscribe(topic, subscription_name=subscription_name)
        return consumer

    def __del__(self):
        self.client.close()

    def send_callback(res, msg_id, args):
        pass
