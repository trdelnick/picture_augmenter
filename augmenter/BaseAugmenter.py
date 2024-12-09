from abc import abstractmethod, ABC
from numpy import ndarray

class BaseAugmenter(ABC):
    @abstractmethod
    def apply(self, pic: ndarray) -> ndarray: pass