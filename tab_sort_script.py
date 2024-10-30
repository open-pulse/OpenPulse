from pathlib import Path

import re

def find_ui_files():
    ui_files_path = list()
    for path in Path("pulse/interface/data/ui_files").rglob("*.ui"):
        ui_files_path.append(path)

    return ui_files_path

def tab_sorting(ui_files: list[Path]):
    for file in ui_files:
        answer = extract_tabs(file)   

def tab_sort_script():
    ui_files = find_ui_files()
    tab_sorting(ui_files)

def extract_tabs(ui_file: Path):
    arch_content = ui_file.read_text()
    tab_regex = re.compile(r"<tabstops>(.|\n)*</tabstops>")
    contains_tab = tab_regex.search(arch_content)

    if contains_tab is not None:
        tabstop_regex = re.compile(r"<tabstop>.*</tabstop")
        widgets_names = tabstop_regex.findall(str(contains_tab))
        print(widgets_names)

tab_sort_script()