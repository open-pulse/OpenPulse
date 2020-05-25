from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.crossSectionInput import CrossSectionInput
from pulse.uix.user_input.loadsInput import LoadsInput
from pulse.uix.user_input.massSpringDamperInput import MassSpringDamperInput
from pulse.uix.user_input.analyseTypeInput import AnalyseTypeInput
from pulse.uix.user_input.analyseSetupInput import AnalyseSetupInput
from pulse.uix.user_input.analyseOutputResultsInput import AnalyseOutputResultsInput
from pulse.uix.user_input.runAnalyseInput import RunAnalyseInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.plotModeShapeInput import PlotModeShapeInput
from pulse.uix.user_input.plotHarmonicResponseInput import PlotHarmonicResponseInput
from pulse.uix.user_input.plotFrequencyResponseInput import PlotFrequencyResponseInput
from pulse.uix.user_input.elementTypeInput import ElementTypeInput
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.project import Project

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
        dof = DOFInput(point_id)

        if dof.dof is None:
            return

        self.project.setStructuralBondaryCondition_by_Node(dof.nodes, dof.dof)
        print("[Set Bondary Condition] - defined in the poins {}".format(dof.nodes))
        self.opv.transformPoints(dof.nodes)

    def setNodalLoads(self):
        point_id = self.opv.getListPickedPoints()
        loads = LoadsInput(point_id)

        if loads.loads is None:
            return

        self.project.setFroce_by_Node(loads.nodes, loads.loads)
        print("[Set Loads] - defined in the poins {}".format(loads.nodes))
        self.opv.transformPoints(loads.nodes)

    def addMassSpringDamper(self):
        point_id = self.opv.getListPickedPoints()
        msd = MassSpringDamperInput(point_id)

        if msd.mass is None:
            return

        self.project.setMass_by_Node(msd.nodes, msd.mass)
        self.project.setSpring_by_Node(msd.nodes, msd.spring)
        self.project.setDamper_by_Node(msd.nodes, msd.damper)
        print("[Set Mass/Spring/Damper] - defined in the poins {}".format(msd.nodes))

    def analyseTypeInput(self):
        analyseType = AnalyseTypeInput()
        if analyseType.typeID is None:
            return
        
        self.project.setAnalysisType(analyseType.typeID, analyseType.type, analyseType.method)
        self.project.setModes(analyseType.modes)
        #It's necessary to change the solution to None because there is a chance that the the user will
        #change the analyseType but before running again, her will try to plot.
        self.project.setSolution(None)
        
        if analyseType.typeID == 0 or analyseType.typeID == 1:
            self.analyseSetup()
        elif analyseType.typeID == 2:
            self.runAnalyse()

    def analyseSetup(self):
        if self.project.getAnalysisTypeID() is None:
            return
        minFrequency, maxFrequency, stepFrequency = self.project.getMinMaxStepFrequency()
        setup = AnalyseSetupInput(self.project.getAnalysisTypeID(), self.project.getAnalysisType(), self.project.getAnalysisMethod(), min_freq = minFrequency, max_freq = maxFrequency, step_freq = stepFrequency)
        
        if not setup.complete:
            return

        self.project.setFrequencies(setup.frequencies, setup.min_frequency, setup.max_frequency, setup.step_frequency)
        self.project.setModes(setup.modes)
        self.project.setDamping(setup.damping)

    def analyseOutputResults(self):
        AnalyseOutputResultsInput()

    def runAnalyse(self):
        solve = self.project.getSolve()
        # mesh = self.project.getMesh()
        analyseType = self.project.getAnalysisTypeID()
        frequencies = self.project.getFrequencies()
        modes = self.project.getModes()
        damping = self.project.getDamping()
        if analyseType is None:
            return
        if len(frequencies) == 0:
            if analyseType == 0 or analyseType == 1:
                return
        solution = RunAnalyseInput(solve, analyseType, frequencies, modes, damping)

        if solution.solution is None:
            return
        
        self.project.setSolution(solution.solution)
        if analyseType == 2:
            self.project.setNaturalFrequencies(solution.naturalFrequencies.tolist())

    def plotModeShapes(self):
        solution = self.project.getSolution()
        analyseType = self.project.getAnalysisTypeID()
        frequencies = self.project.getNaturalFrequencies()
        if analyseType == 2:
            if solution is None:
                return
            plot = PlotModeShapeInput(frequencies)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalyse(plot.mode_index)
        else:
            return

    def plotHarmonicResponse(self):
        solution = self.project.getSolution()
        analyseType = self.project.getAnalysisTypeID()
        frequencies = self.project.getFrequencies()
        if analyseType == 0 or analyseType == 1:
            if solution is None:
                return
            plot = PlotHarmonicResponseInput(frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalyse(plot.frequency)
        else:
            return

    def plotPressureField(self):
        pass

    def plotStressField(self):
        pass

    def plotFrequencyResponse(self):
        analyseType = self.project.getAnalysisTypeID()
        if analyseType == 0 or analyseType == 1:
            solution = self.project.getSolution()
            if solution is None:
                return
            analyseMethod = self.project.getAnalysisMethod()
            frequencies = self.project.getFrequencies()
            mesh = self.project.getMesh()
            PlotFrequencyResponseInput(mesh, analyseMethod, frequencies, solution)

    def newProject(self):
        result = NewProjectInput(self.project)
        return result.create