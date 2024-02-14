from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
import copy

import pandas as pd
import numpy as np

from backends.base import Backend, BackendPlot
from backends.matplotlib import MatplotlibBackend
from backends.plotly import PlotlyBackend
from plot_data.plot_data import PlotData
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
    plot_data: PlotData = None

    def __init__(
        self,
        backend: Union[str, Backend] = "matplotlib",
        backend_obj: BackendPlot = None,
        copy_mode: bool = False,
        style: Style = None,
    ):
        self.backend = backend_selector(backend)
        self.backend_obj: BackendPlot = backend_obj
        self.copy_mode = copy_mode
        self.style = style

    def build(self, data: pd.DataFrame, **kwargs):
        self.plot_data = PlotData(data, copy_mode=self.copy_mode)
        self.plot_type = kwargs.get("plot_type", self.plot_type)
        self.backend = backend_selector(kwargs.get("backend", self.backend))
        self.backend_obj = self.backend.get_plot(self.plot_data, self.plot_type)

    def show(self):
        self.backend_obj.show()

    def to_file(self, file_path: Union[str, Path]):
        self.backend_obj.to_file(file_path)

    def __add__(self, other):
        result = copy.deepcopy(self) if self.copy_mode else self
        self.plot_data += other.plot_data
        result.build(result.plot_data)
        return result

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
