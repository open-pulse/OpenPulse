from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.loadingScreen import LoadingScreen
import vtk
import numpy as np
from math import pi
from time import sleep
# import imageio
# import os

from pulse.postprocessing.plot_structural_data import get_structural_response, get_max_min_values_of_resultant_displacements, get_stresses_to_plot, get_min_max_stresses_values
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response, get_max_min_values_of_pressures

from pulse.uix.vtk.colorTable import ColorTable
from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.interface.tubeActor import TubeActor
from pulse.interface.symbolsActor import SymbolsActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor

class opvAnalysisRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project
        self.opv = opv
        self.setUsePicker(False)

        self._magnificationFactor = 1
        self._currentFrequencyIndex = 0
        self._cacheFrequencyIndex = None
        self.last_frequency_index = None
        
        self._currentPlot = None
        self.colorbar = None 
        self.scaleBar = None

        self.playingAnimation = False
        self.animationIndex = 0
        self.delayCounter = 0
        self.increment = 1

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
        
        self._createSlider()
        self._createPlayer()
        self.reset_min_max_values()
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

    def plot(self):
        self.reset()
        self.opvDeformedTubes = TubeDeformedActor(self.project.get_structural_elements(), self.project)
        self.opvPressureTubes = TubeActor(self.project.get_structural_elements(), self.project, pressure_plot=True)
        self.opvSymbols = SymbolsActor(self.project, deformed=True)
        self.opvPressureTubes.transparent = False

        self._createSlider()
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvDeformedTubes)
        plt(self.opvPressureTubes)
        plt(self.opvSymbols)

        self._addLogosToRender(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)
    
    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()

    def setInUse(self, *args, **kwargs):
        super().setInUse(*args, **kwargs)
        self.pauseAnimation()
    
    def update(self):
        # self.opv.updateDialogs()
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()
    
    def updateAll(self):
        self.updateInfoText()
        self.update_min_max_stresses_text()
        self.opv.update()
        self._renderer.ResetCameraClippingRange()
        self.update()

    def updateHud(self):
        self._createSlider()
        self._createColorBar()
        self._createScaleBar()

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
                            
            _phase_deg = round(self.phase_steps[i]*(360/(2*pi)))
            self.slider.GetRepresentation().SetValue(_phase_deg)
            cached = self._animationFrames[i]
            self.opvTubes._data.DeepCopy(cached)
            self.updateAll()

            if self.export_animation:
                self.add_frame_to_animation_file()
        
    def _plotOnce(self, phase_step):
        self._currentPlot(self._currentFrequencyIndex, phase_step)
        self.updateAll()

    def reset_plot_data(self):
        self.count_cycles = 0
        self.animationIndex = 0
        self._animationFrames.clear()
        self._cacheFrequencyIndex = None
        
    def showDisplacement(self, frequency_index):
        self._currentFrequencyIndex = frequency_index 
        if self._currentFrequencyIndex != self.last_frequency_index or self.opvTubes != self.opvDeformedTubes:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_resultant_displacements(self._currentFrequencyIndex)
        self.opvTubes = self.opvDeformedTubes
        self._currentPlot = self.computeDisplacement
        self.last_frequency_index = frequency_index 
        self._plotOnce(0)

    def showStressField(self, frequency_index):
        self._currentFrequencyIndex = frequency_index 
        if self._currentFrequencyIndex != self.last_frequency_index or self.opvTubes != self.opvDeformedTubes:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_stresses() 
            self.get_min_max_values_to_resultant_displacements(self._currentFrequencyIndex)
        self.opvTubes = self.opvDeformedTubes
        self._currentPlot = self.computeStressField
        self.last_frequency_index = frequency_index 
        self._plotOnce(0)

    def showPressureField(self, frequency_index):
        self._currentFrequencyIndex = frequency_index 
        if self._currentFrequencyIndex != self.last_frequency_index or self.opvTubes != self.opvPressureTubes:
            self.reset_plot_data()
            self.reset_min_max_values()
            self.get_min_max_values_to_pressure(self._currentFrequencyIndex)
        self.opvTubes = self.opvPressureTubes
        self._currentPlot = self.computePressureField
        self.last_frequency_index = frequency_index
        self._plotOnce(0)

    def get_min_max_values_to_resultant_displacements(self, frequency_index):
        solution = self.project.get_structural_solution()
        self.rDisp_min, self.rDisp_max = get_max_min_values_of_resultant_displacements(solution, frequency_index)

    def computeDisplacement(self, frequency, phase_step=0):

        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()    

        _, _, u_def, self._magnificationFactor, self.min_max_rDisp_values_current = get_structural_response(preprocessor, 
                                                                                                            solution, 
                                                                                                            frequency, 
                                                                                                            phase_step=phase_step,
                                                                                                            r_max=self.rDisp_max)
        
        self.opvDeformedTubes.build()
        min_max_values_all = [self.rDisp_min, self.rDisp_max]
        colorTable = ColorTable(self.project, u_def, min_max_values_all)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)

        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)
        
    def get_min_max_values_to_stresses(self): 
        solution = self.project.stresses_values_for_color_table
        self.stress_min, self.stress_max = get_min_max_stresses_values(solution)

    def computeStressField(self, frequency, phase_step=0):

        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()

        *args, self._magnificationFactor, _ = get_structural_response(  preprocessor, 
                                                                        solution, 
                                                                        frequency,
                                                                        phase_step=phase_step,
                                                                        r_max=self.rDisp_max  )
        self.opvDeformedTubes.build()
        
        _stresses = self.project.stresses_values_for_color_table
        stresses_data, self.min_max_stresses_values_current = get_stresses_to_plot( _stresses, 
                                                                                    phase_step=phase_step )

        min_max_values_all = [self.stress_min, self.stress_max]
        colorTable = ColorTable(self.project, stresses_data, min_max_values_all, stress_field_plot=True)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)

    def get_min_max_values_to_pressure(self, frequency_index):
        solution = self.project.get_acoustic_solution()
        self.pressure_min, self.pressure_max = get_max_min_values_of_pressures(solution, frequency_index)

    def computePressureField(self, frequency, phase_step, real_part=True):

        preprocessor = self.project.preprocessor
        solution = self.project.get_acoustic_solution()
        self._currentFrequencyIndex = frequency
        self._colorScalling = 'real part' if real_part else 'absolute'

        *args, pressure_field_data, self.min_max_pressures_values_current = get_acoustic_response(  preprocessor, 
                                                                                                    solution, 
                                                                                                    frequency, 
                                                                                                    phase_step=phase_step  )
        
        self.opvPressureTubes.build()
        min_max_values_all = [self.pressure_min, self.pressure_max]
        colorTable = ColorTable(self.project, pressure_field_data, min_max_values_all, pressure_field_plot=True)
        self.opvPressureTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(False)
        self.opvPressureTubes.getActor().SetVisibility(True)

    def _createSlider(self):

        width, height = self.getSize()

        self._titleActor = vtk.vtkTextActor()
        self.titleProperty = vtk.vtkTextProperty()
        self.titleProperty.SetFontSize(15)
        self.titleProperty.SetColor(self.opv.font_color)
        # self.titleProperty.BoldOn()
        self.titleProperty.SetFontFamilyAsString('Arial')

        self._renderer.RemoveActor2D(self._titleActor)
        
        self.titleProperty.SetVerticalJustificationToTop()
        self.titleProperty.SetJustificationToLeft()
        self._titleActor.SetInput('Animation phase controller [deg]')
        self._titleActor.SetTextProperty(self.titleProperty)
        self._titleActor.SetDisplayPosition(20, height-180)
        self._renderer.AddActor2D(self._titleActor)

        self.slider = vtk.vtkSliderWidget()
        self.sldRep = vtk.vtkSliderRepresentation2D()

        self.sldRep.SetMinimumValue(0)
        self.sldRep.SetMaximumValue(360)
        self.sldRep.SetValue(0)
        
        # sld.SetTitleText('Animation phase controller [deg]')
        # sld.GetTitleProperty().SetFontSize(5)
        # sld.GetTitleProperty().SetFontFamilyAsString('Arial')
        # sld.GetTitleProperty().SetColor(self.opv.font_color)
        # sld.GetTitleProperty().ShadowOff()
        # sld.GetTitleProperty().SetJustificationToLeft()
        self.sldRep.GetLabelProperty().SetColor(self.opv.font_color)
        self.sldRep.GetLabelProperty().ShadowOff()

        self.sldRep.GetSelectedProperty().SetColor(1, 0, 0)
        self.sldRep.GetTubeProperty().SetColor(0.5, 0.5, 0.5)
        self.sldRep.GetCapProperty().SetColor(0.8, 0.8, 0.8)
        
        self.sldRep.SetSliderLength(0.01)
        self.sldRep.SetSliderWidth(0.02)
        self.sldRep.SetTubeWidth(0.02)

        self.sldRep.SetEndCapWidth(0.02)
        self.sldRep.SetEndCapLength(0.005)

        # sld.SetTitleHeight(0.020)
        self.sldRep.SetLabelHeight(0.015)

        self.sldRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
        self.sldRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
        self.sldRep.GetPoint1Coordinate().SetValue(20, height-160)
        self.sldRep.GetPoint2Coordinate().SetValue(220, height-160)

        self.slider.SetInteractor(self.opv)
        self.slider.SetRepresentation(self.sldRep)
        self.slider.AddObserver(vtk.vtkCommand.EndInteractionEvent, self._sliderCallback)

    def _updateFontColor(self, color):
        self.titleProperty.SetColor(color)
        self.sldRep.GetLabelProperty().SetColor(color)

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
        
        LoadingScreen(title, message, target=cache_callback)

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

        self.slider.GetRepresentation().SetValue(0)
        
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
        if ".avi" in path:
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

    def _createColorBar(self):
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(16)
        textProperty.SetItalic(1)
        unit = self.project.get_unit()
        text = "Unit: [{}]".format(unit)

        # titleTextProperty = vtk.vtkTextProperty()
        # titleTextProperty.SetVerticalJustificationToBottom()
        # titleTextProperty.SetJustificationToRight()
        # titleTextProperty.SetFontSize(14)
        # titleTextProperty.SetItalic(1)
        
        self._renderer.RemoveActor(self.colorbar)
        self.colorbar = vtk.vtkScalarBarActor()
        self.colorbar.SetLabelTextProperty(textProperty)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.94, 0.07)
        self.colorbar.SetLabelFormat("%1.0e ")
        self.colorbar.UnconstrainedFontSizeOn()   
        self.colorbar.VisibilityOn()
        # self.colorbar.SetTitleTextProperty(titleTextProperty)
        self.colorbar.SetTitle(text)
        self.colorbar.SetVerticalTitleSeparation(20)
        self.colorbar.GetTitleTextProperty().SetFontSize(20)
        self.colorbar.GetTitleTextProperty().SetJustificationToLeft()
        self._renderer.AddActor(self.colorbar)

    def _createScaleBar(self):
        width, height = self.getSize()
        self._renderer.RemoveActor(self.scaleBar)
        if self.opv.show_reference_scale:
            self.scaleBar = vtk.vtkLegendScaleActor()
            self.scaleBar.AllAxesOff()
            self._renderer.AddActor(self.scaleBar)

    # info text
    def updateInfoText(self, *args, **kwargs):
        mode = self._currentFrequencyIndex + 1
        frequencies = self.project.get_frequencies()
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID not in [2,4]:
            text += self.project.analysis_method_label + "\n"
            text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
        elif self.project.analysis_ID == 2:
            frequencies = self.project.get_structural_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
        elif self.project.analysis_ID == 4:
            frequencies = self.project.get_acoustic_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
            # text += "Color scalling: {}".format(self._colorScalling)
        if not self.project.plot_pressure_field:
            text += "\nMagnification factor: {:.4e}\n".format(self._magnificationFactor)
        # vertical_position_adjust = None
        self.createInfoText(text)

    def update_min_max_stresses_text(self):
                
        min_stress = self.project.min_stress
        max_stress = self.project.max_stress
        stress_label = self.project.stress_label

        text = ""
        if self.min_max_stresses_values_current is not None:
            [max_stress, min_stress] = self.min_max_stresses_values_current
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