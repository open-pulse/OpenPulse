from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
#from pulse.opv.lines import Lines
from pulse.opv.lines import Lines
from pulse.opv.point import Point

from pulse.uix.vtk.mouseInteractor import MouseInteractor


class OPVWidget(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()
        self.parent = parent
        self.project = project
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2,0.2,0.2)
        self.actors = {}
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
        style = MouseInteractor(self)
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

        # self.colorbar = vtk.vtkScalarBarActor()
        # self.colorbar.SetMaximumNumberOfColors(400)
        # self.colorbar.SetLookupTable(self.plot.get_table())
        # self.colorbar.SetWidth(0.05)
        # self.colorbar.SetPosition(0.95, 0.1)
        # self.colorbar.SetLabelFormat("%.3g")
        # self.colorbar.VisibilityOn()

    # def add_actor(self):
    #     self.renderer.AddActor(self.colorbar)

    def remove_all_actors(self):
        for actor in self.renderer.GetActors():
            self.renderer.RemoveActor(actor)
        self.actors = {}

    def before_plot(self):
        self.remove_all_actors()

    def after_plot(self):
        self.setup_renderer()
        self.update()

    def plot_line(self):
        self.before_plot()
        for entity in self.project.getEntities():
            plot = Point(entity.nodes, entity.edges, entity.tag)
            plot.assembly()
            self.actors[plot.get_actor()] = entity.tag
            self.renderer.AddActor(plot.get_actor())
        self.after_plot()

    def plot_nodes(self):
        self.before_plot()

        plot = Lines(self.project.getNodes(), self.project.getElements(), -1)
        plot.assembly()
        self.renderer.AddActor(plot.get_actor())
        self.actors[plot.get_actor()] = -1

        for point in self.project.getNodes():
            print(point)
            plot = Point(point[1]/1000, point[2]/1000, point[3]/1000, point[0])
            plot.assembly()
            self.actors[plot.get_actor()] = point[0]
            self.renderer.AddActor(plot.get_actor())
        self.after_plot()

    def on_context_menu(self, pos, a):
        print(a)
        menu = QMenu()
        menu.addAction(str(a))
        menu.exec_(self.mapToGlobal(pos))

    def plot_elements(self):
        pass

    # def change_line_plot(self, nodes, edges, entities, initial):
    #     self.remove_all_actors()
    #     for i in entities:
    #         if not initial:
    #             if i.tag == self.GetInteractorStyle().currentEntity:
    #                 plot = Lines(nodes=i.nodes, edges=i.edges, tag=i.tag, initial=initial)
    #                 plot.assembly()
    #                 self.actors.append(plot)
    #                 self.renderer.AddActor(plot.get_actor())
    #         else:
    #                 plot = Lines(nodes=i.nodes, edges=i.edges, tag=i.tag, initial=initial)
    #                 plot.assembly()
    #                 self.actors.append(plot)
    #                 self.renderer.AddActor(plot.get_actor())
    #     self.GetInteractorStyle().setActors(self.actors)
    #     self.colorbar.SetLookupTable(self.plot.get_table())
    #     self.setup_renderer()
    #     self.update()
        