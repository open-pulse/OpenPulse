from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.crossInput import CrossInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.forceInput import ForceInput

from pulse.project import Project

class InputWidget:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent

    def material_input(self):
        last = self.parent.getLastPickedEntity()
        if last is None:
            return
        
        mi = MaterialInput()

    def cross_input(self):
        last = self.parent.getLastPickedEntity()
        if last is None:
            return
        
        ci = CrossInput()

    def import_dof(self):
        last = self.parent.getLastPickedPoint()
        if last is None:
            return
        
        imd = ForceInput()

    def dof_input(self):
        last = self.parent.getLastPickedPoint()
        if last is None:
            return
        
        di = DOFInput()