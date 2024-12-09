from typing import override

from numpy import ndarray
import numpy as np

from augmenter.BaseAugmenter import BaseAugmenter
from augmenter.utils import expand_pic


class DenoiserBlur(BaseAugmenter):
    def __init__(self, half_kernel_size: int = 10):
        self._half_kernel_size = half_kernel_size

    @override
    def apply(self, pic: ndarray) -> ndarray:
        if self._half_kernel_size > min(pic.shape) - 1:
            self._half_kernel_size = min(pic.shape) - 1

        expanded_pic = expand_pic(pic, self._half_kernel_size)
        ret_pic = np.zeros_like(pic)
        for i in range(self._half_kernel_size, expanded_pic.shape[0] - self._half_kernel_size):
            for j in range(self._half_kernel_size, expanded_pic.shape[1] - self._half_kernel_size):
                ret_pic[i - self._half_kernel_size][j - self._half_kernel_size] = expanded_pic[i - self._half_kernel_size:i + self._half_kernel_size + 1, j - self._half_kernel_size:j + self._half_kernel_size + 1].mean()
        return ret_pic
