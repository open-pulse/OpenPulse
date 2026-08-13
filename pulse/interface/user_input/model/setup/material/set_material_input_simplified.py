from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout

from pulse import app
from pulse.interface.ui_generated.model.setup.material.set_material_simplified_ui import (
    SetMaterialSimplified_UI,
)
from pulse.interface.user_input.model.setup.material.material_widget import (
    MaterialWidget,
)


class SetMaterialSimplified(SetMaterialSimplified_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

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
        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.scrollArea_table_of_materials.setLayout(self.grid_layout)
        self._add_material_widget()
        self.frame_main_widget.adjustSize()
        self.scrollArea_table_of_materials.adjustSize()

        # # QPushButton
        # self.pushButton_attribute = self.material_widget.pushButton_attribute
        # self.pushButton_exit = self.material_widget.pushButton_exit

        # QTableWidget
        self.tableWidget_material_data = self.material_widget.tableWidget_material_data

    def _create_connections(self):
        self.material_widget.pushButton_exit.clicked.connect(self.close)
        self.material_widget.pushButton_reset_library.clicked.connect(self.reset_material_library_callback)
        self.tableWidget_material_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_material_widget(self):
        self.material_widget = MaterialWidget(dialog=self)
        self.grid_layout.addWidget(self.material_widget)
        self.material_widget.pushButton_remove_column.clicked.connect(self.reset_selected_material_lineEdit)

    def reset_material_library_callback(self):
        self.hide()
        if self.material_widget.reset_library_callback():
            app().main_window.update_plots(False)

    def reset_selected_material_lineEdit(self):
        self.lineEdit_selected_name.clear()

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

        self.lineEdit_selected_name.clear()
        self.lineEdit_identifier.clear()

        if material_name != "":
            self.lineEdit_selected_name.setText(material_name)

        if material_identifier != "":
            self.lineEdit_identifier.setText(material_identifier)

    def get_selected_material(self):
        return self.material_widget.get_selected_material()
