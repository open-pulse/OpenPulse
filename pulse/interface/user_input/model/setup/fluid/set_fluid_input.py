from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.model.setup.fluid.fluid_widget import FluidWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetFluidInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_input.ui"
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())
        self.compressor_thermodynamic_state = kwargs.get("compressor_thermodynamic_state", dict())

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window
        self.project = app().project
        self.file = self.project.file

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._loading_info_at_start()

        if self.compressor_thermodynamic_state:
            if self.fluid_widget.call_refprop_interface():
                return
            self.load_compressor_info()

        while self.keep_window_open:
            self.exec()

    def _load_icons(self):
        self.icon = app().main_window.pulse_icon

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Set fluid")

    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.fluid_path = self.project.get_fluid_list_path()
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

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

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _create_connections(self):
        self.main_window.selection_changed.connect(self.update_selection)
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.pushButton_attribute_fluid.clicked.connect(self.confirm_fluid_attribution)
        # self.tableWidget_fluid_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_fluid_data.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.update_attribution_type()

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

    def update_attribution_type(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            line_ids = self.main_window.selected_entities
            self.write_ids(line_ids)

        self.lineEdit_selected_id.setEnabled(bool(index))
        self.comboBox_attribution_type.setCurrentIndex(index)

    def write_ids(self, list_ids):

        if isinstance(list_ids, int):
            list_ids = [list_ids]

        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)

        self.lineEdit_selected_id.setText(text)

    def _loading_info_at_start(self):
        self.update_selection()    

    def update_selection(self):
        line_ids = self.main_window.selected_entities
        self.write_ids(line_ids)
        self.lineEdit_selected_id.setEnabled(True)
        self.comboBox_attribution_type.setCurrentIndex(1)

    def confirm_fluid_attribution(self):

        selected_fluid = self.fluid_widget.get_selected_fluid()

        if selected_fluid is None:
            self.title = "No fluids selected"
            self.message = "Select a fluid in the list before confirming the fluid attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            if self.comboBox_attribution_type.currentIndex():

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 

                self.project.set_fluid_by_lines(lines_typed, selected_fluid)
                print("[Set fluid] - {} defined in the entities {}".format(selected_fluid.name, lines_typed))

            else:
                self.project.set_fluid_to_all_lines(selected_fluid)       
                print("[Set fluid] - {} defined in all entities".format(selected_fluid.name))

            self.actions_to_finalize()

        except Exception as error_log:
            title = "Error detected on fluid list data"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return

    def actions_to_finalize(self):
        # build_data = self.file.get_segment_build_data_from_file()
        # geometry_handler = GeometryHandler()
        # geometry_handler.set_length_unit(self.file.length_unit)
        # geometry_handler.process_pipeline(build_data)
        self.complete = True
        self.close()

    # def load_project(self):
    #     self.project.initial_load_project_actions(self.file.project_ini_file_path)
    #     self.project.load_project_files()
    #     app().main_window.input_ui.initial_project_action(True)
    #     self.complete = True

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)