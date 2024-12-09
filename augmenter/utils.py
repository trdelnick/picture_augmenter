from numpy import ndarray
import numpy as np

def expand_pic(pic: ndarray, border_size: int) -> ndarray:
    res = np.zeros((pic.shape[0] + border_size * 2, pic.shape[1] + border_size * 2))

    res[border_size:-border_size, border_size:-border_size] = pic.copy()

    res[border_size:-border_size, 0:border_size] = pic[:, 1:border_size + 1][:, ::-1]
    res[border_size:-border_size, -border_size - 1:] = pic[:, -border_size - 1:][:, ::-1]
    res[0:border_size, border_size:-border_size] = pic[1:border_size + 1, :][::-1]
    res[-border_size - 1:, border_size:-border_size] = pic[-border_size - 1:, :][::-1]

    res[0:border_size, 0:border_size] = pic[1:border_size + 1, 1:border_size + 1][::-1, ::-1]
    res[0:border_size, -border_size - 1:] = pic[1:border_size + 1, -border_size - 1:][::-1, ::-1]
    res[-border_size - 1:, 0:border_size] = pic[-border_size - 1:, 1:border_size + 1][::-1, ::-1]
    res[-border_size - 1:, -border_size - 1:] = pic[-border_size - 1:, -border_size - 1:][::-1, ::-1]

    return res