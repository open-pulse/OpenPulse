from PyQt5 import Qt
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

# from pulse.postprocessing.plot_structural_data import get_structural_response
# from pulse.postprocessing.plot_acoustic_data import get_acoustic_response

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
        self.__lastCamera = None

        self.rendererEntity = RendererEntity(self.project, self)
        self.rendererElement = RendererElement(self.project, self)
        self.rendererMesh = RendererMesh(self.project, self)
        self.rendererAnalysis = RendererPostProcessing(self.project, self)

        self.opvRenderer = opvRenderer(self.project, self)
        self.opvAnalisysRenderer = opvAnalisysRenderer(self.project, self)

        self.slider2d = vtk.vtkSliderRepresentation2D()
        self.sliderScale = 1
        self.sliderEnable = False
        self.currentFrequencyIndice = -1
        self.needResetCamera = True

        self.inputObject = None

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
        self.sliderW.AddObserver(vtk.vtkCommand.InteractionEvent, self._sliderCallback)

    def _sliderCallback(self, slider, b):
        sliderValue = slider.GetRepresentation().GetValue()
        # truncNumber = float("{:.1f}".format(sliderValue))
        truncNumber = round(sliderValue, 1)

        if truncNumber != self.sliderScale:
            self.sliderScale = truncNumber
            self.slider2d.SetValue(truncNumber)
            self.needResetCamera = False
            self.changeAndPlotAnalysis(self.currentFrequencyIndice, stress_field_plot=self.rendererAnalysis.stress_field_plot)

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

    def copyCamera(self):
        if self.getActiveRenderer() is not None:
            ren = self.getActiveRenderer().getRenderer()
            cam = ren.GetActiveCamera()
            self.__lastCamera = cam
    
    def applyCamera(self):
        if self.__lastCamera is not None:
            ren = self.getActiveRenderer().getRenderer()
            ren.SetActiveCamera(self.__lastCamera)

    def clearRendereres(self):
        self.GetRenderWindow().RemoveRenderer(self.rendererEntity.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererMesh.getRenderer())
        self.GetRenderWindow().RemoveRenderer(self.rendererAnalysis.getRenderer())

        self.GetRenderWindow().RemoveRenderer(self.opvRenderer.getRenderer())

    def clearRendereresUse(self):
        self.rendererEntity.setInUse(False)
        self.rendererMesh.setInUse(False)
        self.rendererAnalysis.setInUse(False)
        self.opvRenderer.setInUse(False)
        print(self.rendererAnalysis.getInUse())

    def beforeChangePlot(self):
        self.copyCamera()
        self.clearRendereres()
        self.clearRendereresUse()

    def afterChangePlot(self):
        # self.applyCamera()
        self._updateAxes()
        self._updateSlider()
        self.update()

    def changePlotToEntities(self):
        # self.setRenderer(self.opvRenderer)

        # self.opvRenderer.showNodes(False)
        # self.opvRenderer.showLines(True)
        # self.opvRenderer.showDeformedTubes(False)
        # self.opvRenderer.showTubes(True, transparent=False)
        # self.opvRenderer.update()
        # self.opvRenderer.selectLines(False)
        # self.opvRenderer.selectTubes(False)
        # self.opvRenderer.selectNodes(False)
        # self.opvRenderer.selectEntities(True)

        # self._updateAxes()

        self.setRenderer(self.rendererEntity)
        self.rendererEntity.resetCamera()
        self.afterChangePlot()

    def changePlotToMesh(self):
        # self.setRenderer(self.opvRenderer)

        # self.opvRenderer.showNodes(True)
        # self.opvRenderer.showLines(True)
        # self.opvRenderer.showDeformedTubes(False)
        # self.opvRenderer.showTubes(True, transparent=True)
        # self.opvRenderer.update()
        # self.opvRenderer.selectLines(True)
        # self.opvRenderer.selectTubes(False)
        # self.opvRenderer.selectNodes(True)
        # self.opvRenderer.selectEntities(False)

        # self._updateAxes()

        self.setRenderer(self.rendererMesh)
        self.rendererMesh.resetCamera()
        self.afterChangePlot()


        
    def setRenderer(self, renderer):
        # if not renderer.getInUse(): 
        self.beforeChangePlot()
        renderer.setInUse(True)
        self.SetInteractorStyle(renderer.getStyle())
        self.GetRenderWindow().AddRenderer(renderer.getRenderer())

    def changeAndPlotAnalysis(self, frequency_indice, pressure_field_plot=False, stress_field_plot=False, real_part=True): 
        # we call it so many times in so many different files that 
        # i will just continue my code from here and we organize all 
        # these in the future. Im sorry

        self.setRenderer(self.opvAnalisysRenderer)
        self.opvAnalisysRenderer.updateHud()

        if pressure_field_plot:
            self.opvAnalisysRenderer.showPressureField(frequency_indice, real_part)
        elif True or stress_field_plot:
            # please be more carefull when calling this function and select
            # at least one between pressure_field_plot or stress_field_plot
            # then remove this "True or" statement
            self.opvAnalisysRenderer.showStressField(frequency_indice, gain=1)
        else:
            raise ValueError("Neither pressure_field_plot nor stress_field_plot were selected")

        self.afterChangePlot()
        self._updateAxes()
        
        # # TODO: delete this 
        # self.beforeChangePlot()
        # self.changeFrequency(frequency_indice)
        # self.rendererAnalysis.setFrequencyIndice(self.currentFrequencyIndice)
        # if self.project.analysis_ID in [4]:
        #     self.rendererAnalysis.setColorScalling(real_part)
        # self.rendererAnalysis.setSliderFactor(self.sliderScale)        
        # self.rendererAnalysis.setInUse(True)
        # # self.rendererAnalysis.setStress(plot_stress_field)
        # self.SetInteractorStyle(self.rendererAnalysis.getStyle())
        # self.GetRenderWindow().AddRenderer(self.rendererAnalysis.getRenderer())
        # self.rendererAnalysis.plot(pressure_field_plot=pressure_field_plot, stress_field_plot=stress_field_plot, real_part = real_part)
        # if self.needResetCamera:
        #     self.rendererAnalysis.resetCamera()
        # self.afterChangePlot()

    def plotEntities(self, plotRadius = False):
        self.rendererEntity.setPlotRadius(plotRadius)
        self.rendererEntity.plot()

    def plotMesh(self):
        self.opvRenderer.plot()
        self.opvAnalisysRenderer.plot()

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

    def updateRendererMesh(self):
        self.rendererMesh.plotNodes()
        self.rendererMesh.plotElasticLinks()

    def transformPoints(self, points_id):
        self.updateRendererMesh()
        self.rendererMesh.transformPoints(points_id)
        
    def savePNG(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()
    
    def getActiveRenderer(self):
        renderers = [self.rendererEntity, self.rendererElement, self.rendererMesh, self.rendererAnalysis]
        for renderer in renderers:
            if renderer._inUse:
                return renderer
        else:
            return None 

    def updateDialogs(self):
        if self.inputObject is None:
            return

        try:
            self.inputObject.update()
        except Exception:
            print("Update function error")

    def setInputObject(self, obj):
        self.inputObject = obj