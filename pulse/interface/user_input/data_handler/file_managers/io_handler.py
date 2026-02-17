from abc import ABC, abstractmethod
from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedData

from pathlib import Path


class IOHandler(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, file_path: str | Path) -> ImportedData:
        pass
    
    def save(self):
        pass

    def generate_extensions_string_for_error_message(self, extensions: list[str]) -> str:
        if not extensions:
            return ""

        if len(extensions) == 1:
            return extensions[0]

        return ", ".join(extensions[:-1]) + " or " + extensions[-1]

    def raise_extensions_error(self, file_path: str | Path, extensions: list[str]) -> ValueError:
        extensions_text = self.generate_extensions_string_for_error_message(extensions)
        file_path = Path(file_path)

        raise ValueError(
            f"Invalid suffix {file_path.suffix}. Use {extensions_text}"
        )