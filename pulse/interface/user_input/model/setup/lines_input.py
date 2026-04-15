from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.user_input.model.setup.user_input import UserInput


class LinesInput(UserInput):
    def __init__(self):
        super().__init__()

        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self.before_run = app().project.get_pre_solution_model_checks()

    def reset_input_fields(self):
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
