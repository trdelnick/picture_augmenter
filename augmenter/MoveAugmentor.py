from typing import override
from numpy import ndarray

from augmenter.BaseAugmenter import BaseAugmenter
from enum import Enum
import numpy as np


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
class FillingRule(Enum):
    FILL_BLACK = 1,
    FILL_LOOP = 2


class MoveAugmentor(BaseAugmenter):
    def __init__(self, how_many_pix: int, direction: Direction, filling_rule: FillingRule):
        super().__init__()
        self.direction = direction
        self.filling = filling_rule
        self.how_many_pix = how_many_pix

    @override
    def apply(self, pic: ndarray) -> ndarray:
        if self.how_many_pix > min(pic.shape):
            raise RuntimeError("Размер сдвига превышает размер изображения")

        if self.direction == Direction.RIGHT:
            if self.filling == FillingRule.FILL_BLACK:
                pic = pic[:, :-self.how_many_pix]
                a = np.concat( (np.zeros((pic.shape[0], self.how_many_pix)), pic), axis=1)
                return a
            elif self.filling == FillingRule.FILL_LOOP:
                a = np.concat( (pic[:, -self.how_many_pix:], pic[:, :-self.how_many_pix]), axis=1)
                return a
            else:
                raise NotImplementedError("Операция не поддерживается")
        elif self.direction == Direction.LEFT:
            if self.filling == FillingRule.FILL_BLACK:
                pic = pic[:, self.how_many_pix:]
                a = np.concat( (pic, np.zeros((pic.shape[0], self.how_many_pix))), axis=1)
                return a
            elif self.filling == FillingRule.FILL_LOOP:
                a = np.concat( (pic[:, self.how_many_pix:], pic[:, :self.how_many_pix]), axis=1)
                return a
            else:
                raise NotImplementedError("Операция не поддерживается")
        elif self.direction == Direction.DOWN:
            if self.filling == FillingRule.FILL_BLACK:
                pic = pic[:-self.how_many_pix, :]
                a = np.concat( (np.zeros((self.how_many_pix, pic.shape[1])), pic), axis=0)
                return a
            elif self.filling == FillingRule.FILL_LOOP:
                a = np.concat( (pic[-self.how_many_pix:, :],pic[:-self.how_many_pix, :]), axis=0)
                return a
            else:
                raise NotImplementedError("Операция не поддерживается")
        elif self.direction == Direction.UP:
            if self.filling == FillingRule.FILL_BLACK:
                pic = pic[self.how_many_pix:, :]
                a = np.concat( (pic, np.zeros((self.how_many_pix, pic.shape[1]))), axis=0)
                return a
            elif self.filling == FillingRule.FILL_LOOP:
                a = np.concat( (pic[self.how_many_pix:, :], pic[:self.how_many_pix, :]), axis=0)
                return a
            else:
                raise NotImplementedError("Операция не поддерживается")
        else:
            raise NotImplementedError("Операция не поддерживается")

