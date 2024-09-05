from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from PyQt5 import uic

from dataclasses import dataclass

from pulse import app, UI_DIR


@dataclass
class MeshInputFilter:
    all_nodes: bool = False
    all_lines: bool = False
    all_elements: bool = False
    selected_nodes: bool = False
    selected_lines: bool = False
    selected_elements: bool = False


class MeshInputCommon(QDialog):
    """
    A lot of input interfaces have in common the funcionality
    of attribute things to nodes, lines and/or elements.

    This class implements all these behaviors in a common place
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        ui_path = UI_DIR / "common/mesh_input_common.ui"
        uic.loadUi(ui_path, self)

        self.filter = MeshInputFilter()
        self.item_indexes = dict()

        self._config_window()
        self._define_qt_variables()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        self.title_label: QLabel
        self.attribute_to_label: QLabel
        self.selected_label: QLabel
        self.attribute_to_combobox: QComboBox
        self.selected_lineedit: QLineEdit

        self.cancel_button: QPushButton
        self.apply_button: QPushButton
        self.confirm_button: QPushButton

        self.central_widget: QWidget

    def _create_connections(self):
        self.cancel_button.clicked.connect(self.cancel_button_callback)
        app().main_window.selection_changed.connect(self.selection_callback)

    def set_title(self, name: str):
        self.title_label.setText(name)

    def set_central_widget(self, central_widget):
        if not isinstance(central_widget, QWidget):
            return
        
        previous = self.central_widget
        current = central_widget
        self.central_widget = central_widget
        self.layout().replaceWidget(previous, current)

    def filter_attributes(
        self,
        all_nodes=False,
        all_lines=False,
        all_elements=False,
        selected_nodes=False,
        selected_lines=False,
        selected_elements=False,
    ):
        self.filter = MeshInputFilter(
            all_nodes,
            all_lines,
            all_elements,
            selected_nodes,
            selected_lines,
            selected_elements,
        )
        self.update_filter()

    def cancel_button_callback(self):
        self.close()

    def apply_button_callback(self):
        pass

    def confirm_button_callback(self):
        self.apply_button_callback()
        self.close()

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        selected_lines = app().main_window.list_selected_lines()
        selected_elements = app().main_window.list_selected_elements()

        if selected_nodes and self.filter.selected_nodes:
            if not (selected_lines or selected_elements):
                index = self.item_indexes["Selected nodes"]
                self.attribute_to_combobox.setCurrentIndex(index)
            if "nodes" in self.attribute_to_combobox.currentText():
                self.selected_lineedit(", ".join(selected_nodes))

        elif selected_lines and self.filter.selected_lines:
            if not (selected_lines or selected_elements):
                index = self.item_indexes["Selected lines"]
                self.attribute_to_combobox.setCurrentIndex(index)
            if "lines" in self.attribute_to_combobox.currentText():
                self.selected_lineedit(", ".join(selected_lines))

        elif selected_elements and self.filter.selected_elements:
            if not (selected_lines or selected_elements):
                index = self.item_indexes["Selected elements"]
                self.attribute_to_combobox.setCurrentIndex(index)
            if "elements" in self.attribute_to_combobox.currentText():
                self.selected_lineedit(", ".join(selected_elements))

        else:
            self.selected_lineedit.setText("")

    def update_filter(self):
        self.attribute_to_combobox.clear()

        if self.filter.all_nodes:
            self.attribute_to_combobox.addItem("All nodes")

        if self.filter.all_lines:
            self.attribute_to_combobox.addItem("All lines")

        if self.filter.all_elements:
            self.attribute_to_combobox.addItem("All elements")

        if self.filter.selected_nodes:
            self.attribute_to_combobox.addItem("Selected nodes")

        if self.filter.selected_lines:
            self.attribute_to_combobox.addItem("Selected lines")

        if self.filter.selected_elements:
            self.attribute_to_combobox.addItem("Selected elements")

        self.item_indexes = {
            i: self.attribute_to_combobox.itemText(i)
            for i in range(self.attribute_to_combobox.count())
        }

        if len(self.item_indexes) == 1:
            self.attribute_to_combobox.hide()
            self.attribute_to_label.hide()
