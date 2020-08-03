from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorAnalysis import ActorAnalysis
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.colorTable import ColorTable
from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk
import numpy as np

class RendererPostProcessing(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.textActorUnit = vtk.vtkTextActor()
        self.colorbar = vtk.vtkScalarBarActor()
        self.setUsePicker(False)
        self.frequencyIndice = -1
        self.sliderFactor = 1
        self.valueFactor = -1
        self.stress = False

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)

    def setStress(self, value):
        self.stress = value

    def getStress(self):
        return self.stress

    def getColorTable(self, r_def=None):
        if self.stress:
            try:
                imported_data = np.loadtxt("./stress_data.dat", delimiter=" ")
                colorsValues = imported_data[:,3].tolist()
                return ColorTable(self.project, colorsValues)
            except Exception:
                print("Error Import File StressField")
                exit(0)
        else:
            return ColorTable(self.project, r_def)

    def plot(self, acoustic=False):
        self.reset()
        if acoustic:
            _, connect, coord, r_def = get_acoustic_response(self.project.get_mesh(), self.project.get_acoustic_solution(), self.frequencyIndice)
        else:
            connect, coord, r_def, self.valueFactor  = get_structural_response(self.project.get_mesh(), self.project.get_structural_solution(), self.frequencyIndice, gain=self.sliderFactor)            

        # self.valueFactor
        colorTable = self.getColorTable(r_def=r_def)
        self.createColorBarActor(colorTable)

        # for entity in self.project.get_entities():
        #     plot = ActorAnalysis(self.project, entity, connect, coord, colorTable)
        #     plot.build()
        #     self._renderer.AddActor(plot.getActor())
    
        plot = ActorAnalysis(self.project, connect, coord, colorTable, self.stress)
        plot.build()
        self._renderer.AddActor(plot.getActor())

        for node in self.project.get_nodes_bc():
            if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                point = ActorPoint(node, u_def=coord[node.global_index,1:])
            elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                point = ActorPoint(node, u_def=coord[node.global_index,1:])
            else:
                point = ActorPoint(node)
            point.build()
            self._renderer.AddActor(point.getActor())
        self._renderer.AddActor(self.colorbar)

        self.updateInfoText()
        self.updateUnitText()
        self.createScaleActor()

    def updateInfoText(self):
        mode = self.project.get_modes()
        frequencies = self.project.get_frequencies()
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID not in [2,4]:
            text += self.project.analysis_method_label + "\n"
        else:
            frequencies = self.project.get_structural_natural_frequencies()
            text += "Mode: {}\n".format(mode)
        text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self.frequencyIndice])
        if not self.project.plot_pressure_field:
            text += "\nMagnification factor {:.1f}x\n".format(self.valueFactor)
        vertical_position_adjust = None
        self.createInfoText(text, vertical_position_adjust)

    def updateUnitText(self):
        self._renderer.RemoveActor2D(self.textActorUnit)
        unit = self.project.get_unit()
        text = "Unit: [{}]".format(unit)
        self.textActorUnit.SetInput(text)
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(18)
        textProperty.SetBold(1)
        textProperty.SetItalic(1)
        self.textActorUnit.SetTextProperty(textProperty)
        width, height = self._renderer.GetSize()
        self.textActorUnit.SetDisplayPosition(width-90,height-35)
        self._renderer.AddActor2D(self.textActorUnit)

    def createColorBarActor(self, colorTable):
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(15)
        textProperty.SetItalic(1)
        self.colorbar.SetLabelTextProperty(textProperty)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetLookupTable(colorTable)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.95, 0.1)
        self.colorbar.SetLabelFormat("%1.0e ")
        self.colorbar.UnconstrainedFontSizeOn()       
        # print(self.colorbar.GetLabelTextProperty().GetFontSize())
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