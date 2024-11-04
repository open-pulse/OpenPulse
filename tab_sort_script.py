from pathlib import Path

import re

def tab_sort_script():
    ui_files = find_ui_files()
    tab_sorting(ui_files)

def find_ui_files():
    ui_files_path = list()
    for path in Path("pulse/interface/data/ui_files").rglob("*.ui"):
        ui_files_path.append(path)

    return ui_files_path

def tab_sorting(ui_files: list[Path]):
    for file in ui_files:
        arch_content = file.read_text()
        old_tab_string = extract_old_tabs_and_archive_contents(arch_content)

        if old_tab_string:
            widgets_name = sort_existing_tabs(arch_content)
            new_tab_string = generate_tab_string(widgets_name)
        else:
            old_tab_string = "<resources/>"
            widgets_name = find_widgets_name(arch_content)
            new_tab_string = generate_tab_string(widgets_name) + "\n" + old_tab_string

        write_tab_string_in_ui_file(file, old_tab_string, new_tab_string)   

def extract_old_tabs_and_archive_contents(arch_content: str) -> str:
    tab_regex = re.compile(r"<tabstops>(.|\n)*</tabstops>")
    contains_tab = tab_regex.search(arch_content)

    if contains_tab is not None:
        old_tab_string = contains_tab.group(0)
        return old_tab_string
    
    return ""
       
def generate_tab_string(widgets_names: list[str]):
    text = "<tabstops>\n"
    for widget_name in widgets_names:
        text += f"  <tabstop>{widget_name}</tabstop>\n"
    text += "</tabstops>"

    return text

def find_widgets_name(archive_content: str):
    widgets_regex = re.compile(r"<widget.*")
    widgets = widgets_regex.findall(archive_content)
    
    widgets_name_regex = re.compile(r"name=.*")
    widgets_name = list()

    for i in range(len(widgets)):
        widgets_name += widgets_name_regex.findall(widgets[i])
        widgets_name[i] = widgets_name[i][6:len(widgets_name[i])-2]
    
    return widgets_name

def sort_existing_tabs(archive_content: str) -> list[str]:
    tabstop_regex = re.compile(r'(?<=<tabstop>).*(?=</tabstop>)')
    widgets_name = tabstop_regex.findall(str(archive_content))
    
    widgets_name.sort(key=archive_content.find)

    return widgets_name

def write_tab_string_in_ui_file(ui_file: Path, old_tab_string: str, new_tab_string: str):
    arch_content = ui_file.read_text()
    arch_content = arch_content.replace(old_tab_string, new_tab_string)

    ui_file.write_text(arch_content)

tab_sort_script()