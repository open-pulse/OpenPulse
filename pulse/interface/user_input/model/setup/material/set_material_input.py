from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.model.setup.material.material_widget import MaterialInputs
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

class SetMaterialInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/material/set_material.ui"
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.file = app().project.file
        
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Set material")

    def _initialize(self):
        self.selected_row = None
        self.material = None
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.material_path = self.project.get_material_list_path()
        self.lines_from_model = self.preprocessor.lines_from_model

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
        self.lineEdit_selected_material_name = self.findChild(QLineEdit, 'lineEdit_selected_material_name')

        # QScrollArea
        self.scrollArea_table_of_materials : QScrollArea
        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_input_widget()
        self.scrollArea_table_of_materials.adjustSize()

        # QPushButtonget_comboBox_index
        self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')

        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTableWidget, 'tableWidget_material_data')

    def _add_material_input_widget(self):
        self.material_widget = MaterialInputs()
        self.grid_layout.addWidget(self.material_widget)

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        #
        self.pushButton_attribute_material.clicked.connect(self.confirm_material_attribution)
        #
        # self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_material_data.cellDoubleClicked.connect(self.on_cell_double_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def update_attribution_type(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            self.selection_callback()

        self.lineEdit_selected_id.setEnabled(bool(index))

    def selection_callback(self):

        self.comboBox_attribution_type.blockSignals(True)
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:
            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

        self.comboBox_attribution_type.blockSignals(False)

    def on_cell_clicked(self, row, col):
        self.selected_row = row
        self.update_material_selection()

    def on_cell_double_clicked(self, row, col):
        self.selected_row = row
        self.confirm_material_attribution()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_row = current_row
        self.update_material_selection()

    def update_material_selection(self):
        if self.selected_row is None:
            return
        item = self.tableWidget_material_data.item(self.selected_row, 0)
        if item is None:
            return
        material_name = item.text()
        self.lineEdit_selected_material_name.setText("")
        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def confirm_material_attribution(self):

        new_material = self.material_widget.get_selected_material()
        if new_material is None:
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            self.material = new_material
            if self.comboBox_attribution_type.currentIndex():

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
                if self.stop:
                    return True 
                               
                self.project.set_material_by_lines(self.lines_typed, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))

            else:
                self.project.set_material_to_all_lines(self.material)       
                print("[Set Material] - {} defined in all entities".format(self.material.name))

            self.actions_to_finalize()

        except Exception as error_log:
            self.title = "Error detected on material list data"
            self.message = str(error_log)
            PrintMessageInput([window_title_1, self.title, self.message])
            return

    def actions_to_finalize(self):
        build_data = self.file.get_pipeline_data_from_file()
        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(self.file.length_unit)
        geometry_handler.process_pipeline(build_data)
        self.close()

    def load_project(self):
        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_ui.initial_project_action(True)
        self.complete = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_material_attribution()
        elif event.key() == Qt.Key_Delete:
            self.material_widget.remove_selected_row()
        elif event.key() == Qt.Key_Escape:
            self.close()