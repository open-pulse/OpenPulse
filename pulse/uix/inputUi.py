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

    def setMaterial(self):
        mat = MaterialInput(self.project.getMaterialListPath())
        if mat.material is None:
            return

        if mat.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.setMaterial_by_Entity(entity, mat.material)
            print("[Set Material] - {} defined in the entities {}".format(mat.material.name, entities_id))
            self.opv.changeColorEntities(entities_id, mat.material.getNormalizedColorRGB())
        else:
            self.project.setMaterial(mat.material)
            entities = []
            for entity in self.project.getEntities():
                entities.append(entity.getTag())
            print("[Set Material] - {} defined in all entities".format(mat.material.name))
            self.opv.changeColorEntities(entities, mat.material.getNormalizedColorRGB())

    def setFluid(self):
        fld = FluidInput(self.project.getFluidListPath())
        if fld.fluid is None:
            return

        if fld.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.setFluid_by_Entity(entity, fld.fluid)
            print("[Set Fluid] - {} defined in the entities {}".format(fld.fluid.name, entities_id))
            self.opv.changeColorEntities(entities_id, fld.fluid.getNormalizedColorRGB())
        else:
            self.project.setFluid(fld.fluid)
            entities = []
            for entity in self.project.getEntities():
                entities.append(entity.getTag())
            print("[Set Fluid] - {} defined in all entities".format(fld.fluid.name))
            self.opv.changeColorEntities(entities, fld.fluid.getNormalizedColorRGB())

    def setCrossSection(self):
        cross = CrossSectionInput()
        if cross.section is None:
            return

        if cross.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.setCrossSection_by_Entity(entity, cross.section)
            print("[Set CrossSection] - defined in the entities {}".format(entities_id))
        else:
            self.project.setCrossSection(cross.section)
            print("[Set CrossSection] - defined in all the entities")
        self.opv.updateEntityRadius()

    def setElementType(self):
        ElementTypeInput()

    def setDOF(self):
        point_id = self.opv.getListPickedPoints()
        dof = DOFInput(self.project.mesh.nodes, point_id)

        if dof.dof is None:
            return

        self.project.setStructuralBoundaryCondition_by_Node(dof.nodes_typed, dof.dof)
        print("[Set Prescribed DOF] - defined in the point(s) {}".format(dof.nodes_typed))
        self.opv.transformPoints(dof.nodes_typed)

    def setSpecificImpedance(self):
        point_id = self.opv.getListPickedPoints()
        read = SpecificImpedanceInput(self.project.mesh.nodes, point_id)

        if read.specific_impedance is None:
            return

        self.project.setSpecificImpedanceBC_by_Node(read.nodes_typed, read.specific_impedance)
        print("[Set Specific Impedance] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setAcousticPressure(self):
        point_id = self.opv.getListPickedPoints()
        read = AcousticPressureInput(self.project.mesh.nodes, point_id)

        if read.acoustic_pressure is None:
            return

        self.project.setAcousticPressureBC_by_Node(read.nodes_typed, read.acoustic_pressure)
        print("[Set Acoustic Pressure] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setVolumeVelocity(self):
        point_id = self.opv.getListPickedPoints()
        read = VolumeVelocityInput(self.project.mesh.nodes, point_id)

        if read.volume_velocity is None:
            return

        self.project.setVolumeVelocityBC_by_Node(read.nodes_typed, read.volume_velocity)
        print("[Set Volume Velocity Source] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setRadiationImpedance(self):
        point_id = self.opv.getListPickedPoints()
        read = RadiationImpedanceInput(self.project.mesh.nodes, point_id)

        if read.radiation_impedance is None:
            return

        self.project.setRadiationImpedanceBC_by_Node(read.nodes_typed, read.radiation_impedance)
        print("[Set Radiation Impedance Source] - defined in the point(s) {}".format(read.nodes_typed))
        self.opv.transformPoints(read.nodes_typed)

    def setNodalLoads(self):
        point_id = self.opv.getListPickedPoints()
        loads = LoadsInput(self.project.mesh.nodes, point_id)

        if loads.loads is None:
            return

        self.project.setForce_by_Node(loads.nodes_typed, loads.loads)
        print("[Set Nodal Load] - defined in the point(s) {}".format(loads.nodes_typed))
        self.opv.transformPoints(loads.nodes_typed)

    def addMassSpringDamper(self):
        point_id = self.opv.getListPickedPoints()
        msd = MassSpringDamperInput(self.project.mesh.nodes, point_id)
        if msd.input_mass:
            self.project.setMass_by_Node(msd.nodes_typed, msd.mass)
            print("[Set Mass] - defined in the point(s) {}".format(msd.nodes_typed))
        if msd.input_spring:
            self.project.setSpring_by_Node(msd.nodes_typed, msd.spring)
            print("[Set Spring] - defined in the point(s) {}".format(msd.nodes_typed))
        if msd.input_damper:
            self.project.setDamper_by_Node(msd.nodes_typed, msd.damper)
            print("[Set Damper] - defined in the point(s) {}".format(msd.nodes_typed))         

    def analysisTypeInput(self):

        inputs = AnalysisTypeInput()
        self.analysis_ID = inputs.analysis_ID
        self.analysis_type_label = inputs.analysis_type_label
        self.analysis_method_label = inputs.analysis_method_label

        if self.analysis_ID is None:
            return
 
        self.project.setAnalysisType(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.setModes(inputs.modes)
        self.project.setAcousticSolution(None)
        self.project.setStructuralSolution(None)

        if self.analysis_ID in [2,4]:
            if not inputs.complete:
                return
            else:
                self.runAnalysis()
        else:
            self.analysisSetup()
        
    def analysisSetup(self):
        
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0

        if self.project.analysis_ID is None:
            return
        if self.project.file._projectName == "":
            return

        self.project.loadAnalysisFile()
        self.f_min, self.f_max, self.f_step = self.project.minFrequency, self.project.maxFrequency, self.project.stepFrequency
        setup = AnalysisSetupInput(self.analysis_ID, self.analysis_type_label, self.analysis_method_label, f_min = self.f_min, f_max = self.f_max, f_step = self.f_step)
        
        self.frequencies = setup.frequencies
        self.f_min = setup.min_frequency
        self.f_max = setup.max_frequency
        self.f_step = setup.step_frequency

        if not setup.complete:
            return

        self.project.setFrequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

        if self.analysis_ID != 3:
            self.project.setModes(setup.modes)
            self.project.setDamping(setup.damping)
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
            solve = self.project.getStructuralSolve()
            modes = self.project.getModes()
        elif self.analysis_ID == 4:
            solve = self.project.getAcousticSolve()
            modes = self.project.getModes()
        elif self.analysis_ID == 3:
            solve = self.project.getAcousticSolve()
        elif self.analysis_ID in [5,6]:
            solve = self.project.getAcousticSolve()
            modes = self.project.getModes()
            damping = self.project.getDamping()
        else:
            solve = self.project.getStructuralSolve()
            modes = self.project.getModes()
            damping = self.project.getDamping()

        if self.analysis_ID == 2:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [])
            if solution.solution is None:
                return
            self.project.setStructuralSolution(solution.solution)
            self.project.setStructuralNaturalFrequencies(solution.natural_frequencies_structural.tolist())

        elif self.analysis_ID == 4:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [])
            if solution.solution is None:
                return
            self.project.setAcousticSolution(solution.solution)
            self.project.setAcousticNaturalFrequencies(solution.natural_frequencies_acoustic.tolist())

        elif self.analysis_ID == 3:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, [], [])
            if solution.solution is None:
                return
            self.project.setAcousticSolution(solution.solution)
        elif self.analysis_ID in [5,6]:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, project=self.project)
            # if solution.solution_structural is None:
            #     return
            self.project.setStructuralSolution(solution.solution_structural)

        else:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping)
            if solution.solution is None:
                return
            self.project.setStructuralSolution(solution.solution)
 
    def plotStructuralModeShapes(self):
        solution = self.project.getStructuralSolution()
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
        solution = self.project.getStructuralSolution()
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
        solution = self.project.getAcousticSolution()
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
        solution = self.project.getAcousticSolution()
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
            solution = self.project.getStructuralSolution()
            if solution is None:
                return
            PlotStructuralFrequencyResponseInput(self.project.getMesh(), self.analysis_method_label, self.frequencies, solution)

    def plotAcousticFrequencyResponse(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.getAcousticSolution()
            if solution is None:
                return
            PlotAcousticFrequencyResponseInput(self.project.getMesh(), self.analysis_method_label, self.frequencies, solution)

    def plotStressField(self):
        pass

    def newProject(self):
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
            if self.project.mesh.flag_setCrossSection == True:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.flag_setMaterial == True:
                error(material_message, title = title)
                return True
        
        elif self.analysis_ID == 4:
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.flag_setFluid == True:
                error(fluid_message, title = title)
                return True
        
        elif self.analysis_ID == 3:
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                error(cross_section_message, title = title)
                return True
            elif self.project.mesh.flag_setFluid == True:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.sum_volumeVelocity == 0:
                if self.project.mesh.sum_acousticPressures == 0:
                    error(acoustic_message, title = title)
                    return True

        elif self.analysis_ID == 0 or self.analysis_ID == 1:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                error(cross_section_message, title = title)
                return True
            if self.project.mesh.flag_setMaterial == True:
                error(material_message, title = title)
                return True
            elif self.project.mesh.sum_loads == 0:
                if self.project.mesh.sum_prescribedDOFs == 0:
                    error(structural_message, title = title)
                    return True

        elif self.analysis_ID == 5 or self.analysis_ID == 6:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                error(cross_section_message, title = title)
                return True
            elif self.project.mesh.flag_setMaterial == True:
                error(material_message, title = title)
                return True
            elif self.project.mesh.flag_setFluid == True:
                error(fluid_message, title = title)
            elif self.project.mesh.sum_volumeVelocity == 0:
                if self.project.mesh.sum_acousticPressures == 0:
                    error(acoustic_message, title = title)
                    return True