from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
)
from pathlib import Path
from pulse import app, UI_DIR
from opps.model import Bend, Elbow

import numpy as np

class EditBendWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "model/geometry/edit_bend2.ui", self)

        self.geometry_widget = geometry_widget

        self._define_qt_variables()
        self._create_connections()

    def update(self):
        super().update()
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            self.reset_lineEdits()
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            self.reset_lineEdits()
            return

        self.bend_radius.setText(str(structure.curvature))

        start_coords = np.round(structure.start.coords(), 6)
        self.coord_x_start.setText(str(start_coords[0]))
        self.coord_y_start.setText(str(start_coords[1]))
        self.coord_z_start.setText(str(start_coords[2]))

        end_coords = np.round(structure.end.coords(), 6)
        self.coord_x_end.setText(str(end_coords[0]))
        self.coord_y_end.setText(str(end_coords[1]))
        self.coord_z_end.setText(str(end_coords[2]))

    def _define_qt_variables(self):
        # QLineEdit
        self.bend_radius : QLineEdit
        self.coord_x_end : QLineEdit
        self.coord_y_end : QLineEdit
        self.coord_z_end : QLineEdit
        self.coord_x_start : QLineEdit
        self.coord_y_start : QLineEdit
        self.coord_z_start : QLineEdit
        # QListWidget
        self.morph_list : QListWidget
        # QPushButton
        self.change_material_button : QPushButton
        self.change_section_button : QPushButton
        self.remove_bend_button : QPushButton

    def _create_connections(self):
        self.bend_radius.textEdited.connect(self.curvature_modified_callback)
        self.morph_list.itemClicked.connect(self.moph_list_callback)

    def curvature_modified_callback(self, text):
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            return

        try:
            curvature = float(text)
        except ValueError:
            return
        else:
            structure.curvature = curvature
            app().update()

    def moph_list_callback(self):
        items = self.morph_list.selectedItems()
        if not items:
            return
        first_item, *_ = items
        name = first_item.text().lower().strip()

        if name == "bend":
            _type = Bend
        elif name == "elbow":
            _type = Elbow
        else:
            return

        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            return
        
        new_structure = editor.morph(structure, _type)
        editor.select_structures([new_structure])
        app().update()

    def reset_lineEdits(self):

        self.bend_radius.setText("")

        self.coord_x_start.setText("")
        self.coord_y_start.setText("")
        self.coord_z_start.setText("")

        self.coord_x_end.setText("")
        self.coord_y_end.setText("")
        self.coord_z_end.setText("")