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


class EditBendWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "model/geometry/edit_bend.ui", self)

        self.geometry_widget = geometry_widget

        self._define_qt_variables()
        self._create_connections()

    def update(self):
        super().update()
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            return

        self.curvature_box.setText(str(structure.curvature))

    def _define_qt_variables(self):
        self.curvature_box: QLineEdit = self.findChild(QLineEdit, "curvature_box")
        self.morph_list: QListWidget = self.findChild(QListWidget, "morph_list")

    def _create_connections(self):
        self.curvature_box.textEdited.connect(self.curvature_modified_callback)
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

