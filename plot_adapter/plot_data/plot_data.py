from .base import BasePlotData
from .pandas_data import PandasPlotData
import pandas as pd

def backend_selector(data, **kwargs):
    if isinstance(data, pd.DataFrame):
        return PandasPlotData(data, **kwargs)

class PlotData(BasePlotData):
    def __init__(self, data, copy_mode: bool = True):
        super().__init__(data, copy_mode=copy_mode)
        self._backend = backend_selector(data, copy_mode=copy_mode)

    def __add__(self, other):
        return self._backend.__add__(other)

    def __getitem__(self, idx):
        return self._backend.__getitem__(idx)

    def __setitem__(self, idx, value):
        self._backend.__setitem__(idx, value)

    @property
    def index(self):
        return self._backend.index
    
    @property
    def columns(self):
        return self._backend.columns