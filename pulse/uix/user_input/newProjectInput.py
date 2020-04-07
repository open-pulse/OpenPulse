from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox
from pulse.project import Project
from os.path import basename
from PyQt5 import uic
import os
import configparser
from shutil import copyfile
import numpy as np

from PyQt5 import uic

class NewProjectInput(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/newProjectInput.ui', self)
        self.project = project
        self.create = False

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
        if self.line_project_name.text() == "":
            self.error("Digite um nome para o projeto!")
            return
        elif self.line_import_geometry.text() == "":
            self.error("É necessário importar uma geometria!")
            return
        elif self.line_element_size.text() == "":
            self.error("Indique o tamanho do elemento!")
            return
        elif self.line_project_name.text() in os.listdir('Projects'):
            self.error("Já existe um projeto com esse nome!")
        try:
            float(self.line_element_size.text())
        except Exception:
            self.error("Digite um valor válido para o tamanho do elemento!")
        
        if self.createProject():
            self.create = True
            self.close()

    def reject_project(self):
        self.close()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        self.name = basename(self.path)
        self.line_import_geometry.setText(str(self.path))

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        #msg_box.setInformativeText('More information')
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def createProject(self):
        path = 'Projects//{}'.format(self.line_project_name.text())
        if not os.path.exists(path):
            os.makedirs(path)
        
        geometry_file_name = self.line_import_geometry.text().split('/')[-1]
        new_geometry_path = "{}//{}".format(path, geometry_file_name)
        copyfile(self.line_import_geometry.text(), new_geometry_path)

        self.createMaterialFile(path)
        self.createProjectFile(path)
        self.project.newProject(path, self.line_project_name.text(), geometry_file_name, self.line_element_size.text(), 'material.dat')
        return True

    def createProjectFile(self, project_path):
        path = "{}//{}".format(project_path, 'project.ini')
        geometry_file_name = self.line_import_geometry.text().split('/')[-1]
        config = configparser.ConfigParser()
        config['PROJECT'] = {
            'Name': self.line_project_name.text(),
            'GeometryFile': geometry_file_name,
            'ElementSize': self.line_element_size.text(),
            'MaterialFile': 'material.dat'
        }
        with open(path, 'w') as configfile:
            config.write(configfile)

    def createMaterialFile(self, project_path):
        path = "{}//{}".format(project_path, 'material.dat')
        config = configparser.ConfigParser()

        config['STEEL'] = {
            'Name': 'steel',
            'Identifier': 1,
            'Density': 7850,
            'YoungModulus': 210,
            'Poisson': 0.3,
            'Color': '[0,0,255]' #Blue
        }

        config['STAINLESS_STEEL'] = {
            'Name': 'stainless_steel',
            'Identifier': 2,
            'Density': 7750,
            'YoungModulus': 193,
            'Poisson': 0.31,
            'Color': '[255,255,0]' #Yelow
        }

        config['NI-CO-CR_STEEL'] = {
            'Name': 'Ni-Co-Cr_steel',
            'Identifier': 3,
            'Density': 8220,
            'YoungModulus': 212,
            'Poisson': 0.315,
            'Color': '[0,255,255]' #Cyan
        }
        with open(path, 'w') as configfile:
            config.write(configfile)