from typing import override
from numpy import ndarray
from augmenter.BaseAugmenter import BaseAugmenter


class StatisticColorCorrector(BaseAugmenter):
    def __init__(self, source_pic: ndarray):
        super().__init__()
        self.source_pic = source_pic

    @override
    def apply(self, pic: ndarray) -> ndarray:
        Esource = self.source_pic.mean()
        Etarget = pic.mean()

        Dsource = self.source_pic.std()
        Dtarget = pic.std()

        for i in range(pic.shape[0]):
            for j in range(pic.shape[1]):
                pic[i, j] = max(1, Esource + (pic[i, j] - Etarget) * Dsource / Dtarget)

        return pic