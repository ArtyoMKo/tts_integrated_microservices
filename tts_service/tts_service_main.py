from concurrent.futures import ProcessPoolExecutor
import logging
import signal
import json
import sys

from vits_provider import VitsProvider
from pulsar_provider import PulsarProvider, Producer


def signal_handler(sig, frame):
    """
    Signal handler to gracefully exit the program.

    :param sig: Signal number.
    :param frame: Signal frame.
    """
    print("Exiting gracefully...")
    sys.exit(0)


def single_process(text_message: str, producer: Producer) -> None:
    audio_data = tts_vits_provider.transform_tts(text_message)
    producer.send_async(json.dumps(audio_data), PulsarProvider.send_callback)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    tts_pulsar_provider = PulsarProvider()
    tts_audio_consumer = tts_pulsar_provider.create_consumer('row_text')
    tts_audio_producer = tts_pulsar_provider.create_producer('row_audio')

    tts_vits_provider = VitsProvider()

    with ProcessPoolExecutor(max_workers=2) as executor:
        try:
            while True:
                msg = tts_audio_consumer.receive()
                executor.submit(single_process, msg, tts_audio_producer)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupting ...")
            sys.exit(0)
