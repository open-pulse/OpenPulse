from PyQt5.QtWidgets import QLabel, QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QColorDialog, QMessageBox
from os.path import basename
from PyQt5.QtGui import QColor
from PyQt5 import uic
import configparser

class MaterialInput(QDialog):
    def __init__(self, material_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = material_path
        uic.loadUi('pulse/uix/user_input/ui/materialInput.ui', self)

        self.haveNewMaterial = False
        self.buttonBox_save_material = self.findChild(QDialogButtonBox, 'buttonBox_save_material')
        self.buttonBox_save_material.accepted.connect(self.accept_material)
        self.buttonBox_save_material.rejected.connect(self.reject_material)

        self.line_material_name = self.findChild(QLineEdit, 'line_material_name')
        self.line_e = self.findChild(QLineEdit, 'line_e') #Young Modulus
        self.line_v = self.findChild(QLineEdit, 'line_v') #Poisson
        self.line_f = self.findChild(QLineEdit, 'line_f') #Density
        self.line_color = self.findChild(QLineEdit, 'line_color')

        self.toolButton_color = self.findChild(QToolButton, 'toolButton_color')
        self.toolButton_color.clicked.connect(self.material_color)

        self.exec_()
        
    def accept_material(self):
        if self.line_material_name.text() == "":
            self.error("Digite o nome do material!")
            return
        elif self.line_e.text() == "":
            self.error("Digite um valor para Young Modulus")
            return
        elif self.line_v.text() == "":
            self.error("Digite um valor para Poisson")
            return
        elif self.line_f.text() == "":
            self.error("Digite um valor para Density")
            return
        elif self.line_color.text() == "":
            self.error("Selecione uma cor")
            return

        try:
            float(self.line_e.text())
        except Exception:
            self.error("Digite um valor válido para Young Modulus")
            return

        try:
            float(self.line_v.text())
        except Exception:
            self.error("Digite um valor válido para Poisson")
            return

        try:
            float(self.line_f.text())
        except Exception:
            self.error("Digite um valor válido para Density")
            return

        self.addMaterial()
        self.haveNewMaterial = True
        self.close()

    def reject_material(self):
        self.close()

    def material_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            r = color.red()
            g = color.green()
            b = color.blue()
            self.line_color.setText('[{},{},{}]'.format(r,g,b))

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        #msg_box.setInformativeText('More information')
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def addMaterial(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        name = self.line_material_name.text()

        identifier = len(config.sections())

        config[name.upper()] = {
            'Name': name,
            'Identifier': identifier+1,
            'Density': float(self.line_v.text()),
            'YoungModulus': float(self.line_e.text()),
            'Poisson': float(self.line_f.text()),
            'Color': self.line_color.text() #Blue
        }
        with open(self.path, 'w') as configfile:
            config.write(configfile)