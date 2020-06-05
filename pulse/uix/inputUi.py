from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.fluidInput import FluidInput
from pulse.uix.user_input.crossSectionInput import CrossSectionInput
from pulse.uix.user_input.loadsInput import LoadsInput
from pulse.uix.user_input.massSpringDamperInput import MassSpringDamperInput
from pulse.uix.user_input.analysisTypeInput import AnalysisTypeInput
from pulse.uix.user_input.analysisSetupInput import AnalysisSetupInput
from pulse.uix.user_input.analysisOutputResultsInput import AnalysisOutputResultsInput
from pulse.uix.user_input.runAnalysisInput import RunAnalysisInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.specificimpedanceInput import SpecificImpedanceInput
from pulse.uix.user_input.radiationimpedanceInput import RadiationImpedanceInput
from pulse.uix.user_input.volumevelocityInput import VolumeVelocityInput
from pulse.uix.user_input.acousticpressureInput import AcousticPressureInput

from pulse.uix.user_input.plotAcousticModeShapeInput import PlotAcousticModeShapeInput
from pulse.uix.user_input.plotStructuralModeShapeInput import PlotStructuralModeShapeInput
from pulse.uix.user_input.plotHarmonicResponseInput import PlotHarmonicResponseInput
from pulse.uix.user_input.plotStructuralFrequencyResponseInput import PlotStructuralFrequencyResponseInput
from pulse.uix.user_input.plotAcousticFrequencyResponseInput import PlotAcousticFrequencyResponseInput
from pulse.uix.user_input.elementTypeInput import ElementTypeInput
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.project import Project
from pulse.utils import error

class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()
        self.analysis_ID = None

        self.f_min = 0
        self.f_max = 0
        self.f_step = 0

    def set_material(self):
        mat = MaterialInput(self.project.get_material_list_path())
        if mat.material is None:
            return

        if mat.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.set_material_by_entity(entity, mat.material)
            print("[Set Material] - {} defined in the entities {}".format(mat.material.name, entities_id))
            self.opv.changeColorEntities(entities_id, mat.material.getNormalizedColorRGB())
        else:
            self.project.set_material(mat.material)
            entities = []
            for entity in self.project.get_entities():
                entities.append(entity.getTag())
            print("[Set Material] - {} defined in all entities".format(mat.material.name))
            self.opv.changeColorEntities(entities, mat.material.getNormalizedColorRGB())

    def set_fluid(self):
        fld = FluidInput(self.project.get_fluid_list_path())
        if fld.fluid is None:
            return

        if fld.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.set_fluid_by_Entity(entity, fld.fluid)
            print("[Set Fluid] - {} defined in the entities {}".format(fld.fluid.name, entities_id))
            self.opv.changeColorEntities(entities_id, fld.fluid.getNormalizedColorRGB())
        else:
            self.project.set_fluid(fld.fluid)
            entities = []
            for entity in self.project.get_entities():
                entities.append(entity.getTag())
            print("[Set Fluid] - {} defined in all entities".format(fld.fluid.name))
            self.opv.changeColorEntities(entities, fld.fluid.getNormalizedColorRGB())

    def set_crossSection(self):
        cross = CrossSectionInput()
        if cross.section is None:
            return

        if cross.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.set_crossSection_by_entity(entity, cross.section)
            print("[Set CrossSection] - defined in the entities {}".format(entities_id))
        else:
            self.project.set_crossSection(cross.section)
            print("[Set CrossSection] - defined in all the entities")
        self.opv.updateEntityRadius()

    def setElementType(self):
        ElementTypeInput()

    def setDOF(self):
        point_id = self.opv.getListPickedPoints()
        dof = DOFInput(self.project.mesh.nodes, point_id)

        if dof.dof.count(None)==6:
            if not dof.remove_prescribed_dofs:
                return

        self.project.set_prescribed_dofs_bc_by_node(dof.nodes_typed, dof.dof)
        print("[Set Prescribed DOF] - defined in the point(s) {}".format(dof.nodes_typed))
        self.opv.transformPoints(dof.nodes_typed)

    def setAcousticPressure(self):
        point_id = self.opv.getListPickedPoints()
        read = AcousticPressureInput(self.project.mesh.nodes, point_id, self.project._projectName)
        
        if read.acoustic_pressure is None:
            if not read.remove_acoustic_pressure:
                return
        
        if read.new_load_path_table is not None:
            self.project.file.tempPath = read.new_load_path_table
            self.project.file.f_min = read.f_min
            self.project.file.f_max = read.f_max
            self.project.file.f_step = read.df
            self.project.file.frequencies = read.frequencies

        self.project.set_acoustic_pressure_bc_by_node(read.nodes_typed, read.acoustic_pressure)
        print("[Set Acoustic Pressure] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setVolumeVelocity(self):
        point_id = self.opv.getListPickedPoints()
        read = VolumeVelocityInput(self.project.mesh.nodes, point_id)

        if read.volume_velocity is None:
            return

        self.project.set_volume_velocity_bc_by_node(read.nodes_typed, read.volume_velocity)
        print("[Set Volume Velocity Source] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setSpecificImpedance(self):
        point_id = self.opv.getListPickedPoints()
        read = SpecificImpedanceInput(self.project.mesh.nodes, point_id)

        if read.specific_impedance is None:
            return

        self.project.set_specific_impedance_bc_by_node(read.nodes_typed, read.specific_impedance)
        print("[Set Specific Impedance] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)


    def setRadiationImpedance(self):
        point_id = self.opv.getListPickedPoints()
        read = RadiationImpedanceInput(self.project.mesh.nodes, point_id)

        if read.radiation_impedance is None:
            return

        self.project.set_radiation_impedance_bc_by_node(read.nodes_typed, read.radiation_impedance)
        print("[Set Radiation Impedance Source] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setNodalLoads(self):
        point_id = self.opv.getListPickedPoints()
        loads = LoadsInput(self.project.mesh.nodes, point_id)

        if loads.loads is None:
            return

        self.project.set_force_by_node(loads.nodes_typed, loads.loads)
        print("[Set Nodal Load] - defined in the point(s) {}".format(loads.nodes_typed))
        self.opv.transformPoints(loads.nodes_typed)

    def addMassSpringDamper(self):
        point_id = self.opv.getListPickedPoints()
        msd = MassSpringDamperInput(self.project.mesh.nodes, point_id)
        if msd.input_mass:
            self.project.set_mass_by_node(msd.nodes_typed, msd.mass)
            print("[Set Mass] - defined in the point(s) {}".format(msd.nodes_typed))
        if msd.input_spring:
            self.project.set_spring_by_node(msd.nodes_typed, msd.spring)
            print("[Set Spring] - defined in the point(s) {}".format(msd.nodes_typed))
        if msd.input_damper:
            self.project.set_damper_by_node(msd.nodes_typed, msd.damper)
            print("[Set Damper] - defined in the point(s) {}".format(msd.nodes_typed))         

    def analysisTypeInput(self):

        inputs = AnalysisTypeInput()
        if inputs.method_ID == -1:
            return
        self.analysis_ID = inputs.analysis_ID
        self.analysis_type_label = inputs.analysis_type_label
        self.analysis_method_label = inputs.analysis_method_label
 
        if self.analysis_ID is None:
            return
 
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.set_modes(inputs.modes)
        self.project.set_acoustic_solution(None)
        self.project.set_structural_solution(None)

        if self.analysis_ID in [2,4]:
            if not inputs.complete:
                return
            else:
                self.runAnalysis()
        else:
            self.analysisSetup()
        
    def analysisSetup(self):
        
        # self.f_min = 0
        # self.f_max = 0
        # self.f_step = 0

        if self.project.analysis_ID is None:
            return
        if self.project.file._projectName == "":
            return
        
        if self.project.file.tempPath is None:
            self.project.load_analysis_file()
            self.f_min, self.f_max, self.f_step = self.project.f_min, self.project.f_max, self.project.f_step
        else:
            self.project.load_frequencies_from_table()
            self.f_min, self.f_max, self.f_step = self.project.file.f_min, self.project.file.f_max, self.project.file.f_step
        setup = AnalysisSetupInput(self.analysis_ID, self.analysis_type_label, self.analysis_method_label, f_min = self.f_min, f_max = self.f_max, f_step = self.f_step)
        
        self.frequencies = setup.frequencies
        self.f_min = setup.f_min
        self.f_max = setup.f_max
        self.f_step = setup.f_step

        if not setup.complete:
            return

        self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

        if self.analysis_ID != 3:
            self.project.set_modes(setup.modes)
            self.project.set_damping(setup.damping)
        else:
            return
      
    def analysisOutputResults(self):
        AnalysisOutputResultsInput()

    def runAnalysis(self):
        if self.analysis_ID is None:
            return
        if self._check_is_there_a_problem():
            return
        if self.analysis_ID in [0,1,3,5,6]:
            if len(self.frequencies) == 0:
                return          

        if self.analysis_ID == 2:
            solve = self.project.get_structural_solve()
            modes = self.project.get_modes()
        elif self.analysis_ID == 4:
            solve = self.project.get_acoustic_solve()
            modes = self.project.get_modes()
        elif self.analysis_ID == 3:
            solve = self.project.get_acoustic_solve()
        elif self.analysis_ID in [5,6]:
            solve = self.project.get_acoustic_solve()
            modes = self.project.get_modes()
            damping = self.project.get_damping()
        else:
            solve = self.project.get_structural_solve()
            modes = self.project.get_modes()
            damping = self.project.get_damping()

        if self.analysis_ID == 2:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [])
            if solution.solution is None:
                return
            self.project.set_structural_solution(solution.solution)
            self.project.set_structural_natural_frequencies(solution.natural_frequencies_structural.tolist())

        elif self.analysis_ID == 4:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [])
            if solution.solution is None:
                return
            self.project.set_acoustic_solution(solution.solution)
            self.project.set_acoustic_natural_frequencies(solution.natural_frequencies_acoustic.tolist())

        elif self.analysis_ID == 3:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, [], [])
            if solution.solution is None:
                return
            self.project.set_acoustic_solution(solution.solution)
        elif self.analysis_ID in [5,6]:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, project=self.project)
            # if solution.solution_structural is None:
            #     return
            self.project.set_structural_solution(solution.solution_structural)

        else:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping)
            if solution.solution is None:
                return
            self.project.set_structural_solution(solution.solution)
 
    def plotStructuralModeShapes(self):
        self.project.plot_pressure_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID == 2:
            if solution is None:
                return
            plot = PlotStructuralModeShapeInput(self.project.natural_frequencies_structural)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalysis(plot.mode_index)
        else:
            return

    def plotStructuralHarmonicResponse(self):
        self.project.plot_pressure_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0,1,5,6]:
            if solution is None:
                return
            plot = PlotHarmonicResponseInput(self.frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency)
        else:
            return

    def plotAcousticModeShapes(self):
        self.project.plot_pressure_field = True
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID == 2:
            if solution is None:
                return
            plot = PlotAcousticModeShapeInput(self.project.natural_frequencies_acoustic)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalysis(plot.mode_index)
        else:
            return

    def plotPressureField(self):
        self.project.plot_pressure_field = True
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3,5,6]:
            if solution is None:
                return
            plot = PlotHarmonicResponseInput(self.frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency, acoustic=True)
        else:
            return

    def plotStructuralFrequencyResponse(self):
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStructuralFrequencyResponseInput(self.project.get_mesh(), self.analysis_method_label, self.frequencies, solution)

    def plotAcousticFrequencyResponse(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            PlotAcousticFrequencyResponseInput(self.project.get_mesh(), self.analysis_method_label, self.frequencies, solution)

    def plotStressField(self):
        pass

    def new_project(self):
        result = NewProjectInput(self.project)
        return result.create

    def _check_is_there_a_problem(self):

        title = " ERROR: INSUFFICIENT MODEL INPUTS! "

        cross_section_message = "You should to set a Cross-Section to all\n elements before trying to run any Analysis!"
        material_message = "You should to set a Material to all elements\n before trying to run any Analysis!"
        fluid_message = "You should to set a Fluid to all elements\n before trying to run any Analysis!"
        structural_message = "You should to apply an external load to the model or prescribe a \nnon-null DOF value before trying to solve the Harmonic Analysis!"
        acoustic_message = "You should to insert a Volume Velocity or prescribe an Acoustic \nPressure to a node before trying to solve the Harmonic Analysis!"
          
        if self.analysis_ID == 2:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            if self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
        
        elif self.analysis_ID == 4:
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            if self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True

        elif self.analysis_ID == 0 or self.analysis_ID == 1:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(structural=True)

            if self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif not self.project.mesh.is_there_loads:
                if not self.project.mesh.is_there_prescribed_dofs:
                    error(structural_message, title = title)
                    return True
    
        elif self.analysis_ID == 3:
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(acoustic=True)

            if self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif not self.project.mesh.is_there_volume_velocity:
                if not self.project.mesh.is_there_acoustic_pressure:
                    error(acoustic_message, title = title)
                    return True

        elif self.analysis_ID == 5 or self.analysis_ID == 6:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(coupled=True)

            if self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            elif self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
            elif not self.project.mesh.is_there_volume_velocity:
                if not self.project.mesh.is_there_acoustic_pressure:
                    error(acoustic_message, title = title)
                    return True

