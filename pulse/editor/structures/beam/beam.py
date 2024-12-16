from molde.colors import ORANGE_4

from pulse.editor.structures.point import Point
from ..linear_structure import LinearStructure


class Beam(LinearStructure):
    """
    Abstract class to handle common stuff to most structures.
    Also usefull to get diferentiate Beams from other structures.
    """

    def __init__(self, start: Point, end: Point, *args, **kwargs) -> None:
        super().__init__(start, end, *args, **kwargs)
        self.color = ORANGE_4
        self.offset_y = kwargs.get("offset_y", 0)
        self.offset_z = kwargs.get("offset_z", 0)
