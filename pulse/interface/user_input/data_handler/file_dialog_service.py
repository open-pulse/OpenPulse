import platform
from collections import defaultdict
from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from pulse import app


class FileDialogService:
    @staticmethod
    def open_file(file_extensions: list[str], caption: str = "Open file", last_folder: str = "") -> Path | None:
        filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions)
        last_path = app().config.get_last_folder_for(last_folder, default=Path().home())

        path, selected_filter = QFileDialog.getOpenFileName(None, caption, str(last_path), filter_str, **kwargs)

        if not path:
            return None

        path = Path(path)

        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        if last_folder != "":
            app().config.write_last_folder_path_in_file(last_folder, path)

        return path

    @staticmethod
    def open_multiple_files(file_extensions: list[str], caption: str = "Open multiple files", last_folder: str = "") -> list[Path] | None:
        filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions)
        last_path = app().config.get_last_folder_for(last_folder, default=Path().home())

        paths, selected_filter = QFileDialog.getOpenFileNames(None, caption, str(last_path), filter_str, **kwargs)

        if not paths:
            return None

        paths = [Path(path) for path in paths]

        for i, path in enumerate(paths):
            if not path.suffix:
                suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
                paths[i] = path.with_suffix(suffix)

        if last_folder != "":
            app().config.write_last_folder_path_in_file(last_folder, paths[-1])

        return paths

    @staticmethod
    def save_file(file_extensions: list[str], caption: str = "Save file", last_folder: str = "") -> Path | None:
        filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions, open_file=False)
        last_path = app().config.get_last_folder_for(last_folder, default=Path().home())

        path, selected_filter = QFileDialog.getSaveFileName(None, caption, str(last_path), filter_str, **kwargs)

        if not path:
            return None

        path = Path(path)

        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        if last_folder != "":
            app().config.write_last_folder_path_in_file(last_folder, path)

        return path

    @staticmethod
    def get_existing_dir(caption: str = "", dir: str | Path = "") -> Path | None:
        kwargs = {}
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        existing_dir = QFileDialog.getExistingDirectory(caption=caption, dir=str(dir), **kwargs)

        if not existing_dir:
            return None

        return Path(existing_dir)

    @staticmethod
    def _build_dialog_kwargs(file_extensions: list[str], open_file=True):
        kwargs = {}
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        filter_str = FileDialogService._generate_file_extensions_str(file_extensions, open_file)

        return filter_str, kwargs

    @staticmethod
    def _generate_file_extensions_str(file_extensions: list[str], all_files=True):
        file_extensions = sorted(file_extensions, key=FileDialogService._sort_extensions)

        ext_dict = defaultdict(list)
        last_label = FileDialogService._get_file_label(file_extensions[0])
        extensions_text = ''

        for i, ext in enumerate(file_extensions):
            ext_str = f"*.{ext}"
            current_label = FileDialogService._get_file_label(ext)

            ext_dict["All files"].append(ext_str)
            ext_dict[current_label].append(ext_str)

            if current_label != last_label:
                extensions_text += FileDialogService._generate_qt_filter(last_label, ext_dict)
                last_label = current_label

            if i == len(file_extensions) - 1:
                extensions_text += FileDialogService._generate_qt_filter(current_label, ext_dict)

        if not all_files or len(file_extensions) == 1:
            return extensions_text

        return FileDialogService._generate_qt_filter("All files", ext_dict) + extensions_text

    @staticmethod
    def _generate_qt_filter(label: str, extensions_map: dict) -> str:
        return f"{label} ({' '.join(extensions_map[label])});;"

    @staticmethod
    def _get_file_label(extension: str) -> str:
        extension = extension.lower()

        match extension:
            case "xlsx" | "xls":
                return "Spreadsheet files"
            case "dat" | "csv" | "txt":
                return "Text files"
            case "pulse":
                return "Project files"
            case "iges" | "igs" | "step" | "stp":
                return "Geometry files"
            case "msh" | "bdf" | "nas":
                return "Mesh files"
            case "mp4":
                return "Video"
            case "webp":
                return "WEBP"
            case "gif":
                return "GIF"
            case _:
                return f"{extension.title()} files"

    @staticmethod
    def _get_path_extension(string: str) -> str:
        return string.split("*.")[-1].rstrip(")")

    @staticmethod
    def get_existing_directory(caption: str, directory: str | Path) -> Path | None:
        existing_dir = QFileDialog.getExistingDirectory(caption=caption, dir=str(directory))
        existing_dir = Path(existing_dir)

        if existing_dir.exists():
            return existing_dir

    @staticmethod
    def _sort_extensions(extension: str) -> int:
        extension = extension.lower()

        match extension:
            case "xlsx" | "xls":
                return 0
            case "dat" | "txt" | "csv":
                return 1
            case "pulse":
                return 2
            case "iges" | "igs" | "step" | "stp":
                return 3
            case "msh" | "bdf" | "nas":
                return 4
            case "mp4":
                return 5
            case "webp":
                return 6
            case "gif":
                return 7
            case _:
                return 8