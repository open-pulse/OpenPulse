from PyQt5.QtWidgets import (
                            QCheckBox,
                            QFrame,
                            QGridLayout,
                            QHBoxLayout,
                            QLabel,
                            QLineEdit,
                            QPushButton,
                            QStackedLayout,
                            QVBoxLayout,
                            QWidget,
                            )
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from opps.model import Pipe
from pulse import app, UI_DIR

from pathlib import Path
import numpy as np

class EditPipeWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "model/geometry/edit_pipe2.ui", self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

    def _initialize(self):
        pass

    def _define_qt_variables(self):
        # QLineEdit
        self.coord_x_end : QLineEdit
        self.coord_y_end : QLineEdit
        self.coord_z_end : QLineEdit
        self.coord_x_start : QLineEdit
        self.coord_y_start : QLineEdit
        self.coord_z_start : QLineEdit
        # QPushButton
        self.change_material_button : QPushButton
        self.change_section_button : QPushButton
        self.remove_segment_button : QPushButton

    def _create_connections(self):
        self.change_material_button.clicked.connect(self.change_material_callback)
        self.change_section_button.clicked.connect(self.change_section_callback)

    def change_material_callback(self):
        pass

    def change_section_callback(self):
        pass

    def update(self):
        super().update()
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            self.reset_lineEdits()
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Pipe):
            self.reset_lineEdits()
            return

        start_coords = np.round(structure.start.coords(), 6)
        self.coord_x_start.setText(str(start_coords[0]))
        self.coord_y_start.setText(str(start_coords[1]))
        self.coord_z_start.setText(str(start_coords[2]))

        end_coords = np.round(structure.end.coords(), 6)
        self.coord_x_end.setText(str(end_coords[0]))
        self.coord_y_end.setText(str(end_coords[1]))
        self.coord_z_end.setText(str(end_coords[2]))

    def reset_lineEdits(self):

        self.coord_x_start.setText("")
        self.coord_y_start.setText("")
        self.coord_z_start.setText("")

        self.coord_x_end.setText("")
        self.coord_y_end.setText("")
        self.coord_z_end.setText("")