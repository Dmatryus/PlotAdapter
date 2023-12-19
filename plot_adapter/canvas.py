from abc import ABC
from typing import List

from pathlib import Path

from plot import Plot

class Layout(ABC):
    pass


class VerticalLayout(Layout):
    pass


class Canvas:
    def __init__(
        self,
        layout: Layout = None,
        width: int = None,
        height: int = None,
        init_plots: List[Plot] = None,
        style: Style =  None,
        backend: str = None
    ):
        self.layout = layout or VerticalLayout()
        self.width = width
        self.height = height
        self.init_plots = init_plots or []
        self.backend = None
        self.needs_rebuild = True

    def add_plot(self, plot):
        self.init_plots.append(plot)

    def show(self, rebuild=False):
        pass

    def  to_file(self,  file_path: Union[str, Path],  rebuild=False):
        pass
