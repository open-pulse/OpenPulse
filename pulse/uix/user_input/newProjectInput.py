from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget
from pulse.project import Project
from PyQt5.QtGui import QIcon
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

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.create = False

        self.currentTab = 0

        self.userPath = os.path.expanduser('~')
        self.openPulsePath = "{}\\OpenPulse".format(self.userPath)
        self.projectPath = "{}\\OpenPulse\\Projects".format(self.userPath)
        self.materialListName = "materialList.dat"
        self.projectFileName = "project.ini"
        self.materialListPath = ""

        self.button_create_project = self.findChild(QDialogButtonBox, 'button_create_project')
        self.button_create_project.accepted.connect(self.accept_project)
        self.button_create_project.rejected.connect(self.reject_project)

        self.line_project_name = self.findChild(QLineEdit, 'line_project_name')
        self.line_import_geometry = self.findChild(QLineEdit, 'line_import_geometry')
        self.line_element_size = self.findChild(QLineEdit, 'line_element_size')

        self.line_import_cord = self.findChild(QLineEdit, 'line_cord')
        self.line_import_conn = self.findChild(QLineEdit, 'line_conn')

        self.toolButton_import_geometry = self.findChild(QToolButton, 'toolButton_import_geometry')
        self.toolButton_import_geometry.clicked.connect(self.import_geometry)

        self.toolButton_import_cord = self.findChild(QToolButton, 'toolButton_import_cord')
        self.toolButton_import_cord.clicked.connect(self.import_cord)

        self.toolButton_import_conn = self.findChild(QToolButton, 'toolButton_import_conn')
        self.toolButton_import_conn.clicked.connect(self.import_conn)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)
        self.currentTab = self.tabWidget.currentIndex()

        self.exec_()

    def createProjectFolder(self):
        if not os.path.exists(self.openPulsePath):
            os.mkdir(self.openPulsePath)

        if not os.path.exists(self.projectPath):
            os.mkdir(self.projectPath)

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def accept_project(self):
        self.createProjectFolder()
        if self.line_project_name.text() == "":
            self.error("Insert the Project Name!")
            return

        if self.line_project_name.text() in os.listdir(self.projectPath):
            self.error("This Project Already Exists!")
            return

        if self.currentTab == 0: #Iges
            if self.line_import_geometry.text() == "":
                self.error("Error: Import Geometry!")
                return
            if self.line_element_size.text() == "":
                self.error("Error: Element Size!")
                return
            else:
                try:
                    float(self.line_element_size.text())
                except Exception:
                    self.error("Error: Element size isn't a float")
                    return
        
        if self.currentTab == 1: #.dat
            if (self.line_import_conn.text() == "" or self.line_import_cord.text() == ""):
                self.error("Error: Import conn or cord files")
                return
        
        if self.createProject():
            self.create = True
            self.close()

    def reject_project(self):
        self.close()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Iges Files (*.iges)')
        self.name = basename(self.path)
        self.line_import_geometry.setText(str(self.path))

    def import_cord(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.name = basename(self.path)
        self.line_import_cord.setText(str(self.path))

    def import_conn(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.name = basename(self.path)
        self.line_import_conn.setText(str(self.path))

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def createProject(self):
        path = '{}\\{}'.format(self.projectPath, self.line_project_name.text())
        if not os.path.exists(path):
            os.makedirs(path)

        self.createMaterialFile(path)
        self.createProjectFile(path)
        
        if self.currentTab == 0:
            geometry_file_name = self.line_import_geometry.text().split('/')[-1]
            new_geometry_path = "{}\\{}".format(path, geometry_file_name)
            copyfile(self.line_import_geometry.text(), new_geometry_path)
            element_size = float(self.line_element_size.text())
            import_type = 0
            self.project.newProject(path, self.line_project_name.text(), element_size, import_type, self.materialListPath, geometryPath=new_geometry_path)
            return True
        elif self.currentTab == 1:
            cord_file = self.line_import_cord.text().split('/')[-1]
            conn_file = self.line_import_conn.text().split('/')[-1]
            new_cord_path = "{}\\{}".format(path, cord_file)
            new_conn_path = "{}\\{}".format(path, conn_file)
            copyfile(self.line_import_cord.text(), new_cord_path)
            copyfile(self.line_import_conn.text(), new_conn_path)
            element_size = 0
            import_type = 1
            self.project.newProject(path, self.line_project_name.text(), element_size, import_type, self.materialListPath, connPath=new_conn_path, cordPath=new_cord_path)
            return True
        return False

    def createProjectFile(self, project_path):
        path = "{}\\{}".format(project_path, self.projectFileName)
        geometry_file_name = ""
        cord_file_name = ""
        conn_file_name = ""
        import_type = 0
        element_size = 0
        if self.currentTab == 0:
            geometry_file_name = self.line_import_geometry.text().split('/')[-1]
            import_type = 0
            element_size = self.line_element_size.text()
        elif self.currentTab == 1:
            cord_file_name = self.line_import_cord.text().split('/')[-1]
            conn_file_name = self.line_import_conn.text().split('/')[-1]
            import_type = 1

        config = configparser.ConfigParser()
        config['PROJECT'] = {
            'Name': self.line_project_name.text(),
            'Element Size': str(element_size),
            'Import Type': str(import_type),
            'Geometry File': geometry_file_name,
            'Cord File': cord_file_name,
            'Conn File': conn_file_name,
            'MaterialList File': self.materialListName
        }
        with open(path, 'w') as configfile:
            config.write(configfile)

    def createMaterialFile(self, project_path):
        self.materialListPath = "{}\\{}".format(project_path, self.materialListName)
        config = configparser.ConfigParser()

        config['STEEL'] = {
            'Name': 'steel',
            'Identifier': 1,
            'Density': 7860,
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
        with open(self.materialListPath, 'w') as configfile:
            config.write(configfile)