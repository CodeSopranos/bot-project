import random
import numpy as np
from scipy.special import softmax
from typing import List, Dict

import onnx
import onnxruntime
import torchaudio


class DummyModel:
    samples = ["\"London is the capital of Great Britain\"",
               "\"So Betty Botter bought a bit of better butter\"",
               "\"Freezy trees made these trees’ cheese freeze\"",
               "\"To be, or not to be, that is the question: whether 'tis nobler in the mind to suffer\"",
               ]

    def __init__(self):
        pass

    def predict(self, input=None):
        return np.random.randint(0, 100)

    def get_sample(self):
        return random.choice(self.samples)


class AccentModel:
    def __init__(self,
                 model_path: str,
                 samples_path: str,
                 lang_names: List[str],
                 benchmark_langs: List):
        self.model = onnxruntime.InferenceSession(model_path)
        self.lang_names = lang_names
        self.n_classes = len(self.lang_names)
        self.benchmark_langs = benchmark_langs
        f = open(samples_path, 'r')
        self.samples = f.read().split('\n')
        self.template = lambda i, item: f"{i}. {item[0]:<12} {round(item[1] * 100)}%"

    def get_sample(self):
        """Get random sample to dictate"""
        return random.choice(self.samples)

    def predict(self, filename_path, top_k: int = 6) -> Dict:
        fbanks = self.wav2fbank(filename_path)
        probs = np.zeros((self.n_classes,))
        for fbank in fbanks:
            ort_input = {self.model.get_inputs()[0].name: fbank}
            class_logits = self.model.run(None, ort_input)[0][0]
            probs += softmax(class_logits)
        probs = softmax(probs)
        result = {label: prob for label, prob in zip(self.lang_names, probs)}
        score = self.get_score(result)
        prettified = [self.template(i + 1, item) for i, item in
                      enumerate(sorted(result.items(), key=lambda x: x[1], reverse=True))]
        result['pretty_print'] = '\n\n'.join(prettified[: top_k])
        result['score'] = score
        return result

    def get_score(self, class2probs) -> int:
        score = 0
        for lang in self.benchmark_langs:
            score += lang['weight'] * class2probs[lang['label']] * 100
        return round(score)

    @staticmethod
    def wav2fbank(filename):
        waveform, sr = torchaudio.load(filename)
        waveform = waveform - waveform.mean()
        fbank_full = torchaudio.compliance.kaldi.fbank(waveform, htk_compat=True,
                                                       sample_frequency=sr, use_energy=False,
                                                       window_type='hanning', num_mel_bins=128, dither=0.0,
                                                       frame_shift=10)
        fbank_full = fbank_full.cpu().numpy()
        n_frames = fbank_full.shape[0]
        target_length = 256
        split_num = round(n_frames / target_length)
        fbanks = []
        for i in range(split_num):
            start = i * target_length
            end = start + target_length

            if end >= fbank_full.shape[0]:
                end = fbank_full.shape[0]

            fbank = fbank_full[start:end, :]
            n_frames = fbank.shape[0]
            p = target_length - n_frames

            if p > 0:
                fbank = np.pad(fbank, [(0, p), (0, 0)])
            elif p < 0:
                fbank = fbank[0:target_length, :]

            fbank = np.transpose(fbank, (1, 0))
            norm_mean = -5.719665
            norm_std = 4.3323016
            fbank = (fbank - norm_mean) / (norm_std * 2)
            fbank = np.expand_dims(fbank, axis=0)
            fbanks.append(fbank)
        return fbanks
