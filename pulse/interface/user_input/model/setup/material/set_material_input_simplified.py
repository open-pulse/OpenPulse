from PySide6.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.material.material_widget import MaterialWidget

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class SetMaterialSimplified(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/material/set_material_simplified.ui"
        load_ui(ui_path, self, UI_DIR)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        # while self.keep_window_open:
        #     self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Select the material")

    def _initialize(self):
        self.selected_column = None
        self.complete = False
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # QFrame
        self.frame_main_widget : QFrame

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_identifier : QLineEdit
        self.lineEdit_selected_name : QLineEdit

        # QScrollArea
        self.scrollArea_table_of_materials : QScrollArea
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_widget()
        self.frame_main_widget.adjustSize()
        self.scrollArea_table_of_materials.adjustSize()

        # # QPushButton
        # self.pushButton_attribute = self.material_widget.pushButton_attribute
        # self.pushButton_cancel = self.material_widget.pushButton_cancel

        # QTableWidget
        self.tableWidget_material_data = self.material_widget.tableWidget_material_data

    def _create_connections(self):
        self.material_widget.pushButton_cancel.clicked.connect(self.close)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_material_widget(self):
        self.material_widget = MaterialWidget(dialog=self)
        self.grid_layout.addWidget(self.material_widget)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)

    def reset_material_library_callback(self):
        self.hide()
        self.material_widget.reset_library_callback()

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_name.setText("")

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_material_selection()

    def update_material_selection(self):

        if self.selected_column is None:
            return

        item_0 = self.tableWidget_material_data.item(0, self.selected_column)
        if item_0 is None:
            return
        else:
            material_name = item_0.text()
        
        item_1 = self.tableWidget_material_data.item(1, self.selected_column)
        if item_1 is None:
            return
        else:
            material_identifier = item_1.text()

        self.lineEdit_selected_name.setText("")
        self.lineEdit_identifier.setText("")

        if material_name != "":
            self.lineEdit_selected_name.setText(material_name)

        if material_identifier != "":
            self.lineEdit_identifier.setText(material_identifier)

    def get_selected_material(self):
        return self.material_widget.get_selected_material()