from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.material.material_widget import MaterialInputs
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class SetMaterialInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/material/set_material.ui"
        uic.loadUi(ui_path, self)

        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self.attribution_type_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Set material")

    def _initialize(self):

        self.material = None
        self.selected_row = None
        self.keep_window_open = True

        self.before_run = app().project.get_pre_solution_model_checks()

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
        self.material_widget.load_data_from_materials_library()
        self.grid_layout.addWidget(self.material_widget)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute_material.clicked.connect(self.material_attribution_callback)
        #
        # self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_material_data.cellDoubleClicked.connect(self.on_cell_double_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def attribution_type_callback(self):

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
        self.material_attribution_callback()

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

    def material_attribution_callback(self):

        selected_material = self.material_widget.get_selected_material()
        if selected_material is None:
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([window_title_1, self.title, self.message])
            return

        try:

            if self.comboBox_attribution_type.currentIndex():

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
                if self.stop:
                    return True

                print("[Set Material] - {} defined in the entities {}".format(selected_material.name, line_ids))

            else:

                line_ids = list(app().project.model.mesh.lines_from_model.keys())
                print("[Set Material] - {} defined in all entities".format(selected_material.name))

            app().project.model.preprocessor.set_material_by_lines(line_ids, selected_material)
            self.properties._set_line_property("material_id", selected_material.identifier, line_ids)
            self.properties._set_line_property("material", selected_material, line_ids)
            app().pulse_file.write_line_properties_in_file()

            geometry_handler = GeometryHandler()
            geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
            geometry_handler.process_pipeline()
            self.close()
            # self.actions_to_finalize()

        except Exception as error_log:
            self.title = "Error detected on material list data"
            self.message = str(error_log)
            PrintMessageInput([window_title_1, self.title, self.message])
            return

    def actions_to_finalize(self):
        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(app().project.model.preprocessor.length_unit)
        geometry_handler.process_pipeline()
        self.close()

    def load_project(self):
        app().project.initial_load_project_actions()
        # app().project.load_project_files()
        app().loader.load_project_data()
        app().main_window.input_ui.initial_project_action(True)
        self.complete = True

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