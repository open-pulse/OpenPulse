from PySide6.QtWidgets import QFileDialog

import platform
from pathlib import Path


class FileDialogService:

    @staticmethod
    def open_file(file_extensions: list[str], caption: str = "Open file", last_folder: str = None) -> Path | None:

        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        path, selected_filter = QFileDialog.getOpenFileName(
            None,
            caption,
            str(last_folder),
            filter_str,
            **kwargs
        )

        if not path:
            return None
        
        path = Path(path)

        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        return path
       
    @staticmethod
    def open_multiple_files(file_extensions: list[str], caption: str = "Open multiple files", last_folder: str = None) -> list[Path] | None:
            
        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        paths, selected_filter = QFileDialog.getOpenFileNames(
            None,
            caption,
            str(last_folder),
            filter_str,
            **kwargs
        )

        if not paths:
            return None
        
        paths = [Path(path) for path in paths]
        
        for i, path in enumerate(paths):
            if not path.suffix:
                suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
                paths[i] = path.with_suffix(suffix)

        return paths

    @staticmethod
    def save_file(file_extensions: list[str], caption: str = "Save file", last_folder: str = None)-> Path | None:
        
        last_folder, caption, filter_str, kwargs = (
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        path, selected_filter = QFileDialog.getSaveFileName(
            None,
            caption,
            str(last_folder),
            filter_str,
            **kwargs
        )

        if not path:
            return None
        
        path = Path(path)
        
        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        return path
    
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

        filter_str = FileDialogService._generate_file_extensions_str(file_extensions)

        return last_folder, caption, filter_str, kwargs
    
    @staticmethod
    def _generate_file_extensions_str(file_extensions: list[str]):
        str_extensions = "Files ("
        for extension in file_extensions:
            str_extensions += "*."
            str_extensions += extension
            str_extensions += " "
        
        str_extensions = str_extensions.strip()
        str_extensions += ")"

        return str_extensions
    
    @staticmethod
    def _get_path_extension(string: str) -> str:
        return string.split(".")[1][:-1]
