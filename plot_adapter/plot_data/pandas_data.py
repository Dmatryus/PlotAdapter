from .base import BasePlotData

import pandas as pd

class PandasPlotData(BasePlotData):
    def __init__(self, data:pd.DataFrame, copy_mode: bool = True):
        super().__init__(data, copy_mode=copy_mode)
    
    def __add__(self, other):
        result = copy.deepcopy(self) if self.copy_mode else self
        result.data = result.data.join(other.data, how="outer")
        return self

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    @property
    def index(self):
        return self.data.index

    @property
    def columns(self):
        return self.data.columns