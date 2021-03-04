from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from time import sleep
import vtk

from pulse.uix.vtk.renderer.rendererEntity import RendererEntity
from pulse.uix.vtk.renderer.rendererElement import RendererElement
from pulse.uix.vtk.renderer.rendererMesh import RendererMesh
from pulse.uix.vtk.renderer.rendererPoint import RendererPoint
from pulse.uix.vtk.renderer.rendererPostProcessing import RendererPostProcessing
from pulse.interface.opvRenderer import opvRenderer
from pulse.interface.opvAnalisysRenderer import opvAnalisysRenderer


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()

        self.parent = parent
        self.project = project
    
        self.change_plot_to_mesh = False
        self.change_plot_to_entities = False

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
        self.setRenderer(self.opvRenderer)

        self.opvRenderer.showNodes(False)
        self.opvRenderer.showLines(True)
        self.opvRenderer.showSymbols(False)
        self.opvRenderer.showTubes(False)
        self.opvRenderer.update()

        self.opvRenderer.selectNodes(False)
        self.opvRenderer.selectElements(False)
        self.opvRenderer.selectEntities(True)

        self._updateAxes()

    
    def changePlotToEntitiesWithCrossSection(self):
        self.setRenderer(self.opvRenderer)

        self.opvRenderer.showNodes(False)
        self.opvRenderer.showLines(False)
        self.opvRenderer.showSymbols(False)
        self.opvRenderer.showTubes(True, transparent=False)
        self.opvRenderer.update()

        self.opvRenderer.selectNodes(False)
        self.opvRenderer.selectElements(False)
        self.opvRenderer.selectEntities(True)

        self._updateAxes()


    def changePlotToMesh(self):
        self.setRenderer(self.opvRenderer)

        self.opvRenderer.showNodes(True)
        self.opvRenderer.showLines(True)
        self.opvRenderer.showSymbols(True)
        self.opvRenderer.showTubes(True, transparent=True)
        self.opvRenderer.update()

        self.opvRenderer.selectNodes(True)
        self.opvRenderer.selectElements(True)
        self.opvRenderer.selectEntities(False)

        self._updateAxes()

    def changeAndPlotAnalysis(self, frequency_indice, pressure_field_plot=False, stress_field_plot=False, real_part=True): 
        # we call it so many times in so many different files that 
        # i will just continue my code from here and we organize all 
        # these in the future. Im sorry

        self.setRenderer(self.opvAnalisysRenderer)
        self.opvAnalisysRenderer.updateHud()

        if pressure_field_plot:
            self.opvAnalisysRenderer.showPressureField(frequency_indice, real_part)
        elif stress_field_plot:
            self.opvAnalisysRenderer.showStressField(frequency_indice, gain=1)
        else:
            self.opvAnalisysRenderer.showDisplacement(frequency_indice, gain=1)

        self._updateAxes()

    def setRenderer(self, renderer):
        # if renderer.getInUse(): 
        #     return
        
        self.clearRendereres()
        self.clearRendereresUse()
        renderer.setInUse(True)
        self.SetInteractorStyle(renderer.getStyle())
        self.GetRenderWindow().AddRenderer(renderer.getRenderer())

    def updateDialogs(self):
        pass

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

    def setInputObject(self, obj):
        self.inputObject = obj

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
