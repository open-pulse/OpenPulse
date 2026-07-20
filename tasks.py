import hashlib
import os
import re
from typing import Tuple
import xml.etree.ElementTree as ET
from pathlib import Path
from invoke import task
from importlib.metadata import version

UI_FILES_PATH = Path("pulse/interface/data/ui_files")
GENERATED_PATH = Path("pulse/interface/ui_generated")
RESOURCE_DIR = Path("pulse/interface/data/icons") 
RESOURCE_DIR_DARK = RESOURCE_DIR / "dark_theme"
RESOURCE_DIR_LIGHT = RESOURCE_DIR / "light_theme"
QRC_PATH_DARK = RESOURCE_DIR_DARK / "resources.qrc"
QRC_PATH_LIGHT = RESOURCE_DIR_LIGHT / "resources.qrc"
QRC_PREFIX_NAME = "/icons/"
QRC_PREFIX = f":{QRC_PREFIX_NAME}"

RESOURCES_DIR = [RESOURCE_DIR_DARK, RESOURCE_DIR_LIGHT]
QRC_PATHS = [QRC_PATH_DARK, QRC_PATH_LIGHT]


@task
def qrc_codegen(c):
    '''
    Generate a .qrc file with the files (.png) included into the RESOURCE_DIR path.

    Usage example: inv qrc-codegen
    '''
    if not RESOURCE_DIR.exists():
        print(f"❌ Directory '{RESOURCE_DIR}' not found.")
        return

    for dir, qrc_path in zip(RESOURCES_DIR, QRC_PATHS):

        qrc_content = ['<RCC>', '    <qresource prefix="icons">']
        other_themes = [theme_dir for theme_dir in RESOURCES_DIR if theme_dir != dir]

        for file_path in dir.parent.rglob("*.png"):
            if not file_path.is_file():
                continue

            if any(other in file_path.parents for other in other_themes):
                continue

            if dir in file_path.parents:
                alias = file_path.relative_to(dir).as_posix()
            else:
                alias = file_path.relative_to(RESOURCE_DIR).as_posix()

            disk_path = os.path.relpath(file_path, qrc_path.parent).replace(os.sep, "/")
            qrc_content.append(f'        <file alias="{alias}">{disk_path}</file>')

        qrc_content.append('    </qresource>')

    with open(qrc_path, "w", encoding="utf-8") as qrc:
        qrc.write("\n".join(qrc_content))

    print(f"✅ {qrc_path} generated successfully!")


@task(pre=[qrc_codegen])
def qrc_compile(c):
    '''
    Compile .qrc file to resource_rc.py file

    Usage example: inv qrc-compile
    '''
    for dir, qrc_path in zip(RESOURCES_DIR, QRC_PATHS):

        rcc_path = dir / "resources_rc.py"
        command = f"pyside6-rcc \"{str(qrc_path)}\" -o \"{str(rcc_path)}\""
        result = c.run(command, warn=True)
        if result.ok:
            print(f"✅ {rcc_path} generated successfully!")


@task(pre=[qrc_compile])
def ui_compile(c):
    """
    Compile all .ui files to .py with a ready-to-use Widget class.
    
    Usage example: inv ui-compile
    """
    compiler_version = get_current_compiler_version()
    print('Current Compiler Version:', compiler_version)

    root_dir = os.path.abspath(UI_FILES_PATH)
    output_root = os.path.abspath(GENERATED_PATH)

    if not os.path.exists(root_dir):
        print("❌ The specified directory does not exist.")
        return

    # Clean up orphaned generated files
    clean_orphaned_files(root_dir, output_root)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ui"):
                ui_path = os.path.join(dirpath, filename)
                
                relative_path = os.path.relpath(dirpath, root_dir)
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                py_path = os.path.join(output_dir, filename.replace(".ui", "_ui.py"))
                relative_ui_path = os.path.relpath(ui_path, root_dir)

                ui_class_name, qt_class_name = extract_class_names(ui_path)
                hierarchy = extract_widget_hierarchy(ui_path)

                if not ui_class_name or not qt_class_name:
                    print(f"⚠️ Skipping {ui_path} (Could not determine class names)")
                    continue

                wrapper_class_name = to_camel_case(os.path.splitext(filename)[0])

                need_compile, ui_md5 = check_recompile(ui_path, py_path, compiler_version)

                if not need_compile: 
                    continue

                # Run pyside6-uic to generate the Python file
                command = f"pyside6-uic \"{ui_path}\" -o \"{py_path}\""
                result = c.run(command, warn=True)

                if result.ok:
                    with open(py_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()

                    modified_lines = []
                    for line in lines:
                        if line.startswith("# Form implementation generated from reading ui file"):
                            line = f"# Form implementation generated from reading ui file '{relative_ui_path}'\n"
                        if line.startswith('import resources_rc'):
                            # This import is wrongly inserted by the pyuic5 compiler due to include tag into <resources> pointed to the qrc file.
                            # This is fixed using a global import o the application launch.
                            continue
                        modified_lines.append(line)

                    # Generate docstring with hierarchy
                    docstring = f'    """\n    Component Hierarchy:\n    {hierarchy}\n    """\n'

                    wrapper_class = f"""

class {wrapper_class_name}_UI({qt_class_name}, Ui_{ui_class_name}):
{docstring}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
"""
                    modified_lines.append(wrapper_class)

                    with open(py_path, "w", encoding="utf-8") as file:
                        file.writelines(modified_lines)

                    # Saving ui md5 hash for the next recompile checking.
                    save_md5(ui_path, ui_md5)

                    print(f"✅ Generated: {ui_path} → {py_path}")
                else:
                    print(f"❌ Error while generating: {ui_path}")


@task
def fix_ui_files(c):
    '''
    Fix all .ui files to enable use them from designer.
    '''
    root_dir = os.path.abspath(UI_FILES_PATH)

    if not os.path.exists(root_dir):
        print("❌ The specified directory does not exist.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ui"):
                ui_path = os.path.join(dirpath, filename)
                fix_ui_file_text(Path(ui_path))


def clean_orphaned_files(root_dir: str, output_root: str) -> None:
    """Remove generated .py files that don't have corresponding .ui files."""
    if not os.path.exists(output_root):
        return
    
    deleted_count = 0
    for dirpath, _, filenames in os.walk(output_root):
        for filename in filenames:
            if filename.endswith("_ui.py"):
                py_path = os.path.join(dirpath, filename)
                
                # Calculate the corresponding .ui file path
                relative_path = os.path.relpath(dirpath, output_root)
                ui_dir = os.path.join(root_dir, relative_path)
                ui_filename = filename.replace("_ui.py", ".ui")
                ui_path = os.path.join(ui_dir, ui_filename)
                
                # Check if .ui file exists
                if not os.path.exists(ui_path):
                    os.remove(py_path)
                    print(f"🗑️  Deleted orphaned file: {py_path}")
                    deleted_count += 1
                    
                    # Also delete the .md5 file if it exists
                    md5_path = f"{ui_path}.md5"
                    if os.path.exists(md5_path):
                        os.remove(md5_path)
                        print(f"🗑️  Deleted orphaned md5: {md5_path}")
    
    if deleted_count > 0:
        print(f"✅ Cleaned up {deleted_count} orphaned file(s)")


def to_camel_case(filename: str) -> str:
    """Convert filename (snake_case or kebab-case) to CamelCase."""
    return "".join(word.capitalize() for word in re.split(r"[_\s-]+", filename))


def extract_class_names(ui_path: str) -> tuple[str, str]:
    """Extracts Qt base class and UI class name from the .ui XML file."""
    try:
        tree = ET.parse(ui_path)
        root = tree.getroot()

        ui_class = root.find("class")
        ui_class_name = ui_class.text if ui_class is not None else None

        widget = root.find("widget")
        qt_class_name = widget.attrib["class"] if widget is not None else None

        return ui_class_name, qt_class_name
    except Exception as e:
        print(f"⚠️ Error reading {ui_path}: {e}")
        return None, None


def extract_widget_hierarchy(ui_path: str) -> str:
    """Extracts the hierarchical structure of widgets from the .ui file, including deeply nested components."""
    try:
        tree = ET.parse(ui_path)
        root = tree.getroot()

        def parse_widget(element, level=1):
            """Recursively parses widgets and layouts."""
            indent = "    " * level
            result = ""

            if element.tag == "widget" and "name" in element.attrib and "class" in element.attrib:
                widget_name = element.attrib["name"]
                widget_class = element.attrib["class"]
                result += f"{indent}- {widget_name}: {widget_class}\n"

            elif element.tag == "layout" and "class" in element.attrib:
                layout_class = element.attrib["class"]
                result += f"{indent}- (Layout): {layout_class}\n"

            for child in element:
                result += parse_widget(child, level + 1)

            return result

        # Find the root widget and parse recursively
        root_widget = root.find("widget")
        hierarchy = parse_widget(root_widget) if root_widget is not None else ""

        return hierarchy.strip()
    except Exception as e:
        print(f"⚠️ Error extracting hierarchy from {ui_path}: {e}")
        return ""


def get_relative_qrc_path(ui_path: Path, qrc_path: Path = QRC_PATH_DARK) -> str:
    return os.path.relpath(qrc_path, start=ui_path.parent)


def convert_to_qrc_path(icon_path: str) -> str:
    icon_path = Path(icon_path).as_posix()
    if QRC_PREFIX_NAME in icon_path:
        relative_icon_path = icon_path.split(QRC_PREFIX_NAME)[-1]
        return f"{QRC_PREFIX}{relative_icon_path}"
    return icon_path
    

def fix_ui_file_text(file_path: Path) -> None:
    updated_lines = []
    lines = file_path.open('r').readlines()
    for line in lines:
        if QRC_PREFIX in line:
            updated_lines.append(line)
            continue

        if '<resource' in line:
            qrc_resource_tag = f' <resources><include location="{get_relative_qrc_path(file_path)}" /></resources>\n'
            updated_lines.append(qrc_resource_tag)
            continue

        for path in find_relative_paths(line):
            if QRC_PREFIX_NAME in path:
                qrc_path = f'{QRC_PREFIX}{path.split(QRC_PREFIX_NAME)[-1]}'
                line = line.replace(path, qrc_path)
            
        updated_lines.append(line)
    
    file_path.open('w').writelines(updated_lines)
    print(f"✅ Fixed: {file_path}")


def find_relative_paths(text: str) -> list[str]:
    pattern = r'(?:(?:\.\./)+[\w\-/]+\.[\w]+)'
    return re.findall(pattern, text)


def check_recompile(ui_path: str, py_path: str, current_version: str) -> Tuple[bool, str | None]:
    current_md5 = compute_md5(ui_path)
    saved_md5_file = Path(f'{ui_path}.md5')
    saved_py_file = Path(py_path)
    if saved_md5_file.exists() and saved_py_file.exists():
        saved_version = extract_compiler_version_from_compiled_file(py_path)
        if saved_version != current_version:
            return True, current_md5
        
        saved_md5 = saved_md5_file.read_text()
        if current_md5 == saved_md5:
            return False, None
        
    return True, current_md5


def compute_md5(file_path: str, block=8192) -> str:
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            md5.update(chunk)
    return md5.hexdigest()


def save_md5(ui_path: str, md5: str):
    path_md5 = f'{ui_path}.md5'

    with open(path_md5, "w") as f:
        f.write(md5)


def extract_compiler_version_from_compiled_file(py_path: str) -> str | None:
    pattern = r"^## Created by: Qt User Interface Compiler version ([\d\.]+)"

    with open(py_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                return match.group(1)

    return None

def get_current_compiler_version() -> str:
    return version('pyside6')