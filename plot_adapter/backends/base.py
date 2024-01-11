from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

import pandas as pd

class BackendPlot(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def to_file(self, file_path: Union[str, Path]):
        pass

class Backend(ABC):
    pass

    @abstractmethod
    def get_plot(data: pd.DataFrame, plot_type: str) -> BackendPlot:
        pass