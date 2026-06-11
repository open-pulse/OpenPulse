

from pulse.editor.structures.linear_structure import LinearStructure


class RigidElement(LinearStructure):
    def __init__(self, start, end, *args, **kwargs):
        super().__init__(start, end, *args, **kwargs)
    
    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import RigidElementActor
        return RigidElementActor(self)

    def define_gmsh_mesh_constraints(self):
        pass

    