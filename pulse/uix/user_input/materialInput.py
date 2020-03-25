from PyQt5.QtWidgets import QLabel, QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog
from os.path import basename
from PyQt5 import uic

class MaterialInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/materialInput.ui', self)

        self.buttonBox_save_material = self.findChild(QDialogButtonBox, 'buttonBox_save_material')
        self.buttonBox_save_material.accepted.connect(self.accept_dof)
        self.buttonBox_save_material.rejected.connect(self.reject_dof)

        self.line_material_name = self.findChild(QLineEdit, 'line_material_name')
        self.line_e = self.findChild(QLineEdit, 'line_e')
        self.line_v = self.findChild(QLineEdit, 'line_v')
        self.line_f = self.findChild(QLineEdit, 'line_f')
        self.line_color = self.findChild(QLineEdit, 'line_color')

        self.toolButton_color = self.findChild(QToolButton, 'toolButton_color')
        self.toolButton_color.clicked.connect(self.material_color)

        self.exec_()
        
    def accept_dof(self):
        pass

    def reject_dof(self):
        pass

    def material_color(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        self.name = basename(self.path)

