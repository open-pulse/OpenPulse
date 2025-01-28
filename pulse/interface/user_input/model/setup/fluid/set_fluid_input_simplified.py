from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.model.setup.fluid.fluid_widget import FluidWidget
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetFluidInputSimplified(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_input_simplified.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model

        self.state_properties = kwargs.get("state_properties", None)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Set fluid")

    def _initialize(self):
        self.fluid = None
        self.selected_column = None
        self.complete = False
        self.keep_window_open = False

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_fluid_identifier = self.findChild(QLineEdit, 'lineEdit_fluid_identifier')
        self.lineEdit_selected_fluid_name = self.findChild(QLineEdit, 'lineEdit_selected_fluid_name')

        # QScrollArea
        self.scrollArea_table_of_fluids : QScrollArea
        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)
        self._add_fluid_input_widget()
        self.frame_main_widget.adjustSize()

        # QPushButton
        self.pushButton_attribute = self.findChild(QPushButton, 'pushButton_attribute')
        self.pushButton_remove_row = self.fluid_widget.findChild(QPushButton, 'pushButton_remove_row')

        # QTableWidget
        self.tableWidget_fluid_data = self.findChild(QTableWidget, 'tableWidget_fluid_data')

    def _create_connections(self):
        self.fluid_widget.pushButton_cancel.clicked.connect(self.close)
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_fluid_input_widget(self):
        self.fluid_widget = FluidWidget(parent_widget=self, state_properties=self.state_properties)
        self.grid_layout.addWidget(self.fluid_widget)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)

    def reset_fluid_library_callback(self):
        self.hide()
        self.fluid_widget.reset_library_callback()

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.setText("")

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_fluid_selection()

    def update_fluid_selection(self):

        if self.selected_column is None:
            return

        item_0 = self.tableWidget_fluid_data.item(0, self.selected_column)
        if item_0 is None:
            return
        else:
            fluid_name = item_0.text()
        
        item_1 = self.tableWidget_fluid_data.item(1, self.selected_column)
        if item_1 is None:
            return
        else:
            fluid_identifier = item_1.text()

        self.lineEdit_selected_fluid_name.setText("")
        self.lineEdit_fluid_identifier.setText("")

        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

        if fluid_identifier != "":
            self.lineEdit_fluid_identifier.setText(fluid_identifier)

    def get_selected_fluid(self):
        return self.fluid_widget.get_selected_fluid()
    
    def exec_and_keep_window_open(self):
        self.keep_window_open = True
        while self.keep_window_open:
            self.exec()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)