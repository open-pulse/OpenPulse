from PyQt5.QtWidgets import QLabel, QLineEdit, QDialogButtonBox, QDialog
from PyQt5 import uic

class DOFInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/dofInput.ui', self)
        self.node_id = kwargs.get("node_id", -1)

        self.button_save_dof = self.findChild(QDialogButtonBox, 'button_save_dof')
        self.button_save_dof.accepted.connect(self.accept_dof)
        self.button_save_dof.rejected.connect(self.reject_dof)

        self.label_node_id = self.findChild(QLabel, 'label_node_id')

        self.line_ux = self.findChild(QLineEdit, 'line_ux')
        self.line_uy = self.findChild(QLineEdit, 'line_uy')
        self.line_uz = self.findChild(QLineEdit, 'line_uz')
        self.line_yx = self.findChild(QLineEdit, 'line_yx')
        self.line_yy = self.findChild(QLineEdit, 'line_yy')
        self.line_yz = self.findChild(QLineEdit, 'line_yz')

        self.label_node_id.setText("Node - ID [ "+str(self.node_id)+" ]")

        self.exec_()
        
    def accept_dof(self):
        pass

    def reject_dof(self):
        self.close()