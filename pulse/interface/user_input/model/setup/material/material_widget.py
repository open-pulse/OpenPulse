from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize

from pulse import app
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.ui_generated.model.setup.material.material_input_widget_ui import MaterialInputWidget_UI
from pulse.libraries.default_libraries import default_material_library
from pulse.interface.formatters.icons import change_icon_color_for_widgets
from pulse.model.properties.material import Material

from copy import deepcopy
from itertools import count


error_title = "Error"


class MaterialWidget(MaterialInputWidget_UI):

    COLOR_ROW = 6

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.project = app().project
        self.properties = app().project.model.properties

        self.dialog = kwargs.get("dialog", None)

        self._initialize()
        self.create_connections()
        self._config_widgets()
        self._paint_icons()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _add_icon_and_title(self):
        self._config_window()

    def _initialize(self):

        self.preprocessor = self.project.model.preprocessor

        self.row = None
        self.col = None
        self.materials_from_library = dict()

        self.material_data_keys = [
            "name",
            "identifier",
            "density",
            "elasticity_modulus",
            "poisson_ratio",
            "thermal_expansion_coefficient",
            "color",
            ]

    def create_connections(self):
        #
        self.pushButton_add_column.clicked.connect(self.add_column)
        self.pushButton_duplicate.clicked.connect(self.duplicate_selected_material)
        self.pushButton_remove_column.clicked.connect(self.remove_selected_column)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        #
        self.tableWidget_material_data.itemChanged.connect(self.item_changed_callback)
        self.tableWidget_material_data.cellClicked.connect(self.cell_clicked_callback)

    def _config_widgets(self):
        self.tableWidget_material_data.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
    
    def _paint_icons(self):
        icon_color = None
        theme = app().config.user_preferences.interface_theme
        from pulse import LIGHT_ICON_COLOR, DARK_ICON_COLOR
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        widgets = [self.pushButton_duplicate]
        change_icon_color_for_widgets(widgets, icon_color)

    def _update_size_policy(self):
        if len(self.materials_from_library) > 6:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            self.tableWidget_material_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_data_from_materials_library(self):

        self.materials_from_library.clear()
        materials_from_library = app().project.loader.load_materials_library()

        if materials_from_library is None:
            self.reset_library_to_default()
            return

        elif isinstance(materials_from_library, dict):
            if not materials_from_library:
                self.reset_library_to_default()
                return

        self.materials_from_library = materials_from_library

        self.properties.set_materials_library(self.materials_from_library)
        self.update_table_of_materials()

    def update_table_of_materials(self):

        self.tableWidget_material_data.clearContents()
        self.tableWidget_material_data.blockSignals(True)
        self.tableWidget_material_data.setRowCount(self.COLOR_ROW + 1)
        self.tableWidget_material_data.setColumnCount(len(self.materials_from_library))

        for j, material in enumerate(self.materials_from_library.values()):
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
                item.setSizeHint(QSize(80, 30))
                self.tableWidget_material_data.setItem(6, j, item)

        for i in range(self.tableWidget_material_data.rowCount()):
            for j in range(self.tableWidget_material_data.columnCount()):
                self.tableWidget_material_data.item(i, j).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.blockSignals(False)

        self._update_size_policy()

    def get_selected_column(self) -> int:
        selected_items = self.tableWidget_material_data.selectedIndexes()
        if not selected_items:
            return -1
        return selected_items[-1].column()

    def get_selected_material(self) -> Material | None:
        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.materials_from_library):
            return
        
        item = self.tableWidget_material_data.item(1, selected_column)
        material_id  = int(item.text())

        return self.materials_from_library[material_id]

    def add_column(self):
    
        self.tableWidget_material_data.blockSignals(True)

        table_size = self.tableWidget_material_data.columnCount()
        if table_size > len(self.materials_from_library):
            # it means that if you already have a new row
            # to insert data you don't need another one
            self.tableWidget_material_data.blockSignals(False)
            return 

        last_col = self.tableWidget_material_data.columnCount()
        self.tableWidget_material_data.insertColumn(last_col)

        for i in range(self.tableWidget_material_data.rowCount()):
            item = QTableWidgetItem()
            item.setSizeHint(QSize(100, 30))
            self.tableWidget_material_data.setItem(i, last_col, item)
            self.tableWidget_material_data.item(i, last_col).setTextAlignment(Qt.AlignCenter)

        self.tableWidget_material_data.selectColumn(last_col)
        first_item = self.tableWidget_material_data.item(0, last_col)
        self.tableWidget_material_data.blockSignals(False)

    def remove_selected_column(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return

        if selected_column >= len(self.materials_from_library):
            # if it is the last item and a not an already configured
            # material, just remove the last line
            current_size = self.tableWidget_material_data.columnCount()
            self.tableWidget_material_data.setColumnCount(current_size - 1)

            self._update_size_policy()
            self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)
            return

        item = self.tableWidget_material_data.item(1, selected_column)
        identifier = int(item.text())
        material = self.materials_from_library.get(identifier)

        self.remove_material_from_file(material)
        self._update_size_policy()

        self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)

    def duplicate_selected_material(self):

        selected_column = self.get_selected_column()
        if selected_column < 0:
            return
        
        self.refprop = None
        item_identifier = self.tableWidget_material_data.item(1, selected_column)
        if item_identifier.text() == "":
            return

        identifier = int(item_identifier.text())
        material = self.materials_from_library.get(identifier)
        if not isinstance(material, Material):
            return

        dmaterial = deepcopy(material)
        dmaterial.identifier = self.new_identifier()
        dmaterial.name = self.get_suffix_for_duplicated_material(dmaterial.name)

        if self.add_material_data_in_file(dmaterial.__dict__):
            return

        self.load_data_from_materials_library()

        app().processEvents()
        self.set_scroll_bar_to_maximum()

    def get_suffix_for_duplicated_material(self, material_name: str):

        already_used_names = set()
        for material in self.materials_from_library.values():
            material: Material
            if material_name in material.name:
                already_used_names.add(material.name)

        for i in count(1):
            new_name = f"{material_name} ({i})"
            if new_name not in already_used_names:
                return new_name

    def set_scroll_bar_to_maximum(self):
        scroll_bar = self.tableWidget_material_data.horizontalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.minimum())
        app().processEvents()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

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

        self.add_material_data_in_file(item.column())
        self.load_data_from_materials_library()

        self.tableWidget_material_data.blockSignals(False)
        self.tableWidget_material_data.horizontalScrollBar().setSliderPosition(0)

    def go_to_next_cell(self, item : QTableWidgetItem):

        row = item.row()
        column = item.column()

        if row < self.COLOR_ROW - 1:
            next_item = self.tableWidget_material_data.item(row + 1, column)
            if next_item.text() == "":
                self.tableWidget_material_data.setCurrentItem(next_item)
                self.tableWidget_material_data.editItem(next_item)

        elif row == self.COLOR_ROW - 1:
            self.pick_color(row + 1, column)

    def column_has_invalid_name(self, column):

        item = self.tableWidget_material_data.item(0, column)
        if item is None:
            return True

        column_name = item.text()

        if not column_name:
            return True

        for material in self.materials_from_library.values():
            if material.name == column_name:
                return True

        return False 

    def column_has_invalid_identifier(self, column):

        item = self.tableWidget_material_data.item(1, column)

        already_used_ids = set()
        for material in self.materials_from_library.values():
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
        for row in range(self.COLOR_ROW + 1):

            item = self.tableWidget_material_data.item(row, column)
            if item is None:
                return True
            
            if row == self.COLOR_ROW:
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
        if row == self.COLOR_ROW:
            return

        prop_labels = {
            2 : "density",
            3 : "elasticity_modulus",
            4 : "poisson_ratio",
            5 : "thermal_expansion_coefficient",
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

    def cell_clicked_callback(self, row, col):
        if row == self.COLOR_ROW:
            self.pick_color(row, col)

    def add_material_data_in_file(self, material_data: dict):

        # check all inputs before proceeding
        for key in self.material_data_keys:
            value = material_data.get(key)
            if value is None:
                return True

        # material identifier
        identifier = material_data.get("identifier")

        # read material library data from file
        material_library_data = app().project.file.read_material_library_from_file()
        
        # add the new material data
        material_library_data[identifier] = material_data

        # save the modified material data in file
        app().project.file.write_material_library_in_file(material_library_data)

    def remove_material_from_file(self, material: Material):

        # read material library data from file
        material_library_data = app().project.file.read_material_library_from_file()

        str_material_id = str(material.identifier)
        if not str_material_id in material_library_data.keys():
            return

        # remove the selected material
        material_library_data.pop(str_material_id)

        # save the modified material data in file
        app().project.file.write_material_library_in_file(material_library_data)

        self.reset_material_from_lines(material.identifier)
        self.load_data_from_materials_library()

    def reset_material_from_lines(self, material_identifiers: (list | int)):

        if isinstance(material_identifiers, int):
            material_identifiers = [material_identifiers]

        lines_to_remove_material = list()
        for line_id, data in self.properties.line_properties.items():
            material_id = data.get("material_id")
            if material_id is None:
                continue

            if material_id in material_identifiers:
                if line_id not in lines_to_remove_material:
                    lines_to_remove_material.append(line_id)

        if not lines_to_remove_material:
            return

        self.properties._remove_line_property("material_id", lines_to_remove_material)
        self.properties._remove_line_property("material", lines_to_remove_material)
        app().project.model.preprocessor.set_material_by_lines(lines_to_remove_material, None)

        app().project.file.write_line_properties_in_file()
        app().main_window.set_selection()

    def new_identifier(self):
        already_used_ids = set()
        for material in self.materials_from_library.values():
            already_used_ids.add(material.identifier)

        for i in count(1):
            if i not in already_used_ids:
                return i

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

        # read material library data from file
        material_library_data = app().project.file.read_material_library_from_file()

        # get the material identifiers to be removed from properties
        material_identifiers = list()
        if isinstance(material_library_data, dict):
            material_identifiers = [int(material_id) for material_id in material_library_data.keys()]

        # reset the material library to default state
        default_material_library()

        if material_identifiers:
            self.reset_material_from_lines(material_identifiers)

        self.load_data_from_materials_library()

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

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False