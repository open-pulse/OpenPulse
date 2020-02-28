from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from pulse.opv.lines import Lines

colors = vtk.vtkNamedColors()

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, actors, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.actors = actors
        self.currentEntity = -1
        self.LastPickedProperty = vtk.vtkProperty()

    def setActors(self, actors):
        self.actors = actors

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        self.NewPickedActor = picker.GetActor()

        if self.NewPickedActor:
            if self.LastPickedActor:
                self.LastPickedActor.GetMapper().ScalarVisibilityOn()
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())

            for line in self.actors:
                if line.get_actor() == self.NewPickedActor:
                    self.currentEntity = line.tag
                    print(self.currentEntity)

            self.NewPickedActor.GetMapper().ScalarVisibilityOff()
            self.NewPickedActor.GetProperty().SetColor(colors.GetColor3d('Red'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)

            self.LastPickedActor = self.NewPickedActor

        self.OnLeftButtonDown()
        return

class OPVWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.renderer = vtk.vtkRenderer()
        self.actors = []
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
        style = MouseInteractorHighLightActor(self.actors)
        style.SetDefaultRenderer(self.renderer)
        self.SetInteractorStyle(style)

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

        self.colorbar = vtk.vtkScalarBarActor()
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetLookupTable(self.plot.get_table())
        self.colorbar.SetWidth(0.05)
        self.colorbar.SetPosition(0.95, 0.1)
        self.colorbar.SetLabelFormat("%.3g")
        self.colorbar.VisibilityOn()

    def add_actor(self):
        self.renderer.AddActor(self.colorbar)

    def remove_all_actors(self):
        for actor in self.renderer.GetActors():
            self.renderer.RemoveActor(actor)
        self.actors = []

    def change_line_plot(self, nodes, edges, entities, initial):
        self.remove_all_actors()
        for i in entities:
            if not initial:
                if i.tag == self.GetInteractorStyle().currentEntity:
                    plot = Lines(nodes=i.nodes, edges=i.edges, tag=i.tag, initial=initial)
                    plot.assembly()
                    self.actors.append(plot)
                    self.renderer.AddActor(plot.get_actor())
            else:
                    plot = Lines(nodes=i.nodes, edges=i.edges, tag=i.tag, initial=initial)
                    plot.assembly()
                    self.actors.append(plot)
                    self.renderer.AddActor(plot.get_actor())
        self.GetInteractorStyle().setActors(self.actors)
        self.colorbar.SetLookupTable(self.plot.get_table())
        self.setup_renderer()
        self.update()
        