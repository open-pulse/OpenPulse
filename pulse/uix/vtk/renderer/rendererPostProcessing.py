from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorAnalyse import ActorAnalyse
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.colorTable import ColorTable
from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response
import vtk

class RendererPostProcessing(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorBase(self))
        self.project = project
        self.opv = opv
        self.textActorUnit = vtk.vtkTextActor()
        self.colorbar = vtk.vtkScalarBarActor()

        self.setUsePicker(False)

        self.frequencyIndice = -1
        self.sliderFactor = 1
        self.valueFactor = -1

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)

    def plot(self, acoustic=False):
        self.reset()
        if acoustic:
            _, connect, coord, r_def = get_acoustic_response(self.project.getMesh(), self.project.getAcousticSolution(), self.frequencyIndice)
        else:
            connect, coord, r_def, self.valueFactor  = get_structural_response(self.project.getMesh(), self.project.getStructuralSolution(), self.frequencyIndice, gain=self.sliderFactor)            

        # self.valueFactor
        colorTable = ColorTable(self.project, r_def)
        self.createColorBarActor(colorTable)

        # for entity in self.project.getEntities():
        #     plot = ActorAnalyse(self.project, entity, connect, coord, colorTable)
        #     plot.build()
        #     self._renderer.AddActor(plot.getActor())
    
        plot = ActorAnalyse(self.project, connect, coord, colorTable)
        plot.build()
        self._renderer.AddActor(plot.getActor())

        for node in self.project.getNodesBC():
            if sum([value for value in node.prescribed_DOFs_BC  if value != None])==0:
                point = ActorPoint(node)
            else:
                point = ActorPoint(node, u_def=coord[node.global_index,1:])
            point.build()
            self._renderer.AddActor(point.getActor())
        self._renderer.AddActor(self.colorbar)

        self.updateInfoText()
        self.updateUnitText()
        self.createScaleActor()

    def updateInfoText(self):
        mode = self.project.getModes()
        frequencies = self.project.getFrequencies()
        text = self.project.analysisType + "\n"
        if self.project.analysisID != 2:
            text += self.project.analysisMethod + "\n"
        else:
            frequencies = self.project.getNaturalFrequencies()
            text += "Mode: {}\n".format(mode)
        text += "Frequency: {:.3f} [Hz]\n".format(frequencies[self.frequencyIndice])
        text += "Magnification factor {:.1f}x\n".format(self.valueFactor)
        self.createInfoText(text)

    def updateUnitText(self):
        self._renderer.RemoveActor2D(self.textActorUnit)
        unit = self.project.getUnit()
        text = "Unit: [{}]".format(unit)
        self.textActorUnit.SetInput(text)
        width, height = self._renderer.GetSize()
        self.textActorUnit.SetDisplayPosition(width-100,height-30)
        self._renderer.AddActor2D(self.textActorUnit)

    def createColorBarActor(self, colorTable):
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetLookupTable(colorTable)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.90, 0.1)
        self.colorbar.SetLabelFormat("%.1g")
        self.colorbar.VisibilityOn()

    def createScaleActor(self):
        scale = vtk.vtkLegendScaleActor()
        scale.AllAxesOff()
        self._renderer.AddActor(scale)

    def setFrequencyIndice(self, frequencyIndice):
        self.frequencyIndice = frequencyIndice

    def setSliderFactor(self, factor):
        self.sliderFactor = factor

    def update(self):
        self.opv.update()