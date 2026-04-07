from PySide6.QtWidgets import QGridLayout
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.fluid.set_fluid_input_simplified_ui import SetFluidInputSimplified_UI
from pulse.interface.user_input.model.setup.fluid.fluid_widget import FluidWidget


window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetFluidInputSimplified(SetFluidInputSimplified_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model

        self.state_properties = kwargs.get("state_properties", None)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

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
        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)
        self._add_fluid_input_widget()
        self.frame_main_widget.adjustSize()

        # QPushButton
        self.pushButton_attribute = self.fluid_widget.pushButton_attribute
        self.pushButton_exit = self.fluid_widget.pushButton_exit

        # QTableWidget
        self.tableWidget_fluid_data = self.fluid_widget.tableWidget_fluid_data

    def _create_connections(self):
        self.fluid_widget.pushButton_exit.clicked.connect(self.close)
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_fluid_input_widget(self):
        self.fluid_widget = FluidWidget(dialog=self, state_properties=self.state_properties)
        self.grid_layout.addWidget(self.fluid_widget)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)

    def reset_fluid_library_callback(self):
        self.hide()
        if self.fluid_widget.reset_library_callback():
            app().main_window.update_plots()

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.clear()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_fluid_selection()

    def update_fluid_selection(self):

        if self.selected_column is None:
            return

        item_name = self.tableWidget_fluid_data.item(0, self.selected_column)
        if item_name is None:
            return
        else:
            fluid_name = item_name.text()

        item_id = self.tableWidget_fluid_data.item(1, self.selected_column)
        if item_id is None:
            return
        else:
            fluid_identifier = item_id.text()

        self.lineEdit_selected_fluid_name.clear()
        self.lineEdit_fluid_identifier.clear()

        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

        self.lineEdit_fluid_identifier.setText("")
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