from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.fluidInput import FluidInput
from pulse.uix.user_input.crossSectionInput import CrossSectionInput
from pulse.uix.user_input.loadsInput import LoadsInput
from pulse.uix.user_input.massSpringDamperInput import MassSpringDamperInput
from pulse.uix.user_input.analyseTypeInput import AnalyseTypeInput
from pulse.uix.user_input.analyseSetupInput import AnalyseSetupInput
from pulse.uix.user_input.analyseOutputResultsInput import AnalyseOutputResultsInput
from pulse.uix.user_input.runAnalyseInput import RunAnalyseInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.specificimpedanceInput import SpecificImpedanceInput
from pulse.uix.user_input.radiationimpedanceInput import RadiationImpedanceInput
from pulse.uix.user_input.volumevelocityInput import VolumeVelocityInput
from pulse.uix.user_input.acousticpressureInput import AcousticPressureInput

from pulse.uix.user_input.plotModeShapeInput import PlotModeShapeInput
from pulse.uix.user_input.plotHarmonicResponseInput import PlotHarmonicResponseInput
from pulse.uix.user_input.plotFrequencyResponseInput import PlotFrequencyResponseInput
from pulse.uix.user_input.elementTypeInput import ElementTypeInput
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.project import Project
from pulse.utils import error

class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()

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

    def analyseTypeInput(self):
        analysis_input = AnalyseTypeInput()
        if analysis_input.typeID is None:
            return
 
        self.project.setAnalysisType(analysis_input.typeID, analysis_input.type, analysis_input.method)
        self.project.setModes(analysis_input.modes)
        self.project.setAcousticSolution(None)
        self.project.setStructuralSolution(None)

        if analysis_input.typeID == 0 or analysis_input.typeID == 1:
            self.analyseSetup()
        elif analysis_input.typeID == 2:
            if not analysis_input.complete:
                return
            else:
                self.runAnalyse()
   
    def analyseSetup(self):

        if self.project.getAnalysisTypeID() is None:
            return

        self.project.loadAnalysisFile()
        f_min, f_max, df = self.project.minFrequency, self.project.maxFrequency, self.project.stepFrequency
        TypeID, AnalysisType, AnalysisMethod = self.project.getAnalysisTypeID(), self.project.getAnalysisType(), self.project.getAnalysisMethod() 
        setup = AnalyseSetupInput(TypeID, AnalysisType, AnalysisMethod, min_freq = f_min, max_freq = f_max, step_freq = df)
      
        if not setup.complete:
            return
    
        elif self.project.getAnalysisTypeID() == 0 or self.project.getAnalysisTypeID() == 1:
            if self.project.getAnalysisType() == "Harmonic Analysis - Structural":
                self.project.setFrequencies(setup.frequencies, setup.min_frequency, setup.max_frequency, setup.step_frequency)
                self.project.setModes(setup.modes)
                self.project.setDamping(setup.damping)
            elif self.project.getAnalysisType() == "Harmonic Analysis - Acoustic":
                self.project.setFrequencies(setup.frequencies, setup.min_frequency, setup.max_frequency, setup.step_frequency)

    def analyseOutputResults(self):
        AnalyseOutputResultsInput()

    def runAnalyse(self):
        if self._check_is_there_a_problem():
            return
        analyseTypeID = self.project.getAnalysisTypeID()
        analysis_type = self.project.getAnalysisType()
        frequencies = self.project.getFrequencies()

        if analyseTypeID == 0 or analyseTypeID == 1:
            if self.project.getAnalysisType() == "Harmonic Analysis - Structural":
                solve = self.project.getStructuralSolve()
                modes = self.project.getModes()
                damping = self.project.getDamping()
            elif self.project.getAnalysisType() == "Harmonic Analysis - Acoustic":
                solve = self.project.getAcousticSolve()
        elif analyseTypeID == 2:
            solve = self.project.getStructuralSolve()
            modes = self.project.getModes()
                
        if analyseTypeID is None:
            return
        if len(frequencies) == 0:
            if analyseTypeID == 0 or analyseTypeID == 1:
                return

        if analyseTypeID == 0 or analyseTypeID == 1:
            if self.project.getAnalysisType() == "Harmonic Analysis - Structural":
                solution = RunAnalyseInput(solve, analyseTypeID, analysis_type, frequencies, modes, damping)
                if solution.solution is None:
                    return
                self.project.setStructuralSolution(solution.solution)
            elif self.project.getAnalysisType() == "Harmonic Analysis - Acoustic":
                solution = RunAnalyseInput(solve, analyseTypeID, analysis_type, frequencies, [], [])
                if solution.solution is None:
                    return
                self.project.setAcousticSolution(solution.solution)

        if analyseTypeID == 2:
            solution = RunAnalyseInput(solve, analyseTypeID, analysis_type, [], modes, [])
            if solution.solution is None:
                return
            self.project.setStructuralSolution(solution.solution)
            self.project.setNaturalFrequencies(solution.naturalFrequencies.tolist())

    def plotModeShapes(self):
        solution = self.project.getStructuralSolution()
        analyseTypeID = self.project.getAnalysisTypeID()
        frequencies = self.project.getNaturalFrequencies()
        if analyseTypeID == 2:
            if solution is None:
                return
            plot = PlotModeShapeInput(frequencies)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalyse(plot.mode_index)
        else:
            return

    def plotHarmonicResponse(self):
        solution = self.project.getStructuralSolution()
        analyseTypeID = self.project.getAnalysisTypeID()
        frequencies = self.project.getFrequencies()
        if analyseTypeID == 0 or analyseTypeID == 1:
            if solution is None:
                return
            plot = PlotHarmonicResponseInput(frequencies)
            if plot.frequency is None:
                return
            if analyseTypeID == 0:
                if self.project.getAnalysisType() == "Harmonic Analysis - Structural":
                    self.opv.changeAndPlotAnalyse(plot.frequency)
                else:
                    self.opv.changeAndPlotAnalyse(plot.frequency, acoustic=True)
            else:
                self.opv.changeAndPlotAnalyse(plot.frequency)    
        else:
            return

    def plotPressureField(self):
        solution = self.project.getAcousticSolution()
        analyseTypeID = self.project.getAnalysisTypeID()
        analysis_type = self.project.getAnalysisType()
        frequencies = self.project.getFrequencies()
        if analyseTypeID == 0 or analyseTypeID == 1:
            if solution is None:
                return
            plot = PlotHarmonicResponseInput(frequencies)
            if plot.frequency is None:
                return
            if analyseTypeID == 0 and analysis_type  == "Harmonic Analysis - Acoustic":
                    self.opv.changeAndPlotAnalyse(plot.frequency, acoustic=True)
            # else:
            #     self.opv.change_to_mode_superposition(plot.frequency)
        # else:
            return

    def plotStressField(self):
        pass

    def plotFrequencyResponse(self):
        analyseTypeID = self.project.getAnalysisTypeID()
        if analyseTypeID == 0 or analyseTypeID == 1:
            solution = self.project.getStructuralSolution()
            if solution is None:
                return
            analyseMethod = self.project.getAnalysisMethod()
            frequencies = self.project.getFrequencies()
            mesh = self.project.getMesh()
            PlotFrequencyResponseInput(mesh, analyseMethod, frequencies, solution)

    def newProject(self):
        result = NewProjectInput(self.project)
        return result.create

    def _check_is_there_a_problem(self):
  
        if self.project.getAnalysisTypeID() == 2:
            self.project.mesh.check_Material_and_CrossSection_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                message = "You should to set a Cross-Section to all\n elements before trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True
            if self.project.mesh.flag_setMaterial == True:
                message = "You should to set a Material to all elements\n before trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True

        if self.project.getAnalysisType() == "Harmonic Analysis - Structural":
            self.project.mesh.check_Material_and_CrossSection_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                message = "You should to set a Cross-Section to all \nelements before trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True
            if self.project.mesh.flag_setMaterial == True:
                message = "You should to set a Material to all \nelements before trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True
            elif self.project.mesh.sum_loads == 0:
                if self.project.mesh.sum_prescribedDOFs == 0:
                    message = "You should to apply an external load to the model or prescribe a \nnon-null DOF value before trying to solve the Harmonic Analysis!"
                    error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                    return True

        if self.project.getAnalysisType() == "Harmonic Analysis - Acoustic":
            self.project.mesh.check_Fluid_and_CrossSection_in_all_elements()
            if self.project.mesh.flag_setCrossSection == True:
                message = "You should to set a Cross-Section to all \nelements before trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True
            elif self.project.mesh.flag_setFluid == True:
                message = "You should to set a Fluid to all elements \nbefore trying to run any Analysis!"
                error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                return True
            elif self.project.mesh.sum_volumeVelocity == 0:
                if self.project.mesh.sum_acousticPressures == 0:
                    message = "You should to insert a Volume Velocity or prescribe an Acoustic \nPressure to a node before trying to solve the Harmonic Analysis!"
                    error(message, title = " ERROR: INSUFFICIENT MODEL INPUTS! ")
                    return True