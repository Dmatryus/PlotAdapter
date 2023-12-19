from abc import ABC, abstractmethod
from typing import Iterable

class Styler(ABC):
    @abstractmethod
    def apply(self):
        pass

class Style(Styler):
    def __init__(stylers:  Iterable[Styler]):
        self.stylers = stylers

    def apply(self):
        for styler in self.stylers:
            styler.apply()