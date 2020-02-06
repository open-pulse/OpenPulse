from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from pulse.opv.lines import Lines

class OPVWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.renderer = vtk.vtkRenderer()
        self.plot = Lines()

        self.setup_camera()
        self.setup_renderer()
        self.plot.assembly()
        self.show_axes()
        self.Initialize()

    def reset(self):
        self.plot = Lines()
        self.plot.assembly()
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

    def add_actor(self):
        self.renderer.AddActor(self.plot.get_actor())

    def remove_all_actors(self):
        for actor in self.renderer.GetActors():
            self.renderer.RemoveActor(actor)

    def change_line_plot(self, nodes, edges):
        self.remove_all_actors()
        self.plot = Lines(nodes=nodes, edges=edges)
        self.plot.assembly()
        self.add_actor()
        self.setup_renderer()
        self.update()
        