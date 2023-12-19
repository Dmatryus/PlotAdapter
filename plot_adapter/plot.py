from abc import ABC, abstractmethod


class Plot(ABC):
    def __init__(
        self,
        width: int = None,
        height: int = None,
        backend: Backend = None,
        style: Style = None,
    ):
        self.width = width
        self.height = height
        self.backend = backend
        self.style = style
        self.cache = None

    def _build(self, **kwargs):
        pass

    def show(self, rebuild=False):
        pass

    def to_file(self, file_path: Union[str, Path], rebuild=False):
        pass
