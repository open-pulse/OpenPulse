import re
from copy import deepcopy
from itertools import count
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QDialog, QHeaderView, QMenu, QTableWidgetItem

from pulse import app, ICON_DIR
from pulse.interface import error_title
from pulse.interface.formatters.icons import change_icon_color_for_widgets
from pulse.interface.ui_generated.model.setup.fluid.fluid_input_widget_ui import (
    FluidInputWidget_UI,
)
from pulse.interface.user_input.data_handler.file_dialog_service import (
    FileDialogService,
)
from pulse.interface.user_input.model.setup.fluid.set_fluid_composition_input import (
    SetFluidCompositionInput,
)
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    convert_pressure_unit,
    convert_temperature_unit,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.libraries.default_libraries import default_fluid_library
from pulse.model.properties.fluid import Fluid


class FluidWidget(FluidInputWidget_UI):

    COLOR_ROW = 13

    def __init__(self, *argas, **kwargs):
        super().__init__()
        self.dialog = kwargs.get("dialog", None)

        self.main_window = app().main_window
        self.project = app().project
        self.properties = app().project.model.properties

        self.state_properties = kwargs.get("state_properties", dict())

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._paint_icons()
        self.load_data_from_fluids_library()

    def _initialize(self):

        self.row = None
        self.col = None
        self.refprop = None
        self.selected_column = None

        self.fluid_data_refprop = dict()
        self.fluids_from_library = dict()
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
            "adiabatic_bulk_modulus",
            "vapor_pressure",
            "molar_mass",
            "color"
            ]

    def _define_qt_variables(self):
        self.tableWidget_fluid_data.setStyleSheet("")

    def _create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_fluid)
        self.pushButton_refprop.clicked.connect(self.refprop_interface_callback)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        # self.pushButton_reset_library.clicked.connect(self.reset_library_callback)
        #
        self.tableWidget_fluid_data.cellClicked.connect(self.cell_clicked_callback)
        self.tableWidget_fluid_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_fluid_data.cellDoubleClicked.connect(self.cell_double_clicked_callback)
        #
        self.tableWidget_fluid_data.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_fluid_data.customContextMenuRequested.connect(self.right_click_callback)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _config_widgets(self):
        self.tableWidget_fluid_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
    
    def _update_size_policy(self):
        if len(self.fluids_from_library) > 6:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_fluid_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from pulse import DARK_ICON_COLOR, LIGHT_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_duplicate]
        change_icon_color_for_widgets(widgets, icon_color)

    def _add_icon_and_title(self):
        self._config_window()

    def load_data_from_fluids_library(self):

        self.fluids_from_library.clear()
        self.fluid_name_to_refprop_data.clear()

        fluids_from_library = app().project.loader.load_fluids_library()
        if isinstance(fluids_from_library, dict):
            if not fluids_from_library:
                self.reset_library_to_default()
                return

        self.fluids_from_library = fluids_from_library

        for fluid in fluids_from_library.values():
            if not isinstance(fluid, Fluid):
                continue

            refprop_parameters = [
                                  fluid.name,
                                  fluid.temperature, 
                                  fluid.pressure, 
                                  fluid.key_mixture, 
                                  fluid.molar_fractions
                                  ]

            if refprop_parameters.count(None) == 0:
                self.fluid_name_to_refprop_data[fluid.name] = refprop_parameters

        # self.properties.set_fluids_library(self.fluids_from_library)
        self.update_fluid_properties_table()

    def update_fluid_properties_table(self):

        self.tableWidget_fluid_data.clearContents()
        self.tableWidget_fluid_data.blockSignals(True)
        self.tableWidget_fluid_data.setRowCount(self.COLOR_ROW + 1)
        self.tableWidget_fluid_data.setColumnCount(len(self.fluids_from_library))

        for j, fluid in enumerate(self.fluids_from_library.values()):
            if isinstance(fluid, Fluid):

                self.tableWidget_fluid_data.setItem( 0, j, QTableWidgetItem(str(fluid.name)))
                self.tableWidget_fluid_data.setItem( 1, j, QTableWidgetItem(str(fluid.identifier)))
                self.tableWidget_fluid_data.setItem( 2, j, QTableWidgetItem(str(fluid.temperature)))
                self.tableWidget_fluid_data.setItem( 3, j, QTableWidgetItem(f"{fluid.pressure : .6e}"))
                self.tableWidget_fluid_data.setItem( 4, j, QTableWidgetItem(str(fluid.density)))
                self.tableWidget_fluid_data.setItem( 5, j, QTableWidgetItem(str(fluid.speed_of_sound)))
                self.tableWidget_fluid_data.setItem( 6, j, QTableWidgetItem(str(fluid.isentropic_exponent)))
                self.tableWidget_fluid_data.setItem( 7, j, QTableWidgetItem(f"{fluid.thermal_conductivity : .6e}"))
                self.tableWidget_fluid_data.setItem( 8, j, QTableWidgetItem(str(fluid.specific_heat_Cp)))
                self.tableWidget_fluid_data.setItem( 9, j, QTableWidgetItem(f"{fluid.dynamic_viscosity : .6e}"))

                if fluid.adiabatic_bulk_modulus is None:
                    _bulk_modulus = fluid.bulk_modulus
                else:
                    _bulk_modulus = fluid.adiabatic_bulk_modulus
                self.tableWidget_fluid_data.setItem(10, j, QTableWidgetItem(f"{_bulk_modulus : .6e}"))

                if fluid.vapor_pressure is None:
                    _vapor_pressure = "--"
                else:
                    _vapor_pressure = f"{fluid.vapor_pressure : .6e}"
                self.tableWidget_fluid_data.setItem(11, j, QTableWidgetItem(_vapor_pressure))

                if fluid.vapor_pressure is None:
                    self.tableWidget_fluid_data.item(11, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                if fluid.molar_mass is None:
                    molar_mass = "--"
                else:
                    molar_mass = str(fluid.molar_mass)
                self.tableWidget_fluid_data.setItem(12, j, QTableWidgetItem(molar_mass))

                item = QTableWidgetItem()
                q_color = QColor(*fluid.color)

                item.setBackground(q_color)
                item.setForeground(q_color)
                self.tableWidget_fluid_data.setItem(self.COLOR_ROW, j, item)

                if fluid.name in self.fluid_name_to_refprop_data.keys():
                    for i in range(13):
                        self.tableWidget_fluid_data.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            for j in range(self.tableWidget_fluid_data.columnCount()):
                self.tableWidget_fluid_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.blockSignals(False)
        self._update_size_policy()

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_fluid_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_fluid(self) -> Fluid | None:
        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.fluids_from_library):
            return
        
        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())

        return self.fluids_from_library.get(identifier)

    def load_state_properties_in_SI_units(self, last_col: int):
        """
        This method returns the state properties in SI unit system.
        """
        if not self.state_properties:
            return

        if self.state_properties.get('source') is not None:
            connection_type = self.state_properties.get("connection_type")
            if connection_type == "discharge":
                pressure = self.state_properties.get("discharge_pressure")
                temperature = self.state_properties.get("discharge_temperature")
            else:
                pressure = self.state_properties.get("suction_pressure")
                temperature = self.state_properties.get("suction_temperature")

            pressure_unit = self.state_properties.get("pressure_unit")
            temperature_unit = self.state_properties.get("temperature_unit")

            pressure_Pa = convert_pressure_unit(pressure, pressure_unit, "Pa")
            temperature_K = convert_temperature_unit(temperature, temperature_unit, "K")

            self.tableWidget_fluid_data.item(3, last_col).setText(f"{pressure_Pa : .8e}")
            self.tableWidget_fluid_data.item(2, last_col).setText(f"{temperature_K : .8f}")

            isentropic_exponent = self.state_properties.get("isentropic_exponent")
            if isinstance(isentropic_exponent, float):
                self.tableWidget_fluid_data.item(6, last_col).setText(f"{isentropic_exponent}")

            molar_mass = self.state_properties.get("molar_mass")
            if isinstance(molar_mass, float):
                self.tableWidget_fluid_data.item(12, last_col).setText(f"{molar_mass}")

    def add_column(self):

        self.tableWidget_fluid_data.blockSignals(True)

        table_size = self.tableWidget_fluid_data.columnCount()
        if table_size > len(self.fluids_from_library):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_fluid_data.blockSignals(False)
            return 

        last_col = self.tableWidget_fluid_data.columnCount()
        self.tableWidget_fluid_data.insertColumn(last_col)

        for i in range(self.tableWidget_fluid_data.rowCount()):
            item = QTableWidgetItem()
            item.setSizeHint(QSize(100, 30))
            self.tableWidget_fluid_data.setItem(i, last_col, item)
            self.tableWidget_fluid_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_fluid_data.selectColumn(last_col)
        first_item = self.tableWidget_fluid_data.item(0, last_col)
        if self.refprop is None:
            self.load_state_properties_in_SI_units(last_col)
            self.tableWidget_fluid_data.editItem(first_item)

        self.tableWidget_fluid_data.blockSignals(False)

        app().processEvents()
        self.set_scroll_bar_to_maximum()

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.fluids_from_library):
            # if it is the last item and a not an already configured
            # fluid, just remove the last line
            current_size = self.tableWidget_fluid_data.columnCount()
            self.tableWidget_fluid_data.setColumnCount(current_size - 1)
            
            self._update_size_policy()
            self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)
            return

        item = self.tableWidget_fluid_data.item(1, selected_column)
        identifier = int(item.text())
        fluid = self.fluids_from_library.get(identifier)

        self.remove_fluid_from_file(fluid)
        self._update_size_policy()

        self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)

    def duplicate_selected_fluid(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return
        
        self.refprop = None
        item = self.tableWidget_fluid_data.item(1, selected_column)
        if item.text() == "":
            return

        identifier = int(item.text())
        fluid = self.fluids_from_library.get(identifier)
        if not isinstance(fluid, Fluid):
            return

        dfluid = deepcopy(fluid)
        dfluid.identifier = self.new_identifier()
        dfluid.name = self.get_suffix_for_duplicated_fluid(dfluid.name)

        fluid_data = dfluid.__dict__

        if self.add_fluid_data_in_file([fluid_data]):
            return

        self.load_data_from_fluids_library()

        app().processEvents()
        self.set_scroll_bar_to_maximum()

    def get_suffix_for_duplicated_fluid(self, fluid_name: str) -> str:

        already_used_names = set()
        for fluid in self.fluids_from_library.values():
            fluid: Fluid
            if fluid_name in fluid.name:
                already_used_names.add(fluid.name)

        for i in count(1):

            new_suffix = f"({i})"
            pattern = r'\s?\(\d+\)$'

            if re.search(pattern, fluid_name):
                new_name = re.sub(pattern, f" {new_suffix}", fluid_name)
            else:
                new_name = f"{fluid_name.strip()} {new_suffix}"

            if new_name not in already_used_names:
                return new_name

    def set_scroll_bar_to_maximum(self):
        scroll_bar = self.tableWidget_fluid_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def item_changed_callback(self, item: QTableWidgetItem):

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

        fluid_data = self.get_fluid_data_for_selected_column(item.column())
        if fluid_data is None:
            self.tableWidget_fluid_data.blockSignals(False)
            return

        if self.add_fluid_data_in_file([fluid_data]):
            self.tableWidget_fluid_data.blockSignals(False)
            return

        self.load_data_from_fluids_library()

        self.tableWidget_fluid_data.blockSignals(False)
        self.tableWidget_fluid_data.horizontalScrollBar().setSliderPosition(0)
    
    def go_to_next_cell(self, item):

        row = item.row()
        column = item.column()

        if row < self.COLOR_ROW - 1:
            next_item = self.tableWidget_fluid_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_fluid_data.setCurrentItem(next_item)
                self.tableWidget_fluid_data.editItem(next_item)

        elif row == self.COLOR_ROW - 1:
            self.pick_color_for_item(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_fluid_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for fluid in self.fluids_from_library.values():
            if fluid.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_fluid_data.item(1, column)

        already_used_ids = set()
        for fluid in self.fluids_from_library.values():
            already_used_ids.add(fluid.identifier)
        
        if item.text() == "":
            return True
        
        try:
            if int(item.text()) in already_used_ids:
                item.setText("")
                return True
        except Exception:
            item.setText("")
            return True

    def column_has_empty_items(self, column):
        for row in range(self.COLOR_ROW + 1):

            item = self.tableWidget_fluid_data.item(row, column)
            if item is None:
                return True
            
            if row == self.COLOR_ROW:
                color = item.background().color().getRgb()
                if list(color) == 0:
                    return True

            elif item.text() == "":
                if row in [10, 11, 12]:
                    return False
                return True

        return False

    def item_is_invalid_number(self, item):

        if item is None:
            return True

        row = item.row()
        if row == self.COLOR_ROW:
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
            10 : "adiabatic_bulk_modulus",
            11 : "vapor_pressure",
            12 : "molar_mass"
            }

        if row not in prop_labels.keys():
            return True

        if item.text() in ["", "--"]:
            if row in [10, 11, 12]:
                return False
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
            PrintMessageInput([error_title, title, message])
            item.setText("")
            return True

        if value < 0:
            title = "Negative value not allowed"
            message = f"The value typed for '{prop_labels[row]}' must be a non-zero positive number."
            PrintMessageInput([error_title, title, message])
            item.setText("")
            return True

        return False

    def add_fluid_data_in_file(self, fluids_data: list[dict], from_refprop: bool=False):

        # read fluid library data from file
        fluid_library_data = app().project.file.read_fluid_library_from_file()

        # get list of new fluid identifiers
        identifiers = self.get_new_identifiers(len(fluids_data))

        for j, fluid_data in enumerate(fluids_data):
            filt_fluid_data = dict()

            # check all inputs before proceeding
            for key in self.fluid_data_keys:
                value = fluid_data.get(key)

                if value is None:
                    if key in ["vapor_pressure", "adiabatic_bulk_modulus"]:
                        continue

                    if key == "identifier" and from_refprop:
                        filt_fluid_data["identifier"] = identifiers[j]
                        continue

                    elif key == "color":
                        picked_color = self.pick_color()
                        if picked_color:
                            filt_fluid_data[key] = picked_color

                        continue

                    return True

                filt_fluid_data[key] = value

            # additionally, check all refprop inputs before proceeding    
            if from_refprop:
                for key in ["key_mixture", "molar_fractions"]:
                    value = fluid_data.get(key)
                    if value is None:
                        return True
                    filt_fluid_data[key] = value

            # fluid identifier
            identifier = filt_fluid_data.get("identifier")

            # add the new fluid data
            fluid_library_data[identifier] = filt_fluid_data

        # save the modified fluid data in file
        app().project.file.write_fluid_library_in_file(fluid_library_data)

    def get_fluid_data_for_selected_column(self, column: int):
        try:

            fluid_data = dict()
            for i, key in enumerate(self.fluid_data_keys):
                item = self.tableWidget_fluid_data.item(i, column)

                # ignore the empty entries for vapor pressure, 
                # adiabatic bulk modulus, and molar mass
                if item.row() in [10, 11, 12]:
                    if item.text() in ["", "--"]:
                        continue

                if key == "name":
                    fluid_data[key] = item.text()

                elif key == "color":
                    color = item.background().color().getRgb()
                    fluid_data[key] = list(color[:3])

                elif key == "identifier":
                    identifier = int(item.text())
                    fluid_data[key] = identifier

                else:
                    fluid_data[key] = float(item.text())

            if self.refprop is not None:
                fluid_data['key_mixture'] = self.refprop_fluids_data.get("key_mixture")
                fluid_data['molar_fractions'] = self.refprop_fluids_data.get("molar_fractions")
                fluid_data['molar_mass'] = round(self.refprop_fluids_data.get("molar_mass"), 6)

            return fluid_data
                    
        except Exception as error_log:
            title = "Error while writing fluid data in file"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return None

    def remove_fluid_from_file(self, fluid: Fluid):

        # read fluid library data from file
        fluid_library_data = app().project.file.read_fluid_library_from_file()

        str_fluid_id = str(fluid.identifier)
        if len(str_fluid_id in fluid_library_data.keys()) == 0:
            return

        # remove the selected fluid
        fluid_library_data.pop(str_fluid_id)

        # save the modified fluid data in file
        app().project.file.write_fluid_library_in_file(fluid_library_data)

        self.reset_fluid_from_lines(fluid.identifier)
        self.load_data_from_fluids_library()

    def cell_clicked_callback(self, row, col):
        if row == self.COLOR_ROW:
            self.pick_color_for_item(row, col)

    def cell_double_clicked_callback(self, row, col):

        try:
            identifier = int(self.tableWidget_fluid_data.item(1, col).text())
        except Exception:
            return

        selected_fluid = self.fluids_from_library.get(identifier)
        if not isinstance(selected_fluid, Fluid):
            return

        self.tableWidget_fluid_data.blockSignals(True)
        fluid_name = self.tableWidget_fluid_data.item(0, col).text()

        if fluid_name in self.fluid_name_to_refprop_data.keys():
            if self.refprop_interface_callback(selected_fluid = selected_fluid):
                self.tableWidget_fluid_data.blockSignals(False)
                return

        self.tableWidget_fluid_data.selectColumn(col)
        self.tableWidget_fluid_data.blockSignals(False)

    def right_click_callback(self, pos):
        menu = QMenu(self)
        export_action = menu.addAction("Export fluid")
        export_icon = QIcon(str(ICON_DIR / "common/save_as.png"))
        export_action.setIcon(export_icon)

        font = export_action.font()
        font.setPointSize(10)

        menu.setStyleSheet("""
            QMenu {
            border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 1px;
            }
            QMenu::item {
            margin-top: 6px;
            margin-right: 10px;
            margin-bottom: 6px;
            margin-left: 10px;
            }
            """)

        action = menu.exec_(self.tableWidget_fluid_data.viewport().mapToGlobal(pos))
        if action != export_action:
            return

        item = self.tableWidget_fluid_data.itemAt(pos)
        if not item:
            return

        col = item.column()
        self.tableWidget_fluid_data.selectColumn(col)

        _fluid_id = self.tableWidget_fluid_data.item(1, col).text()
        if _fluid_id != "":
            fluid_id = int(_fluid_id)

        fluid_data = self.properties.fluids_library.get(fluid_id)
        if not isinstance(fluid_data, Fluid):
            return

        extensions = ["json"]

        path = app().config.get_last_folder_for("export_data_folder")
        if path is None:
            last_path = Path().home()
        else:
            last_path = path

        file_path = FileDialogService.save_file(extensions, "Export fluid data", last_path)
        if file_path is None:
            return False

        app().project.file._write_file(file_path, fluid_data.as_dict())

    def get_new_identifiers(self, N: int):

        new_identifiers = list()
        already_used_ids = list(self.fluids_from_library.keys())
        for n in range(N):
            for i in count(1):
                if i not in already_used_ids:
                    already_used_ids.append(i)
                    new_identifiers.append(i)
                    break

        return new_identifiers

    def new_identifier(self):

        already_used_ids = set()
        for fluid in self.fluids_from_library.values():
            fluid: Fluid
            already_used_ids.add(fluid.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

    def pick_color(self):

        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        pick = PickColorInput()
        if not pick.complete:
            return list()

        return pick.color

    def pick_color_for_item(self, row, col):

        picked_color = self.pick_color()
        if not picked_color:
            return True

        self.set_color_to_item(row, col, picked_color)
        self.tableWidget_fluid_data.item(row, 0).setSelected(True)

    def set_color_to_item(self, row: int, col: int, rgb_color: list):
        item = QTableWidgetItem()
        item.setBackground(QColor(*rgb_color))
        item.setForeground(QColor(*rgb_color))
        self.tableWidget_fluid_data.setItem(row, col, item)

    def get_confirmation_to_proceed(self):

        title = "Fluids library resetting"
        message = "Would you like to reset the fluid library to default values?"

        buttons_config = {  
            "left_button_label" : "No", 
            "right_button_label" : "Yes",
            "left_button_size" : 80,
            "right_button_size" : 80,
            }

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

        # read fluid library data from file
        fluid_library_data = app().project.file.read_fluid_library_from_file()

        # get the fluid identifiers to be removed from properties
        fluid_identifiers = list()
        if isinstance(fluid_library_data, dict):
            fluid_identifiers = [int(fluid_id) for fluid_id in fluid_library_data.keys()]

        # reset the fluid library to default state
        default_fluid_library()

        if fluid_identifiers:
            self.reset_fluid_from_lines(fluid_identifiers)

        self.load_data_from_fluids_library()

    def reset_fluid_from_lines(self, fluid_identifiers: (int | list)):

        if isinstance(fluid_identifiers, int):
            fluid_identifiers = [fluid_identifiers]

        lines_to_remove_fluid = list()
        for line_id, data in self.properties.line_properties.items():
            fluid_id = data.get("fluid_id")
            if fluid_id is None:
                continue

            if fluid_id in fluid_identifiers:
                if line_id not in lines_to_remove_fluid:
                    lines_to_remove_fluid.append(line_id)

        if not lines_to_remove_fluid:
            return

        self.properties._remove_line_property("fluid_id", lines_to_remove_fluid)
        self.properties._remove_line_property("fluid", lines_to_remove_fluid)
        app().project.model.preprocessor.set_fluid_by_lines(lines_to_remove_fluid, None)

        app().project.file.write_line_properties_in_file()
        app().main_window.set_selection()

    def refprop_interface_callback(self, selected_fluid: Fluid | None = None):

        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        self.refprop = SetFluidCompositionInput(
            fluid_to_edit = selected_fluid,
            state_properties = self.state_properties,
            )

        if app().main_window.force_close:
            self.dialog.close()
            return True
        
        if not self.refprop.complete:
            self.refprop = None
            app().main_window.set_input_widget(self)
            return True

        self.postproc_refprop_fluid_properties()
        self.refprop = None

    def postproc_refprop_fluid_properties(self):

        if not self.refprop.complete:
            return

        refprop_fluids_data = deepcopy(self.refprop.refprop_fluids_data)
        fluid_properties = self.refprop.fluid_properties

        if refprop_fluids_data.get("thermodynamic_states") == "multiple_states":
            fluids_data = list(fluid_properties.values())
        else:
            fluids_data = [fluid_properties]

        if self.add_fluid_data_in_file(fluids_data, from_refprop=True):
            return

        self.load_data_from_fluids_library()

        app().processEvents()
        self.set_scroll_bar_to_maximum()

        self.tableWidget_fluid_data.blockSignals(False)

        self.load_state_properties_info()
        self.refprop = None

        if self.state_properties:
            if isinstance(self.dialog, QDialog):
                last_col = self.tableWidget_fluid_data.columnCount()
                self.dialog.tableWidget_fluid_data.selectColumn(last_col-1)

    def load_state_properties_info(self):

        if self.state_properties:

            source = self.state_properties.get("source", None)
            if source is None:
                return

            if isinstance(self.dialog, QDialog):

                line_id = self.state_properties.get("line_id", None)
                if isinstance(line_id, int):

                    app().main_window.set_selection(lines=[line_id])

                    if self.fluid_data_refprop:
                        column = self.tableWidget_fluid_data.columnCount()
                        self.tableWidget_fluid_data.selectColumn(column - 1)

                    connection_type = self.state_properties['connection_type']
                    if source == "reciprocating_pump":
                        title = f"Set a fluid for the reciprocating pump ({connection_type})"
                    
                    elif source == "reciprocating_compressor":
                        title = f"Set a fluid for the reciprocating compressor ({connection_type})"

                    self.dialog.setWindowTitle(title)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if isinstance(self.dialog, QDialog):
                self.dialog.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_selected_column()

        elif event.key() == Qt.Key_Escape:
            if isinstance(self.dialog, QDialog):
                self.dialog.close()
            else:
                self.close()