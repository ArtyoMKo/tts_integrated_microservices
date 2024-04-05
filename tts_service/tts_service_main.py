# pylint: disable=unused-argument
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import signal
import json
import sys

from vits_provider import VitsProvider
from pulsar_provider import PulsarProvider, Producer

MAX_WORKERS = 2


def signal_handler(sig: int, frame):
    """
    Signal handler to gracefully exit the program.

    :param sig: Signal number.
    :param frame: Signal frame.
    """
    print("Exiting gracefully...")
    sys.exit(0)


def transform_produce(text_message: str, producer: Producer, tts_vits_provider) -> None:
    """
    Transforms text message to audio data and sends it asynchronously.

    :param text_message: The text message to transform.
    :param producer: The Pulsar producer instance.
    :param tts_vits_provider: The VitsProvider instance.
    """
    audio_data = tts_vits_provider.transform_tts(text_message)
    producer.send_async(
        json.dumps(audio_data).encode("utf-8"), PulsarProvider.send_callback
    )


def tts_handler_subprocess(process_ind: int):
    """
    Defines a single process for handling Pulsar consumer and producer.

    :param process_ind: The process index.
    """
    tts_vits_provider = VitsProvider()

    tts_pulsar_provider = PulsarProvider()
    tts_audio_consumer = tts_pulsar_provider.create_consumer(
        "row_text", subscription_name=f"my_sub_{process_ind}"
    )
    tts_audio_producer = tts_pulsar_provider.create_producer("row_audio")

    while True:
        msg = tts_audio_consumer.receive()
        msg_batch_decoded = msg.value().decode()
        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:  # Todo: replace ThreadPoolExecutor with Process ... for cloud microservice solution  # pylint: disable=line-too-long, fixme
            if not isinstance(msg_batch_decoded, list):
                msg_batch_decoded = [msg_batch_decoded]
            futures = [
                executor.submit(transform_produce, message, tts_audio_producer, tts_vits_provider)
                for message in msg_batch_decoded
            ]
            _ = [future.result() for future in futures if future.result()]

        tts_audio_producer.flush()
        _ = [tts_audio_consumer.acknowledge(message) for message in msg_batch_decoded]


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    processes = [
        multiprocessing.Process(target=tts_handler_subprocess, args=(i,))
        for i in range(MAX_WORKERS)
    ]  # Todo: make adaptive !  # pylint: disable=fixme
    _ = [p.start() for p in processes]
    _ = [p.join() for p in processes]
