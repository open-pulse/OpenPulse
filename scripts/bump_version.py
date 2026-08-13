import re
import subprocess
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import date
from importlib.metadata import version
from pathlib import Path
from typing import Self


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def software_version(cls) -> Self:
        x, y, z = version("pulse").split(".")
        return cls(int(x), int(y), int(z))

    def bump_major(self) -> Self:
        return Version(self.major + 1, 0, 0)

    def bump_minor(self) -> Self:
        return Version(self.major, self.minor + 1, 0)

    def bump_patch(self) -> Self:
        return Version(self.major, self.minor, self.patch + 1)

    def copy(self) -> Self:
        return Version(self.major, self.minor, self.patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def release_date() -> str:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    today = date.today()
    current_month = months[today.month - 1]
    current_year = today.year
    return f"{current_month} {current_year}"


def green_text(txt: str) -> str:
    return "\033[32m" + txt + "\033[0m"


def replace_in_file(path: Path, pattern: str, replacement: str):
    current_text = path.read_text()
    new_text = re.sub(
        pattern,
        replacement,
        current_text,
    )
    path.write_text(new_text)


def update_version(new_version: Version):
    date_regex = r"((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec))\s+\d{4}"
    current_date = release_date()

    replace_in_file(
        Path("pulse.iss"),
        r'#define\s+MyAppVersion\s+"\d\.\d\.\d"',
        f'#define MyAppVersion "{new_version}"',
    )
    replace_in_file(
        Path("pulse/__init__.py"),
        r'return\s+"\d\.\d\.\d"',
        f'return "{new_version}"',
    )
    replace_in_file(
        Path("pulse/__init__.py"),
        date_regex,
        current_date,
    )
    replace_in_file(
        Path("pyproject.toml"),
        r'version\s+=\s+"\d\.\d\.\d"',
        f'version = "{new_version}"',
    )
    replace_in_file(
        Path("README.md"),
        r"\*\s*[vV]\d\.\d\.\d\s+" + date_regex,
        f"*v{new_version} {current_date}",
    )


def main():
    parser = ArgumentParser(description="CLI for control version.")
    parser.add_argument(
        "command",
        choices=["major", "minor", "patch", "sync"],
        help="Version to be bumped.",
    )
    args = parser.parse_args()

    current_version = Version.software_version()

    match args.command:
        case "major":
            new_version = current_version.bump_major()
        case "minor":
            new_version = current_version.bump_minor()
        case "patch":
            new_version = current_version.bump_patch()
        case "sync":
            new_version = current_version.copy()

    update_version(new_version)
    print(green_text(f"{current_version} → {new_version}"))


if __name__ == "__main__":
    main()
