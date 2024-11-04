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
        old_tab_string, new_tab_string, arch_content = extract_tabs(file)
        write_tab_string_in_ui_file(file, old_tab_string, new_tab_string, arch_content)   


def extract_tabs(ui_file: Path):
    arch_content = ui_file.read_text()

    tab_regex = re.compile(r"<tabstops>(.|\n)*</tabstops>")
    contains_tab = tab_regex.search(arch_content)

    if contains_tab is not None:
        old_tab_string = contains_tab.group(0)

        tabstop_regex = re.compile(r"<tabstop>.*</tabstop>")
        widgets = tabstop_regex.findall(str(arch_content))

        widgets_name = list()
        for widget in widgets:
            widgets_name.append(widget[9:len(widget)-10])
        
        widgets_name.sort(key=arch_content.find)
        new_tab_string = generate_tab_string(widgets_name)

        return old_tab_string, new_tab_string, arch_content
    
    widgets_name = find_widgets(arch_content)
       
def generate_tab_string(widgets_names: list[str]):
    text = "<tabstops>\n"
    for widget_name in widgets_names:
        text += f"  <tabstop>{widget_name}</tabstop>\n"
    text += "</tabstops>"

    return text

def find_widgets(archive_content: str):
    old_string_regex = re.compile(r"<resources/>(.|\n)*") 
    old_string = old_string_regex.search(archive_content).group(0)

    widgets_regex = re.compile(r"<widget.*")
    widgets = widgets_regex.findall(archive_content)
    
    widgets_name_regex = re.compile(r"name=.*")
    widgets_name = list()

    for i in range(len(widgets)):
        widgets_name += widgets_name_regex.findall(widgets[i])
        widgets_name[i] = widgets_name[i][6:len(widgets_name[i])-2]
    
    return widgets_name

def write_tab_string_in_ui_file(ui_file: Path, old_tab_string: str, new_tab_string: str, arch_content: str):
    arch_content = arch_content.replace(old_tab_string, new_tab_string)

    archive = open(ui_file, "w")
    archive.write(arch_content)
    archive.close()

tab_sort_script()