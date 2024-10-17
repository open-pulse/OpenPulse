from itertools import pairwise

from pulse.editor.structures import (
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Flange,
    IBeam,
    Pipe,
    RectangularBeam,
    Reducer,
    TBeam,
    Valve,
)

from .editor import Editor


class ConnectionEditor(Editor):
    def connect_pipes(self, **kwargs):
        return self._generic_structure_connection(Pipe, **kwargs)

    def connect_bent_pipes(self, curvature_radius: float, **kwargs):
        pipes = self.connect_pipes(**kwargs)
        bends = self.pipeline.add_bend(curvature_radius, **kwargs)
        return pipes + bends

    def connect_expansion_joints(self, **kwargs):
        return self._generic_structure_connection(ExpansionJoint, **kwargs)

    def connect_flanges(self, **kwargs):
        return self._generic_structure_connection(Flange, **kwargs)

    def connect_valves(self, **kwargs):
        return self._generic_structure_connection(Valve, **kwargs)

    def connect_reducer_eccentrics(self, **kwargs):
        return self._generic_structure_connection(Reducer, **kwargs)

    def connect_circular_beams(self, **kwargs):
        return self._generic_structure_connection(CircularBeam, **kwargs)

    def connect_rectangular_beams(self, **kwargs):
        return self._generic_structure_connection(RectangularBeam, **kwargs)

    def connect_i_beams(self, **kwargs):
        return self._generic_structure_connection(IBeam, **kwargs)

    def connect_c_beams(self, **kwargs):
        return self._generic_structure_connection(CBeam, **kwargs)

    def connect_t_beams(self, **kwargs):
        return self._generic_structure_connection(TBeam, **kwargs)

    def _generic_structure_connection(self, structure_type, **kwargs):
        structures = []
        for point_a, point_b in pairwise(self.pipeline.selected_points):
            structure = structure_type(point_a, point_b, **kwargs)
            self.pipeline.add_structure(structure)
            structures.append(structure)
        return structures
