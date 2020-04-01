from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog
from os.path import basename
from PyQt5 import uic

from PyQt5 import uic

class NewProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/newProjectInput.ui', self)

        self.button_create_project = self.findChild(QDialogButtonBox, 'button_create_project')
        self.button_create_project.accepted.connect(self.accept_project)
        self.button_create_project.rejected.connect(self.reject_project)

        self.line_project_name = self.findChild(QLineEdit, 'line_project_name')
        self.line_import_geometry = self.findChild(QLineEdit, 'line_import_geometry')
        self.line_element_size = self.findChild(QLineEdit, 'line_element_size')

        self.toolButton_import_geometry = self.findChild(QToolButton, 'toolButton_import_geometry')
        self.toolButton_import_geometry.clicked.connect(self.import_geometry)

        self.exec_()

    def accept_project(self):
        pass

    def reject_project(self):
        self.close()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        self.name = basename(self.path)
        self.line_import_geometry.setText(str(self.path))