from PyQt5.QtWidgets import QLabel, QLineEdit, QDialogButtonBox, QDialog, QMessageBox
from pulse.preprocessing.boundary_condition import BoundaryCondition
from PyQt5 import uic

class FrequencyInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/frequencyRange.ui', self)

        self.frequencies = []
        self.button_save = self.findChild(QDialogButtonBox, 'button_save')
        self.button_save.accepted.connect(self.accept_frequency)
        self.button_save.rejected.connect(self.reject_frequency)

        self.line_min = self.findChild(QLineEdit, 'line_min')
        self.line_max = self.findChild(QLineEdit, 'line_max')
        self.line_step = self.findChild(QLineEdit, 'line_step')
        self.line_freq = self.findChild(QLineEdit, 'line_freq')
        self.exec_()
        
    def accept_frequency(self):
        min_ = 0
        max_ = 0
        step_ = 0
        if self.line_min.text() != "":
            try:
                min_ = int(self.line_min.text())
            except Exception:
                self.error("Digite um valor válido (min)")
                return

        if self.line_max.text() != "":
            try:
                max_ = int(self.line_max.text())
            except Exception:
                self.error("Digite um valor válido (max)")
                return

        if self.line_step.text() != "":
            try:
                step_ = int(self.line_step.text())
            except Exception:
                self.error("Digite um valor válido (step)")
                return
        
        for i in range(min_, max_+1, step_):
            self.frequencies.append(i)

        self.close()

    def reject_frequency(self):
        self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        #msg_box.setInformativeText('More information')
        msg_box.setWindowTitle(title)
        msg_box.exec_()