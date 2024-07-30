from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.libraries.default_libraries import default_material_library
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.preprocessing.material import Material

import configparser
from itertools import count
from pathlib import Path

window_title = "Error"
window_title2 = "Warning"

COLOR_COLUMN = 5

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class MaterialInputs(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/material/material_input_widget.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project

        self._initialize()
        self.define_qt_variables()
        self.create_connections()
        self.load_data_from_materials_library()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _add_icon_and_title(self):
        self._load_icons()
        self._config_window()

    def _initialize(self):

        self.file = self.project.file
        self.preprocessor = self.project.preprocessor
        self.material_path = self.file.material_list_path

        self.row = None
        self.col = None
        self.list_of_materials = list()

    def define_qt_variables(self):

        # QPushButton
        self.pushButton_attribute_material : QPushButton
        self.pushButton_add_row : QPushButton
        self.pushButton_remove_row : QPushButton
        self.pushButton_reset_library : QPushButton

        # QTableWidget
        self.tableWidget_material_data : QTableWidget

    def create_connections(self):
        self.pushButton_add_row.clicked.connect(self.add_row)
        self.pushButton_remove_row.clicked.connect(self.remove_selected_row)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)

    def config_table_of_material_data(self):
        header = [
            'Name',
            'Density \n[kg/m³]',
            'Elasticity \nmodulus [GPa]',
            'Poisson',
            'Thermal expansion \ncoefficient [m/mK]',
            'Color',
        ]
        
        self.tableWidget_material_data.setColumnCount(len(header))
        self.tableWidget_material_data.setHorizontalHeaderLabels(header)
        self.tableWidget_material_data.setSelectionBehavior(1)
        self.tableWidget_material_data.resizeColumnsToContents()

        self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(0)
        self.tableWidget_material_data.horizontalHeader().setStretchLastSection(True)

        for j, width in enumerate([140, 80, 120, 80, 140, 40]):
            self.tableWidget_material_data.horizontalHeader().resizeSection(j, width)
            self.tableWidget_material_data.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)
    
    def load_data_from_materials_library(self):
        self.material_path = Path(self.material_path)
        if not self.material_path.exists():
            return

        try:
            config = configparser.ConfigParser()
            config.read(self.material_path)

        except Exception as error_log:
            self.title = "Error while loading the material list"
            self.message = str(error_log)
            PrintMessageInput([window_title, self.title, self.message])
            self.close()

        self.list_of_materials.clear()
        for section in config.sections():
            material = Material(
                name = config[section]['name'],
                density = float(config[section]['density']),
                poisson_ratio = float(config[section]['poisson']),
                young_modulus = float(config[section]['young modulus']) * 1e9,
                identifier = int(config[section]['identifier']), 
                thermal_expansion_coefficient = float(config[section]['thermal expansion coefficient']), 
                color = getColorRGB(config[section]['color'])
            )
            self.list_of_materials.append(material)
        
        self.update_table()

    def update_table(self):

        self.config_table_of_material_data()
        self.tableWidget_material_data.setRowCount(len(self.list_of_materials))
        self.tableWidget_material_data.setColumnCount(COLOR_COLUMN + 1)

        for i, material in enumerate(self.list_of_materials):
            self.tableWidget_material_data.setItem(i, 0, QTableWidgetItem(str(material.name)))
            self.tableWidget_material_data.setItem(i, 1, QTableWidgetItem(str(material.density)))
            self.tableWidget_material_data.setItem(i, 2, QTableWidgetItem(f"{material.young_modulus/1e9 :.2f}"))
            self.tableWidget_material_data.setItem(i, 3, QTableWidgetItem(str(material.poisson_ratio)))
            self.tableWidget_material_data.setItem(i, 4, QTableWidgetItem(str(material.thermal_expansion_coefficient)))

            item = QTableWidgetItem()
            item.setBackground(QColor(*material.color))
            item.setForeground(QColor(*material.color))
            self.tableWidget_material_data.setItem(i, 5, item)

        for i in range(self.tableWidget_material_data.rowCount()):
            for j in range(self.tableWidget_material_data.columnCount()):
                item = self.tableWidget_material_data.item(i,j)
                item.setTextAlignment(Qt.AlignCenter)

    def get_selected_row(self) -> int:
        selected_items = self.tableWidget_material_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].row()

    def get_selected_material(self) -> Material | None:
        selected_row = self.get_selected_row()
        if selected_row < 0:
            return

        if selected_row >= len(self.list_of_materials):
            return

        return self.list_of_materials[selected_row]

    def add_row(self):
        table_size = self.tableWidget_material_data.rowCount()
        if table_size > len(self.list_of_materials):
            # it means that if you already have a new row
            # to insert data you don't need another one
            return 

        last_row = self.tableWidget_material_data.rowCount()
        self.tableWidget_material_data.insertRow(last_row)
        for j in range(self.tableWidget_material_data.columnCount()):
            item = QTableWidgetItem()
            self.tableWidget_material_data.setItem(last_row, j, item)
            self.tableWidget_material_data.item(last_row,j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.selectRow(last_row)
        first_item = self.tableWidget_material_data.item(last_row, 0)
        self.tableWidget_material_data.editItem(first_item)

    def remove_selected_row(self):
        selected_row = self.get_selected_row()
        if selected_row < 0:
            return

        if selected_row >= len(self.list_of_materials):
            # if it is the last item and a not an already configured
            # material, just remove the last line
            current_size = self.tableWidget_material_data.rowCount()
            self.tableWidget_material_data.setRowCount(current_size - 1)
            return

        title = "Additional confirmation required to proceed"
        message = "Would you like to remove the selected material from material library?"
        if self.get_confirmation_to_proceed(title, message):
            material = self.list_of_materials[selected_row]
            self.remove_material_from_file(material)
    
    def item_changed_callback(self, item):
        if self.row_has_empty_items(item.row()):
            return

        if self.row_has_invalid_name(item.row()):
            return

        if self.item_is_invalid_number(item):
            return

        self.add_material_to_file(item.row())
        self.load_data_from_materials_library()

    def cell_clicked_callback(self, row, col):
        if col == 5:
            self.pick_color(row, col)
            
    def row_has_empty_items(self, row):
        for j in range(self.tableWidget_material_data.columnCount()):
            item = self.tableWidget_material_data.item(row, j)
            if item is None:
                return True

            if j == COLOR_COLUMN:
                # color = item.background().color().getRgb()
                # if list(color) == 0:
                #     return True
                continue

            if item.text() == "":
                return True

        return False
    
    def row_has_invalid_name(self, row):
        item = self.tableWidget_material_data.item(row, 0)
        if item is None:
            return True

        row_name = item.text()

        if not row_name:
            return True

        for material in self.list_of_materials:
            if material.name == row_name:
                return True

        return False 

    def item_is_invalid_number(self, item):
        if item is None:
            return True
        
        if item.column() not in [2, 3, 4, 5]:
            return False
    
        prop_labels = {
                        2 : "density", 
                        3 : "young modulus",
                        4 : "poisson",
                        5 : "thermal expansion coefficient"
                    }
        
        try:
            value = float(item.text())

        except Exception as error:
            window_title = "Error"
            title = "Invalid real number"
            message = f"The value typed for '{prop_labels[item.column()]}' must be a non-zero positive number."
            PrintMessageInput([window_title, title, message])
            item.setText("")
            return True

        if value < 0:
            window_title = "Error"
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[item.column()]}' must be a non-zero positive number."
            PrintMessageInput([window_title, title, message])
            item.setText("")
            return True
        
        return False

    def add_material_to_file(self, row):
        try:

            material_data = dict()

            keys = [
                    "name", 
                    "density", 
                    "young modulus", 
                    "poisson", 
                    "thermal expansion coefficient", 
                    "color"
                ]

            for j, key in enumerate(keys):
                item = self.tableWidget_material_data.item(row, j)
                if key == "color":
                    color = item.background().color().getRgb()
                    material_data[key] = list(color)
                else:
                    material_data[key] = item.text()
            material_data["identifier"] = self.new_identifier()

            material_name = material_data["name"]
            if not material_name:
                return

            config = configparser.ConfigParser()
            config.read(self.material_path)
            config[material_name] = material_data

            with open(self.material_path, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as error_log:
            title = "Error while writing material data in file"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return True

    def remove_material_from_file(self, material):
        config = configparser.ConfigParser()
        config.read(self.material_path)

        if not material.name in config.sections():
            return
        
        config.remove_section(material.name)
        with open(self.material_path, 'w') as config_file:
            config.write(config_file)

        for line_id, entity in self.preprocessor.dict_tag_to_entity.items():
            if entity.material is None:
                continue

            if entity.material.name == material.name:
                self.project.set_material_by_lines(line_id, None)

        self.load_data_from_materials_library()

    def new_identifier(self):
        already_used_ids = set()
        for material in self.list_of_materials:
            already_used_ids.add(material.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

    def pick_color(self, row, col):
        read = PickColorInput()
        if not read.complete:
            return

        picked_color = read.color
        item = QTableWidgetItem()
        item.setBackground(QColor(*picked_color))
        item.setForeground(QColor(*picked_color))
        self.tableWidget_material_data.setItem(row, col, item)
        self.tableWidget_material_data.item(row, 0).setSelected(True)

    def get_selected_material_id(self):
        material = self.get_selected_material()
        if material is None:
            return None
        return material.identifier
            
    def get_confirmation_to_proceed(self):

        self.hide()

        title = "Additional confirmation required to proceed"
        message = "Would you like to reset the material library to default values?"

        buttons_config = {  "left_button_label" : "No", 
                            "right_button_label" : "Yes",
                            "left_button_size" : 80,
                            "right_button_size" : 80}

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return False

        if read._continue:
            return True

    def reset_library_to_default(self):

        if self.get_confirmation_to_proceed():

            config_cache = configparser.ConfigParser()
            config_cache.read(self.material_path)  
            sections_cache = config_cache.sections()

            default_material_library(self.material_path)
            config = configparser.ConfigParser()
            config.read(self.material_path)

            material_names = []
            for section_cache in sections_cache:
                if section_cache not in config.sections():
                    material_names.append(config_cache[section_cache]["name"])

            for line_id, entity in self.preprocessor.dict_tag_to_entity.items():
                if entity.material is not None:
                    if entity.material.name in material_names:
                        self.project.set_material_by_lines(line_id, None)

            self.load_data_from_materials_library()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        elif event.key() == Qt.Key_Delete:
            self.remove_selected_row()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False