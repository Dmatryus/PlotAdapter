try:
   from .base import Backend, BackendPlot
except:
   from base import Backend, BackendPlot

from pathlib import Path
from typing import Union
import pandas as pd
import matplotlib.pyplot as plt

class MatplotlibPlot(BackendPlot):
   def __init__(self, fig, axs):
      self.fig = fig
      self.axs = axs

   def show(self):
      self.fig.show()

   def to_file(self, file_path: Union[str, Path]):
      self.fig.savefig(str(file_path))


class MatplotlibBackend(Backend):
   name = "matplotlib_backend"

   @staticmethod
   def get_plot(data: pd.DataFrame, plot_type: str) -> MatplotlibPlot:
      fig, axs = plt.subplots()
      if plot_type == "line":
         for f in data.columns:
            axs.plot(data.index, data[f], label=f)
         axs.legend()
         return MatplotlibPlot(fig, axs)