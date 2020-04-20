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

from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.uix.user_input.preProcessingInfo import PreProcessingInfo

from pulse.processing.solution import direct_method, modal_superposition
from pulse.postprocessing.plot_data import get_displacement_matrix

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

    def setDOF(self):
        point_id = self.opv.getListPickedPoints()
        dof = DOFInput(point_id)

        if dof.dof is None:
            return

        self.project.setBondaryCondition_by_Node(point_id, dof.dof)
        print("[Set Bondary Condition] - defined in the poins {}".format(point_id))
        self.opv.changeColorPoints(point_id, (0,1,0))

    def setNodalLoads(self):
        point_id = self.opv.getListPickedPoints()
        loads = LoadsInput(point_id)

        if loads.loads is None:
            return

        self.project.setFroce_by_Node(point_id, loads.loads)
        print("[Set Loads] - defined in the poins {}".format(point_id))
        self.opv.changeColorPoints(point_id, (0,1,0))

    def addMassSpringDamper(self):
        MassSpringDamperInput()

    def analyseTypeInput(self):
        AnalyseTypeInput()

    def analyseSetup(self):
        AnalyseSetupInput()

    def analyseOutputResults(self):
        AnalyseOutputResultsInput()

    def runAnalyse(self):
        RunAnalyseInput()

    def plotModeShapes(self):
        PlotModeShapeInput()

    def plotHarmonicResponse(self):
        PlotHarmonicResponseInput()

    def plotPressureField(self):
        pass

    def plotStressField(self):
        pass

    def plotFrequencyResponse(self):
        PlotFrequencyResponseInput()

    def newProject(self):
        result = NewProjectInput(self.project)
        return result.create

    def direct_method(self):
        freq = FrequencyInput()
        try:
            if len(freq.frequencies) == 0:
                print("Nenhuma frequencia")
                return
            if not self.project.checkEntityMaterial():
                print("Erro check material")
                return
            if not self.project.checkEntityCross():
                print("Erro check cross")
                return
            direct = direct_method(self.project.getMesh(), freq.frequencies)
            self.project.setDirectMatriz(direct)
            self.project.setFrequencies(freq.frequencies)
            self.opv.change_to_direct_method(0)
        except Exception as e:
            print("{}".format(e))

    def modal_superposition(self):
        freq = FrequencyInput()
        try:
            if len(freq.frequencies) == 0:
                print("Nenhuma frequencia")
                return
            if not self.project.checkEntityMaterial():
                print("Erro check material")
                return
            if not self.project.checkEntityCross():
                print("Erro check cross")
                return
            modes = 140
            modal = modal_superposition(self.project.getMesh(), freq.frequencies, modes)
            self.project.setModalMatriz(modal)
            self.project.setFrequencies(freq.frequencies)
            self.project.setModes(modes)
            self.opv.change_to_modal_superposition(0)
        except Exception as e:
            print("{}".format(e))

    def changeFrequencyInput(self):
        freq = FrequencyList(self.project.getFrequencies())
        if freq.current_item is None:
            return
        self.opv.changeFrequency(freq.current_item)
