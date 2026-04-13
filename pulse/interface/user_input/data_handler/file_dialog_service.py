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
            FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder, open_file=False)
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
        last_folder: str | None,
        open_file = True
    ):
        if last_folder is None:
            last_folder = Path().home()

        kwargs = {}
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        filter_str = FileDialogService._generate_file_extensions_str(file_extensions, open_file)

        return last_folder, caption, filter_str, kwargs
    
    @staticmethod
    def _generate_file_extensions_str(file_extensions: list[str], all_files=True):
        extensions_control = ";;".join(f"{ext.upper()} Files (*.{ext.lower()})" for ext in file_extensions)

        if not all_files:
            return extensions_control

        all_files_string = f"All files ({' '.join(f'*.{ext}' for ext in file_extensions)});;"

        return all_files_string + extensions_control
    
    @staticmethod
    def _get_path_extension(string: str) -> str:
        return string.split("*.")[-1].rstrip(")")
    
    @staticmethod
    def get_existing_directory(caption: str, directory: str | Path) -> Path | None:
        existing_dir = QFileDialog.getExistingDirectory(caption=caption, dir=str(directory))
        existing_dir = Path(existing_dir)

        if existing_dir.exists():
            return existing_dir



