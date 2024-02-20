from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
import numpy as np
import matplotlib.pyplot as plt

from pulse import UI_DIR
from pulse.lib.default_libraries import default_material_library
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput


window_title = "Error"
window_title2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class MaterialInputs(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "model/setup/general/material_input_widget.ui", self)

        self.main_window = main_window

        self.reset()
        self.define_qt_variables()
        self.create_connections()
        self.load_data_from_materials_library()

    def reset(self):
        self.row = None
        self.col = None
        self.project = self.main_window.project
        self.file = self.project.file
        self.preprocessor = self.project.preprocessor
        self.material_path = self.file.material_list_path
        self.material_data = dict()
        self.disable_item_changed = True

    def define_qt_variables(self):

        # QPushButton
        self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')
        self.pushButton_add_row = self.findChild(QPushButton, 'pushButton_add_row')
        self.pushButton_remove_row = self.findChild(QPushButton, 'pushButton_remove_row')
        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        # self.pushButton_attribute_material.setDisabled(True)

        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTableWidget, 'tableWidget_material_data')

    def create_connections(self):
        self.pushButton_add_row.clicked.connect(self.add_row)
        self.pushButton_remove_row.clicked.connect(self.remove_selected_row)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_material_data.itemChanged.connect(self.item_changed)
        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.cell_changed)

    def config_table_of_material_data(self):

        header = [  'Name',
                    'ID',
                    'Density \n[kg/m³]',
                    'Elasticity \nmodulus [GPa]',
                    'Poisson',
                    'Thermal expansion \ncoefficient [m/mK]',
                    'Color'  ]
        
        self.tableWidget_material_data.setColumnCount(len(header))
        self.tableWidget_material_data.setHorizontalHeaderLabels(header)
        self.tableWidget_material_data.setSelectionBehavior(1)
        self.tableWidget_material_data.resizeColumnsToContents()

        self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(0)
        self.tableWidget_material_data.horizontalHeader().setStretchLastSection(True)

        for j, width in enumerate([140, 40, 80, 100, 80, 120, 40]):
            self.tableWidget_material_data.horizontalHeader().resizeSection(j, width)
            self.tableWidget_material_data.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)

    def load_data_from_materials_library(self):

        self.list_names = []
        self.list_ids = []
        self.list_colors = []
        self.disable_item_changed = True

        self.tableWidget_material_data.clear()
        self.config_table_of_material_data()

        try:
            if os.path.exists(self.material_path):
                    
                config = configparser.ConfigParser()
                config.read(self.material_path)
                sections = list(config.sections())

                rows = len(sections)
                self.tableWidget_material_data.setRowCount(rows)

                for i, section in enumerate(sections):

                    name = str(config[section]['name'])
                    identifier =  str(config[section]['identifier'])
                    color =  str(config[section]['color'])

                    colorRGB = getColorRGB(color)
                    self.list_names.append(name)
                    self.list_ids.append(int(identifier))
                    self.list_colors.append(colorRGB)

                    self.tableWidget_material_data.setItem(i, 0, QTableWidgetItem(config[section]['name']))
                    self.tableWidget_material_data.setItem(i, 1, QTableWidgetItem(config[section]['identifier']))
                    self.tableWidget_material_data.setItem(i, 2, QTableWidgetItem(config[section]['density']))
                    self.tableWidget_material_data.setItem(i, 3, QTableWidgetItem(config[section]['young modulus']))
                    self.tableWidget_material_data.setItem(i, 4, QTableWidgetItem(config[section]['poisson']))
                    self.tableWidget_material_data.setItem(i, 5, QTableWidgetItem(config[section]['thermal expansion coefficient']))
                    
                    item = QTableWidgetItem(str(colorRGB))
                    item.setBackground(QColor(*colorRGB))
                    item.setForeground(QColor(*colorRGB))
                    self.tableWidget_material_data.setItem(i, 6, item)
                
                    for j in range(7):
                        self.tableWidget_material_data.item(i,j).setTextAlignment(Qt.AlignCenter)
            
            self.disable_item_changed = False
                    
        except Exception as error_log:
            self.title = "Error while loading the material list"
            self.message = str(error_log)
            PrintMessageInput([window_title, self.title, self.message])
            self.close()

    def add_row(self):
        last_row = self.tableWidget_material_data.rowCount()
        self.tableWidget_material_data.insertRow(last_row)
        for j in range(6):
            item = QTableWidgetItem()
            self.tableWidget_material_data.setItem(last_row, j, item)
            self.tableWidget_material_data.item(last_row,j).setTextAlignment(Qt.AlignCenter)

    def remove_selected_row(self):
        if self.row is not None:
            if self.process_material_removal():
                self.row = None
                self.col = None
    
    def item_changed(self, item):

        if self.disable_item_changed:
            return

        if item is None:
            return
        
        if item.text() == "":
            return
        
        row = item.row()
        col = item.column()

        self.row = row
        self.col = col

        item = self.tableWidget_material_data.item(row, col)
        if item is None:
            return

        if col == 0:
            if self.check_input_material_name(row, col):
                self.tableWidget_material_data.setCurrentCell(row, col)
                return
        elif col == 1:
            if self.check_input_material_id(row, col):
                self.tableWidget_material_data.setCurrentCell(row, col)
                return
        elif col in [2, 3, 4, 5]:
            if self.check_material_properties(row, col):
                self.tableWidget_material_data.setCurrentCell(row, col)
                return

        if col <= 5:
            self.tableWidget_material_data.setCurrentCell(row, col+1)

        self.check_inputs_and_add_material_to_library(row)

    def cell_clicked(self, row, col):

        self.row = row
        self.col = col

        if col == 6:
            self.pick_color(row, col)

        if self.check_if_all_input_fields(row):
            return
        #     self.pushButton_attribute_material.setDisabled(True)
        # else:
        #     self.pushButton_attribute_material.setDisabled(False)
        
    def cell_changed(self, current_row, current_col, previous_row, previous_col):

        item = self.tableWidget_material_data.item(previous_row, previous_col)
        if item is None:
            return 
        
        if current_col == 6:
            self.pick_color(current_row, current_col)
        
        self.check_inputs_and_add_material_to_library(current_row)
            
    def check_if_all_input_fields(self, row):
        for j in range(7):
            item = self.tableWidget_material_data.item(row,j)
            if item is None:
                return True
            elif j < 6:
                if item.text() == "":
                    return True
        return False

    def check_inputs_and_add_material_to_library(self, row):
        if self.check_if_all_input_fields(row):
            return
            # self.pushButton_attribute_material.setDisabled(True)
        else:
            # self.pushButton_attribute_material.setDisabled(False)
            self.add_material_to_file(row)
            self.load_data_from_materials_library()
            self.material_data = dict()

    def add_material_to_file(self, row):
        try:

            self.material_data = dict()

            keys = ["name", 
                    "identifier", 
                    "density", 
                    "young modulus", 
                    "poisson", 
                    "thermal expansion coefficient", 
                    "color"]
            
            for j, key in enumerate(keys):
                item = self.tableWidget_material_data.item(row, j)
                if key == "color":
                    color = item.background().color().getRgb()
                    self.material_data[key] = list(color)
                else:
                    self.material_data[key] = item.text()

            material_name = self.material_data["name"]
            
            if material_name != "":

                config = configparser.ConfigParser()
                config.read(self.material_path)
                config[material_name] = self.material_data

                with open(self.material_path, 'w') as config_file:
                    config.write(config_file)
                    
        except Exception as error_log:
            title = "Error while writing material data in file"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return True

    def pick_color(self, row, col):

        read = PickColorInput()
        if read.complete:
        
            picked_color = read.color
            if picked_color in self.list_colors:
                return True

            self.material_data["color"] = picked_color
            item = QTableWidgetItem(str(picked_color))
            item.setBackground(QColor(*picked_color))
            item.setForeground(QColor(*picked_color))
            self.tableWidget_material_data.setItem(row, col, item)
            self.tableWidget_material_data.item(row, 0).setSelected(True)

    def check_input_material_name(self, row, col):
        try:

            item = self.tableWidget_material_data.item(row, col)
            if self.row + 1 <= len(self.list_names):
                if item.text() == self.list_names[self.row]:
                    return True
            
            for name in self.list_names:
                if item.text() in name:
                    item.setText("")
                    return True

            self.material_data["name"] = item.text()

        except:
            pass

    def check_input_material_id(self, row, col):
        try:

            item = self.tableWidget_material_data.item(row, col)
            input_id = int(item.text())

            if self.row + 1 <= len(self.list_ids):
                if input_id == self.list_ids[self.row]:
                    return True
            
            if input_id in self.list_ids:
                item.setText("")
                return True
            
            if input_id <= 0:
                window_title = "Error"
                title = "Negative value not allowed"
                message = f"The value typed to 'material identifier' must be a non-zero positive integer number."
                PrintMessageInput([window_title, title, message])
                item.setText("")
                return True

            self.material_data["identifier"] = input_id

        except:
            pass

    def check_material_properties(self, row, col):

        prop_labels = { 2 : "density", 
                        3 : "young modulus",
                        4 : "poisson",
                        5 : "thermal expansion coefficient" }
        
        item = self.tableWidget_material_data.item(row, col)

        try:

            value = float(item.text())

            if value <= 0:
                window_title = "Error"
                title = "Negative value not allowed"
                message = f"The value typed for '{prop_labels[col]}' must be a non-zero positive number."
                PrintMessageInput([window_title, title, message])
                item.setText("")
                return True

            if col == 2:
                self.material_data["density"] = value

            if col == 3:
                self.material_data["young modulus"] = value

            if col == 4:
                self.material_data["poisson"] = value

            if col == 5:
                self.material_data["thermal expansion coefficient"] = value

        except:

            item.setText("")
            self.tableWidget_material_data.setCurrentCell(row, col)

    def get_selected_material_id(self):
        if self.row is not None:
            item = self.tableWidget_material_data.item(self.row,1)
            if item.text() != "":
                return int(item.text())
            
    def get_confirmation_to_proceed(self, title : str, message : str):
        """
        """
        buttons_config = {  "left_button_label" : "No", 
                            "right_button_label" : "Yes",
                            "left_button_size" : 80,
                            "right_button_size" : 80}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            return False

        if read._continue:
            return True

    def process_material_removal(self):

        try:

            title = "Additional confirmation required to proceed"
            message = "Do you really want to remove the selected material from material library?"

            config = configparser.ConfigParser()
            config.read(self.material_path)
            sections = config.sections()
            selected_material = self.tableWidget_material_data.item(self.row,0).text()

            if selected_material in sections:

                if not self.get_confirmation_to_proceed(title, message):
                    return True

                config.remove_section(selected_material)

                with open(self.material_path, 'w') as config_file:
                    config.write(config_file)

                for line_id, entity in self.preprocessor.dict_tag_to_entity.items():
                    if entity.material is not None:
                        if entity.material.name == self.lineEdit_name_remove.text():
                            self.project.set_material_by_lines(line_id, None)

                self.load_data_from_materials_library()

            else:

                self.tableWidget_material_data.removeRow(self.row)
                return True

        except Exception as error_log:
            self.title = "Error occured in material removal"
            self.message = str(error_log)
            PrintMessageInput([window_title, self.title, self.message])
            return

    def reset_library_to_default(self):

        title = "Additional confirmation required to proceed"
        message = "Do you really want to reset the material library to default values?"

        if self.get_confirmation_to_proceed(title, message):

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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)