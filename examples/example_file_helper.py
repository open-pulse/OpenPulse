

from pathlib import Path


def get_example_file_path(subpath: str) -> Path:
    return Path(__file__).parent / subpath