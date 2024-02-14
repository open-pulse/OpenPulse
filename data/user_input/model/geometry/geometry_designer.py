from PyQt5.QtWidgets import QStackedWidget,  QWidget, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from data.user_input.model.geometry.add_widget import AddStructuresWidget
from data.user_input.model.geometry.edit_bend_widget import EditBendWidget
from data.user_input.model.geometry.edit_point_widget import EditPointWidget
from data.user_input.model.geometry.edit_pipe_widget import EditPipeWidget

from opps.model import Pipe, Bend


class OPPGeometryDesignerInput(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(Path('data/user_input/ui_files/Model/geometry/geometry_designer_tabs.ui'), self)

        self.geometry_widget = geometry_widget

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()

    def _define_qt_variables(self):
        self.tab_widget: QTabWidget
        self.add_tab: QWidget
        self.edit_tab: QWidget
        self.edit_stack: QStackedWidget
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

    def _create_connections(self):
        self.geometry_widget.selection_changed.connect(self.selection_callback)

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

