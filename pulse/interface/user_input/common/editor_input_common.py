from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from PyQt5 import uic

from dataclasses import dataclass

from pulse import app, UI_DIR


class EditorInputCommon(QDialog):
    '''
    A simple window with buttons to confirm and cancel
    that handles any widgets inside it.
    '''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        ui_path = UI_DIR / "common/editor_input_common.ui"
        uic.loadUi(ui_path, self)
        self._define_qt_variables()

    def _define_qt_variables(self):
        self.title_label: QLabel

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

    def cancel_button_callback(self):
        self.close()

    def apply_button_callback(self):        
        pass

    def confirm_button_callback(self):
        self.apply_button_callback()
        self.close()
