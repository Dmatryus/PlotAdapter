from abc import ABC, abstractmethod, abstractproperty
import copy

class BasePlotData(ABC):
    def _get_data(self, data):
        return copy.deepcopy(data) if self.copy_mode else data
    
    def __init__(self, data, copy_mode: bool = True):
        self.copy_mode = copy_mode
        self.data = self._get_data(data)

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, idx):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, idx, value):
        raise NotImplementedError

    @abstractproperty
    def index(self):
        raise NotImplementedError

    @abstractproperty
    def columns(self):
        raise NotImplementedError
        