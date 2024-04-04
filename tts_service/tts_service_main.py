from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import signal
import json
import sys

from vits_provider import VitsProvider
from pulsar_provider import PulsarProvider, Producer

MAX_WORKERS = 2


def signal_handler(sig, frame):
    """
    Signal handler to gracefully exit the program.

    :param sig: Signal number.
    :param frame: Signal frame.
    """
    print("Exiting gracefully...")
    sys.exit(0)


def transform_produce(text_message: str, producer: Producer, vp) -> None:
    audio_data = vp.transform_tts(text_message)
    producer.send_async(json.dumps(audio_data), PulsarProvider.send_callback)


def single_process_tmp(n):
    vp = VitsProvider()

    tts_pulsar_provider = PulsarProvider()
    tts_audio_consumer = tts_pulsar_provider.create_consumer('row_text', subscription_name=f"my_sub_{n}")
    tts_audio_producer = tts_pulsar_provider.create_producer('row_audio')

    while True:
        msg = tts_audio_consumer.receive()
        msg_batch_decoded = msg.value().decode()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:  # Todo: replace ThreadPoolExecutor with Process ... for cloud microservice solution
            if type(msg_decoded) != list:
                msg_decoded = [msg_decoded]
            futures = [
                executor.submit(transform_produce, message, tts_audio_producer, vp) for message in msg_batch_decoded
            ]
            results = [future.result() for future in futures if future.result()]


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    tts_vits_provider = VitsProvider()

    processes = [multiprocessing.Process(target=single_process_tmp, args=(i,)) for i in range(MAX_WORKERS)]  # Todo: make adaptive !
    [p.start() for p in processes]
    [p.join() for p in processes]
