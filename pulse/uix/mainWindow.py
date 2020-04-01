import sys
from os.path import expanduser, basename
from pathlib import Path

import numpy as np
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar, QSplitter, QFrame, QHBoxLayout, QFileDialog, QMessageBox
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAction, QToolBar, QSplitter, QFileDialog, QMessageBox, QMainWindow

from pulse.mesh import Mesh
from pulse.uix.infoUi import InfoUi
from pulse.uix.opvUi import OPVUi
from pulse.project import Project
from pulse.uix.inputUi import InputUi

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.project = Project()
        self._load_icons()
        self._config()
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_basic_layout()
        self.show()

    def _load_icons(self):
        icons_path = 'pulse\\data\\icons\\'
        self.pulse_icon = QIcon(icons_path + 'pulse.png')
        self.new_icon = QIcon(icons_path + 'new.png')
        self.open_icon = QIcon(icons_path + 'open.png')
        self.exit_icon = QIcon(icons_path + 'exit.png')

    def _config(self):
        self.setMinimumSize(QSize(800, 600))
        self.setWindowIcon(self.pulse_icon)
        self._change_window_title()

    def _change_window_title(self, msg = ""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def _create_actions(self):
        self.new_action = QAction(self.new_icon, '&New', self)        
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('New document')
        self.new_action.triggered.connect(self.new_call)

        self.import_action = QAction(self.open_icon, '&Import Geometry', self)        
        self.import_action.setShortcut('Ctrl+O')
        self.import_action.setStatusTip('Import Geometry')
        self.import_action.triggered.connect(self.import_call)

        self.exit_action = QAction(self.exit_icon, '&Exit', self)        
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        self.entities_action = QAction(self.exit_icon, '&Entity', self)        
        self.entities_action.setShortcut('Ctrl+1')
        self.entities_action.setStatusTip('Plot Entities')
        self.entities_action.triggered.connect(self.plot_entities)

        self.elements_action = QAction(self.exit_icon, '&Elements', self)        
        self.elements_action.setShortcut('Ctrl+2')
        self.elements_action.setStatusTip('Plot Elements')
        self.elements_action.triggered.connect(self.plot_elements)

        self.points_action = QAction(self.exit_icon, '&Points', self)        
        self.points_action.setShortcut('Ctrl+3')
        self.points_action.setStatusTip('Plot Points')
        self.points_action.triggered.connect(self.plot_points)

    def _create_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        graphicMenu = menuBar.addMenu('&Graphic')
        helpMenu = menuBar.addMenu("&Help")

        fileMenu.addAction(self.new_action)
        fileMenu.addAction(self.import_action)
        fileMenu.addAction(self.exit_action)

        graphicMenu.addAction(self.entities_action)
        graphicMenu.addAction(self.elements_action)
        graphicMenu.addAction(self.points_action)

    def _create_tool_bar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)      
        self.toolbar.addSeparator()

    def _create_basic_layout(self):
        self.info_widget = InfoUi(self)
        self.opv_widget = OPVUi(self.project, self)
        self.inputWidget = InputUi(self.project, self)

        working_area = QSplitter(Qt.Horizontal)
        self.setCentralWidget(working_area)

        working_area.addWidget(self.info_widget)
        working_area.addWidget(self.opv_widget)
        working_area.setSizes([100,300])

    def new_call(self):
        path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        name = basename(path)
        self._change_window_title(name)
        self.project.newProject("test", path, 0.1)
        self.draw()

    def import_call(self):
        self.inputWidget.newProject()
        return

    def plot_entities(self):
        self.opv_widget.change_to_entities()

    def plot_elements(self):
        self.opv_widget.change_to_elements()

    def plot_points(self):
        self.opv_widget.change_to_points()

    def draw(self):
        self.opv_widget.plot_entities()
        self.opv_widget.plot_points()
        self.opv_widget.plot_elements()
        self.plot_entities()

    def generate(self, min, max):
        #self.project.generate(min, max)
        self.draw()

    def closeEvent(self, event):
        close = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure want to stop process?",
            QMessageBox.No | QMessageBox.Yes)
        
        if close == QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    def getInputWidget(self):
        return self.inputWidget

    def getInfoWidget(self):
        return self.info_widget

    def getOPVWidget(self):
        return self.opv_widget