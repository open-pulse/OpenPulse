from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.model.setup.material.material_widget import MaterialWidget
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class SetMaterialSimplified(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/material/set_material_simplified.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

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
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_identifier = self.findChild(QLineEdit, 'lineEdit_identifier')
        self.lineEdit_selected_name = self.findChild(QLineEdit, 'lineEdit_selected_name')

        # QScrollArea
        self.scrollArea_table_of_materials : QScrollArea
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_input_widget()
        self.frame_main_widget.adjustSize()
        self.scrollArea_table_of_materials.adjustSize()

        # QPushButton
        # self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')
        # self.pushButton_remove_row = self.material_widget.findChild(QPushButton, 'pushButton_remove_row')

        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTableWidget, 'tableWidget_material_data')

    def _create_connections(self):
        self.material_widget.pushButton_cancel.clicked.connect(self.close)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_material_input_widget(self):
        self.material_widget = MaterialWidget()
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