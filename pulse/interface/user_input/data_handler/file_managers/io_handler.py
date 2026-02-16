from abc import ABC, abstractmethod
from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedFile


class IOHandler(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, file_path: str) -> ImportedFile:
        pass
    
    def save(self):
        pass

