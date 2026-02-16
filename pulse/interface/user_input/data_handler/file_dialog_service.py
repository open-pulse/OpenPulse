from PySide6.QtWidgets import QFileDialog

import platform
import os


class FileDialogService:

    @staticmethod
    def open_file(file_extensions: list[str], caption: str = "Open file", last_folder: str = None):

        last_folder, caption, filter_str, kwargs = (
            FileDialogService.__build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        return QFileDialog.getOpenFileName(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )

       
    @staticmethod
    def open_multiple_files(file_extensions: list[str], caption: str = "Open multiple files", last_folder: str = None):
            
        last_folder, caption, filter_str, kwargs = (
            FileDialogService.__build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        return QFileDialog.getOpenFileNames(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )

    @staticmethod
    def save_file(file_extensions: list[str], caption: str = "Save file", last_folder: str = None):
        
        last_folder, caption, filter_str, kwargs = (
            FileDialogService.__build_dialog_kwargs(file_extensions, caption, last_folder)
        )

        return QFileDialog.getSaveFileName(
            None,
            caption,
            last_folder,
            filter_str,
            **kwargs
        )
    
    @staticmethod
    def __build_dialog_kwargs(
        file_extensions: list[str],
        caption: str,
        last_folder: str | None
    ):
        if last_folder is None:
            last_folder = os.path.expanduser("~")

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