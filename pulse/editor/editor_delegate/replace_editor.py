from .editor import Editor

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
    SimpleCurve,
    LinearStructure
)


class ReplaceEditor(Editor):
    def replace_by_pipe(self, **kwargs):
        return self.replace_selection_by(Pipe, **kwargs)
    
    # def replace_by_bent_pipes(self, curvature_radius, **kwargs):
    #     return self.replace_selection_by(Pipe, **kwargs)

    def replace_by_flanges(self, **kwargs):
        return self.replace_selection_by(Flange, **kwargs)

    def replace_by_expansion_joints(self, **kwargs):
        return self.replace_selection_by(ExpansionJoint, **kwargs)

    def replace_by_valves(self, **kwargs):
        return self.replace_selection_by(Valve, **kwargs)

    def replace_by_reducer_eccentrics(self, **kwargs):
        return self.replace_selection_by(Reducer, **kwargs)

    def replace_by_circular_beams(self, **kwargs):
        return self.replace_selection_by(CircularBeam, **kwargs)

    def replace_by_rectangular_beams(self, **kwargs):
        return self.replace_selection_by(RectangularBeam, **kwargs)

    def replace_by_i_beams(self, **kwargs):
        return self.replace_selection_by(IBeam, **kwargs)

    def replace_by_c_beams(self, **kwargs):
        return self.replace_selection_by(CBeam, **kwargs)

    def replace_by_t_beams(self, **kwargs):
        return self.replace_selection_by(TBeam, **kwargs)

    def replace_selection_by(self, structure_type, **kwargs):
        for original_structure in self.pipeline.selected_points:
            self.replace_structure(original_structure, structure_type, **kwargs)

    def replace_structure(self, original_structure, structure_type, **kwargs):
        if not isinstance(original_structure, LinearStructure):
            return

        if not issubclass(structure_type, LinearStructure):
            return
        
        new_structure = structure_type(
            start=original_structure.start,
            end=original_structure.end,
            **kwargs,
        )
        self.pipeline.remove_structure(original_structure)
        self.pipeline.add_structure(new_structure)
