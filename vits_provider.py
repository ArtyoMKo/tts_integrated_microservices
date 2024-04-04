import torch
from typing import Dict

import vits.commons as commons
import vits.utils as utils
from vits.models import SynthesizerTrn
from vits.text.symbols import symbols
from vits.text import text_to_sequence


def get_text(text: str, hps: utils.HParams) -> torch.LongTensor:
    """
    Convert text into a sequence of integers.

    :param text: Input text.
    :param hps: Hyperparameters.
    :return: LongTensor representing the text sequence.
    """
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


class VitsProvider:
    def __init__(
            self,
            hparams_dir: str = "./vits/configs/ljs_base.json",
            pretrained_model_dir: str = "./vits/pretrained_models/pretrained_ljs.pth"
    ) -> None:
        """
        Initialize VitsProvider.

        :param hparams_dir: Directory containing hyperparameters configuration (default: "./vits/configs/ljs_base.json").
        :param pretrained_model_dir: Directory containing the pretrained model (default: "pretrained_models/
        pretrained_ljs.pth").
        """
        self.hps = utils.get_hparams_from_file(hparams_dir)
        hps = self.hps
        self.net_g = SynthesizerTrn(
            len(symbols),
            hps.data.filter_length // 2 + 1,
            hps.train.segment_size // hps.data.hop_length,
            **hps.model).cuda()
        _ = self.net_g.eval()

        _ = utils.load_checkpoint(pretrained_model_dir, self.net_g, None)

    def transform_tts(self, text: str) -> Dict[str, list]:
        """
        Transform text-to-speech.

        :param text: Input text.
        :return: Dictionary containing audio and sampling rate.
        """
        stn_tst = get_text(text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            audio = self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][
                0, 0].data.cpu().float().numpy()
        return {
            'audio': audio.tolist(),
            'sampling_rate': self.hps.data.sampling_rate
        }
