from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.materialList import MaterialList
from pulse.uix.user_input.crossInput import CrossInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.dofImport import DOFImport
from pulse.uix.user_input.newProjectInput import NewProjectInput

from pulse.project import Project

class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()

    def material_input(self):
        pass
        # last = self.parent.getLastPickedEntity()
        # if last is None:
        #     return
        
        # mi = MaterialInput()

    def material_list(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        selected_material = MaterialList()
        if selected_material.material is None:
            return
        for entity in entities_id:
            self.project.setMaterial_by_Entity(entity, selected_material.material)
        print("### Material {} defined in the entities {}".format(selected_material.material.name, entities_id))

    def cross_input(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        cross_section = CrossInput()
        if cross_section.cross is None:
            return
        for entity in entities_id:
            self.project.setMaterial_by_Entity(entity, selected_material.material)
        # last = self.parent.getLastPickedEntity()
        # if last is None:
        #     return
        
        # ci = CrossInput()

    def import_dof(self):
        pass
        # last = self.parent.getLastPickedPoint()
        # if last is None:
        #     return
        
        # imd = DOFImport()

    def dof_input(self):
        pass
        # last = self.parent.getLastPickedPoint()
        # if last is None:
        #     return
        
        # di = DOFInput()

    def newProject(self):
        a = NewProjectInput()

    def define_material_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        selected_material = MaterialList()
        
        if selected_material.material is not None:
            self.project.setMaterial(selected_material.material)

    def define_cross_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        cross_section = CrossInput()
        if cross_section.cross is not None:
            self.project.setCrossSection(cross_section.cross)
        