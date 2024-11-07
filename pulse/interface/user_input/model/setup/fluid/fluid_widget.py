from PyQt5.QtWidgets import QDialog, QPushButton, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR, TEMP_PROJECT_FILE
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_composition_input import SetFluidCompositionInput
from pulse.tools.utils import get_list_of_values_from_string

from pulse.model.properties.fluid import Fluid
from pulse.libraries.default_libraries import default_fluid_library

from itertools import count
from os.path import exists


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
    def __init__(self, *argas, **kwargs):
        super().__init__()
        
        ui_path = UI_DIR  / "model/setup/fluid/fluid_input_widget.ui"
        uic.loadUi(ui_path, self)

        self.parent_widget = kwargs.get("parent_widget", None)
        self.compressor_info = kwargs.get("compressor_info", dict())

        self.main_window = app().main_window
        self.project = app().project
        self.properties = app().project.model.properties

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_data_from_fluids_library()

    def _initialize(self):

        self.row = None
        self.col = None
        self.refprop = None
        self.selected_column = None

        self.list_of_fluids = dict()
        self.fluid_data_refprop = dict()
        self.fluid_name_to_refprop_data = dict()

        self.fluid_data_keys = [
                                "name",
                                "identifier",
                                "temperature",
                                "pressure",
                                "density",
                                "speed_of_sound",
                                "isentropic_exponent",
                                "thermal_conductivity",
                                "specific_heat_Cp",
                                "dynamic_viscosity",
                                "molar_mass",
                                "color"
                                ]

    def _define_qt_variables(self):

        # QPushButton
        self.pushButton_add_column: QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_refprop: QPushButton
        self.pushButton_remove_column: QPushButton
        self.pushButton_reset_library: QPushButton

        # QTableWidget
        self.tableWidget_fluid_data: QTableWidget
        self.tableWidget_fluid_data.setStyleSheet("")

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        # self.pushButton_cancel.clicked.connect(self.close_window)
        self.pushButton_refprop.clicked.connect(self.call_refprop_interface)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_fluid_data.cellDoubleClicked.connect(self.cell_double_clicked_callback)

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

        if not exists(TEMP_PROJECT_FILE):
            self.reset_library_to_default()
            return

        config = app().pulse_file.read_fluid_library_from_file()
        if config is None:
            self.reset_library_to_default()
            return

        self.list_of_fluids.clear()
        self.fluid_name_to_refprop_data.clear()

        if not list(config.sections()):
            self.update_table()
            return

        for tag in config.sections():

            section = config[tag]
            keys = config[tag].keys()

            name = section['name']
            identifier =  int(section['identifier'])
            density =  float(section['density'])
            speed_of_sound =  float(section['speed_of_sound'])
            color =  get_color_rgb(section['color'])

            if 'isentropic_exponent' in keys:
                isentropic_exponent = float(section['isentropic_exponent'])
            else:
                isentropic_exponent = ""

            if 'thermal_conductivity' in keys:
                thermal_conductivity = float(section['thermal_conductivity'])
            else:
                thermal_conductivity = ""

            if 'specific_heat_Cp' in keys:
                specific_heat_Cp = float(section['specific_heat_Cp'])
            else:
                specific_heat_Cp = ""

            if 'dynamic_viscosity' in keys:
                dynamic_viscosity = float(section['dynamic_viscosity'])
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

            if "molar_mass" in keys:
                if section["molar_mass"] == "None":
                    molar_mass = None
                else:
                    molar_mass = float(section["molar_mass"])
            else:
                molar_mass = None

            fluid = Fluid(  name = name,
                            density = density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure,
                            molar_mass = molar_mass  )

            self.list_of_fluids[identifier] = fluid

            aux = [temperature, pressure, key_mixture, molar_fractions]
            if aux.count(None) == 0:
                self.fluid_name_to_refprop_data[name] = [   name, 
                                                            temperature, 
                                                            pressure, 
                                                            key_mixture, 
                                                            molar_fractions   ]

        self.update_table()

    def update_table(self):

        self.config_table_of_fluid_data()
        self.tableWidget_fluid_data.clearContents()
        self.tableWidget_fluid_data.blockSignals(True)
        self.tableWidget_fluid_data.setRowCount(COLOR_ROW + 1)
        self.tableWidget_fluid_data.setColumnCount(len(self.list_of_fluids))

        for j, fluid in enumerate(self.list_of_fluids.values()):
            if isinstance(fluid, Fluid):

                self.tableWidget_fluid_data.setItem( 0, j, QTableWidgetItem(str(fluid.name)))
                self.tableWidget_fluid_data.setItem( 1, j, QTableWidgetItem(str(fluid.identifier)))
                self.tableWidget_fluid_data.setItem( 2, j, QTableWidgetItem(str(fluid.temperature)))
                self.tableWidget_fluid_data.setItem( 3, j, QTableWidgetItem(str(fluid.pressure)))
                self.tableWidget_fluid_data.setItem( 4, j, QTableWidgetItem(str(fluid.density)))
                self.tableWidget_fluid_data.setItem( 5, j, QTableWidgetItem(str(fluid.speed_of_sound)))
                self.tableWidget_fluid_data.setItem( 6, j, QTableWidgetItem(str(fluid.isentropic_exponent)))
                self.tableWidget_fluid_data.setItem( 7, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .4e}"))
                self.tableWidget_fluid_data.setItem( 8, j, QTableWidgetItem(str(fluid.specific_heat_Cp)))
                self.tableWidget_fluid_data.setItem( 9, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .4e}"))
                self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(str(fluid.molar_mass)))

                item = QTableWidgetItem()
                item.setBackground(QColor(*fluid.color))
                item.setForeground(QColor(*fluid.color))
                self.tableWidget_fluid_data.setItem(COLOR_ROW, j, item)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            for j in range(self.tableWidget_fluid_data.columnCount()):
                self.tableWidget_fluid_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.blockSignals(False)

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
        
        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())

        return self.list_of_fluids[identifier]

    def add_column(self):
    
        self.tableWidget_fluid_data.blockSignals(True)

        table_size = self.tableWidget_fluid_data.columnCount()
        if table_size > len(self.list_of_fluids):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_fluid_data.blockSignals(False)
            return 

        last_col = self.tableWidget_fluid_data.columnCount()
        self.tableWidget_fluid_data.insertColumn(last_col)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
            self.tableWidget_fluid_data.setItem(i, last_col, item)
            self.tableWidget_fluid_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.selectColumn(last_col)
        first_item = self.tableWidget_fluid_data.item(0, last_col)
        if self.refprop is None:
            self.tableWidget_fluid_data.editItem(first_item)

        self.tableWidget_fluid_data.blockSignals(False)

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

        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())
        fluid = self.list_of_fluids[identifier]

        self.remove_fluid_from_file(fluid)

    def item_changed_callback(self, item):

        self.tableWidget_fluid_data.blockSignals(True)

        if item.row() == 0:
            if self.column_has_invalid_name(item.column()):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        elif item.row() == 1:
            if self.column_has_invalid_identifier(item.column()):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        else:
            if self.item_is_invalid_number(item):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        self.go_to_next_cell(item)
        if self.column_has_empty_items(item.column()):
            self.tableWidget_fluid_data.blockSignals(False)
            return

        self.add_fluid_to_file(item.column())
        self.load_data_from_fluids_library()

        self.tableWidget_fluid_data.blockSignals(False)
    
    def go_to_next_cell(self, item):

        row = item.row()
        column = item.column()

        if row < COLOR_ROW - 1:
            next_item = self.tableWidget_fluid_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_fluid_data.setCurrentItem(next_item)
                self.tableWidget_fluid_data.editItem(next_item)

        elif row == COLOR_ROW - 1:
            self.pick_color(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_fluid_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for fluid in self.list_of_fluids.values():
            if fluid.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_fluid_data.item(1, column)

        already_used_ids = set()
        for fluid in self.list_of_fluids.values():
            already_used_ids.add(fluid.identifier)
        
        if item.text() == "":
            return True
        
        try:
            if int(item.text()) in already_used_ids:
                item.setText("")
                return True
        except:
            item.setText("")
            return True

    def column_has_empty_items(self, column):
        for row in range(COLOR_ROW + 1):

            item = self.tableWidget_fluid_data.item(row, column)
            if item is None:
                return True
            
            if row == COLOR_ROW:
                color = item.background().color().getRgb()
                if list(color) == 0:
                    return True

            elif item.text() == "":
                return True

        return False

    def item_is_invalid_number(self, item):

        if item is None:
            return True

        row = item.row()
        if row == COLOR_ROW:
            return
        
        prop_labels = {
                        2 : "temperature", 
                        3 : "pressure",
                        4 : "density",
                        5 : "speed_of_sound",
                        6 : "isentropic_exponent",
                        7 : "thermal_conductivity",
                        8 : "specific_heat_Cp",
                        9 : "dynamic_viscosity",
                       10 : "molar_mass"
                    }

        if row not in prop_labels.keys():
            return True
        
        if item.text() == "":
            return True

        try:

            str_value = item.text().replace(",", ".")
            item.setText(str_value)
            value = float(str_value)

        except Exception as error_log:
            title = "Invalid real number"
            message = f"The value typed for '{prop_labels[row]}' "
            message += "must be a non-zero positive number.\n\n"
            message += f"Details: {error_log}"
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True

        if value < 0:
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[row]}' must be a non-zero positive number."
            PrintMessageInput([window_title_1, title, message])
            item.setText("")
            return True

        return False

    def add_fluid_to_file(self, column):
        try:

            fluid_data = dict()

            for i, key in enumerate(self.fluid_data_keys):
                item = self.tableWidget_fluid_data.item(i, column)
                if key == "color":
                    color = item.background().color().getRgb()
                    fluid_data[key] = list(color[:3])
                else:
                    fluid_data[key] = item.text()
            
            identifier = fluid_data["identifier"]

            if self.refprop is not None:
                [key_mixture, molar_fractions] = self.fluid_setup
                fluid_data['key mixture'] = key_mixture
                fluid_data['molar fractions'] = molar_fractions
                fluid_data["molar_mass"] = round(self.fluid_data_refprop["molar_mass"], 6)

            config = app().pulse_file.read_fluid_library_from_file()
            config[identifier] = fluid_data

            app().pulse_file.write_fluid_library_in_file(config)
                    
        except Exception as error_log:
            title = "Error while writing fluid data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True

    def remove_fluid_from_file(self, fluid: Fluid):

        config = app().pulse_file.read_fluid_library_from_file()

        identifier = str(fluid.identifier)
        if not identifier in config.sections():
            return

        self.reset_fluid_from_lines([identifier])

        config.remove_section(identifier)
        app().pulse_file.write_fluid_library_in_file(config)

        self.load_data_from_fluids_library()

    def reset_fluid_from_lines(self, fluid_identifiers: list):

        lines_to_remove_fluid = list()
        for line_id, data in self.properties.line_properties.items():
            if "fluid_id" in data.keys():
                fluid_id = data["fluid_id"]
                if fluid_id in fluid_identifiers:
                    app().project.model.preprocessor.set_fluid_by_lines(line_id, None)
                    if fluid_id not in lines_to_remove_fluid:
                        lines_to_remove_fluid.append(line_id)

        for _line_id in lines_to_remove_fluid:
            self.properties._remove_line_property("fluid_id", line_id=_line_id)
            self.properties._remove_line_property("fluid", line_id=_line_id)

        app().pulse_file.write_line_properties_in_file()

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color(row, col)

    def cell_double_clicked_callback(self, row, col):

        fluid_name = self.tableWidget_fluid_data.item(0, col).text()

        if fluid_name in self.fluid_name_to_refprop_data.keys():
            if isinstance(self.parent_widget, QDialog):
                self.parent_widget.hide()

            selected_fluid = self.fluid_name_to_refprop_data[fluid_name]
            self.refprop = SetFluidCompositionInput(selected_fluid_to_edit = selected_fluid, 
                                                    compressor_info = self.compressor_info)

            if not self.refprop.complete:
                app().main_window.set_input_widget(self.parent_widget)
                return

            self.selected_column = col
            self.after_getting_fluid_properties_from_refprop()
            self.selected_column = None

    def new_identifier(self):

        already_used_ids = set()
        for fluid in self.list_of_fluids.values():
            already_used_ids.add(fluid.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

    def pick_color(self, row, col):

        read = PickColorInput()
        if not read.complete:
            return True

        picked_color = read.color

        item = QTableWidgetItem()
        item.setBackground(QColor(*picked_color))
        item.setForeground(QColor(*picked_color))
        self.tableWidget_fluid_data.setItem(row, col, item)
        self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    def get_confirmation_to_proceed(self):

        self.hide()

        title = "Resetting the fluids library"
        message = "Would you like to reset the fluid library to default values?"

        buttons_config = {  "left_button_label" : "No", 
                            "right_button_label" : "Yes",
                            "left_button_size" : 80,
                            "right_button_size" : 80}

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return False

        if read._continue:
            return True

    def reset_library_callback(self):
        if self.get_confirmation_to_proceed():
            self.reset_library_to_default()
            return True
        return False

    def reset_library_to_default(self):

        config_cache = app().pulse_file.read_fluid_library_from_file()

        sections_cache = list()
        if config_cache is not None:
            sections_cache = config_cache.sections()

        default_fluid_library()

        config = app().pulse_file.read_fluid_library_from_file()

        fluid_identifiers = list()
        for section_cache in sections_cache:
            if section_cache not in config.sections():
                identifier = config_cache[section_cache]["identifier"]
                fluid_identifiers.append(int(identifier))

        self.reset_fluid_from_lines(fluid_identifiers)
        self.load_data_from_fluids_library()
        
    def call_refprop_interface(self):

        if isinstance(self.parent_widget, QDialog):
            self.parent_widget.hide()

        self.refprop = SetFluidCompositionInput(compressor_info = self.compressor_info)

        if app().main_window.force_close:
            self.parent_widget.close()
            return True

        if not self.refprop.complete:
            app().main_window.set_input_widget(self.parent_widget)
            return True

        self.after_getting_fluid_properties_from_refprop()

    def after_getting_fluid_properties_from_refprop(self):

        if self.refprop.complete:

            self.fluid_setup = self.refprop.fluid_setup
            self.fluid_data_refprop = self.refprop.fluid_properties

            if self.selected_column is None:
                self.add_column()
                self.tableWidget_fluid_data.blockSignals(True)
                selected_column = self.tableWidget_fluid_data.columnCount() - 1
            else:
                selected_column = self.selected_column

            for row, key in enumerate(self.fluid_data_keys):

                if key == "identifier":
                    _data = str(self.new_identifier())

                elif key == "color":
                    if self.selected_column is None:
                        self.pick_color(row, selected_column)
                    continue

                else:

                    data = self.fluid_data_refprop[key]
                    if isinstance(data, float):

                        if key in ["pressure", "thermal_conductivity", "dynamic_viscosity"]:
                            _data = f"{data : .6e}"
                        else:
                            _data = f"{data : .6f}"

                    elif isinstance(data, str):
                        _data = data

                self.tableWidget_fluid_data.item(row, selected_column).setText(_data)

            self.add_fluid_to_file(selected_column)
            self.tableWidget_fluid_data.blockSignals(False)
            self.load_data_from_fluids_library()

        else:
            self.refprop = None

    def load_compressor_info(self):

        if self.compressor_info:

            if isinstance(self.parent_widget, QDialog):

                line_id = self.compressor_info['line_id']
                app().main_window.set_selection(lines=[line_id])

                # self.parent_widget.lineEdit_selected_id.setText(str(line_id))
                # self.parent_widget.comboBox_attribution_type.setCurrentIndex(1)
                # # self.parent_widget.selection_callback()
                # self.parent_widget.lineEdit_selected_id.setDisabled(True)

                column = self.tableWidget_fluid_data.columnCount()
                self.tableWidget_fluid_data.selectColumn(column-1)

                if self.fluid_data_refprop:
                    fluid_name = self.fluid_data_refprop["name"]
                    self.parent_widget.lineEdit_selected_fluid_name.setText(fluid_name)

                print(self.compressor_info['connection_type'])

                connection_type = self.compressor_info['connection_type']
                title = f"Set a fluid thermodynamic state at the compressor {connection_type}"

                self.parent_widget.setWindowTitle(title)

    def update_compressor_fluid_temperature_and_pressure(self):
        return

        temperature_lineEdits = [self.lineEdit_temperature, self.lineEdit_temperature_rp]
        pressure_lineEdits = [self.lineEdit_pressure, self.lineEdit_pressure_rp]

        for temperature_lineEdit in temperature_lineEdits:
            temperature_lineEdit.setText(str(round(self.temperature_comp,4)))
            temperature_lineEdit.setDisabled(True)

        for pressure_lineEdit in pressure_lineEdits:
            pressure_lineEdit.setText(str(round(self.pressure_comp,4)))
            pressure_lineEdit.setDisabled(True)

    def update_compressor_info(self):
        if self.compressor_info:
            if self.refprop is not None:
                if self.refprop.complete:
                    self.compressor_info["temperature (discharge)"] = round(self.fluid_data_refprop["temperature"], 4)
                    self.compressor_info["molar_mass"] = self.fluid_data_refprop["molar_mass"]

    # def close_window(self):
    #     if isinstance(self.parent_widget, QDialog):
    #         self.parent_widget.close()
    #     else:
    #         self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        elif event.key() == Qt.Key_Delete:
            self.remove_selected_column()
        elif event.key() == Qt.Key_Escape:
            self.close()