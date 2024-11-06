from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.editor.structures import Point

import gmsh

from copy import deepcopy
from pulse.utils.text_utils import pascal_to_snake_case
from molde.colors import Color, WHITE


class Structure:
    """
    Abstract class to handle methods and properties common every structure.
    """

    color: Color
    selected: bool
    staged: bool
    tag: int
    extra_info: dict

    def __init__(self, **kwargs) -> None:
        self.color: Color = kwargs.get("color", WHITE)
        self.selected: bool = kwargs.get("selected", False)
        self.staged: bool = kwargs.get("staged", False)
        self.tag: int = kwargs.get("tag", -1)
        self.extra_info: dict = kwargs.get("extra_info", dict())

    @property
    def arc_length(self) -> float:
        class_name = type(self).__name__
        return NotImplementedError(
            f'arc_length method not implemented in "{class_name}".'
        )

    @classmethod
    def name(cls):
        return pascal_to_snake_case(cls.__name__)

    def get_points(self) -> list["Point"]:
        class_name = type(self).__name__
        raise NotImplementedError(
            f'get_points method not implemented in "{class_name}".'
        )

    def replace_point(self, old, new):
        class_name = type(self).__name__
        raise NotImplementedError(
            f'replace_point method not implemented in "{class_name}".'
        )

    def as_dict(self) -> dict:
        return {
            "color": self.color,
            "tag": self.tag,
            "extra_info": self.extra_info,
        }

    def copy(self):
        new_structure = deepcopy(self)
        new_structure.tag = -1
        return new_structure

    def as_vtk(self):
        class_name = type(self).__name__
        raise NotImplementedError(f'as_vtk method not implemented in "{class_name}".')

    def __hash__(self) -> int:
        return id(self)
