from molde.colors import TEAL_7

from .linear_structure import LinearStructure


class Reducer(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.initial_diameter = kwargs.get("initial_diameter", 0.1)
        self.final_diameter = kwargs.get("final_diameter", 0.05)
        self.initial_offset_y = kwargs.get("initial_offset_y", 0)
        self.initial_offset_z = kwargs.get("initial_offset_z", 0)
        self.final_offset_y = kwargs.get("final_offset_y", 0)
        self.final_offset_z = kwargs.get("final_offset_z", 0)
        self.thickness = kwargs.get("thickness", 0.01)
        self.color = TEAL_7

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ReducerActor

        return ReducerActor(self)
