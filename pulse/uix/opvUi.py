from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
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
        self.renderer_post_processing = vtk.vtkRenderer()

        self.renderer_entities.SetBackground(0.2,0.2,0.2)
        self.renderer_elements.SetBackground(0.2,0.2,0.2)
        self.renderer_points.SetBackground(0.2,0.2,0.2)
        self.renderer_post_processing.SetBackground(0.2,0.2,0.2)

        self.style_entities = MouseInteractorEntity(self)
        self.style_elements = MouseInteractorElement(self)
        self.style_points = MouseInteractorPoint(self)
        self.style_post_processing = MouseInteractorPostProcessing(self)

        self.style_entities.SetDefaultRenderer(self.renderer_entities)
        self.style_elements.SetDefaultRenderer(self.renderer_elements)
        self.style_points.SetDefaultRenderer(self.renderer_points)
        self.style_post_processing.SetDefaultRenderer(self.renderer_post_processing)

        self.textActorEntity = vtk.vtkTextActor()
        self.textActorPoint = vtk.vtkTextActor()
        self.textActorPostProcessing = vtk.vtkTextActor()
        self.textUnit = vtk.vtkTextActor()

        self.colorbar = vtk.vtkScalarBarActor()

        self.in_entities = False
        self.in_elements = False
        self.in_points = False
        self.in_result = False

        self.actors_entities = {}
        self.actors_elements = {}
        self.actors_points = {}

        #Set initial plot & config
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

        for actor in self.renderer_post_processing.GetActors():
            self.renderer_post_processing.RemoveActor(actor)

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

    def update_text_actor_post_processing(self, type_, frequency, frequencies, factor, modal=None):
        self.renderer_post_processing.RemoveActor2D(self.textActorPostProcessing)
        text = ""
        if type_ == 1:
            text += "Direct Method\n"
        elif type_ == 2:
            text += "Modal Superposition\nModes: {}\n".format(modal)
        text += "Frequency: {} [Hz]\n".format(frequencies[frequency])
        text += "Magnification factor {:.1f}x\n".format(factor)
        self.textActorPostProcessing.SetInput(text)
        width, height = self.renderer_post_processing.GetSize()
        self.textActorPostProcessing.SetDisplayPosition(width-250,35)
        self.renderer_post_processing.AddActor2D(self.textActorPostProcessing)

    def updateTextUnit(self, unit):
        self.renderer_post_processing.RemoveActor2D(self.textUnit)
        text = "Unit: [{}]".format(unit)
        self.textUnit.SetInput(text)
        width, height = self.renderer_post_processing.GetSize()
        self.textUnit.SetDisplayPosition(width-100,height-30)
        self.renderer_post_processing.AddActor2D(self.textUnit)

    def create_colorBarActor(self, colorTable):
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetLookupTable(colorTable)
        self.colorbar.SetWidth(0.06)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.90, 0.1)
        self.colorbar.SetLabelFormat("%.1g")
        self.colorbar.VisibilityOn()
        
    def _create_axes(self):
        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def _atualizar_axes(self):
        self.axes.SetEnabled(0)
        self._create_axes()

    def remove_all_renderers(self):
        self.GetRenderWindow().RemoveRenderer(self.renderer_entities)
        self.GetRenderWindow().RemoveRenderer(self.renderer_elements)
        self.GetRenderWindow().RemoveRenderer(self.renderer_points)
        self.GetRenderWindow().RemoveRenderer(self.renderer_post_processing)

    def beforeChangePlot(self):
        self.remove_all_renderers()
        self.in_entities = False
        self.in_elements = False
        self.in_points = False
        self.in_result = False

    def afterChangePlot(self):
        self._atualizar_axes()
        self.update()

    def change_to_entities(self):
        self.beforeChangePlot()
        self.in_entities = True
        self.SetInteractorStyle(self.style_entities)
        self.GetRenderWindow().AddRenderer(self.renderer_entities)
        self.renderer_entities.ResetCamera()
        self.afterChangePlot()

    def change_to_elements(self):
        self.beforeChangePlot()
        self.in_elements = True
        self.SetInteractorStyle(self.style_elements)
        self.GetRenderWindow().AddRenderer(self.renderer_elements)
        self.renderer_elements.ResetCamera()
        self.afterChangePlot()

    def change_to_points(self):
        self.beforeChangePlot()
        self.in_points = True
        self.SetInteractorStyle(self.style_points)
        self.GetRenderWindow().AddRenderer(self.renderer_points)
        self.renderer_points.ResetCamera()
        self.afterChangePlot()

    def change_to_direct_method(self, frequency_indice):
        self.beforeChangePlot()
        self.in_result = True
        factor = self.plot_direct_method(self.project.getSolution(), frequency_indice)
        self.SetInteractorStyle(self.style_post_processing)
        self.GetRenderWindow().AddRenderer(self.renderer_post_processing)
        self.renderer_post_processing.ResetCamera()
        self.update_text_actor_post_processing(1, frequency_indice, self.project.getFrequencies(), factor, self.project.getModes())
        self.updateTextUnit(self.project.getUnit())
        self.afterChangePlot()

    def change_to_modal_superposition(self, frequency_indice):
        self.beforeChangePlot()
        self.in_result = True
        factor = self.plot_modal_superposition(self.project.getSolution(), frequency_indice)
        self.SetInteractorStyle(self.style_post_processing)
        self.GetRenderWindow().AddRenderer(self.renderer_post_processing)
        self.renderer_post_processing.ResetCamera()
        self.update_text_actor_post_processing(2, frequency_indice, self.project.getFrequencies(), factor, self.project.getModes())
        self.updateTextUnit(self.project.getUnit())
        self.afterChangePlot()

    def change_to_modal_analyse(self, frequency_indice):
        self.beforeChangePlot()
        self.in_result = True
        self.plot_modal_analyse(self.project.getSolution(), frequency_indice)
        self.SetInteractorStyle(self.style_post_processing)
        self.GetRenderWindow().AddRenderer(self.renderer_post_processing)
        self.renderer_post_processing.ResetCamera()
        self.afterChangePlot()

    def plot_modal_analyse(self, modal, frequency_indice):
        for actor in self.renderer_post_processing.GetActors():
            self.renderer_post_processing.RemoveActor(actor)

        connect, coord_def, r_def, scale  = get_displacement_matrix(self.project.getMesh(), modal, frequency_indice)
        colorTable = ColorTable(self.project, r_def)
        self.create_colorBarActor(colorTable)
        plot = PostProcessingLines(self.project, connect, coord_def, colorTable)
        plot.assembly()
        self.renderer_post_processing.AddActor(plot.get_actor())
        self.renderer_post_processing.AddActor(self.colorbar)

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_post_processing.AddActor(scale)

    def plot_modal_superposition(self, modal, frequency_indice):
        for actor in self.renderer_post_processing.GetActors():
            self.renderer_post_processing.RemoveActor(actor)

        connect, coord_def, r_def, factor  = get_displacement_matrix(self.project.getMesh(), modal, frequency_indice)
        colorTable = ColorTable(self.project, r_def)
        self.create_colorBarActor(colorTable)
        plot = PostProcessingLines(self.project, connect, coord_def, colorTable)
        plot.assembly()
        self.renderer_post_processing.AddActor(plot.get_actor())
        self.renderer_post_processing.AddActor(self.colorbar)

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_post_processing.AddActor(scale)
        return factor

    def plot_direct_method(self, direct, frequency_indice):
        for actor in self.renderer_post_processing.GetActors():
            self.renderer_post_processing.RemoveActor(actor)

        connect, coord_def, r_def, factor  = get_displacement_matrix(self.project.getMesh(), direct, frequency_indice)
        colorTable = ColorTable(self.project, r_def)
        self.create_colorBarActor(colorTable)
        plot = PostProcessingLines(self.project, connect, coord_def, colorTable)
        plot.assembly()
        self.renderer_post_processing.AddActor(plot.get_actor())
        self.renderer_post_processing.AddActor(self.colorbar)

        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff ()
        self.renderer_post_processing.AddActor(scale)
        return factor

    def plot_entities(self):
        for actor in self.renderer_entities.GetActors():
            self.renderer_entities.RemoveActor(actor)
        self.actors_entities = {}

        for entity in self.project.getEntities():
            plot = Lines(entity)
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

    def changeColorEntities(self, entity_id, color):
        actors = [key  for (key, value) in self.actors_entities.items() if value in entity_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)
        self.update_text_actor_entity()
        self.style_entities.clear()

    def changeColorCross(self):
        self.update_text_actor_entity()
        #...

    def transformPoints(self, points_id):
        nodeAll = []
        nodeBC = []
        nodeF = []
        nodeND = []
        for node_id in points_id:
            node = self.project.getNode(node_id)
            if node.haveBoundaryCondition() and node.haveForce():
                nodeAll.append(node_id)
            elif node.haveBoundaryCondition():
                nodeBC.append(node_id)
            elif node.haveForce():
                nodeF.append(node_id)
            else:
                nodeND.append(node_id)

        colorAll = [0,1,0]
        colorBC = [0,1,1]
        colorF = [1,1,0]
        colorND = [0,0,1]
        self.changeColorPoints(nodeAll, colorAll)
        self.changeColorPoints(nodeBC, colorBC)
        self.changeColorPoints(nodeF, colorF)
        self.changeColorPoints(nodeND, colorND)

        self.transformPointsToCube(nodeND)
        self.transformPointsToSphere(nodeAll)
        self.transformPointsToSphere(nodeBC)
        self.transformPointsToSphere(nodeF)

        self.update_text_actor_point()
        self.style_points.clear()

    def changeColorPoints(self, points_id, color):
        actors = [key  for (key, value) in self.actors_points.items() if value in points_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)

    def transformPointsToSphere(self, points_id):
        actors = [key  for (key, value) in self.actors_points.items() if value in points_id]
        for actor in actors:
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(0.03)
            pos = actor.GetCenter()
            sphere.SetCenter(pos[0], pos[1], pos[2])
            sphere.SetPhiResolution(11)
            sphere.SetThetaResolution(21)
            actor.GetMapper().SetInputConnection(sphere.GetOutputPort())

    def transformPointsToCube(self, points_id):
        actors = [key  for (key, value) in self.actors_points.items() if value in points_id]
        for actor in actors:
            cube = vtk.vtkCubeSource()
            pos = actor.GetCenter()
            cube.SetXLength(0.01)
            cube.SetYLength(0.01)
            cube.SetZLength(0.01)
            cube.SetCenter(pos[0], pos[1], pos[2])
            actor.GetMapper().SetInputConnection(cube.GetOutputPort())

    def getListPickedEntities(self):
        return self.style_entities.getListPickedActors()

    def getListPickedPoints(self):
        return self.style_points.getListPickedActors()

    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()