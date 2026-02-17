from PySide6.QtWidgets import QFileDialog

import platform
from pathlib import Path


class FileDialogService:

    @staticmethod
    def open_file(file_extensions: list[str], caption: str = "Open file", last_folder: str = None) -> Path:

        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        path, _ = QFileDialog.getOpenFileName(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )

        return Path(path)
       
    @staticmethod
    def open_multiple_files(file_extensions: list[str], caption: str = "Open multiple files", last_folder: str = None) -> list[Path]:
            
        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        paths, _ = QFileDialog.getOpenFileNames(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )

        return [Path(path) for path in paths]

    @staticmethod
    def save_file(file_extensions: list[str], caption: str = "Save file", last_folder: str = None)-> Path:
        
        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        path, _ = QFileDialog.getSaveFileName(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )

        return Path(path)
    
    @staticmethod
    def _build_dialog_kwargs(
        file_extensions: list[str],
        caption: str,
        last_folder: str | None
    ):
        if last_folder is None:
            last_folder = Path().home()

        kwargs = {}
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        filter_str = FileDialogService.generate_file_extensions_str(file_extensions)

        return last_folder, caption, filter_str, kwargs
    
    @staticmethod
    def generate_file_extensions_str(file_extensions: list[str]):
        str_extensions = "Files ("
        for extension in file_extensions:
            str_extensions += "*."
            str_extensions += extension
            str_extensions += " "
        
        str_extensions = str_extensions.strip()
        str_extensions += ")"

        return str_extensions