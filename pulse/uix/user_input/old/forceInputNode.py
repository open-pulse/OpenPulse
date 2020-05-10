from PyQt5.QtWidgets import QLabel, QLineEdit, QDialogButtonBox, QDialog, QMessageBox
from pulse.preprocessing.boundary_condition import BoundaryCondition
from PyQt5 import uic

class ForceInputNode(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/forceInputNode.ui', self)

        self.force = None
        self.nodes = []
        self.button_save_dof = self.findChild(QDialogButtonBox, 'button_save_dof')
        self.button_save_dof.accepted.connect(self.accept_dof)
        self.button_save_dof.rejected.connect(self.reject_dof)

        self.label_node_id = self.findChild(QLabel, 'label_node_id')
        self.line_ux = self.findChild(QLineEdit, 'line_node')

        self.line_ux = self.findChild(QLineEdit, 'line_ux')
        self.line_uy = self.findChild(QLineEdit, 'line_uy')
        self.line_uz = self.findChild(QLineEdit, 'line_uz')
        self.line_yx = self.findChild(QLineEdit, 'line_yx')
        self.line_yy = self.findChild(QLineEdit, 'line_yy')
        self.line_yz = self.findChild(QLineEdit, 'line_yz')

        self.label_node_id.setText("Node - Force")

        self.exec_()
        
    def accept_dof(self):
        dx = None
        dy = None
        dz = None
        rx = None
        ry = None
        rz = None
        if self.line_node.text() != "":
            try:
                nodes = self.line_node.text().split(',')
                for node in nodes:
                    self.nodes.append(int(node))
            except Exception:
                self.error("Digite um valor válido")
                self.nodes = []
                return

        if self.line_ux.text() != "":
            try:
                dx = int(self.line_ux.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        if self.line_uy.text() != "":
            try:
                dy = int(self.line_uy.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        if self.line_uz.text() != "":
            try:
                dz = int(self.line_uz.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        if self.line_yx.text() != "":
            try:
                rx = int(self.line_yx.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        if self.line_yy.text() != "":
            try:
                ry = int(self.line_yy.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        if self.line_yz.text() != "":
            try:
                rz = int(self.line_yz.text())
            except Exception:
                self.error("Digite um valor válido")
                return

        self.force = [dx,dy,dz,rx,ry,rz]
        self.close()

    def reject_dof(self):
        self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        #msg_box.setInformativeText('More information')
        msg_box.setWindowTitle(title)
        msg_box.exec_()