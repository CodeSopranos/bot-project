import random
import numpy as np
from scipy.special import softmax

import onnx
import onnxruntime
import torchaudio


class ScoringModel:
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
    def __init__(self, model_path, samples_path):
        self.model = onnxruntime.InferenceSession(model_path)
        self.class_names = ["American 🇺🇸", "Canadian 🇨🇦", "English 🇬🇧", "Scottish 🏴󠁧󠁢󠁳󠁣󠁴󠁿"]
        f = open(samples_path, 'r')
        self.samples = f.read().split('\n')
        self.template = lambda i, item: f"{i}. {item[0]:<12} {round(item[1] * 100)}%"

    def get_sample(self):
        """Get random sample to dictate"""
        return random.choice(self.samples)

    def predict(self, filename_path):
        fbank = self.wav2fbank(filename_path)
        ort_inputs = {self.model.get_inputs()[0].name: fbank}
        class_logits = self.model.run(None, ort_inputs)[0][0].tolist()
        class_probs = softmax(class_logits)
        result = {label: prob for label, prob in zip(self.class_names, class_probs)}
        score = self.get_score(result)
        prettified = [self.template(i + 1, item) for i, item in
                      enumerate(sorted(result.items(), key=lambda x: x[1], reverse=True))]
        result['pretty_print'] = '\n\n'.join(prettified)
        result['score'] = score
        return result

    @staticmethod
    def get_score(class2probs):
        eng_impact = 0.7 * 100 * class2probs["English 🇬🇧"]
        us_impact = 0.3 * 100 * class2probs["American 🇺🇸"]
        return round(eng_impact + us_impact)

    @staticmethod
    def wav2fbank(filename):
        waveform, sr = torchaudio.load(filename)
        waveform = waveform - waveform.mean()
        fbank = torchaudio.compliance.kaldi.fbank(waveform, htk_compat=True,
                                                  sample_frequency=sr, use_energy=False,
                                                  window_type='hanning', num_mel_bins=128, dither=0.0,
                                                  frame_shift=10)
        fbank = fbank.cpu().numpy()
        target_length = 256
        n_frames = fbank.shape[0]

        p = target_length - n_frames

        if p > 0:
            fbank = np.pad(fbank, [(0, p), (0, 0)])
        elif p < 0:
            fbank = fbank[0:target_length, :]
        norm_mean = -4.71
        norm_std = 4.93
        fbank = (fbank - norm_mean) / (norm_std * 2)
        fbank = np.expand_dims(fbank, axis=0)
        return fbank


dummy_model = ScoringModel()

accent_model = AccentModel(model_path='models/accent_model.onnx',
                           samples_path='models/phrases.txt')
