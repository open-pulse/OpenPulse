from PyQt5.QtWidgets import QLabel, QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog
from os.path import basename
from PyQt5 import uic

class DOFImport(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/dofImport.ui', self)
        self.node_id = kwargs.get("node_id", -1)

        self.button_save_dof = self.findChild(QDialogButtonBox, 'button_save_dof')
        self.button_save_dof.accepted.connect(self.accept_dof)
        self.button_save_dof.rejected.connect(self.reject_dof)

        self.label_node_id = self.findChild(QLabel, 'label_node_id')

        self.line_file_name = self.findChild(QLineEdit, 'line_file_name')

        self.toolButton_import = self.findChild(QToolButton, 'toolButton_import')
        self.toolButton_import.clicked.connect(self.import_dof)

        self.label_node_id.setText("Node - ID [ "+str(self.node_id)+" ]")
        self.exec_()

    def accept_dof(self):
        pass

    def reject_dof(self):
        self.close()

    def import_dof(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        self.name = basename(self.path)