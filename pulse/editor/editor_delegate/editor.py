from pulse.editor.structures import ArcBend, Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.editor import Pipeline


class Editor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline

    def is_bend_allowed(self, selected_points: list[Point]):
        for point in selected_points:
            for structure in self.pipeline.structures_of_type(ArcBend):
                if point in structure.get_points():
                    return False

        return True
