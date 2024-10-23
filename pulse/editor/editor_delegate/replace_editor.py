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
