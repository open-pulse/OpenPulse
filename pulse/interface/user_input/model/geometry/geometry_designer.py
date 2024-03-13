from PyQt5.QtWidgets import QPushButton, QStackedWidget, QTabWidget, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.geometry.add_widget import AddStructuresWidget
from pulse.interface.user_input.model.geometry.edit_bend_widget import EditBendWidget
from pulse.interface.user_input.model.geometry.edit_point_widget import EditPointWidget
from pulse.interface.user_input.model.geometry.edit_pipe_widget import EditPipeWidget
from pulse.tools.utils import get_new_path

from opps.model import Pipe, Bend


class OPPGeometryDesignerInput(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "model/geometry/geometry_designer_tabs.ui", self)

        self.geometry_widget = geometry_widget
        self.geometry_handler = GeometryHandler()

        self.project = app().project
        self.file = self.project.file

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self.setContentsMargins(2,2,2,2)

    def _define_qt_variables(self):
        self.pushButton_cancel: QPushButton
        self.pushButton_finalize: QPushButton
        self.edit_stack: QStackedWidget
        self.tab_widget: QTabWidget       
        self.add_tab: QWidget
        self.edit_tab: QWidget
        self.empty_widget: QWidget

    def _create_layout(self):

        self.add_widget = AddStructuresWidget(self.geometry_widget)
        self.edit_pipe_widget = EditPipeWidget(self.geometry_widget)
        self.edit_bend_widget = EditBendWidget(self.geometry_widget)
        self.edit_point_widget = EditPointWidget(self.geometry_widget)

        self.add_tab.layout().addWidget(self.add_widget)
        self.edit_stack.addWidget(self.edit_pipe_widget)
        self.edit_stack.addWidget(self.edit_bend_widget)
        self.edit_stack.addWidget(self.edit_point_widget)

        self.setMinimumWidth(360)

    def _create_connections(self):
        self.geometry_widget.selection_changed.connect(self.selection_callback)
        self.pushButton_cancel.clicked.connect(self.close_callback)
        self.pushButton_finalize.clicked.connect(self.process_geometry_callback)
        self.add_widget.pushButton_add_segment.clicked.connect(self._disable_finalize_button)
        self.add_widget.pushButton_remove_selection.clicked.connect(self._disable_finalize_button)

    def _disable_finalize_button(self, _bool=False):
        self.pushButton_finalize.setDisabled(_bool)
        self.add_widget._disable_add_segment_button()
        self.add_widget.selection_callback()
        if _bool:
            self.add_widget._update_permissions(force_disable=True)

    def selection_callback(self):

        editor = self.geometry_widget.editor

        if editor.selected_structures:
            self.structures_selection_callback()
        elif editor.selected_points:
            self.edit_stack.setCurrentWidget(self.edit_point_widget)
        else:
            self.edit_stack.setCurrentWidget(self.empty_widget)

        self.edit_stack.currentWidget().update()

    def structures_selection_callback(self):

        editor = self.geometry_widget.editor
        structure, *_ = editor.selected_structures

        if isinstance(structure, Pipe):
            self.edit_stack.setCurrentWidget(self.edit_pipe_widget)
        elif isinstance(structure, Bend):
            self.edit_stack.setCurrentWidget(self.edit_bend_widget)
        else:
            self.edit_stack.setCurrentWidget(self.empty_widget)

    def process_geometry_callback(self):
        editor = app().geometry_toolbox.editor
        editor.dismiss()

        self.geometry_handler.export_entity_file()
        self.update_project_attributes()
        self.load_project()
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.action_front_view_callback()
        self.geometry_widget.set_info_text("")

    def update_project_attributes(self):
        self.file.modify_project_attributes(length_unit = self.add_widget.length_unit,
                                            element_size = 0.01, 
                                            geometry_tolerance = 1e-6,
                                            import_type = 1)

    def load_project(self):
        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_widget.initial_project_action(True)
        self.complete = True

    def get_file_path_inside_project_directory(self, filename):
        return get_new_path(self.file._project_path, filename)

    def close_callback(self):
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.action_front_view_callback()