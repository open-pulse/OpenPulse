from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.fluid.fluid_widget import FluidWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class SetFluidInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_input.ui"
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())
        self.compressor_thermodynamic_state = kwargs.get("compressor_thermodynamic_state", dict())

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
    
        self.attribution_type_callback()

        if self.compressor_thermodynamic_state:
            if self.fluid_widget.call_refprop_interface():
                return

            self.load_compressor_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.before_run = app().project.get_pre_solution_model_checks()

        self.keep_window_open = True

        self.fluid = None
        self.selected_column = None
        self.complete = False

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLineEdit
        self.lineEdit_selected_id = self.findChild(QLineEdit, 'lineEdit_selected_id')
        self.lineEdit_selected_fluid_name = self.findChild(QLineEdit, 'lineEdit_selected_fluid_name')

        # QScrollArea
        self.scrollArea_table_of_fluids : QScrollArea
        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)
        self._add_fluid_input_widget()
        self.frame_main_widget.adjustSize()

        # QPushButtonget_comboBox_index
        self.pushButton_attribute_fluid = self.findChild(QPushButton, 'pushButton_attribute_fluid')
        self.pushButton_remove_row = self.fluid_widget.findChild(QPushButton, 'pushButton_remove_row')

        # QTableWidget
        self.tableWidget_fluid_data = self.findChild(QTableWidget, 'tableWidget_fluid_data')

    def _add_fluid_input_widget(self):
        self.fluid_widget = FluidWidget(parent_widget=self, compressor_thermodynamic_state=self.compressor_thermodynamic_state)
        self.grid_layout.addWidget(self.fluid_widget)

    def load_compressor_info(self):
        self.fluid_widget.load_compressor_info()

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute_fluid.clicked.connect(self.fluid_attribution_callback)
        #
        # self.tableWidget_fluid_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        #
        # self.tableWidget_fluid_data.cellDoubleClicked.connect(self.on_cell_double_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.comboBox_attribution_type.blockSignals(True)
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:
            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

        self.comboBox_attribution_type.blockSignals(False)

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            self.selection_callback()

        self.lineEdit_selected_id.setEnabled(bool(index))

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_fluid_selection()

    def update_fluid_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_fluid_data.item(0, self.selected_column)
        if item is None:
            return

        fluid_name = item.text()
        self.lineEdit_selected_fluid_name.setText("")
        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

    def fluid_attribution_callback(self):

        selected_fluid = self.fluid_widget.get_selected_fluid()

        if selected_fluid is None:
            self.title = "No fluids selected"
            self.message = "Select a fluid in the list before confirming the fluid attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            if self.comboBox_attribution_type.currentIndex():

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
                if self.stop:
                    return True 

                print("[Set fluid] - {} defined in the entities {}".format(selected_fluid.name, line_ids))

            else:

                line_ids = list(app().project.model.mesh.lines_from_model.keys())
                print("[Set fluid] - {} defined in all entities".format(selected_fluid.name))
    
            app().project.model.preprocessor.set_fluid_by_lines(line_ids, selected_fluid)
            self.properties._set_line_property("fluid_id", selected_fluid.identifier, line_ids)
            self.properties._set_line_property("fluid", selected_fluid, line_ids)
            app().pulse_file.write_line_properties_in_file()

            # geometry_handler = GeometryHandler()
            # geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
            # geometry_handler.process_pipeline()

            self.complete = True
            self.close()

        except Exception as error_log:
            title = "Error detected on fluid list data"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.material_attribution_callback()
        elif event.key() == Qt.Key_Delete:
            self.material_widget.remove_selected_column()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)