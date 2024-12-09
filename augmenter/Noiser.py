from typing import override
from numpy import ndarray
from numpy.random import randn

from augmenter.BaseAugmenter import BaseAugmenter


class Noiser(BaseAugmenter):
    def __init__(self, deviation: float = 1):
        self.deviation = deviation

    @override
    def apply(self, pic: ndarray) -> ndarray:
        noise = self.deviation * randn(*pic.shape)
        return pic + noise