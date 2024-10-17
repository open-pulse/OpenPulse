from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.editor import Pipeline


class Editor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline
