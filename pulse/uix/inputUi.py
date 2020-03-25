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

    def material_input(self):
        last = self.parent.getLastPickedEntity()
        if last is None:
            return
        
        mi = MaterialInput()

    def material_list(self):
        ml = MaterialList()

    def cross_input(self):
        last = self.parent.getLastPickedEntity()
        if last is None:
            return
        
        ci = CrossInput()

    def import_dof(self):
        last = self.parent.getLastPickedPoint()
        if last is None:
            return
        
        imd = DOFImport()

    def dof_input(self):
        last = self.parent.getLastPickedPoint()
        if last is None:
            return
        
        di = DOFInput()

    def newProject(self):
        a = NewProjectInput()