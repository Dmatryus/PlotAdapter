from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
import copy

import pandas as pd
import numpy as np

from backends.base import Backend, BackendPlot
from backends.matplotlib import MatplotlibBackend
from backends.plotly import PlotlyBackend
from style import Style

def backend_selector(backend: Union[str, Backend]):
    if isinstance(backend, Backend):
        return backend
    if backend == "matplotlib":
        return MatplotlibBackend()
    elif backend == "plotly":
        return PlotlyBackend()
    else:
        raise ValueError(f"Backend {backend} not supported")


class Plot(ABC):
    plot_type = None
    plot_data = {}

    def __init__(
        self,
        backend: Union[str, Backend] = "matplotlib",
        backend_obj: BackendPlot = None,
        style: Style = None,
    ):
        self.backend = backend_selector(backend)
        self.backend_obj: BackendPlot = backend_obj
        self.style = style

    def build(self, data: pd.DataFrame, **kwargs):
        self.plot_type = kwargs.get("plot_type", self.plot_type)
        self.backend = backend_selector(kwargs.get("backend", self.backend))
        self.backend_obj = self.backend.get_plot(data, self.plot_type)
        self.plot_data = self.backend_obj.get_data()
    def show(self):
        self.backend_obj.show()

    def to_file(self, file_path: Union[str, Path]):
        self.backend_obj.to_file(file_path)

    def __add__(self, other):
        result = copy.deepcopy(self)
        result.backend_obj = result.backend.sum(result.backend_obj, other.backend_obj)
        result.plot_data = result.backend_obj.get_data()
        return result

    # def 

    def rebuild(self):
        pass

class LinePlot(Plot):
    plot_type = "line"
    linear_functions = {}

    def build_linear_trend(self, data: pd.DataFrame, **kwargs):
        linear_data = {
            data.index.name: data.index
        }

        for c in data.columns:
            y = data[c].values.reshape(1, -1)[0]
            x_is_time = isinstance(data.index, DatetimeIndex)
            x = (
                [t.timestamp() for t in data.index]
                if x_is_time
                else data.index
            )
            lr_function = np.poly1d(np.polyfit(x, y, 1))
            self.linear_functions[c] = lr_function
            linear_data[c] = lr_function(x)

        result = pd.DataFrame(result).set_index(data.index.name).sort_index()
