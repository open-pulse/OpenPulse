import sys
from os.path import expanduser
from pathlib import Path
import vtk
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar, QSplitter
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from .infoLayout import InfoLayout
from .opvLayout import OPVLayer
from pulse.opv.openPulse3DLines import OpenPulse3DLines

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.init()
        self.show()

    def init(self):
        self.setMinimumSize(QSize(800, 600))
        icons_path = self.getIconPath()
        self.setWindowIcon(QIcon(icons_path+'new.png'))
        self.changeWindowTitle()
        self.create_actions()
        self.createMenuBar()
        self.createToolBar()
        self.createBasicLayout()

    def changeWindowTitle(self, msg = ""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def create_actions(self):
        icons_path = self.getIconPath()

        self.new_action = QAction(QIcon(icons_path + 'new.png'), '&New', self)        
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('New document')
        self.new_action.triggered.connect(self.newCall)

        self.import_action = QAction(QIcon(icons_path + 'open.png'), '&Import Geometry', self)        
        self.import_action.setShortcut('Ctrl+O')
        self.import_action.setStatusTip('Import Geometry')
        self.import_action.triggered.connect(self.importCall)

        self.exit_action = QAction(QIcon(icons_path + 'exit.png'), '&Exit', self)        
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

    def createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        helpMenu = menuBar.addMenu("&Help")

        fileMenu.addAction(self.new_action)
        fileMenu.addAction(self.import_action)
        fileMenu.addAction(self.exit_action)

    def createToolBar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)      
        self.toolbar.addSeparator()

    def createBasicLayout(self):
        info_widget = QWidget()
        info_widget.setStyleSheet('background-color:red')

        graphics_widget = QWidget()
        graphics_widget.setStyleSheet('background-color:green')

        working_area_splitter = QSplitter(Qt.Horizontal)
        working_area_splitter.addWidget(info_widget)
        working_area_splitter.addWidget(graphics_widget)
        working_area_splitter.setSizes([70,100])

        self.setCentralWidget(working_area_splitter)

        return 

        generalFrame = QFrame()
        generalLayout = QHBoxLayout()

        self.infoLayout = InfoLayout(self)
        self.OPVLayout = OPVLayer(self)

        generalLayout.addLayout(self.infoLayout,1)
        generalLayout.addLayout(self.OPVLayout,2)

        generalFrame.setLayout(generalLayout)
        self.setCentralWidget(generalFrame)

    def importCall(self):
        self.infoLayout.import_from_main()

    def newCall(self):
        self.change_plot(None, None)
        self.infoLayout.reset()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                        "QUIT",
                                        "Are you sure want to stop process?",
                                        QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if close == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    def clickMethod(self):
        print('PyQt')


    #============
    #Get path to icon and examples from current path

    def getIconPath(self):
        return str(Path(__file__).parent.parent) + "/data/icons/"

    def getExamplesPath(self):
        return str(Path(__file__).parent.parent.parent) + "/examples/"

    def change_plot(self, a,b):
        self.OPVLayout.change_line_plot(a,b)