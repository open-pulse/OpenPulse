import vtk
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMenu, QAction


colors = vtk.vtkNamedColors()

class MouseInteractorPostProcessing(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        pass