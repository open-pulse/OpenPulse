from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR, TEMP_PROJECT_FILE

from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from pulse.libraries.default_libraries import default_material_library
from pulse.model.properties.material import Material

from itertools import count
import os

window_title_1 = "Error"
window_title_2 = "Warning"

COLOR_ROW = 6

def get_color_rgb(color):
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
        self.properties = app().project.model.properties

        self._initialize()
        self.define_qt_variables()
        self.create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _add_icon_and_title(self):
        self._config_window()

    def _initialize(self):

        self.preprocessor = self.project.preprocessor

        self.row = None
        self.col = None
        self.library_materials = dict()

        self.material_data_keys = [
                                    "name",
                                    "identifier",
                                    "density",
                                    "elasticity_modulus",
                                    "poisson_ratio",
                                    "thermal_expansion_coefficient",
                                    "color"
                                    ]

    def define_qt_variables(self):

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_add_column: QPushButton
        self.pushButton_remove_column: QPushButton
        self.pushButton_reset_library: QPushButton

        # QTableWidget
        self.tableWidget_material_data: QTableWidget

    def create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)

    def config_table_of_material_data(self):
        return
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

        if not os.path.exists(TEMP_PROJECT_FILE):
            self.reset_library_to_default()
            return

        config = app().pulse_file.read_material_library_from_file()
        if config is None:
            self.reset_library_to_default()
            return

        self.library_materials.clear()

        if not list(config.sections()):
            self.update_table()
            return

        for tag in config.sections():
            section = config[tag]
            material = Material(
                                name = section['name'],
                                identifier = int(section['identifier']),
                                density = float(section['density']),
                                poisson_ratio = float(section['poisson_ratio']),
                                elasticity_modulus = float(section['elasticity_modulus']) * 1e9,
                                thermal_expansion_coefficient = float(section['thermal_expansion_coefficient']), 
                                color = get_color_rgb(section['color'])
                                )

            self.library_materials[int(tag)] = material

        self.update_table()

    def update_table(self):

        self.config_table_of_material_data()
        self.tableWidget_material_data.clearContents()
        self.tableWidget_material_data.blockSignals(True)
        self.tableWidget_material_data.setRowCount(COLOR_ROW + 1)
        self.tableWidget_material_data.setColumnCount(len(self.library_materials))

        for j, material in enumerate(self.library_materials.values()):
            if isinstance(material, Material):

                self.tableWidget_material_data.setItem(0, j, QTableWidgetItem(str(material.name)))
                self.tableWidget_material_data.setItem(1, j, QTableWidgetItem(str(material.identifier)))
                self.tableWidget_material_data.setItem(2, j, QTableWidgetItem(str(material.density)))
                self.tableWidget_material_data.setItem(3, j, QTableWidgetItem(f"{material.elasticity_modulus/1e9 :.2f}"))
                self.tableWidget_material_data.setItem(4, j, QTableWidgetItem(str(material.poisson_ratio)))
                self.tableWidget_material_data.setItem(5, j, QTableWidgetItem(str(material.thermal_expansion_coefficient)))

                item = QTableWidgetItem()
                item.setBackground(QColor(*material.color))
                item.setForeground(QColor(*material.color))
                self.tableWidget_material_data.setItem(6, j, item)

        for i in range(self.tableWidget_material_data.rowCount()):
            for j in range(self.tableWidget_material_data.columnCount()):
                self.tableWidget_material_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.blockSignals(False)

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_material_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_material(self) -> Material | None:
        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.library_materials):
            return
        
        item = self.tableWidget_material_data.item(1, selected_column)
        material_id  = int(item.text())

        return self.library_materials[material_id]

    def add_column(self):
    
        self.tableWidget_material_data.blockSignals(True)

        table_size = self.tableWidget_material_data.columnCount()
        if table_size > len(self.library_materials):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_material_data.blockSignals(False)
            return 

        last_col = self.tableWidget_material_data.columnCount()
        self.tableWidget_material_data.insertColumn(last_col)

        for i in range(self.tableWidget_material_data.rowCount()):
            item = QTableWidgetItem()
            self.tableWidget_material_data.setItem(i, last_col, item)
            self.tableWidget_material_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.selectColumn(last_col)
        first_item = self.tableWidget_material_data.item(0, last_col)
        self.tableWidget_material_data.blockSignals(False)

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.library_materials):
            # if it is the last item and a not an already configured
            # material, just remove the last line
            current_size = self.tableWidget_material_data.columnCount()
            self.tableWidget_material_data.setColumnCount(current_size - 1)
            return

        material = self.library_materials[selected_column]
        self.remove_material_from_file(material)
    
    def item_changed_callback(self, item : QTableWidgetItem):

        self.tableWidget_material_data.blockSignals(True)

        if item.row() == 0:
            if self.column_has_invalid_name(item.column()):
                self.tableWidget_material_data.blockSignals(False)
                return

        elif item.row() == 1:
            if self.column_has_invalid_identifier(item.column()):
                self.tableWidget_material_data.blockSignals(False)
                return

        else:
            if self.item_is_invalid_number(item):
                self.tableWidget_material_data.blockSignals(False)
                return

        self.go_to_next_cell(item)
        if self.column_has_empty_items(item.column()):
            self.tableWidget_material_data.blockSignals(False)
            return

        self.add_material_to_file(item.column())
        self.load_data_from_materials_library()

        self.tableWidget_material_data.blockSignals(False)

    def go_to_next_cell(self, item : QTableWidgetItem):

        row = item.row()
        column = item.column()

        if row < COLOR_ROW - 1:
            next_item = self.tableWidget_material_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_material_data.setCurrentItem(next_item)
                self.tableWidget_material_data.editItem(next_item)

        elif row == COLOR_ROW - 1:
            self.pick_color(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_material_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for material in self.library_materials:
            if material.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_material_data.item(1, column)

        already_used_ids = set()
        for material in self.library_materials:
            already_used_ids.add(material.identifier)
        
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

            item = self.tableWidget_material_data.item(row, column)
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
                        2 : "density", 
                        3 : "elasticity_modulus",
                        4 : "poisson_ratio",
                        5 : "thermal_expansion_coefficient"
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

    def cell_clicked_callback(self, row, col):
        if row == COLOR_ROW:
            self.pick_color(row, col)

    def add_material_to_file(self, column):
        try:

            material_data = dict()

            for i, key in enumerate(self.material_data_keys):
                item = self.tableWidget_material_data.item(i, column)
                if key == "color":
                    color = item.background().color().getRgb()
                    material_data[key] = list(color[:3])
                else:
                    material_data[key] = item.text()

            # material_data["identifier"] = self.new_identifier()

            material_name = material_data["name"]
            if not material_name:
                return

            config = app().pulse_file.read_material_library_from_file()
            config[material_name] = material_data

            app().pulse_file.write_material_library_in_file(config)
 
        except Exception as error_log:
            title = "Error while writing material data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True

    def remove_material_from_file(self, material : Material):

        config = app().pulse_file.read_material_library_from_file()

        identifier = str(material.identifier)
        if not identifier in config.sections():
            return
        
        self.reset_material_from_lines([identifier])
        config.remove_section(identifier)

        app().pulse_file.write_material_library_in_file(config)
        self.load_data_from_materials_library()

    def reset_material_from_lines(self, material_identifiers: list):

        lines_to_remove_material = list()
        for line_id, data in self.properties.line_properties.items():
            if "material_id" in data.keys():
                material_id = data["material_id"]
                if material_id in material_identifiers:
                    app().project.model.preprocessor.set_material_by_lines(line_id, None)
                    if material_id not in lines_to_remove_material:
                        lines_to_remove_material.append(line_id)

        for _line_id in lines_to_remove_material:
            self.properties._remove_line_property("material_id", line_id=_line_id)
            self.properties._remove_line_property("material", line_id=_line_id)

        app().pulse_file.write_line_properties_in_file()

    def new_identifier(self):
        already_used_ids = set()
        for material in self.library_materials:
            already_used_ids.add(material.identifier)

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
        self.tableWidget_material_data.setItem(row, col, item)
        self.tableWidget_material_data.item(row, 0).setSelected(True)

    def get_selected_material_id(self):
        material = self.get_selected_material()
        if material is None:
            return None
        return material.identifier

    def get_confirmation_to_proceed(self):

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

    def reset_library_callback(self):
        if self.get_confirmation_to_proceed():
            self.reset_library_to_default()
            return True
        return False

    def reset_library_to_default(self):

        config_cache = app().pulse_file.read_material_library_from_file()

        sections_cache = list()
        if config_cache is not None:
            sections_cache = config_cache.sections()

        default_material_library()

        config = app().pulse_file.read_material_library_from_file()

        material_identifiers = list()
        for section_cache in sections_cache:
            if section_cache not in config.sections():
                identifier = config_cache[section_cache]["identifier"]
                material_identifiers.append(int(identifier))

        self.reset_material_from_lines(material_identifiers)
        self.load_data_from_materials_library()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        elif event.key() == Qt.Key_Delete:
            self.remove_selected_column()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False