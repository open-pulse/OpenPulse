from abc import ABC, abstractmethod
from pathlib import Path

from pulse.interface.user_input.data_handler.imported_data import ImportedData


class IOHandler(ABC):

    @staticmethod
    @abstractmethod
    def read(self, file_path: str | Path) -> ImportedData:
        pass

    @staticmethod
    def save(self):
        pass