

from pulse.editor.structures.linear_structure import LinearStructure
from pulse.editor.structures.point import Point


class RigidElement(LinearStructure):
    def __init__(self, start, end, *args, **kwargs):
        super().__init__(start, end, *args, **kwargs)

    def add_to_gmsh(self, cad, convert_unit):
        line_tags = super().add_to_gmsh(cad, convert_unit)
        self._gmsh_line_tags = line_tags
        return line_tags
    
    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import RigidElementActor
        return RigidElementActor(self)

    def define_gmsh_mesh_constraints(self):
        import gmsh
        for tag in self._gmsh_line_tags:
            gmsh.model.mesh.setTransfiniteCurve(tag, 2)

    @classmethod
    def load_from_data(cls, data: dict) -> "RigidElement":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        structure = cls(start, end)
        structure.extra_info["structural_element_type"] = "rigid_element"
        return structure

    