import sys
import os
from pathlib import Path
import vtk
from os.path import expanduser
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from .infoLayout import InfoLayout
from .opvLayout import OPVLayer
from pulse.opv.openPulse3DLines import OpenPulse3DLines

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        self.init()
        self.show()

    def init(self):
        self.setMinimumSize(QSize(800, 600))
        icons_path = self.getIconPath()
        self.setWindowIcon(QIcon(icons_path+'new.png'))
        self.changeWindowTitle()
        self.createMenuBar()
        self.createToolBar()
        self.createBasicLayout()

    def changeWindowTitle(self, msg = ""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def createMenuBar(self):

        icons_path = self.getIconPath()

        newAction = QAction(QIcon(icons_path + 'new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        openAction = QAction(QIcon(icons_path + 'open.png'), '&Import Geometry', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Import Geometry')
        openAction.triggered.connect(self.importCall)

        exitAction = QAction(QIcon(icons_path + 'exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        helpMenu = menuBar.addMenu("&Help")

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

    def createToolBar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        icons_path = self.getIconPath()

        newAction = QAction(QIcon(icons_path + 'new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        openAction = QAction(QIcon(icons_path + 'open.png'), '&Import Geometry', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Import Geometry')
        openAction.triggered.connect(self.importCall)

        exitAction = QAction(QIcon(icons_path + 'exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        
        
        self.toolbar.addSeparator()

    def createBasicLayout(self):
        generalFrame = Qt.QFrame()
        generalLayout = Qt.QHBoxLayout()

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