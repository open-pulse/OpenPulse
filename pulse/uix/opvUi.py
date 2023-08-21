from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from pulse.interface.opvRenderer import opvRenderer, PlotFilter, SelectionFilter
from pulse.interface.opvGeometryRenderer import opvGeometryRenderer
from pulse.interface.opvAnalysisRenderer import opvAnalysisRenderer
from data.user_input.project.loadingScreen import LoadingScreen


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()

        self.parent = parent
        self.project = project

        self.inputObject = None
        self.defaultPreferences()
    
        self.opvRenderer = opvRenderer(self.project, self)
        self.opvAnalysisRenderer = opvAnalysisRenderer(self.project, self)
        self.opvGeometryRenderer = opvGeometryRenderer(self.project, self)

        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False
        self.change_plot_to_raw_lines = False

        self._createAxes()        

    def defaultPreferences(self):
        self.background_color = (0,0,0)
        self.font_color = (1,1,1)
        self.add_OpenPulse_logo = True
        self.add_MOPT_logo = True
        self.show_reference_scale = True

    def setUserInterfacePreferences(self, preferences):
        """
        """
        if preferences:

            self.background_color = preferences['background_color']
            self.font_color = preferences['font_color']
            self.nodes_color = preferences['nodes_color']
            self.lines_color = preferences['lines_color']
            self.surfaces_color = preferences['surfaces_color']
            self.add_OpenPulse_logo = preferences['OpenPulse_logo']
            self.add_MOPT_logo = preferences['mopt_logo']
            self.show_reference_scale = preferences['reference_scale']
            self.elements_transparency = preferences['transparency']
            #
            self.opvRenderer.changeBackgroundColor(self.background_color)
            self.opvAnalysisRenderer.changeBackgroundColor(self.background_color)
            self.opvGeometryRenderer.changeBackgroundColor(self.background_color)

            self.opvRenderer.changeFontColor(self.font_color)
            self.opvAnalysisRenderer.changeFontColor(self.font_color)
            self.opvGeometryRenderer.changeFontColor(self.font_color)

            self.opvRenderer.changeReferenceScaleFontColor(self.font_color)
            self.opvAnalysisRenderer.changeReferenceScaleFontColor(self.font_color)
            self.opvGeometryRenderer.changeReferenceScaleFontColor(self.font_color)

            self.opvRenderer.changeNodesColor(self.nodes_color)
            self.opvRenderer.changeSurfacesColor(self.surfaces_color)
            self.opvRenderer.changeElementsTransparency(self.elements_transparency)
        
    def clearRendereres(self):
        self.GetRenderWindow().RemoveRenderer(self.opvRenderer.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.opvAnalysisRenderer.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.opvGeometryRenderer.getRenderer())

    def clearRendereresUse(self):
        self.opvRenderer.setInUse(False)
        self.opvAnalysisRenderer.setInUse(False)
        self.opvGeometryRenderer.setInUse(False)

    def updatePlots(self):
        # def callback():
        self.project.preprocessor.add_lids_to_variable_cross_sections()
        self.opvRenderer.plot()
        self.opvAnalysisRenderer.plot()
        self.opvGeometryRenderer.plot()
        # LoadingScreen('Updating Plot', target=callback)

    def changePlotToRawGeometry(self):
        
        if self.opvGeometryRenderer.plot():
            return

        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False
        self.change_plot_to_raw_lines = True
        self.setRenderer(self.opvGeometryRenderer)

        plot_filter = PlotFilter(raw_lines=True)
        selection_filter = SelectionFilter()

        # self.opvRenderer.setPlotFilter(plot_filter)
        # self.opvRenderer.setSelectionFilter(selection_filter)
        self._updateAxes()

    def changePlotToEntities(self):
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = True
        self.change_plot_to_entities_with_cross_section = False
        self.change_plot_to_raw_lines = False
        self.setRenderer(self.opvRenderer)

        plot_filter = PlotFilter(lines=True)
        selection_filter = SelectionFilter(entities=True)

        self.opvRenderer.setPlotFilter(plot_filter)
        self.opvRenderer.setSelectionFilter(selection_filter)
        self._updateAxes()

    def changePlotToEntitiesWithCrossSection(self):
        self.change_plot_to_mesh = False
        self.change_plot_to_entities_with_cross_section = True
        self.change_plot_to_entities = False
        self.change_plot_to_raw_lines = False
        self.setRenderer(self.opvRenderer)

        plot_filter = PlotFilter(lines=True, tubes=True)
        selection_filter = SelectionFilter(entities=True)

        self.opvRenderer.setPlotFilter(plot_filter)
        self.opvRenderer.setSelectionFilter(selection_filter)
        self._updateAxes()

    def changePlotToMesh(self):
        self.change_plot_to_mesh = True
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False
        self.change_plot_to_raw_lines = False
        self.setRenderer(self.opvRenderer)

        plot_filter = PlotFilter(
            nodes=True,
            lines=True,
            tubes=True,
            transparent=True,
            acoustic_symbols=True,
            structural_symbols=True,
        )

        selection_filter = SelectionFilter(nodes=True, elements=True)

        self.opvRenderer.setPlotFilter(plot_filter)
        self.opvRenderer.setSelectionFilter(selection_filter)
        self._updateAxes()
    
    def custom_plot(self, plot_filter, selection_filter):
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

        self.setRenderer(self.opvRenderer)
        self.opvRenderer.setPlotFilter(plot_filter)
        self.opvRenderer.setSelectionFilter(selection_filter)
        self._updateAxes()

    def plot_displacement_field(self, frequency_indice, absolute=False):
        self.setRenderer(self.opvAnalysisRenderer)
        self.opvAnalysisRenderer.updateHud()
        self.opvAnalysisRenderer.showDisplacementField(frequency_indice, 
                                                       absolute=absolute)
        self._updateAxes()
        self.opvAnalysisRenderer._renderer.ResetCamera()
        #
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

    def plot_stress_field(self, frequency_indice, absolute=False): 
        self.setRenderer(self.opvAnalysisRenderer)
        self.opvAnalysisRenderer.updateHud()
        self.opvAnalysisRenderer.showStressField(frequency_indice, 
                                                   absolute=absolute)
        self._updateAxes()
        self.opvAnalysisRenderer._renderer.ResetCamera()
        #
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

    def plot_pressure_field(self, frequency_indice, absolute=False): 
        self.setRenderer(self.opvAnalysisRenderer)
        self.opvAnalysisRenderer.updateHud()
        self.opvAnalysisRenderer.showPressureField(frequency_indice, 
                                                   absolute=absolute)
        self._updateAxes()
        self.opvAnalysisRenderer._renderer.ResetCamera()
        #
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

    def setRenderer(self, renderer):
        if renderer.getInUse(): 
            return
        
        if (self.opvRenderer.getInUse()):
            lastCamera = self.opvRenderer._renderer.GetActiveCamera()

        elif (self.opvAnalysisRenderer.getInUse()):
            lastCamera = self.opvAnalysisRenderer._renderer.GetActiveCamera()

        elif (self.opvGeometryRenderer.getInUse()):
            lastCamera = self.opvGeometryRenderer._renderer.GetActiveCamera()
        
        else:
            lastCamera = None

        if lastCamera is not None:
            renderer._renderer.GetActiveCamera().DeepCopy(lastCamera)
        renderer._renderer.ResetCameraClippingRange()
        renderer._renderer.ResetCamera()

        self.clearRendereres()
        self.clearRendereresUse()
        renderer.setInUse(True)
        self.SetInteractorStyle(renderer.getStyle())
        self.GetRenderWindow().AddRenderer(renderer.getRenderer())

    def setCameraView(self, view=6):
        if (self.opvRenderer.getInUse()):
            x,y,z = self.opvRenderer._renderer.GetActiveCamera().GetFocalPoint()
        elif (self.opvAnalysisRenderer.getInUse()):
            x,y,z = self.opvAnalysisRenderer._renderer.GetActiveCamera().GetFocalPoint()
        elif (self.opvGeometryRenderer.getInUse()):
            x,y,z = self.opvGeometryRenderer._renderer.GetActiveCamera().GetFocalPoint()
        else:
            return

        vx, vy, vz = (0,1,0)

        ORTH   = 0
        TOP    = 1
        BOTTOM = 2
        LEFT   = 3 
        RIGHT  = 4
        FRONT  = 5
        BACK   = 6

        if view == TOP:
            y += 1
            vx, vy, vz = (0,0,-1)
        elif view == BOTTOM:
            y -= 1
            vx, vy, vz = (0,0,1)
        elif view == LEFT:
            x -= 1
        elif view == RIGHT:
            x += 1
        elif view == FRONT:
            z += 1
        elif view == BACK:
            z -= 1 
        elif view == ORTH:
            x -= 1
            y -= 1
            z -= 1
        else:
            return

        self.opvRenderer._renderer.GetActiveCamera().SetPosition(x, y, z)
        self.opvRenderer._renderer.GetActiveCamera().SetViewUp(vx, vy, vz)
        self.opvRenderer._renderer.GetActiveCamera().SetParallelProjection(True)
        self.opvRenderer._renderer.ResetCamera(*self.opvRenderer.getBounds())
        self.opvRenderer.update()

        self.opvGeometryRenderer._renderer.GetActiveCamera().SetPosition(x, y, z)
        self.opvGeometryRenderer._renderer.GetActiveCamera().SetViewUp(vx, vy, vz)
        self.opvGeometryRenderer._renderer.GetActiveCamera().SetParallelProjection(True)
        self.opvGeometryRenderer._renderer.ResetCamera(*self.opvGeometryRenderer.getBounds())
        self.opvGeometryRenderer.update()

        self.opvAnalysisRenderer._renderer.GetActiveCamera().SetPosition(x, y, z)
        self.opvAnalysisRenderer._renderer.GetActiveCamera().SetViewUp(vx, vy, vz)
        self.opvAnalysisRenderer._renderer.GetActiveCamera().SetParallelProjection(True)
        self.opvAnalysisRenderer._renderer.ResetCamera()
        self.opvAnalysisRenderer.update()

    def updateDialogs(self):
        if self.inputObject is None:
            return

        try:
            self.inputObject.update()
        except Exception:
            print("Update function error")

    def setInputObject(self, obj):
        self.inputObject = obj

    def _createAxes(self):
        axesActor = vtk.vtkAxesActor()
        
        axesActor.SetShaftTypeToCylinder()
        axesActor.SetCylinderRadius(0.03)
        axesActor.SetConeRadius(0.5)
        axesActor.SetNormalizedTipLength(0.25, 0.25, 0.25)
        axesActor.SetNormalizedLabelPosition(1.3,1.3,1.3)
        
        axesActor.SetXAxisLabelText("X")
        axesActor.SetYAxisLabelText("Y")
        axesActor.SetZAxisLabelText("Z")
        
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def _updateAxes(self):
        self.axes.EnabledOff()
        self._createAxes()

    def getListPickedPoints(self):
        return self.opvRenderer.getListPickedPoints()

    def getListPickedElements(self):
        return self.opvRenderer.getListPickedElements()

    def getListPickedLines(self):
        return self.opvRenderer.getListPickedLines()

    def updateEntityRadius(self, *args, **kwargs):
        self.opvRenderer.plot()
        self.opvAnalysisRenderer.plot()
        self.opvGeometryRenderer.plot()
        # self.updatePlots()

    def updateRendererMesh(self, *args, **kwargs):
        self.updatePlots()

    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()