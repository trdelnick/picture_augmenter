from typing import override
from numpy import ndarray, identity
import cv2
from augmenter.BaseAugmenter import BaseAugmenter


class MotionBlur(BaseAugmenter):
    def __init__(self, pix: int):
        super().__init__()
        self.pix = pix

    @override
    def apply(self, pic: ndarray) -> ndarray:
        return cv2.filter2D(src=pic, ddepth=-1, kernel=identity(self.pix) / self.pix)
