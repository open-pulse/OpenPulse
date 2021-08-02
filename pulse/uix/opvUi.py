from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from pulse.interface.opvRenderer import opvRenderer, ViewOptions, SelectOptions
from pulse.interface.opvAnalisysRenderer import opvAnalisysRenderer


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()

        self.parent = parent
        self.project = project

        self.inputObject = None
    
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False
        self.change_plot_to_custom = False

        self.opvRenderer = opvRenderer(self.project, self)
        self.opvAnalisysRenderer = opvAnalisysRenderer(self.project, self)

        self._createAxes()        

    def clearRendereres(self):
        self.GetRenderWindow().RemoveRenderer(self.opvRenderer.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.opvAnalisysRenderer.getRenderer())

    def clearRendereresUse(self):
        self.opvRenderer.setInUse(False)
        self.opvAnalisysRenderer.setInUse(False)

    def updatePlots(self):
        self.opvRenderer.plot()
        self.opvAnalisysRenderer.plot()
    
    def changePlotToEntities(self):
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = True
        self.change_plot_to_entities_with_cross_section = False

        viewOpt = ViewOptions.SHOW_LINES
        selectOpt = SelectOptions.SELECT_ENTITIES

        self.setRenderer(self.opvRenderer)
        self.opvRenderer.setShowOptions(viewOpt)
        self.opvRenderer.setSelectionOptions(selectOpt)

        self.opvRenderer.update()
        self._updateAxes()
    
    def changePlotToEntitiesWithCrossSection(self):
        self.change_plot_to_mesh = False
        self.change_plot_to_entities_with_cross_section = True
        self.change_plot_to_entities = False

        viewOpt = ViewOptions.SHOW_LINES | ViewOptions.SHOW_TUBES
        selectOpt = SelectOptions.SELECT_ENTITIES

        self.setRenderer(self.opvRenderer)
        self.opvRenderer.setShowOptions(viewOpt)
        self.opvRenderer.setSelectionOptions(selectOpt)

        self.opvRenderer.update()
        self._updateAxes()


    def changePlotToMesh(self):
        self.change_plot_to_mesh = True
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

        viewOpt = (
            ViewOptions.SHOW_NODES | ViewOptions.SHOW_LINES | ViewOptions.SHOW_SYMBOLS |
            ViewOptions.SHOW_TUBES | ViewOptions.SHOW_TRANSP
        )

        selectOpt = SelectOptions.SELECT_NODES | SelectOptions.SELECT_ELEMENTS

        self.setRenderer(self.opvRenderer)
        self.opvRenderer.setShowOptions(viewOpt)
        self.opvRenderer.setSelectionOptions(selectOpt)

        self.opvRenderer.update()
        self._updateAxes()

    def changePlotToCustom(self, viewOpt=1, selectOpt=2):
        self.setRenderer(self.opvRenderer)
        self.opvRenderer.setShowOptions(viewOpt)
        self.opvRenderer.setSelectionOptions(selectOpt)
        self.opvRenderer.update()
        self._updateAxes()

    def changeAndPlotAnalysis(self, frequency_indice, pressure_field_plot=False, stress_field_plot=False, real_part=True): 
        # we call it so many times in so many different files that 
        # i will just continue my code from here and we organize all 
        # these in the future.

        self.setRenderer(self.opvAnalisysRenderer)
        self.opvAnalisysRenderer.updateHud()

        if pressure_field_plot:
            self.opvAnalisysRenderer.showPressureField(frequency_indice, real_part)
        elif stress_field_plot:
            self.opvAnalisysRenderer.showStressField(frequency_indice, gain=1)
        else:
            self.opvAnalisysRenderer.showDisplacement(frequency_indice, gain=1)

        self._updateAxes()

        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False
        self.change_plot_to_entities_with_cross_section = False

    def setRenderer(self, renderer):
        self.clearRendereres()
        self.clearRendereresUse()
        renderer.setInUse(True)
        self.SetInteractorStyle(renderer.getStyle())
        self.GetRenderWindow().AddRenderer(renderer.getRenderer())


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

    def getListPickedEntities(self):
        return self.opvRenderer.getListPickedEntities()

    def transformPoints(self, *args, **kwargs):
        self.updatePlots()

    def updateEntityRadius(self, *args, **kwargs):
        self.updatePlots()

    def updateRendererMesh(self, *args, **kwargs):
        self.updatePlots()

    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()
