from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QCloseEvent, QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.model.setup.general.fluid_widget import FluidWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetFluidInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_inputs.ui"
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        self.main_window = app().main_window
        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)
        self.file = self.project.file
        
        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._loading_info_at_start()

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
        self.fluid_widget = FluidWidget()
        self.grid_layout.addWidget(self.fluid_widget)

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _create_connections(self):
        # return
        # self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.pushButton_remove_row.clicked.connect(self.hide)
        # self.pushButton_attribute_fluid.clicked.connect(self.confirm_fluid_attribution)
        # self.tableWidget_fluid_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_fluid_data.cellDoubleClicked.connect(self.on_cell_double_clicked)

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
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)
        elif index == 1:
            self.write_ids(self.lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def update_selection(self):
        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)
        else:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)

    def _loading_info_at_start(self):
        if self.cache_selected_lines:
            self.lines_ids = self.cache_selected_lines
            self.update_selection()
        else:
            self.update()        

    def update(self):
        self.lines_ids = self.opv.getListPickedLines()
        self.update_selection()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)