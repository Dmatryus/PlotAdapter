try:
   from .base import Backend, BackendPlot
except:
   from base import Backend, BackendPlot

from pathlib import Path
from typing import Union
import pandas as pd
import plotly.express as px

class PlotlyPlot(BackendPlot):
   def __init__(self, fig):
      self.fig = fig

   def show(self):
      self.fig.show()

   def to_file(self, file_path: Union[str, Path], **kwargs):
      file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
      if file_path.suffix == ".html":
         self.fig.write_html(str(file_path), **kwargs)
      elif file_path.suffix == ".json":
         self.fig.write_json(str(file_path), **kwargs)
      else:
         self.fig.write_image(str(file_path), format=file_path.suffix[1:], **kwargs)


class PlotlyBackend(Backend):
   name = "plotly_backend"

   @staticmethod
   def get_plot(data: pd.DataFrame, plot_type: str) -> PlotlyPlot:
      if plot_type == "line":
         fig = px.line(data)
         return PlotlyPlot(fig)