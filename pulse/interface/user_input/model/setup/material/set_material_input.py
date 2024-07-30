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

        self.main_window = app().main_window
        self.opv = app().main_window.opv_widget
        app().main_window.input_ui.set_input_widget(self)
        self.project = app().project
        self.file = self.project.file
        
        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._loading_info_at_start()
        self.exec()

    def _load_icons(self):
        self.icon = app().main_window.pulse_icon

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set material")
        self.setWindowIcon(self.icon)

    def _initialize(self):
        self.selected_row = None
        self.material = None
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.material_path = self.project.get_material_list_path()
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

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
        self.main_window.selection_changed.connect(self.update_selection)
        self.comboBox_attribution_type.currentIndexChanged.connect(self.update_attribution_type)
        self.pushButton_attribute_material.clicked.connect(self.confirm_material_attribution)
        # self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_material_data.cellDoubleClicked.connect(self.on_cell_double_clicked)

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

    def update_attribution_type(self):
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)
        elif index == 1:
            lines_ids = self.main_window.selected_entities
            self.write_ids(lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def update_selection(self):
        lines_ids = self.main_window.selected_entities

        if lines_ids:
            self.write_ids(lines_ids)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)
        else:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.comboBox_attribution_type.setCurrentIndex(0)

    def _loading_info_at_start(self):
        self.update_selection()
        # if self.cache_selected_lines != []:
        #     # self.lines_ids = self.cache_selected_lines
        #     self.update_selection()
        # else:
        #     self.update()        

    def update(self):
        # self.lines_ids = self.opv.getListPickedLines()
        self.update_selection()

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
                self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 
                               
                self.project.set_material_by_lines(self.lines_typed, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_typed, self.material.getNormalizedColorRGB())
            else:
                self.project.set_material_to_all_lines(self.material)       
                print("[Set Material] - {} defined in all entities".format(self.material.name))
                # self.opv.changeColorEntities(entities, self.material.getNormalizedColorRGB())
            self.actions_to_finalize()

        except Exception as error_log:
            self.title = "Error detected on material list data"
            self.message = str(error_log)
            PrintMessageInput([window_title_1, self.title, self.message])
            return

    def actions_to_finalize(self):
        build_data = self.file.get_segment_build_data_from_file()
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