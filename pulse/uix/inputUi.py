from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.materialList import MaterialList
from pulse.uix.user_input.crossInput import CrossInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.dofImport import DOFImport
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.uix.user_input.preProcessingInfo import PreProcessingInfo

from pulse.project import Project

class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()

    def material_input(self):
        pass
        #MaterialInput(self.project.materialPath)

    def material_list(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        selected_material = MaterialList(self.project.materialListPath)
        if selected_material.material is None:
            return
        for entity in entities_id:
            self.project.setMaterial_by_Entity(entity, selected_material.material)
        print("### Material {} defined in the entities {}".format(selected_material.material.name, entities_id))
        self.opv.changeColorEntities(entities_id, selected_material.material.getNormalizedColorRGB())
        

    def cross_input(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        cross_section = CrossInput()
        if cross_section.cross is None:
            return
        for entity in entities_id:
            self.project.setCrossSection_by_Entity(entity, cross_section.cross)
        print("### Cross defined in the entities {}".format(entities_id))
        self.opv.changeColorCross()

    def import_dof(self):
        pass
        # last = self.parent.getLastPickedPoint()
        # if last is None:
        #     return
        
        # imd = DOFImport()

    def dof_input(self):
        pass
        point_id = self.opv.getListPickedPoints()
        if len(point_id) == 0:
            return

        dof = DOFInput()
        if dof.bondary is None:
            return
        print(point_id)
        self.project.setBondaryCondition_by_Node(point_id, dof.bondary)
        print("### BC defined in the Points {}".format(point_id))
        self.opv.changeColorPoints(point_id, (0,1,0))

    def newProject(self):
        result = NewProjectInput(self.project)
        return result.create

    def define_material_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        selected_material = MaterialList(self.project.materialListPath)
        
        if selected_material.material is not None:
            self.project.setMaterial(selected_material.material)
        entities = []
        for entity in self.project.getEntities():
            entities.append(entity.getTag())
        self.opv.changeColorEntities(entities, selected_material.material.getNormalizedColorRGB())

    def define_cross_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        cross_section = CrossInput()
        if cross_section.cross is not None:
            self.project.setCrossSection(cross_section.cross)
        self.opv.changeColorCross()

    def preProcessingInfo(self):
        pre = PreProcessingInfo(self.project.entityPath, self.project.nodePath)
        if not pre.hasError:
            self.opv.change_to_preProcessing()