import numpy as np
import random


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


dummy_model = ScoringModel()
