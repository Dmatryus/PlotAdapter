import copy

from pathlib import Path
from typing import Union
import pandas as pd
import matplotlib.pyplot as plt

try:
    from .base import Backend, BackendPlot
except:
    from base import Backend, BackendPlot


class MatplotlibPlot(BackendPlot):
    def __init__(self, fig, axs, plot_type: str):
        self.fig = fig
        self.axs = axs
        self.plot_type = plot_type

    def show(self):
        self.fig.show()

    def to_file(self, file_path: Union[str, Path]):
        self.fig.savefig(str(file_path))

    def refresh_style(self):
        self.axs.legend()

    def get_data(self):
        if self.plot_type == "line":
            lines_data = [
                pd.DataFrame(
                    {
                        self.axs.get_xlabel(): l.get_xdata(),
                        l.get_label(): l.get_ydata(),
                    }
                ).set_index(self.axs.get_xlabel())
                for l in self.axs.get_lines()
            ]
            result = lines_data[0]
            for l in lines_data[1:]:
                result = result.join(l, how="outer")
            return result


class MatplotlibBackend(Backend):
    name = "matplotlib_backend"

    @staticmethod
    def get_plot(data: pd.DataFrame, plot_type: str) -> MatplotlibPlot:
        fig, axs = plt.subplots()
        axs.set_xlabel(data.index.name)
        if plot_type == "line":
            for f in data.columns:
                axs.plot(data.index, data[f], label=f)
            axs.legend()
        return MatplotlibPlot(fig, axs, plot_type)

    @staticmethod
    def sum(plot1: MatplotlibPlot, plot2: MatplotlibPlot) -> MatplotlibPlot:
        result = copy.deepcopy(plot1)
        for line in plot2.axs.get_lines():
            result.axs.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
        result.refresh_style()
        return result
