from typing import override

from numpy import ndarray

from augmenter.BaseAugmenter import BaseAugmenter


class Equalizer(BaseAugmenter):
    def __init__(self):
        super().__init__()

    @override
    def apply(self, pic: ndarray) -> ndarray:
        max_light = 256
        histo = [0 for i in range(max_light)]

        for i in range(max_light):
            histo[i] = 0
        for i in range(pic.shape[0]):
            for j in range(pic.shape[1]):
                histo[pic[i, j]] += 1
        for i in range(max_light):
            histo[i] /= (pic.shape[0] * pic.shape[1])

        for i in range(1, max_light):
            histo[i] += histo[i - 1]
        for i in range(pic.shape[0]):
            for j in range(pic.shape[1]):
                pic[i, j] = histo[pic[i, j]] * 255

        return pic