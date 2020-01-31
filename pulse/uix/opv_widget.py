from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from pulse.opv.openPulse3DLines import OpenPulse3DLines

class OPVWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.renderer = vtk.vtkRenderer()
        self.plot = OpenPulse3DLines()

        self.setup_camera()
        self.setup_renderer()
        self.plot.start()
        self.show_axes()
        self.Initialize()

    def reset(self):
        self.plot = OpenPulse3DLines()
        self.plot.start()
        self.generic_init()
    
    def setup_camera(self):
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.SetInteractorStyle(self.style)

    def setup_renderer(self):
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer.ResetCamera()
        
    def show_axes(self):
        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def addActor(self):
        self.renderer.AddActor(self.plot.getActor())

    def change_line_plot(self, nodes, edges):
        self.plot = OpenPulse3DLines(nodes, edges)
        self.plot.start()
        self.addActor()
        self.setup_renderer()
        self.update()
        