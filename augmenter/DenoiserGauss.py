import filecmp
from operator import length_hint
from typing import override

import numpy as np
from numpy import ndarray
from augmenter.BaseAugmenter import BaseAugmenter
from augmenter.utils import expand_pic


class DenoiserGauss(BaseAugmenter):
    def __init__(self, deviation: float = 1):
        self.deviation = deviation

    @override
    def apply(self, pic: ndarray) -> ndarray:
        border_size = int(np.round(self.deviation * 6, 0))
        if border_size > min(pic.shape) - 1:
            border_size = min(pic.shape)-1
        expanded_pic = expand_pic(pic, border_size)

        coefficient = 1/2/np.pi/self.deviation**2
        gauss_matrix = np.zeros((border_size*2+1, border_size*2+1))
        for i in range(border_size*2+1):
            for j in range(border_size*2+1):
                squared_length = (i-border_size)**2 + (j-border_size)**2
                gauss_matrix[i][j] = np.exp(-squared_length / 2 / self.deviation ** 2) * coefficient

        ret_pic = np.zeros_like(pic)
        for i in range(border_size, expanded_pic.shape[0] - border_size):
            for j in range(border_size, expanded_pic.shape[1] - border_size):
                ret_pic[i - border_size][j - border_size] = (gauss_matrix * expanded_pic[i - border_size:i + border_size + 1, j - border_size:j + border_size + 1]).sum()
        return ret_pic
