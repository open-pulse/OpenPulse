from data.user_input.project.loading_screen import LoadingScreen
import vtk
import numpy as np
from math import pi
# import imageio
# import os

from pulse.postprocessing.plot_structural_data import get_structural_response, get_max_min_values_of_resultant_displacements, get_stresses_to_plot, get_min_max_stresses_values
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response, get_max_min_values_of_pressures

from pulse.uix.vtk.colorTable import ColorTable
from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
# from pulse.interface.symbolsActor import SymbolsActor
from pulse.interface.cutting_plane_actor import CuttingPlaneActor
from pulse.interface.tubeActor import TubeActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor
from pulse.interface.tubeClippableActor import TubeClippableActor
from pulse.interface.tubeClippableDeformedActor import TubeClippableDeformedActor

class opvAnalysisRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project
        self.opv = opv
        self.setUsePicker(False)

        self.hidden_elements = set()

        self._absolute = False
        self._scaling_setup = dict()
        self._magnificationFactor = 1
        self._currentFrequencyIndex = 0
        self._currentPhase = 0
        self._cacheFrequencyIndex = None
        self.last_frequency_index = None
        
        self._currentPlot = None
        self.colorbar = None 
        self.scaleBar = None

        self.playingAnimation = False
        self.animationIndex = 0
        self.delayCounter = 0
        self.increment = 1

        self.clipping_plane_active = False
        self.first_configuration = True
        self.plane_origin = None
        self.plane_normal = None

        #default values to the number of frames and cycles
        self.number_frames = 40
        self.number_cycles = 5
        self.count_cycles = 0
        self.total_frames = (self.number_frames+1)*self.number_cycles
        self.number_frames_changed = False
        self.export_animation = False
        self.update_phase_steps_attribute()
                
        # just ignore it 
        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.lineToElements = dict()

        self.opvDeformedTubes = None
        self.opvPressureTubes = None
        self.opvTubes = None
        self.opvSymbols = None

        self.slider = None
        self.logoWidget = None
        self.stressesTextProperty = vtk.vtkTextProperty()

        # self._createPlayer()
        self.reset_min_max_values()
        self.cache_plot_state()
        self.updateHud()
        self._animationFrames = []

    def update_phase_steps_attribute(self):
        d_theta = 2*pi/self.number_frames
        # self.phase_steps = np.arange(0, 2*pi + d_theta, d_theta)
        self.phase_steps = np.arange(0, self.number_frames+1, 1)*d_theta

    def _setNumberFrames(self, frames):
        self.number_frames = frames
        self.update_phase_steps_attribute()
    
    def _setNumberCycles(self, cycles):
        self.number_cycles = cycles
        self.total_frames = (self.number_frames+1)*self.number_cycles
    
    def _numberFramesHasChanged(self, _bool):
        self.number_frames_changed = _bool
 
    def reset_min_max_values(self):
        self.count_cycles = 0
        self.rDisp_min = None
        self.rDisp_max = None
        self.stress_min = None
        self.stress_max = None
        self.pressure_min = None
        self.pressure_max = None
        self.min_max_rDisp_values_current = None
        self.min_max_stresses_values_current = None
        self.min_max_pressures_values_current = None
        self.plot_state = [False, False, False]

    def plot(self):
        self.reset()
    
        self.opvDeformedTubes = TubeDeformedActor(self.project, self.opv, hidden_elements=self.hidden_elements)
        self.opvPressureTubes = TubeActor(self.project, self.opv, pressure_plot=True, hidden_elements=self.hidden_elements)

        self.opvClippableDeformedTubes = TubeClippableDeformedActor(self.project, self.opv, hidden_elements=self.hidden_elements)
        self.opvClippablePressureTubes = TubeClippableActor(self.project, self.opv, pressure_plot=True, hidden_elements=self.hidden_elements)

        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(3, 3, 3)
        # self.opvSymbols = SymbolsActor(self.project, deformed=True)
        self.opvPressureTubes.transparent = False

        # self._createSlider()
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvDeformedTubes)
        plt(self.opvPressureTubes)
        plt(self.opvClippableDeformedTubes)
        plt(self.opvClippablePressureTubes)
        # plt(self.opvSymbols)
        self._renderer.AddActor(self.plane_actor)

        self._createLogos(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)

    def calculate_hidden_by_plane(self, plane_origin, plane_normal):
        hidden = set()
        for i, element in self.project.get_structural_elements().items():
            element_vector = element.element_center_coordinates - plane_origin
            if np.dot(element_vector, plane_normal) > 0:
                hidden.add(i)
        return hidden

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()

    def setInUse(self, *args, **kwargs):
        super().setInUse(*args, **kwargs)
        self.pauseAnimation()
    
    def update(self):
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()
    
    def updateAll(self):
        self.updateInfoText()
        self.update_min_max_stresses_text()
        self.opv.update()
        self._renderer.ResetCameraClippingRange()
        self.update()

    def updateHud(self):
        # self._createSlider()
        self._createColorBar()
        self._createScaleBar()

    def cache_plot_state(self, displacement=False, stress=False, pressure=False):
        self.plot_changed = False
        if self.plot_state != [displacement, stress, pressure]: 
            self.plot_changed = True
        self.plot_state = [displacement, stress, pressure]
            
    def _cacheFrames(self):
        self._animationFrames.clear()
        for phase_step in self.phase_steps:
            self._currentPlot(self._currentFrequencyIndex, phase_step)
            cached = vtk.vtkPolyData()
            cached.DeepCopy(self.opvTubes._data)
            self._animationFrames.append(cached)

    def _plotCached(self):
        if self._animationFrames:
             
            if self.animationIndex >= len(self._animationFrames):
                self.animationIndex = 0
                
            i = self.animationIndex
            self.animationIndex += 1
                            
            # _phase_deg = round(self.phase_steps[i]*(360/(2*pi)))
            # self._currentPhase = _phase_deg
            # self.slider.GetRepresentation().SetValue(_phase_deg)
            cached = self._animationFrames[i]
            self.opvTubes._data.DeepCopy(cached)
            self.updateAll()

            if self.export_animation:
                self.add_frame_to_animation_file()
        
    def _plotOnce(self, phase_step):
        self._currentPhase = phase_step
        self._currentPlot(self._currentFrequencyIndex, phase_step)
        self.updateAll()

    def reset_plot_data(self):
        self.count_cycles = 0
        self.animationIndex = 0
        self._animationFrames.clear()
        self._cacheFrequencyIndex = None
        
    def showDisplacementField(self, frequency_index, current_scaling):
        self.cache_plot_state(displacement=True)
        self._currentFrequencyIndex = frequency_index
        self._currentPhase = 0
        self._current_scaling = current_scaling
        if self._currentFrequencyIndex != self.last_frequency_index or self.plot_changed:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_resultant_displacements(self._currentFrequencyIndex,
                                                               current_scaling)
        self.opvTubes = self.opvDeformedTubes
        self._currentPlot = self.computeDisplacementField
        self.last_frequency_index = frequency_index 
        self._plotOnce(self._currentPhase)

    def showStressField(self, frequency_index, scaling_setup):
        self.cache_plot_state(stress=True)
        self._currentFrequencyIndex = frequency_index
        self._currentPhase = 0
        self._scaling_setup = scaling_setup
        if self._currentFrequencyIndex != self.last_frequency_index or self.plot_changed:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_stresses() 
            self.get_min_max_values_to_resultant_displacements(self._currentFrequencyIndex,
                                                               scaling_setup)
        self.opvTubes = self.opvDeformedTubes
        self._currentPlot = self.computeStressField
        self.last_frequency_index = frequency_index 
        self._plotOnce(self._currentPhase)

    def showPressureField(self, frequency_index, absolute=False):
        self.cache_plot_state(pressure=True)
        self._currentFrequencyIndex = frequency_index
        self._currentPhase = 0
        self._absolute = absolute
        if self._currentFrequencyIndex != self.last_frequency_index or self.plot_changed:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_pressure(self._currentFrequencyIndex)

        self.opvTubes = self.opvPressureTubes
        self._currentPlot = self.computePressureField
        self.last_frequency_index = frequency_index
        self._plotOnce(self._currentPhase)

    def get_min_max_values_to_resultant_displacements(self, frequency_index, current_scaling):
        solution = self.project.get_structural_solution()
        self.rDisp_min, self.rDisp_max = get_max_min_values_of_resultant_displacements(solution, 
                                                                                       frequency_index,
                                                                                       current_scaling)

    def computeDisplacementField(self, frequency_index, phase_step):

        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()

        _, _, u_def, self._magnificationFactor, self.min_max_rDisp_values_current = get_structural_response(preprocessor, 
                                                                                                            solution, 
                                                                                                            frequency_index, 
                                                                                                            phase_step = phase_step,
                                                                                                            r_max = self.rDisp_max,
                                                                                                            current_scaling = self._current_scaling)
        
        self.opvDeformedTubes.build()
        min_max_values_all = [self.rDisp_min, self.rDisp_max]
        colorTable = ColorTable(self.project, u_def, min_max_values_all)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)

        # self.slider.SetEnabled(True)

        if self.clipping_plane_active:
            self.opvClippableDeformedTubes.build()
            self.opvClippableDeformedTubes.setColorTable(colorTable)
            self.opvDeformedTubes.getActor().SetVisibility(False)
            self.opvPressureTubes.getActor().SetVisibility(False)
            self.opvClippableDeformedTubes.getActor().SetVisibility(True)
            self.opvClippablePressureTubes.getActor().SetVisibility(False)
        else:
            self.opvClippableDeformedTubes.getActor().SetVisibility(False)
            self.opvClippablePressureTubes.getActor().SetVisibility(False)
            self.opvDeformedTubes.getActor().SetVisibility(True)
            self.opvPressureTubes.getActor().SetVisibility(False)

        
    def get_min_max_values_to_stresses(self):
        solution = self.project.stresses_values_for_color_table
        self.stress_min, self.stress_max = get_min_max_stresses_values(solution)
        
    def computeStressField(self, frequency, phase_step):

        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()

        *args, self._magnificationFactor, _ = get_structural_response(  preprocessor,
                                                                        solution, 
                                                                        frequency,
                                                                        phase_step = phase_step,
                                                                        r_max = self.rDisp_max,
                                                                        scaling_setup = self._scaling_setup  )
        self.opvDeformedTubes.build()
        
        _stresses = self.project.stresses_values_for_color_table
        stresses_data, self.min_max_stresses_values_current = get_stresses_to_plot( _stresses, 
                                                                                    phase_step=phase_step )

        min_max_values_all = [self.stress_min, self.stress_max]
        colorTable = ColorTable(self.project, stresses_data, min_max_values_all, stress_field_plot=True)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        # self.slider.SetEnabled(True)

        if self.clipping_plane_active:
            self.opvClippableDeformedTubes.build()
            self.opvClippableDeformedTubes.setColorTable(colorTable)
            self.opvDeformedTubes.getActor().SetVisibility(False)
            self.opvPressureTubes.getActor().SetVisibility(False)
            self.opvClippableDeformedTubes.getActor().SetVisibility(True)
            self.opvClippablePressureTubes.getActor().SetVisibility(False)
        else:
            self.opvClippableDeformedTubes.getActor().SetVisibility(False)
            self.opvClippablePressureTubes.getActor().SetVisibility(False)
            self.opvDeformedTubes.getActor().SetVisibility(True)
            self.opvPressureTubes.getActor().SetVisibility(False)



    def get_min_max_values_to_pressure(self, frequency_index):
        solution = self.project.get_acoustic_solution()
        self.pressure_min, self.pressure_max = get_max_min_values_of_pressures(solution, 
                                                                               frequency_index, 
                                                                               absolute=self._absolute)

    def computePressureField(self, frequency, phase_step):

        preprocessor = self.project.preprocessor
        solution = self.project.get_acoustic_solution()
        self._currentFrequencyIndex = frequency
        self._colorScalling = 'absolute' if self._absolute else 'real part'

        *args, pressure_field_data, self.min_max_pressures_values_current = get_acoustic_response(  preprocessor, 
                                                                                                    solution, 
                                                                                                    frequency, 
                                                                                                    phase_step=phase_step,
                                                                                                    absolute=self._absolute  )
        
        self.opvPressureTubes.build()
        min_max_values_all = [self.pressure_min, self.pressure_max]
        colorTable = ColorTable(self.project, pressure_field_data, min_max_values_all, pressure_field_plot=True)
        self.opvPressureTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        # self.slider.SetEnabled(True)

        if self.clipping_plane_active:
            self.opvClippablePressureTubes.build()
            self.opvClippablePressureTubes.setColorTable(colorTable)
            self.opvDeformedTubes.getActor().SetVisibility(False)
            self.opvPressureTubes.getActor().SetVisibility(False)
            self.opvClippableDeformedTubes.getActor().SetVisibility(False)
            self.opvClippablePressureTubes.getActor().SetVisibility(True)
        else:
            self.opvClippableDeformedTubes.getActor().SetVisibility(False)
            self.opvClippablePressureTubes.getActor().SetVisibility(False)
            self.opvDeformedTubes.getActor().SetVisibility(False)
            self.opvPressureTubes.getActor().SetVisibility(True)


    # def _createSlider(self):

    #     width, height = self.getSize()
    #     self.sliderTitleProperty = vtk.vtkTextProperty()
    #     self._titleActor = vtk.vtkTextActor()
    #     self._renderer.RemoveActor2D(self._titleActor)
    #     self.sliderTitleProperty.SetFontSize(15)
    #     self.sliderTitleProperty.SetColor(self.opv.font_color)
    #     # self.sliderTitleProperty.BoldOn()
    #     self.sliderTitleProperty.SetFontFamilyAsString('Arial')        
    #     self.sliderTitleProperty.SetVerticalJustificationToTop()
    #     self.sliderTitleProperty.SetJustificationToLeft()
    #     self._titleActor.SetInput('Animation phase controller [deg]')
    #     self._titleActor.SetTextProperty(self.sliderTitleProperty)
    #     self._titleActor.SetDisplayPosition(20, height-190)
    #     self._renderer.AddActor2D(self._titleActor)

    #     self.slider = vtk.vtkSliderWidget()
    #     self.sldRep = vtk.vtkSliderRepresentation2D()

    #     self.sldRep.SetMinimumValue(0)
    #     self.sldRep.SetMaximumValue(360)
    #     self.sldRep.SetValue(0)
    #     self.sliderLabelProperty = self.sldRep.GetLabelProperty()
        
    #     self.sliderLabelProperty.SetColor(self.opv.font_color)
    #     self.sliderLabelProperty.ShadowOff()
    #     # self.sliderLabelProperty.SetFontSize(10)

    #     self.sldRep.GetSelectedProperty().SetColor(1, 0, 0)
    #     self.sldRep.GetTubeProperty().SetColor(0.5, 0.5, 0.5)
    #     self.sldRep.GetCapProperty().SetColor(0.8, 0.8, 0.8)
        
    #     self.sldRep.SetSliderLength(0.01)
    #     self.sldRep.SetSliderWidth(0.03)
    #     self.sldRep.SetTubeWidth(0.02)

    #     self.sldRep.SetEndCapWidth(0.02)
    #     self.sldRep.SetEndCapLength(0.005)

    #     # self.sldRep.SetTitleHeight(0.010)
    #     self.sldRep.SetLabelHeight(0.018)

    #     self.sldRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    #     self.sldRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    #     self.sldRep.GetPoint1Coordinate().SetValue(20, height-165)
    #     self.sldRep.GetPoint2Coordinate().SetValue(220, height-165)

    #     self.slider.SetInteractor(self.opv)
    #     self.slider.SetRepresentation(self.sldRep)
    #     self.slider.AddObserver(vtk.vtkCommand.EndInteractionEvent, self._sliderCallback)

    def _createPlayer(self):
        self.opv.Initialize()
        self.opv.CreateRepeatingTimer(1000 * 100)
        self.opv.AddObserver('TimerEvent', self._animationCallback)

    def playAnimation(self):
        
        def cache_callback():
            self._cacheFrames()
            self._cacheFrequencyIndex = self._currentFrequencyIndex
            self.playingAnimation = True
        
        if self._currentPlot is None:
            return
        
        if self.playingAnimation:
            return
        
        if self.clipping_plane_active:
            return

        if self._cacheFrequencyIndex == self._currentFrequencyIndex and not self.number_frames_changed:
            self.playingAnimation = True
            return
        
        if self.number_frames_changed:
            self.number_frames_changed = False

        title = "Processing in progress"

        if self.export_animation:
            message = "The animation file exporting is in progress..."
        else:
            message = "The animation frames calculation is in progress..."
        
        LoadingScreen(title = title, 
                      message = message, 
                      target = cache_callback)

    def pauseAnimation(self):
        self.playingAnimation = False

    def tooglePlayPauseAnimation(self):

        if self.playingAnimation:
            self.pauseAnimation()
        else:
            self.playAnimation()

    def _animationCallback(self, caller, event):
        if self._currentPlot is None:
            return 

        if not self.playingAnimation:
            return

        # self.slider.GetRepresentation().SetValue(0)
        
        self.count_cycles += 1
        if self.count_cycles <= self.total_frames:
            self._plotCached()
        else:
            self.pauseAnimation()
            self.count_cycles = 0
            if self.export_animation:
                self.end_export_animation_to_file()
                return

    def _sliderCallback(self, slider, b):
        if self._currentPlot is None:
            return 
        
        self.playingAnimation = False
        delta_phase_deg = (360/self.number_frames)
        sliderValue = round(slider.GetRepresentation().GetValue()/delta_phase_deg)*delta_phase_deg
        slider.GetRepresentation().SetValue(sliderValue)
        phase_rad = sliderValue*(2*pi/360)
        self._plotOnce(phase_rad)

    def slider_callback(self, phase_deg):
        if self._currentPlot is None:
            return 
        
        self.playingAnimation = False
        # delta_phase_deg = (360/self.number_frames)
        phase_rad = phase_deg*(2*pi/360)
        self._plotOnce(phase_rad)

    def start_export_animation_to_file(self, path, frame_rate):
        self.animation_path = path
        #Setup filter
        self.renWin = self._renderer.GetRenderWindow()
        self.imageFilter = vtk.vtkWindowToImageFilter()
        self.imageFilter.SetInput(self.renWin)
        self.imageFilter.SetInputBufferTypeToRGB()
        self.imageFilter.ReadFrontBufferOff()
        self.imageFilter.Update()
        #Setup movie writer
        if ".avi" in str(path):
            self.moviewriter = vtk.vtkAVIWriter()
        else:
            self.moviewriter = vtk.vtkOggTheoraWriter()
        self.moviewriter.SetFileName(path)
        self.moviewriter.SetInputConnection(self.imageFilter.GetOutputPort())
        self.moviewriter.SetRate(30)
        self.moviewriter.SetQuality(2)
        self.moviewriter.Start()
        #
        self.export_animation = True
    
    def add_frame_to_animation_file(self):
        self.imageFilter.Update()
        self.imageFilter.Modified()
        self.moviewriter.Write()

    def end_export_animation_to_file(self):
        self.moviewriter.End()
        self.export_animation = False
        # for _format in [".avi", ".mp4", ".mpeg"] :
        #     if _format in self.animation_path:
        #         self.convert_animation_to_gif()
        #         break

    # def convert_animation_to_gif(self):
    #     input_filename = self.animation_path.split(".")[0]
    #     _reader = imageio.get_reader(self.animation_path)
    #     fps = _reader.get_meta_data()['fps']
    #     output_filename = input_filename + ".gif"
    #     writer = imageio.get_writer(output_filename, fps=fps)
    #     for i,im in enumerate(_reader):
    #         writer.append_data(im)
    #     writer.close()

    def _updateFontColor(self, color):
        self.sliderTitleProperty.SetColor(color)
        self.sliderLabelProperty.SetColor(color)
        self.colorBarTitleProperty.SetColor(color)
        self.stressesTextProperty.SetColor(color)
        self.scaleBarTitleProperty.SetColor(color)
        self.colorBarLabelProperty.SetColor(color)
        self.scaleBarLabelProperty.SetColor(color)
        self.colorBarTitleProperty.SetColor(color)
        self.changeReferenceScaleFontColor(color)

    # info text
    def updateInfoText(self, *args, **kwargs):
        
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID in [2, 4]:
            if self.project.analysis_type_label == "Structural Modal Analysis":
                frequencies = self.project.get_structural_natural_frequencies()
            if self.project.analysis_type_label == "Acoustic Modal Analysis":
                frequencies = self.project.get_acoustic_natural_frequencies()
            mode = self._currentFrequencyIndex + 1
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
        else:
            frequencies = self.project.get_frequencies()
            if self.project.analysis_method_label is not None:
                text += self.project.analysis_method_label + "\n"
            text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])

        if not self.project.plot_pressure_field:
            text += "\nMagnification factor: {:.4e}\n".format(self._magnificationFactor)
        # vertical_position_adjust = None
        self.createInfoText(text, color=self.opv.font_color)

    def update_min_max_stresses_text(self):
                
        stress_label = self.project.stress_label

        text = ""
        if self.min_max_stresses_values_current is not None:
            [min_stress, max_stress] = self.min_max_stresses_values_current
            text += "Minimum {} stress: {:.3e} [Pa]\n".format(stress_label, min_stress)
            text += "Maximum {} stress: {:.3e} [Pa]\n".format(stress_label, max_stress)
        
        width, height = self._renderer.GetSize()
        
        self.textActorStress.SetInput(text)
        self.stressesTextProperty.SetFontSize(17)
        self.stressesTextProperty.SetBold(1)
        # self.stressesTextProperty.SetItalic(1)
        self.stressesTextProperty.ShadowOff()
        self.stressesTextProperty.SetColor(self.opv.font_color)
        self.textActorStress.SetTextProperty(self.stressesTextProperty)
        self.textSize = [0,0]
        self.textActorStress.GetSize(self._renderer, self.textSize)
        
        xTextPosition = int((width - self.textSize[0])/2)

        self.textActorStress.SetDisplayPosition(xTextPosition, height-75)
        self._renderer.AddActor2D(self.textActorStress)

    # functions to be removed but currently break the execution
    def getElementsInfoText(self, *args, **kwargs):
        pass
    
    def getEntityInfoText(self, *args, **kwargs):
        pass 

    def getPlotRadius(self, *args, **kwargs):
        return 
    
    def changeColorEntities(self, *args, **kwargs):
        return 

    def setPlotRadius(self, plt):
        pass

    def configure_clipping_plane(self, x, y, z, rx, ry, rz):
        if self.playingAnimation:
            self.pauseAnimation()

        self.clipping_plane_active = True
        self.plane_origin = self._calculate_relative_position([x, y, z])
        self.plane_normal = self._calculate_normal_vector([rx, ry, rz])
        self.plane_actor.SetPosition(self.plane_origin)
        self.plane_actor.SetOrientation(rx, ry, rz)
        self.plane_actor.GetProperty().SetOpacity(0.9)
        self.plane_actor.VisibilityOn()
        self.update()

    def apply_clipping_plane(self):
        if self.plane_origin is None:
            return

        if self.plane_normal is None:
            return

        if self.playingAnimation:
            self.pauseAnimation()

        if self.first_configuration:
            self._plotOnce(self._currentPhase)
            self.first_configuration = False 

        self.opvClippablePressureTubes.apply_cut(self.plane_origin, self.plane_normal)
        self.opvClippableDeformedTubes.apply_cut(self.plane_origin, self.plane_normal)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()
    
    def dismiss_clipping_plane(self):                
        self.plane_origin = None
        self.plane_normal = None
    
        self.opvClippablePressureTubes.disable_cut()
        self.opvClippableDeformedTubes.disable_cut()
        self.plane_actor.VisibilityOff()
        self.update()
        self.first_configuration = True
        self.clipping_plane_active = False
        self._plotOnce(self._currentPhase)

    def calculate_hidden_by_plane(self, plane_origin, plane_normal):
        hidden = set()
        for i, element in self.project.get_structural_elements().items():
            element_vector = element.element_center_coordinates - plane_origin
            if np.dot(element_vector, plane_normal) > 0:
                hidden.add(i)
        return hidden

    def _calculate_relative_position(self, position):
        def lerp(a, b, t):
           return a + (b - a) * t
        
        bounds = self.opv.opvRenderer.getBounds()
        x = lerp(bounds[0], bounds[1], position[0] / 100)
        y = lerp(bounds[2], bounds[3], position[1] / 100)
        z = lerp(bounds[4], bounds[5], position[2] / 100)
        return np.array([x, y, z])
    
    def _calculate_normal_vector(self, orientation):
        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = self._rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return -normal[:3]

    def _rotation_matrices(self, ax, ay, az):
        sin = np.sin([ax, ay, az])
        cos = np.cos([ax, ay, az])

        rx = np.array(
            [
                [1, 0, 0, 0],
                [0, cos[0], -sin[0], 0],
                [0, sin[0], cos[0], 0],
                [0, 0, 0, 1],
            ]
        )

        ry = np.array(
            [
                [cos[1], 0, sin[1], 0],
                [0, 1, 0, 0],
                [-sin[1], 0, cos[1], 0],
                [0, 0, 0, 1],
            ]
        )

        rz = np.array(
            [
                [cos[2], -sin[2], 0, 0],
                [sin[2], cos[2], 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        return rx, ry, rz
