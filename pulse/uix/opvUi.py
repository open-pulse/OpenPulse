from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response

from pulse.uix.vtk.renderer.rendererEntity import RendererEntity
from pulse.uix.vtk.renderer.rendererElement import RendererElement
from pulse.uix.vtk.renderer.rendererPoint import RendererPoint
from pulse.uix.vtk.renderer.rendererPostProcessing import RendererPostProcessing


class OPVUi(QVTKRenderWindowInteractor):
    def __init__(self, project, parent):
        super().__init__()
        self.parent = parent
        self.project = project

        self.rendererEntity = RendererEntity(self.project, self)
        self.rendererElement = RendererElement(self.project, self)
        self.rendererPoint = RendererPoint(self.project, self)
        self.rendererAnalyse = RendererPostProcessing(self.project, self)

        self.slider2d = vtk.vtkSliderRepresentation2D()
        self.sliderScale = 1
        self.sliderEnable = True
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

        width, _ = self.rendererAnalyse.getSize()

        self.slider2d.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
        self.slider2d.GetPoint1Coordinate().SetValue(width-250,20)
        self.slider2d.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
        self.slider2d.GetPoint2Coordinate().SetValue(width-50, 20)

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
            self.changeAndPlotAnalyse(self.currentFrequencyIndice)

    def _updateSlider(self):
        if self.rendererAnalyse.getInUse():
            if not self.sliderEnable:
                self.sliderEnable = True
                self._createSlider()
        else:
            self.sliderEnable = False
    
    def changeFrequency(self, frequency_indice):
        if self.currentFrequencyIndice != frequency_indice:
            self.currentFrequencyIndice = frequency_indice
            self.sliderScale = 1
            self.slider2d.SetValue(self.sliderScale)
            self.needResetCamera = True

    def clearRendereres(self):
        self.GetRenderWindow().RemoveRenderer(self.rendererEntity.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererElement.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererPoint.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererAnalyse.getRenderer())

    def clearRendereresUse(self):
        self.rendererEntity.setInUse(False)
        self.rendererElement.setInUse(False)
        self.rendererPoint.setInUse(False)
        self.rendererAnalyse.setInUse(False)

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

    def changePlotToElements(self):
        self.beforeChangePlot()
        self.rendererElement.setInUse(True)
        self.SetInteractorStyle(self.rendererElement.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererElement.getRenderer())
        self.rendererElement.resetCamera()
        self.afterChangePlot()

    def changePlotToPoints(self):
        self.beforeChangePlot()
        self.rendererPoint.setInUse(True)
        self.SetInteractorStyle(self.rendererPoint.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererPoint.getRenderer())
        self.rendererPoint.resetCamera()
        self.afterChangePlot()

    def changeAndPlotAnalyse(self, frequency_indice, acoustic=False):
        self.beforeChangePlot()
        self.changeFrequency(frequency_indice)
        self.rendererAnalyse.setFrequencyIndice(self.currentFrequencyIndice)
        self.rendererAnalyse.setSliderFactor(self.sliderScale)
        self.rendererAnalyse.setInUse(True)
        self.SetInteractorStyle(self.rendererAnalyse.getStyle())
        self.GetRenderWindow().AddRenderer(self.rendererAnalyse.getRenderer())
        self.rendererAnalyse.plot(acoustic=acoustic)
        if self.needResetCamera:
            self.rendererAnalyse.resetCamera()
        self.afterChangePlot()

    def plotEntities(self, plotRadius = False):
        self.rendererEntity.setPlotRadius(plotRadius)
        self.rendererEntity.plot()

    def plotElements(self):
        self.rendererElement.plot()

    def plotPoints(self):
        self.rendererPoint.plot()

    def getListPickedEntities(self):
        return self.rendererEntity.getListPickedEntities()

    def getListPickedPoints(self):
        return self.rendererPoint.getListPickedPoints()

    def updateEntityRadius(self):
        self.plotEntities(self.rendererEntity.getPlotRadius())

    def changeColorEntities(self, entity_id, color):
        self.rendererEntity.changeColorEntities(entity_id, color)

    def changeColorCross(self):
        pass #Well.. Actually it is only here just in case it is necessary

    def changeColorPoints(self, points_id, color):
        self.rendererPoint.changeColorPoints(points_id, color)

    def transformPoints(self, points_id):
        self.rendererPoint.transformPoints(points_id)
        
    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()

   
    # def transformPoints(self, points_id):
    #     nodeAll = []
    #     nodeBC = []
    #     nodeF = []
    #     nodeND = []
    #     for node_id in points_id:
    #         node = self.project.getNode(node_id)
    #         if node.haveBoundaryCondition() and node.haveForce():
    #             nodeAll.append(node_id)
    #         elif node.haveBoundaryCondition():
    #             nodeBC.append(node_id)
    #             if sum([value for value in node.prescribed_DOFs_BC if value != None])==0:
    #                 colorBC = [0,0,0]
    #             else:
    #                 colorBC = [1,1,1]
    #             self.changeColorPoints(nodeBC, colorBC)
    #         elif node.haveForce():
    #             nodeF.append(node_id)
    #             colorF = [1,1,0]
    #             self.changeColorPoints(nodeF, colorF)
    #         else:
    #             nodeND.append(node_id)

    #     colorAll = [0,1,0]
    #     colorND = [0,0,1]
    #     self.changeColorPoints(nodeAll, colorAll)
    #     self.changeColorPoints(nodeND, colorND)

    #     self.transformPointsToCube(nodeND)
    #     self.transformPointsToSphere(nodeAll)
    #     self.transformPointsToSphere(nodeBC)
    #     self.transformPointsToSphere(nodeF)

