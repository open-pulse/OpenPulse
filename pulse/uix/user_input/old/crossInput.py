from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox, QDialog
from pulse.preprocessing.cross_section import CrossSection
from PyQt5 import uic

class CrossInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/crossInput.ui', self)
        self.cross = None
        #Pipe

        self.button_save_pipe = self.findChild(QDialogButtonBox, 'button_save_pipe')
        self.button_save_pipe.accepted.connect(self.accept_pipe)
        self.button_save_pipe.rejected.connect(self.reject_pipe)

        self.line_diam_externo = self.findChild(QLineEdit, 'line_diam_externo')
        self.line_diam_interno = self.findChild(QLineEdit, 'line_diam_interno')
        self.line_excen_x = self.findChild(QLineEdit, 'line_excen_x')
        self.line_excen_y = self.findChild(QLineEdit, 'line_excen_y')


        #Beam

        self.button_save_beam = self.findChild(QDialogButtonBox, 'button_save_beam')
        self.button_save_beam.accepted.connect(self.accept_beam)
        self.button_save_beam.rejected.connect(self.reject_beam)

        self.line_area = self.findChild(QLineEdit, 'line_area')
        self.line_iyy = self.findChild(QLineEdit, 'line_iyy')
        self.line_iyz = self.findChild(QLineEdit, 'line_iyz')
        self.line_izz = self.findChild(QLineEdit, 'line_izz')

        self.exec_()

    def accept_pipe(self):
        line_diam_externo = float(self.line_diam_externo.text())
        line_diam_interno = float(self.line_diam_interno.text())
        self.cross = CrossSection(line_diam_externo, line_diam_interno)
        self.close()

    def reject_pipe(self):
        self.close()

    def accept_beam(self):
        print("Implementar")

    def reject_beam(self):
        self.close()