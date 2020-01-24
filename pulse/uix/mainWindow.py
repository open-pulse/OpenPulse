"""
* OpenPulse Project - LVA UFSC
* Multidisciplinary Optimization Group
*
* mainWindow.py
* <file description>
*
*
* Written by José Luiz de Souza <joseloolo@hotmail.com>
* Modified by <>
"""

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
from opv.openPulse3DLines import OpenPulse3DLines

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
        self.insertBasicWidgets()

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

        openAction = QAction(QIcon(icons_path + 'open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)

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

        openAction = QAction(QIcon(icons_path + 'open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)

        exitAction = QAction(QIcon(icons_path + 'exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        
        
        self.toolbar.addSeparator()

    def createBasicLayout(self):
        self.generalFrame = Qt.QFrame()
        self.generalLayout = Qt.QHBoxLayout()

        #populate generalLayout
        self.info_layer = InfoLayout()
        #self.info_layer = Qt.QVBoxLayout()
        self.opv_layer = Qt.QHBoxLayout()

        self.generalLayout.addLayout(self.info_layer,1)
        self.generalLayout.addLayout(self.opv_layer,2)

        self.generalFrame.setLayout(self.generalLayout)
        self.setCentralWidget(self.generalFrame)

    def insertBasicWidgets(self):
        #Info Layer
        #view_1 = Qt.QVBoxLayout()
        #view_2 = Qt.QVBoxLayout()

        #home_directory = expanduser('~')
        #model = QDirModel()

        #model_temp = QStandardItemModel(0, 1, self)
        #model_temp.setHeaderData(0, 1, "OpenPulse")

        #tree = QTreeView()
        #tree.setModel(model)
        #model_temp.insertRow(0)
        #item = QStandardItem("text")
        #model_temp.setItemData(item,0)

        #tree.setRootIndex(model.index(home_directory))

        #tree1 = QTreeView()
        #tree1.setModel(model)
        #tree1.setRootIndex(model.index(home_directory))

        #view_1.addWidget(tree)
        #view_2.addWidget(tree1)

        #self.info_layer.addLayout(view_1)
        #self.info_layer.addLayout(view_2)

        temp = OpenPulse3DLines()
        temp.start()
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)

        self.opv_layer.addWidget(self.vtkWidget)

        self.vtkWidget.GetRenderWindow().AddRenderer(temp.getRenderer())
        temp.getRenderer().ResetCamera()
        self.iren.Initialize()


    def openCall(self):
        self.changeWindowTitle("T")
        print('Open')

    def newCall(self):

        examples_path = self.getExamplesPath()

        coordinates = np.array(np.loadtxt(examples_path+'coord.dat'))
        connectivity = np.array(np.loadtxt(examples_path+'connect.dat'), int)
        temp = OpenPulse3DLines(vertex=coordinates, edges=connectivity)
        
        temp.start()

        t = Qt.QVBoxLayout()
        t2 = Qt.QHBoxLayout()

        home_directory = expanduser('~')
        model = QDirModel()
        view = QTreeView()
        view.setModel(model)
        view.setRootIndex(model.index(home_directory))

        view2 = QTreeView()
        view2.setModel(model)
        view2.setRootIndex(model.index(home_directory))

        self.frame = Qt.QFrame()
        self.vl = Qt.QHBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)

        a = Qt.QVBoxLayout()
        b = Qt.QVBoxLayout()

        t.addLayout(a,1)
        t.addLayout(b,1)

        self.vl.addLayout(t,1)
        self.vl.addLayout(t2,2.7)

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)
        #self.vl.addWidget(t,1)
        #self.vl.addWidget(self.vtkWidget,2.7)
        a.addWidget(view,1)
        b.addWidget(view2,1)
        
        self.opv_layer.removeItem(self.opv_layer.itemAt(0))
        #self.opv_layer.itemAt(0).widget().close()
        self.opv_layer.addWidget(self.vtkWidget,1)
        #t2.addWidget(self.vtkWidget,1)
        self.vtkWidget.GetRenderWindow().AddRenderer(temp.getRenderer())
        temp.getRenderer().ResetCamera()
        self.frame.setLayout(self.vl)
        #self.setCentralWidget(self.frame)
        self.iren.Initialize()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                        "QUIT",
                                        "Are you sure want to stop process?",
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
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