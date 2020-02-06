import sys
from os.path import expanduser, basename
from pathlib import Path

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar, QSplitter, QFrame, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from pulse.mesh import Mesh
from pulse.uix.infoWidget import InfoWidget
from pulse.uix.opvWidget import OPVWidget

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.mesh = Mesh()
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

    def _create_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        helpMenu = menuBar.addMenu("&Help")

        fileMenu.addAction(self.new_action)
        fileMenu.addAction(self.import_action)
        fileMenu.addAction(self.exit_action)

    def _create_tool_bar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)      
        self.toolbar.addSeparator()

    def _create_basic_layout(self):
        self.info_widget = InfoWidget(self)
        self.opv_widget = OPVWidget(self)

        working_area = QSplitter(Qt.Horizontal)
        self.setCentralWidget(working_area)

        working_area.addWidget(self.info_widget)
        working_area.addWidget(self.opv_widget)
        working_area.setSizes([100,300])

    def new_call(self):
        #print('THIS DOES NOT WORK')
        con = np.array(np.loadtxt('examples/matplotlib/Ex_02/connect.dat'), int)
        print(type(con))
        cor = np.array(np.loadtxt('examples/matplotlib/Ex_02/coord.dat'))
        self.opv_widget.change_line_plot(cor, con)

    def import_call(self):
        path, _type = QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        name = basename(path)
        self.mesh.path = path
        self._change_window_title(name)

    def plot(self):
        self.opv_widget.change_line_plot(self.mesh.nodes, self.mesh.edges)


    # HERITAGE
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

    def clickMethod(self):
        print('PyQt')
