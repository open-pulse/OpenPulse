from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
#from pulse.opv.lines import Lines
from pulse.opv.lines import Lines
from pulse.opv.linesPoint import LinesPoint
from pulse.opv.point import Point
from pulse.opv.element import Element

from pulse.uix.vtk.mouseInteractorPoint import MouseInteractorPoint
from pulse.uix.vtk.mouseInteractorElement import MouseInteractorElement
from pulse.uix.vtk.mouseInteractorEntity import MouseInteractorEntity


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()
        self.parent = parent
        self.project = project

        #==========================
        #          Renderer
        #==========================

        self.renderer_entities = vtk.vtkRenderer()
        self.renderer_elements = vtk.vtkRenderer()
        self.renderer_points = vtk.vtkRenderer()

        self.renderer_entities.SetBackground(0.2,0.2,0.2)
        self.renderer_elements.SetBackground(0.2,0.2,0.2)
        self.renderer_points.SetBackground(0.2,0.2,0.2)

        #self.style_entities = MouseInteractorTemp(self)
        self.style_entities = MouseInteractorEntity(self)
        self.style_elements = MouseInteractorElement(self)
        self.style_points = MouseInteractorPoint(self)

        self.style_entities.SetDefaultRenderer(self.renderer_entities)
        self.style_elements.SetDefaultRenderer(self.renderer_elements)
        self.style_points.SetDefaultRenderer(self.renderer_points)

        self.in_entities = False
        self.in_elements = False
        self.in_points = False

        self.actors_entities = {}
        self.actors_elements = {}
        self.actors_points = {}

        #Set initial plot & config
        self.create_actions()
        #self.change_to_entities()
        self.SetInteractorStyle(self.style_entities)
        self.GetRenderWindow().AddRenderer(self.renderer_entities)
        self.renderer_entities.ResetCamera()
        self.update()

        self.plot = Lines()
        self.plot.assembly()
        self._create_axes()

        self.Initialize()         #VTK Initialize - Don't remove this function
        
    def _create_axes(self):
        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def remove_all_renderers(self):
        self.GetRenderWindow().RemoveRenderer(self.renderer_entities)
        self.GetRenderWindow().RemoveRenderer(self.renderer_elements)
        self.GetRenderWindow().RemoveRenderer(self.renderer_points)

    def change_to_entities(self):
        self.remove_all_renderers()
        self.in_entities = True
        self.in_elements = False
        self.in_points = False
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.SetInteractorStyle(self.style_entities)
        self.GetRenderWindow().AddRenderer(self.renderer_entities)
        self.renderer_entities.ResetCamera()
        self.update()

    def change_to_elements(self):
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = True
        self.in_points = False
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.style_elements.LastPickedActor = None
        self.SetInteractorStyle(self.style_elements)
        self.GetRenderWindow().AddRenderer(self.renderer_elements)
        self.renderer_elements.ResetCamera()
        self.update()

    def change_to_points(self):
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = False
        self.in_points = True
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.style_points.LastPickedActor = None
        self.SetInteractorStyle(self.style_points)
        self.GetRenderWindow().AddRenderer(self.renderer_points)
        self.renderer_points.ResetCamera()
        self.update()

    def plot_entities(self):
        for actor in self.renderer_entities.GetActors():
            self.renderer_entities.RemoveActor(actor)
        self.actors_entities = {}
    
        for entity in self.project.getEntities():
            plot = Lines(entity.getNodes(), entity.getElements(), entity.getTag())
            plot.assembly()
            self.actors_entities[plot.get_actor()] = entity.getTag()
            self.renderer_entities.AddActor(plot.get_actor())
            
    def plot_elements(self):
        for actor in self.renderer_elements.GetActors():
            self.renderer_elements.RemoveActor(actor)
        self.actors_elements = {}

        for key, element in self.project.getElements().items():
            plot = Element(element, key)
            plot.assembly()
            self.actors_elements[plot.get_actor()] = key
            self.renderer_elements.AddActor(plot.get_actor())

    def getListPickedEntities(self):
        return self.style_entities.getListPickedActors()

    def getLastPickedEntity(self):
        if self.in_entities:
            return self.style_entities.getLastPickedActor()
        return None

    def getLastPickedPoint(self):
        if self.in_points:
            return self.style_points.getLastPickedActor()
        return None

    def plot_points(self):
        for actor in self.renderer_points.GetActors():
            self.renderer_points.RemoveActor(actor)
        self.actors_points = {}

        # #Add actors
        # plot = LinesPoint(self.project.getNodes(), self.project.getElements(), -1)
        # plot.assembly()
        # self.renderer_points.AddActor(plot.get_actor())
        # self.actors_points[plot.get_actor()] = -1

        for key, node in self.project.getNodes().items():
            plot = Point(node.x, node.y, node.z, key)
            plot.assembly()
            self.actors_points[plot.get_actor()] = key
            self.renderer_points.AddActor(plot.get_actor())

        #self.change_to_points()






        # self.colorbar = vtk.vtkScalarBarActor()
        # self.colorbar.SetMaximumNumberOfColors(400)
        # self.colorbar.SetLookupTable(self.plot.get_table())
        # self.colorbar.SetWidth(0.05)
        # self.colorbar.SetPosition(0.95, 0.1)
        # self.colorbar.SetLabelFormat("%.3g")
        # self.colorbar.VisibilityOn()

    # def add_actor(self):
    #     self.renderer.AddActor(self.colorbar)


    # def plot_nodes(self):
    #     self.before_plot()

    #     plot = Lines3(self.project.getNodes(), self.project.getElements(), -1)
    #     plot.assembly()
    #     self.renderer.AddActor(plot.get_actor())
    #     self.actors[plot.get_actor()] = -1

    #     for point in self.project.getNodes():
    #         print(point)
    #         plot = Point(point[1]/1000, point[2]/1000, point[3]/1000, point[0])
    #         plot.assembly()
    #         self.actors[plot.get_actor()] = point[0]
    #         self.renderer.AddActor(plot.get_actor())
    #     self.after_plot()

    def create_actions(self):
        self.cross_action = QAction('&Cross', self)        
        self.cross_action.setStatusTip("Set Cross Section")
        self.cross_action.triggered.connect(self.cross_call)

        self.dof_action = QAction('&DOF', self)        
        self.dof_action.setStatusTip("Set DOFs")
        self.dof_action.triggered.connect(self.dof_call)

        self.dof_import_action = QAction('&DOF_I', self)        
        self.dof_import_action.setStatusTip("Import DOF's")
        self.dof_import_action.triggered.connect(self.dof_import_call)

    def on_context_menu2(self, pos, type, id):
        #type 0 = Entity
        #type 1 = Element
        #Type 2 = Point
        menu = QMenu()
        if (type == 0 and self.in_entities):
            menu.addAction('Entity'+str(id))
            menu.addAction("Set Material")
            menu.addAction(self.cross_action)
        elif (type == 1 and self.in_elements):
            pass
        elif (type == 2 and self.in_points):
            menu.addAction("Point "+ str(id))
            menu.addAction(self.dof_action)
            menu.addAction(self.dof_import_action)
            menu.addAction("Set F")

        menu.exec_(self.mapToGlobal(pos))

    def on_context_menu(self, pos, type, id):
        #type 0 = Entity
        #type 1 = Element
        #Type 2 = Point
        print(pos)
        menu = QMenu()
        if (type == 0 and self.in_entities):
            menu.addAction('Entity'+str(id))
            menu.addAction("Set Material")
            menu.addAction(self.cross_action)
        elif (type == 1 and self.in_elements):
            pass
        elif (type == 2 and self.in_points):
            menu.addAction("Point "+ str(id))
            menu.addAction(self.dof_action)
            menu.addAction(self.dof_import_action)
            menu.addAction("Set F")

        menu.exec_(self.mapToGlobal(pos))

    def cross_call(self):
        CrossInput()

    def dof_call(self):
        DOFInput()

    def dof_import_call(self):
        ForceInput()

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
        