from vits_provider import VitsProvider
from pulsar_provider import PulsarProvider


if __name__ == '__main__':
    tts_pulsar_provider = PulsarProvider()
    tts_audio_consumer = tts_pulsar_provider.create_producer('row_text')
    tts_audio_producer = tts_pulsar_provider.create_producer('row_audio')

    tts_vits_provider = VitsProvider()