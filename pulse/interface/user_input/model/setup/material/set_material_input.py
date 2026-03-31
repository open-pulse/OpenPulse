from PySide6.QtWidgets import QGridLayout
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.material.set_material_ui import SetMaterial_UI
from pulse.interface.user_input.model.setup.material.material_widget import MaterialWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput


from enum import IntEnum

class AssignmentType(IntEnum):
    ALL_LINES = 0
    SELECTED_LINES = 1


error_title = "Error"


class SetMaterialInput(SetMaterial_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.cache_selected_lines = kwargs.get("cache_selected_lines", list())

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Set material")

    def _initialize(self):

        self.material = None
        self.selected_column = None
        self.keep_window_open = True

        self.before_run = app().project.get_pre_solution_model_checks()

    def _define_qt_variables(self):
        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_input_widget()
        self.scrollArea_table_of_materials.adjustSize()

        # QPushButton
        self.pushButton_attribute = self.material_widget.pushButton_attribute
        self.pushButton_exit = self.material_widget.pushButton_exit

        # QTableWidget
        self.tableWidget_material_data = self.material_widget.tableWidget_material_data

    def _add_material_input_widget(self):
        self.material_widget = MaterialWidget(dialog=self)
        self.material_widget.load_data_from_materials_library()
        self.grid_layout.addWidget(self.material_widget)

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        #
        # self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)
        # self.tableWidget_material_data.cellDoubleClicked.connect(self.on_cell_double_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.comboBox_attribution_type.blockSignals(True)
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:
            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)

            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.SELECTED_LINES)

        else:

            if self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_LINES:
                self.attribution_type_callback()
            else:
                self.lineEdit_selected_id.setText("")

        self.comboBox_attribution_type.blockSignals(False)

    def attribution_type_callback(self):

        all_lines = self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_LINES
        if all_lines:
            self.lineEdit_selected_id.setText("All lines")
        else:
            self.selection_callback()

        self.lineEdit_selected_id.setEnabled(all_lines)

    # def on_cell_clicked(self, row, col):
    #     self.selected_column = col
    #     self.update_material_selection()

    # def on_cell_double_clicked(self, row, col):
    #     self.selected_column = col
    #     self.attribute_callback()

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.selected_column = current_col
        self.update_material_selection()

    def update_material_selection(self):

        if self.selected_column is None:
            return

        item = self.tableWidget_material_data.item(0, self.selected_column)
        if item is None:
            return

        material_name = item.text()
        self.lineEdit_selected_material_name.setText("")
        if material_name != "":
            self.lineEdit_selected_material_name.setText(material_name)

    def attribute_callback(self):

        selected_material = self.material_widget.get_selected_material()
        if selected_material is None:
            self.hide()
            self.title = "No materials selected"
            self.message = "Select a material in the list before confirming the material attribution."
            PrintMessageInput([error_title, self.title, self.message])
            app().main_window.set_input_widget(self)
            return

        all_lines_assignment = self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_LINES

        if all_lines_assignment:
            line_ids = app().project.model.mesh.lines_from_model

        else:
            lineEdit = self.lineEdit_selected_id.text()
            self.stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True 

        app().project.model.preprocessor.set_material_by_lines(line_ids, selected_material)
        self.properties._set_line_property("material_id", selected_material.identifier, line_ids)
        self.properties._set_line_property("material", selected_material, line_ids)
        app().project.file.write_line_properties_in_file()

        geometry_handler = GeometryHandler(app().project)
        geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
        geometry_handler.process_pipeline()

        if all_lines_assignment:
            self.close()

        self.complete = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.material_widget.remove_selected_column()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)