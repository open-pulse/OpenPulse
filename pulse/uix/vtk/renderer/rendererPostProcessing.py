from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorAnalysis import ActorAnalysis
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.colorTable import ColorTable
from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkSymbols import vtkSymbols
import vtk
import numpy as np

class RendererPostProcessing(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.symbols = vtkSymbols()
        self.textActorUnit = vtk.vtkTextActor()
        self.textActorStress = vtk.vtkTextActor()
        self.colorbar = vtk.vtkScalarBarActor()
        self.setUsePicker(False)
        self.frequencyIndice = -1
        self.sliderFactor = 1
        self.valueFactor = -1
        self.stress_field_plot = False
        self.pressure_field_plot = False

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)

    def getColorTable(self, r_def=None):
        if self.stress_field_plot:
            return ColorTable(self.project, self.project.stresses_values_for_color_table, stress_field_plot=True)
        elif self.pressure_field_plot:
            return ColorTable(self.project, r_def, pressure_field_plot=True)
        else:
            return ColorTable(self.project, r_def)

    def plot(self, pressure_field_plot=False, stress_field_plot=False,  real_part = True):
        self.reset()
        self.stress_field_plot = stress_field_plot
        self.pressure_field_plot = pressure_field_plot
        if self.pressure_field_plot:
            _, connect, coord, r_def = get_acoustic_response( self.project.get_mesh(), 
                                                              self.project.get_acoustic_solution(), 
                                                              self.frequencyIndice,
                                                              real_part = real_part)
        else:
            connect, coord, r_def, self.valueFactor = get_structural_response(  self.project.get_mesh(), 
                                                                                self.project.get_structural_solution(), 
                                                                                self.frequencyIndice, 
                                                                                gain=self.sliderFactor)            

        # self.valueFactor
        colorTable = self.getColorTable(r_def=r_def)
        self.createColorBarActor(colorTable)

        # for entity in self.project.get_entities():
        #     plot = ActorAnalysis(self.project, entity, connect, coord, colorTable)
        #     plot.build()
        #     self._renderer.AddActor(plot.getActor())
    
        plot = ActorAnalysis(self.project, connect, coord, colorTable, self.stress_field_plot, self.pressure_field_plot)
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
        self.update_min_max_stresses_text()

    def update_min_max_stresses_text(self):
                
        min_stress = self.project.min_stress
        max_stress = self.project.max_stress
        stress_label = self.project.stress_label

        text = ""
        if self.project.min_stress != "" and self.project.max_stress != "":
            text += "Maximum {} stress: {:.3e} [Pa]\n".format(stress_label, max_stress)
            text += "Minimum {} stress: {:.3e} [Pa]\n".format(stress_label, min_stress)

        self.textActorStress.SetInput(text)
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(17)
        textProperty.SetBold(1)
        textProperty.SetItalic(1)
        self.textActorStress.SetTextProperty(textProperty)
        _, height = self._renderer.GetSize()
        self.textActorStress.SetDisplayPosition(600, height-75)
        self._renderer.AddActor2D(self.textActorStress)

    def updateInfoText(self):
        mode = self.frequencyIndice + 1
        frequencies = self.project.get_frequencies()
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID not in [2,4]:
            text += self.project.analysis_method_label + "\n"
        elif self.project.analysis_ID == 2:
            frequencies = self.project.get_structural_natural_frequencies()
            text += "Mode: {}\n".format(mode)
        elif self.project.analysis_ID == 4:
            frequencies = self.project.get_acoustic_natural_frequencies()
            text += "Mode: {}\n".format(mode)
        text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self.frequencyIndice])
        if not self.project.plot_pressure_field:
            text += "\nMagnification factor {:.1f}x\n".format(self.valueFactor)
        # vertical_position_adjust = None
        self.createInfoText(text)

    def updateUnitText(self):
        if self.project.stresses_values_for_color_table == []:
            self.stress_field_plot = False
        self._renderer.RemoveActor2D(self.textActorUnit)   
        unit = self.project.get_unit(stress=self.stress_field_plot)
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