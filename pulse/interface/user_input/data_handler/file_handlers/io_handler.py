from abc import ABC, abstractmethod
from pulse.interface.user_input.data_handler.imported_data import ImportedData

from pathlib import Path


class IOHandler(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, file_path: str | Path) -> ImportedData:
        pass
    
    def save(self):
        pass