from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

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


class Plot:
    plot_type = None

    def __init__(
        self,
        backend: Union[str, Backend] = "matplotlib",
        style: Style = None,
    ):
        self.backend = backend_selector(backend)
        self.backend_obj: BackendPlot = None
        self.style = style
        self.cache = None

    def build(self, data, **kwargs):
        self.plot_type = kwargs.get("plot_type", self.plot_type)
        self.backend = backend_selector(kwargs.get("backend", self.backend))
        self.backend_obj = self.backend.get_plot(data, self.plot_type)

    def show(self):
        self.backend_obj.show()

    def to_file(self, file_path: Union[str, Path]):
        self.backend_obj.to_file(file_path)

class LinePlot(Plot):
    plot_type = "line"