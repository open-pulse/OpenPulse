from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response

from pulse.uix.vtk.renderer.rendererEntity import RendererEntity
from pulse.uix.vtk.renderer.rendererMesh import RendererMesh
from pulse.uix.vtk.renderer.rendererPostProcessing import RendererPostProcessing


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()
        self.parent = parent
        self.project = project

        self.rendererEntity = RendererEntity(self.project, self)
        self.rendererMesh = RendererMesh(self.project, self)
        self.rendererAnalysis = RendererPostProcessing(self.project, self)

        self.slider2d = vtk.vtkSliderRepresentation2D()
        self.sliderScale = 1
        self.sliderEnable = False
        self.currentFrequencyIndice = -1
        self.needResetCamera = True

        #Set initial plot & config
        self.SetInteractorStyle(self.rendererEntity.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererEntity.getRenderer())
        self.rendererEntity.resetCamera()
        self.update()

        self._createAxes()

        self.Initialize()         #VTK Initialize - Don't remove this function

    def _createAxes(self):
        axesActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def _updateAxes(self):
        #It's necessary because after change the renderer the axe freeze.
        self.axes.SetEnabled(0)
        self._createAxes()

    def _createSlider(self):
        #Empiric values
        tubeWidth = 0.005
        sliderLength = 0.01
        sliderWidth = 0.01
        titleHeight = 0.015
        labelHeight = 0.015

        self.slider2d.SetMinimumValue(0)
        self.slider2d.SetMaximumValue(2)
        self.slider2d.SetValue(self.sliderScale)
        self.slider2d.SetEndCapWidth(0.02)
        self.slider2d.SetEndCapLength(0.01)
        #self.slider2d.SetTitleText('Scale')

        width, height = self.rendererAnalysis.getSize()
        height -= 150
        width = 20

        self.slider2d.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
        self.slider2d.GetPoint1Coordinate().SetValue(width,height)
        self.slider2d.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
        self.slider2d.GetPoint2Coordinate().SetValue(width + 200, height)

        self.slider2d.SetTubeWidth(tubeWidth)
        self.slider2d.SetSliderLength(sliderLength)
        self.slider2d.SetSliderWidth(sliderWidth)
        self.slider2d.SetTitleHeight(titleHeight)
        self.slider2d.SetLabelHeight(labelHeight)

        self.sliderW = vtk.vtkSliderWidget()
        self.sliderW.SetInteractor(self)
        self.sliderW.SetRepresentation(self.slider2d)
        self.sliderW.SetAnimationModeToOff()
        self.sliderW.SetNumberOfAnimationSteps(10)
        self.sliderW.SetEnabled(True)
        self.sliderW.AddObserver(vtk.vtkCommand.InteractionEvent,self._sliderCallback)

    def _sliderCallback(self, slider, b):
        sliderValue = slider.GetRepresentation().GetValue()
        truncNumber = float("{:.1f}".format(sliderValue))
        if truncNumber != self.sliderScale:
            self.sliderScale = truncNumber
            self.needResetCamera = False
            self.changeAndPlotAnalysis(self.currentFrequencyIndice)

    def _updateSlider(self):
        if self.rendererAnalysis.getInUse():
            if self.project.plot_pressure_field:
                self._createSlider()
                self.sliderW.SetEnabled(False)
                self.sliderEnable = False
            elif not self.sliderEnable:
                self.sliderEnable = True
                self._createSlider()
    
    def changeFrequency(self, frequency_indice):
        if self.currentFrequencyIndice != frequency_indice:
            self.currentFrequencyIndice = frequency_indice
            self.sliderScale = 1
            self.slider2d.SetValue(self.sliderScale)
            self.needResetCamera = True

    def clearRendereres(self):
        self.GetRenderWindow().RemoveRenderer(self.rendererEntity.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererMesh.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererAnalysis.getRenderer())

    def clearRendereresUse(self):
        self.rendererEntity.setInUse(False)
        self.rendererMesh.setInUse(False)
        self.rendererAnalysis.setInUse(False)

    def beforeChangePlot(self):
        self.clearRendereres()
        self.clearRendereresUse()

    def afterChangePlot(self):
        self._updateAxes()
        self._updateSlider()
        self.update()

    def changePlotToEntities(self):
        self.beforeChangePlot()
        self.rendererEntity.setInUse(True)
        self.SetInteractorStyle(self.rendererEntity.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererEntity.getRenderer())
        self.rendererEntity.resetCamera()
        self.afterChangePlot()

    def changePlotToMesh(self):
        self.beforeChangePlot()
        self.rendererMesh.setInUse(True)
        self.rendererMesh.resetPlot()
        self.SetInteractorStyle(self.rendererMesh.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererMesh.getRenderer())
        self.rendererMesh.resetCamera()
        self.afterChangePlot()

    def changeAndPlotAnalysis(self, frequency_indice, acoustic=False):
        self.beforeChangePlot()
        self.changeFrequency(frequency_indice)
        self.rendererAnalysis.setFrequencyIndice(self.currentFrequencyIndice)
        self.rendererAnalysis.setSliderFactor(self.sliderScale)
        self.rendererAnalysis.setInUse(True)
        self.SetInteractorStyle(self.rendererAnalysis.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererAnalysis.getRenderer())
        self.rendererAnalysis.plot(acoustic=acoustic)
        if self.needResetCamera:
            self.rendererAnalysis.resetCamera()
        self.afterChangePlot()

    def plotEntities(self, plotRadius = False):
        self.rendererEntity.setPlotRadius(plotRadius)
        self.rendererEntity.plot()

    def plotMesh(self):
        self.rendererMesh.plot()

    def getListPickedEntities(self):
        return self.rendererEntity.getListPickedEntities()

    def getListPickedPoints(self):
        return self.rendererMesh.getListPickedPoints()

    def getListPickedElements(self):
        return self.rendererMesh.getListPickedElements()

    def updateEntityRadius(self):
        self.plotEntities(self.rendererEntity.getPlotRadius())

    def changeColorEntities(self, entity_id, color):
        self.rendererEntity.changeColorEntities(entity_id, color)

    def changeColorCross(self):
        pass #Well.. Actually it is only here just in case it is necessary

    def transformPoints(self, points_id):
        self.rendererMesh.transformPoints(points_id)
        
    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()
