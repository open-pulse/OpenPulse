from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
#from pulse.opv.lines import Lines
from pulse.opv.lines import Lines
from pulse.opv.linesPoint import LinesPoint
from pulse.opv.preProcessingLines import PreProcessingLines
from pulse.opv.postProcessingLines import PostProcessingLines
from pulse.opv.point import Point
from pulse.opv.element import Element
from pulse.opv.colorTable import ColorTable
from pulse.postprocessing.plot_data import get_displacement_matrix

from pulse.uix.vtk.mouseInteractorPoint import MouseInteractorPoint
from pulse.uix.vtk.mouseInteractorElement import MouseInteractorElement
from pulse.uix.vtk.mouseInteractorEntity import MouseInteractorEntity
from pulse.uix.vtk.mouseInteractorPostProcessing import MouseInteractorPostProcessing


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
        self.renderer_pre_processing = vtk.vtkRenderer()

        self.renderer_entities.SetBackground(0.2,0.2,0.2)
        self.renderer_elements.SetBackground(0.2,0.2,0.2)
        self.renderer_points.SetBackground(0.2,0.2,0.2)
        self.renderer_pre_processing.SetBackground(0.2,0.2,0.2)

        #self.style_entities = MouseInteractorTemp(self)
        self.style_entities = MouseInteractorEntity(self)
        self.style_elements = MouseInteractorElement(self)
        self.style_points = MouseInteractorPoint(self)
        self.style_pre_processing = MouseInteractorPostProcessing(self)

        self.style_entities.SetDefaultRenderer(self.renderer_entities)
        self.style_elements.SetDefaultRenderer(self.renderer_elements)
        self.style_points.SetDefaultRenderer(self.renderer_points)
        self.style_pre_processing.SetDefaultRenderer(self.renderer_pre_processing)

        self.textActorEntity = vtk.vtkTextActor()
        self.textActorPoint = vtk.vtkTextActor()
        self.textActorPreProcessing = vtk.vtkTextActor()

        self.colorbar = vtk.vtkScalarBarActor()

        self.in_entities = False
        self.in_elements = False
        self.in_points = False
        self.in_direct = False
        self.in_modal = False

        self.changedSelectedEntityColors = False

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

    def resetInfo(self):
        for actor in self.renderer_entities.GetActors():
            self.renderer_entities.RemoveActor(actor)
        self.actors_entities = {}

        for actor in self.renderer_elements.GetActors():
            self.renderer_elements.RemoveActor(actor)
        self.actors_elements = {}

        for actor in self.renderer_points.GetActors():
            self.renderer_points.RemoveActor(actor)
        self.actors_points = {}

        self.style_entities.clear()
        self.style_elements.clear()
        self.style_points.clear()

        self.update_text_actor_entity()

    def update_text_actor_entity(self):
        self.renderer_entities.RemoveActor2D(self.textActorEntity)
        actors_id = self.getListPickedEntities()
        if len(actors_id) == 0:
            self.textActorEntity.SetInput("")
        elif len(actors_id) == 1:
            entity = self.project.getEntity(actors_id[0])
            material_name = "Undefined"
            diam_ext = "Undefined"
            diam_int = "Undefined"
            if entity.getMaterial() is not None:
                material_name = entity.getMaterial().getName()
            if entity.getCrossSection() is not None:
                diam_ext = entity.getCrossSection().getExternalDiameter()
                diam_int = entity.getCrossSection().getInternalDiameter()
            text = "Line ID  {}\nMaterial:  {}\nExternal Diameter:  {}\nInternal Diameter:  {}".format(actors_id[0], material_name, diam_ext, diam_int)
            self.textActorEntity.SetInput(text)
        else:
            text = "Selected Lines:\n"
            i = 0
            for ids in actors_id:
                if i == 30:
                    text += "..."
                    break
                if i == 10 or i == 20:
                    text += "{}\n".format(ids)
                else:
                    text += "{}  ".format(ids)
                i+=1
            self.textActorEntity.SetInput(text)

        width, height = self.renderer_entities.GetSize()
        self.textActorEntity.SetDisplayPosition(width-250,35)
        self.renderer_entities.AddActor2D(self.textActorEntity)

    def update_text_actor_point(self):
        self.renderer_points.RemoveActor2D(self.textActorPoint)
        actors_id = self.getListPickedPoints()
        if len(actors_id) == 0:
            self.textActorPoint.SetInput("")
        elif len(actors_id) == 1:
            node = self.project.getNode(int(actors_id[0]))
            text = "Node ID  {}\nPosition:  ({:.3f}, {:.3f}, {:.3f})\nDisplacement:  ({}, {}, {})\nRotation:  ({}, {}, {})".format(actors_id[0], node.x, node.y, node.z, node.getBondaryCondition()[0], node.getBondaryCondition()[1], node.getBondaryCondition()[2], node.getBondaryCondition()[3], node.getBondaryCondition()[4], node.getBondaryCondition()[5])
            self.textActorPoint.SetInput(text)
        else:
            text = "Selected Points:\n"
            i = 0
            for ids in actors_id:
                if i == 30:
                    text += "..."
                    break
                if i == 10 or i == 20:
                    text += "{}\n".format(ids)
                else:
                    text += "{}  ".format(ids)
                i+=1
            self.textActorPoint.SetInput(text)

        width, height = self.renderer_points.GetSize()
        self.textActorPoint.SetDisplayPosition(width-250,35)
        self.renderer_points.AddActor2D(self.textActorPoint)

    def update_text_actor_post_processing(self, type_, frequency, frequencies, modal=None):
        self.renderer_pre_processing.RemoveActor2D(self.textActorPreProcessing)
        text = ""
        if type_ == 1:
            text += "Direct Method\n"
        elif type_ == 2:
            text += "Modal Superposition\nModes: {}\n".format(modal)
        text += "Frequency: {}\n".format(frequencies[frequency])
        text += "Frequency List: {}".format(frequencies)
        self.textActorPreProcessing.SetInput(text)
        width, height = self.renderer_pre_processing.GetSize()
        self.textActorPreProcessing.SetDisplayPosition(width-250,35)
        self.renderer_pre_processing.AddActor2D(self.textActorPreProcessing)

    def create_colorBarActor(self, colorTable):
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetLookupTable(colorTable)
        self.colorbar.SetWidth(0.05)
        self.colorbar.SetPosition(0.95, 0.1)
        self.colorbar.SetLabelFormat("%.3g")
        self.colorbar.VisibilityOn()
        
    def _create_axes(self):
        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

        

        

        # self.slider = vtk.vtkSliderRepresentation2D()
        # self.slider.SetMinimumValue(-4.5)
        # self.slider.SetMaximumValue(4.5)
        # self.slider.SetValue(-4.5)
        # self.slider.SetTitleText("U min")

        # self.slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        # self.slider.GetPoint1Coordinate().SetValue(40, 40)
        # self.slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        # self.slider.GetPoint2Coordinate().SetValue(100, 40)

        # tubeWidth = 0.1
        # sliderLength = 0.1
        # titleHeight = 0.1
        # labelHeight = 0.1

        # self.slider.SetTubeWidth(tubeWidth)
        # self.slider.SetSliderLength(sliderLength)
        # self.slider.SetTitleHeight(titleHeight)
        # self.slider.SetLabelHeight(labelHeight)

        # self.w = vtk.vtkSliderWidget()
        # self.w.SetInteractor(self)
        # self.w.SetRepresentation(self.slider)
        # #self.w.SetAnimationModeToAnimate()
        # self.w.EnabledOn()

    def _atualizar_axes(self):
        self.axes.SetEnabled(0)
        self._create_axes()

    def remove_all_renderers(self):
        self.GetRenderWindow().RemoveRenderer(self.renderer_entities)
        self.GetRenderWindow().RemoveRenderer(self.renderer_elements)
        self.GetRenderWindow().RemoveRenderer(self.renderer_points)
        self.GetRenderWindow().RemoveRenderer(self.renderer_pre_processing)

    def change_to_entities(self):
        self.remove_all_renderers()
        self.in_entities = True
        self.in_elements = False
        self.in_points = False
        self.in_direct = False
        self.in_modal = False
        self.SetInteractorStyle(self.style_entities)
        self.GetRenderWindow().AddRenderer(self.renderer_entities)
        self.renderer_entities.ResetCamera()
        self._atualizar_axes()
        self.update()

    def change_to_elements(self):
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = True
        self.in_points = False
        self.in_direct = False
        self.in_modal = False
        self.SetInteractorStyle(self.style_elements)
        self.GetRenderWindow().AddRenderer(self.renderer_elements)
        self.renderer_elements.ResetCamera()
        self._atualizar_axes()
        self.update()

    def change_to_points(self):
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = False
        self.in_points = True
        self.in_direct = False
        self.in_modal = False
        self.SetInteractorStyle(self.style_points)
        self.GetRenderWindow().AddRenderer(self.renderer_points)
        self.renderer_points.ResetCamera()
        self._atualizar_axes()
        self.update()

    def change_to_direct_method(self, frequency_indice):
        self.style_entities.clear()
        self.style_elements.clear()
        self.style_points.clear()
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = False
        self.in_points = False
        self.in_direct = True
        self.in_modal = False
        self.plot_direct_method(self.project.getDirectMatriz(), frequency_indice)
        self.SetInteractorStyle(self.style_pre_processing)
        self.GetRenderWindow().AddRenderer(self.renderer_pre_processing)
        self.renderer_pre_processing.ResetCamera()
        self._atualizar_axes()
        self.update_text_actor_post_processing(1, frequency_indice, self.project.getFrequencies())
        self.update() 

    def change_to_modal_superposition(self, frequency_indice):
        self.style_entities.clear()
        self.style_elements.clear()
        self.style_points.clear()
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = False
        self.in_points = False
        self.in_direct = False
        self.in_modal = True
        self.plot_modal_superposition(self.project.getModalMatriz(), frequency_indice)
        self.SetInteractorStyle(self.style_pre_processing)
        self.GetRenderWindow().AddRenderer(self.renderer_pre_processing)
        self.renderer_pre_processing.ResetCamera()
        self._atualizar_axes()
        self.update_text_actor_post_processing(2, frequency_indice, self.project.getFrequencies(), self.project.getModes())
        self.update()

    def changeFrequency(self, frequency_indice):
        if self.in_direct:
            self.plot_direct_method(self.project.getDirectMatriz(), frequency_indice)
            self.update_text_actor_post_processing(1, frequency_indice, self.project.getFrequencies())
        elif self.in_modal:
            self.plot_modal_superposition(self.project.getModalMatriz(), frequency_indice)
            self.update_text_actor_post_processing(2, frequency_indice, self.project.getFrequencies(), self.project.getModes())

    def plot_modal_superposition(self, modal, frequency_indice):
        for actor in self.renderer_pre_processing.GetActors():
            self.renderer_pre_processing.RemoveActor(actor)

        coord_def, r_def = get_displacement_matrix(self.project.getMesh(), modal, frequency_indice)
        #matriz = get_displacement_matrix(self.project.getMesh(), modal, frequency_indice)
        colorTable = ColorTable(self.project, r_def)
        self.create_colorBarActor(colorTable)
        plot = PostProcessingLines(self.project, coord_def, colorTable)
        plot.assembly()
        self.renderer_pre_processing.AddActor(plot.get_actor())
        self.renderer_pre_processing.AddActor(self.colorbar)

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_pre_processing.AddActor(scale)

    def plot_direct_method(self, direct, frequency_indice):
        for actor in self.renderer_pre_processing.GetActors():
            self.renderer_pre_processing.RemoveActor(actor)

        coord_def, r_def = get_displacement_matrix(self.project.getMesh(), direct, frequency_indice)
        #matriz = get_displacement_matrix(self.project.getMesh(), direct, frequency_indice)
        colorTable = ColorTable(self.project, r_def)
        self.create_colorBarActor(colorTable)
        plot = PostProcessingLines(self.project, coord_def, colorTable)
        plot.assembly()
        self.renderer_pre_processing.AddActor(plot.get_actor())
        self.renderer_pre_processing.AddActor(self.colorbar)

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_pre_processing.AddActor(scale)

    def plot_entities(self):
        for actor in self.renderer_entities.GetActors():
            self.renderer_entities.RemoveActor(actor)
        self.actors_entities = {}

        for entity in self.project.getEntities():
            plot = Lines(entity)
            plot.assembly()
            self.actors_entities[plot.get_actor()] = entity.getTag()
            self.renderer_entities.AddActor(plot.get_actor())
    
        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_entities.AddActor(scale)

    def plot_elements(self):
        for actor in self.renderer_elements.GetActors():
            self.renderer_elements.RemoveActor(actor)
        self.actors_elements = {}

        for key, element in self.project.getElements().items():
            plot = Element(element, key)
            plot.assembly()
            self.actors_elements[plot.get_actor()] = key
            self.renderer_elements.AddActor(plot.get_actor())
        
        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_elements.AddActor(scale)

    def changeColorEntities(self, entity_id, color):
        actors = [key  for (key, value) in self.actors_entities.items() if value in entity_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)
        self.update_text_actor_entity()
        self.style_entities.clear()

    def changeColorCross(self):
        self.update_text_actor_entity()
        #...

    def changeColorPoints(self, points_id, color):
        actors = [key  for (key, value) in self.actors_points.items() if value in points_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)
        self.update_text_actor_point()
        self.style_points.clear()

    def getListPickedEntities(self):
        return self.style_entities.getListPickedActors()

    def getListPickedPoints(self):
        return self.style_points.getListPickedActors()

    def plot_points(self):
        for actor in self.renderer_points.GetActors():
            self.renderer_points.RemoveActor(actor)
        self.actors_points = {}

        for entity in self.project.getEntities():
            plot = LinesPoint(entity)
            plot.assembly()
            self.renderer_points.AddActor(plot.get_actor())
            self.actors_points[plot.get_actor()] = -1

        for key, node in self.project.getNodes().items():
            plot = Point(node, key)
            plot.assembly()
            self.actors_points[plot.get_actor()] = key
            self.renderer_points.AddActor(plot.get_actor())

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_points.AddActor(scale)

    #====================

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
