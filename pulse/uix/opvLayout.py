from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from pulse.opv.openPulse3DLines import OpenPulse3DLines

class OPVLayer(Qt.QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.renderer = vtk.vtkRenderer()
        self.plot = OpenPulse3DLines()
        self.plot.start()
        self.generic_init()

    def resetCamera(self):
        self.renderer.ResetCamera()

    def reset(self):
        self.removeWidget(self.vtkWidget)
        self.plot = OpenPulse3DLines()
        self.plot.start()
        self.generic_init()
        
    def generic_init(self):
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.resetCamera()

        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self.iren)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

        self.addWidget(self.vtkWidget)
        self.iren.Initialize()

    def addActor(self):
        self.renderer.AddActor(self.plot.getActor())

    def change_line_plot(self, a,b):
        self.plot = OpenPulse3DLines(a,b)
        self.plot.start()
        self.addActor()
        self.resetCamera()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtkWidget.update()
        