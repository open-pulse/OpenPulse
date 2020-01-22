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
import vtk
from os.path import expanduser
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from opv.openPulse3DLines import OpenPulse3DLines

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        self.setMinimumSize(QSize(800, 600))    
        self.setWindowTitle("OpenPulse")

        #a = MenuBar(self)
        self.createMenuBar()
        self.createToolBar()
        self.newCall()

        #self.l1 = Qt.QHBoxLayout()

        self.show()

    def openCall(self):
        print('Open')

    def newCall(self):
        coordinates = np.array(np.loadtxt('../examples/coord.dat'))
        connectivity = np.array(np.loadtxt('../examples/connect.dat'), int)
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
        t2.addWidget(self.vtkWidget,1)
        self.vtkWidget.GetRenderWindow().AddRenderer(temp.getRenderer())
        temp.getRenderer().ResetCamera()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.iren.Initialize()

    def exitCall(self):
        newAction = QAction(QIcon('interface/icons/open.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        self.toolbar.addAction(newAction)

    def clickMethod(self):
        print('PyQt')

    def createToolBar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(32,32))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        newAction = QAction(QIcon('objects/icons/new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        self.toolbar.addAction(newAction)
        
        self.toolbar.addSeparator()
        
    def createToolBar2(self):
        newAction = QAction(QIcon('interface/icons/new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)
        
        self.toolbar = self.addToolBar('New')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(newAction)

    def createMenuBar(self):
        
        newAction = QAction(QIcon('objects/icons/new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        openAction = QAction(QIcon('interface/icons/open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        menuBar.addMenu("&Help")
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
