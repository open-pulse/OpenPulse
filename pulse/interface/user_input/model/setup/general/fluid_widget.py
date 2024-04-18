from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.preprocessing.fluid import Fluid
from pulse.libraries.default_libraries import default_fluid_library
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.interface.user_input.model.setup.general.set_fluid_composition_input import SetFluidCompositionInput
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.tools.utils import *

import numpy as np
from configparser import ConfigParser
from pathlib import Path
from itertools import count

window_title_1 = "Error"
window_title_2 = "Warning"
COLOR_ROW = 11


def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class FluidWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        ui_path = UI_DIR  / "model/setup/fluid/fluid_input_widget.ui"
        uic.loadUi(ui_path, self)
        
        self.main_window = app().main_window
        self.project = app().project
        self.file = app().file

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_data_from_fluids_library()

    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.fluid_path = self.file.fluid_list_path

        self.row = None
        self.col = None
        self.list_of_fluids = list()
        self.fluid_name_to_REFPROP_data = dict()

    def _define_qt_variables(self):

        # QPushButton
        self.pushButton_attribute_fluid : QPushButton
        self.pushButton_add_row : QPushButton
        self.pushButton_remove_row : QPushButton
        self.pushButton_reset_library : QPushButton

        # QTableWidget
        self.tableWidget_fluid_data : QTableWidget
        self.tableWidget_fluid_data.setStyleSheet("")

    def _create_connections(self):
        # return
        self.pushButton_add_row.clicked.connect(self.add_column)
        self.pushButton_remove_row.clicked.connect(self.remove_selected_column)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)

    def config_table_of_fluid_data(self):
        return
        header = [
            'Name',
            'Density \n[kg/m³]',
            'Elasticity \nmodulus [GPa]',
            'Poisson',
            'Thermal expansion \ncoefficient [m/mK]',
            'Color',
        ]
        
        self.tableWidget_fluid_data.setColumnCount(len(header))
        self.tableWidget_fluid_data.setHorizontalHeaderLabels(header)
        self.tableWidget_fluid_data.setSelectionBehavior(1)
        self.tableWidget_fluid_data.resizeColumnsToContents()

        self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(0)
        self.tableWidget_fluid_data.horizontalHeader().setStretchLastSection(True)

        for j, width in enumerate([140, 80, 120, 80, 140, 40]):
            self.tableWidget_fluid_data.horizontalHeader().resizeSection(j, width)
            self.tableWidget_fluid_data.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)
    
    def load_data_from_fluids_library(self):

        self.fluid_path = Path(self.fluid_path)
        if not self.fluid_path.exists():
            return

        try:
            config = configparser.ConfigParser()
            config.read(self.fluid_path)

        except Exception as error_log:
            self.title = "Error while loading the fluid list"
            self.message = str(error_log)
            PrintMessageInput([window_title_1, self.title, self.message])
            self.close()

        self.list_of_fluids.clear()
        for tag in config.sections():

            section = config[tag]
            keys = config[tag].keys()

            name = section['name']
            fluid_density =  float(section['fluid density'])
            speed_of_sound =  float(section['speed of sound'])
            color =  get_color_rgb(section['color'])
            identifier =  int(section['identifier'])

            if 'isentropic exponent' in keys:
                isentropic_exponent = float(section['isentropic exponent'])
            else:
                isentropic_exponent = ""

            if 'thermal conductivity' in keys:
                thermal_conductivity = float(section['thermal conductivity'])
            else:
                thermal_conductivity = ""

            if 'specific heat Cp' in keys:
                specific_heat_Cp = float(section['specific heat Cp'])
            else:
                specific_heat_Cp = ""

            if 'dynamic viscosity' in keys:
                dynamic_viscosity = float(section['dynamic viscosity'])
            else:
                dynamic_viscosity = ""
            
            if 'temperature' in keys:
                temperature = float(section['temperature'])
            else:
                temperature = None

            if 'pressure' in keys:
                pressure = float(section['pressure'])
            else:
                pressure = None

            if 'key mixture' in keys:
                key_mixture = section['key mixture']
            else:
                key_mixture = None

            if 'molar fractions' in keys:
                str_molar_fractions = section['molar fractions']
                molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
            else:
                molar_fractions = None

            fluid = Fluid(  name = name,
                            density = fluid_density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure  )

            self.list_of_fluids.append(fluid)

            aux = [temperature, pressure, key_mixture, molar_fractions]
            if aux.count(None) == 0:
                self.fluid_name_to_REFPROP_data[name] = [   name, 
                                                            temperature, 
                                                            pressure, 
                                                            key_mixture, 
                                                            molar_fractions   ]

        self.update_table()

    def update_table(self):

        self.config_table_of_fluid_data()
        # self.tableWidget_fluid_data.setRowCount(len(self.list_of_fluids))
        self.tableWidget_fluid_data.setRowCount(12)
        self.tableWidget_fluid_data.setColumnCount(len(self.list_of_fluids))

        for j, fluid in enumerate(self.list_of_fluids):
            self.tableWidget_fluid_data.setItem(0, j, QTableWidgetItem(str(fluid.name)))
            self.tableWidget_fluid_data.setItem(1, j, QTableWidgetItem(str(fluid.identifier)))
            self.tableWidget_fluid_data.setItem(2, j, QTableWidgetItem(str(fluid.temperature)))
            self.tableWidget_fluid_data.setItem(3, j, QTableWidgetItem(str(fluid.pressure)))
            self.tableWidget_fluid_data.setItem(4, j, QTableWidgetItem(str(fluid.density)))
            self.tableWidget_fluid_data.setItem(5, j, QTableWidgetItem(str(fluid.speed_of_sound)))
            self.tableWidget_fluid_data.setItem(6, j, QTableWidgetItem(str(fluid.impedance)))
            self.tableWidget_fluid_data.setItem(7, j, QTableWidgetItem(str(fluid.isentropic_exponent)))
            self.tableWidget_fluid_data.setItem(8, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .4e}"))
            self.tableWidget_fluid_data.setItem(9, j, QTableWidgetItem(str(fluid.specific_heat_Cp)))
            self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .4e}"))

            item = QTableWidgetItem()
            item.setBackground(QColor(*fluid.color))
            item.setForeground(QColor(*fluid.color))
            self.tableWidget_fluid_data.setItem(COLOR_ROW, j, item)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            for j in range(self.tableWidget_fluid_data.columnCount()):
                item = self.tableWidget_fluid_data.item(i,j)
                item.setTextAlignment(Qt.AlignCenter)

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_fluid_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_fluid(self) -> Fluid | None:
        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.list_of_fluids):
            return

        return self.list_of_fluids[selected_column]

    def add_column(self):
        table_size = self.tableWidget_fluid_data.columnCount()
        if table_size > len(self.list_of_fluids):
            # it means that if you already have a new row
            # to insert data you don't need another one
            return 

        last_col = self.tableWidget_fluid_data.columnCount()
        self.tableWidget_fluid_data.insertColumn(last_col)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
            self.tableWidget_fluid_data.setItem(i, last_col, item)
            self.tableWidget_fluid_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.selectColumn(last_col)
        first_item = self.tableWidget_fluid_data.item(0, last_col)
        self.tableWidget_fluid_data.editItem(first_item)

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.list_of_fluids):
            # if it is the last item and a not an already configured
            # fluid, just remove the last line
            current_size = self.tableWidget_fluid_data.columnCount()
            self.tableWidget_fluid_data.setColumnCount(current_size - 1)
            return

        title = "Additional confirmation required to proceed"
        message = "Would you like to remove the selected fluid from fluid library?"
        if self.get_confirmation_to_proceed(title, message):
            fluid = self.list_of_fluids[selected_column]
            self.remove_fluid_from_file(fluid)
    
    def item_changed_callback(self, item):

        if self.column_has_empty_items(item.column()):
            return

        if self.column_has_invalid_name(item.column()):
            return

        if self.item_is_invalid_number(item):
            return

        self.add_fluid_to_file(item.column())
        self.load_data_from_fluids_library()
    
    def column_has_empty_items(self, column):

        for i in range(self.tableWidget_fluid_data.rowCount()):

            item = self.tableWidget_fluid_data.item(i, column)
            if item is None:
                return True

            if i == COLOR_ROW:
                color = item.background().color().getRgb()
                if list(color):
                    return True

            if item.text() == "":
                return True

        return False
    
    def column_has_invalid_name(self, column):

        item = self.tableWidget_fluid_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for fluid in self.list_of_fluids:
            if fluid.name == column_name:
                return True

        return False 

    def item_is_invalid_number(self, item):

        if item is None:
            return True

        if item.row() not in [2, 3, 4, 6, 7, 8, 9, 10]:
            return False
    
        prop_labels = {
                        2 : "temperature", 
                        3 : "pressure",
                        4 : "density",
                        6 : "speed of sound",
                        7 : "isetropic exponent",
                        8 : "thermal conductivity",
                        9 : "specific heat Cp",
                       10 : "dynamic viscosity"
                    }

        try:
            value = float(item.text())

        except Exception as error:
            title = "Invalid real number"
            message = f"The value typed for '{prop_labels[item.row()]}' "
            message += "must be a non-zero positive number."
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True

        if value < 0:
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[item.row()]}' must be a non-zero positive number."
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True
        
        return False


    def add_fluid_to_file(self, column):
        try:

            fluid_data = dict()

            keys = [
                "name",
                "identifier",
                "temperature",
                "pressure",
                "fluid density", 
                "speed of sound",
                "impedance",
                "isentropic exponent",
                "thermal conductivity",
                "specific heat Cp",
                "dynamic viscosity",
                "color"
            ]

            for i, key in enumerate(keys):
                item = self.tableWidget_fluid_data.item(i, column)
                if key == "color":
                    color = item.background().color().getRgb()
                    fluid_data[key] = list(color)
                else:
                    fluid_data[key] = item.text()

            fluid_data["identifier"] = self.new_identifier()

            fluid_name = fluid_data["name"]
            if not fluid_name:
                return

            config = configparser.ConfigParser()
            config.read(self.fluid_path)
            config[fluid_name] = fluid_data

            with open(self.fluid_path, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as error_log:
            title = "Error while writing fluid data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True

    def remove_fluid_from_file(self, fluid):

        config = configparser.ConfigParser()
        config.read(self.fluid_path)

        if not fluid.name in config.sections():
            return
        
        config.remove_section(fluid.name)
        with open(self.fluid_path, 'w') as config_file:
            config.write(config_file)

        for line_id, entity in self.preprocessor.dict_tag_to_entity.items():
            if entity.fluid is None:
                continue

            if entity.fluid.name == fluid.name:
                self.project.set_fluid_by_lines(line_id, None)

        self.load_data_from_fluids_library()

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color(row, col)

    def new_identifier(self):

        already_used_ids = set()
        for fluid in self.list_of_fluids:
            already_used_ids.add(fluid.identifier)

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
        self.tableWidget_fluid_data.setItem(row, col, item)
        self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    def get_confirmation_to_proceed(self, title : str, message : str):

        buttons_config = {  "left_button_label" : "No", 
                            "right_button_label" : "Yes",
                            "left_button_size" : 80,
                            "right_button_size" : 80}

        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            return False

        if read._continue:
            return True

    def reset_library_to_default(self):

        title = "Additional confirmation required to proceed"
        message = "Would you like to reset the fluid library to default values?"

        if self.get_confirmation_to_proceed(title, message):

            config_cache = configparser.ConfigParser()
            config_cache.read(self.fluid_path)  
            sections_cache = config_cache.sections()

            default_fluid_library(self.fluid_path)
            config = configparser.ConfigParser()
            config.read(self.fluid_path)

            fluid_names = list()
            for section_cache in sections_cache:
                if section_cache not in config.sections():
                    fluid_names.append(config_cache[section_cache]["name"])

            for line_id, entity in self.preprocessor.dict_tag_to_entity.items():
                if entity.fluid is not None:
                    if entity.fluid.name in fluid_names:
                        self.project.set_fluid_by_lines(line_id, None)

            self.load_data_from_fluids_library()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        elif event.key() == Qt.Key_Delete:
            self.remove_selected_column()
        elif event.key() == Qt.Key_Escape:
            self.close()