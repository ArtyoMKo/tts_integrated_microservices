import pytest
import torch
from unittest.mock import MagicMock
from vits_provider import VitsProvider, get_text


# VP = VitsProvider()

@pytest.mark.skip(reason="Test disabled for GitHub Actions")
def get_vp():
    return VitsProvider()


VP = get_vp()


def test_transform_tts():
    text = "test"
    result = VP.transform_tts(text)
    assert isinstance(result, dict)
    assert "audio" in result
    assert "sampling_rate" in result


def test_get_text():
    hparams = MagicMock()
    hparams.data.text_cleaners = ["english_cleaners2"]
    text = "test"
    result = get_text(text, hparams)
    assert isinstance(result, torch.Tensor)
