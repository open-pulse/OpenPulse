
import numpy as np
from enum import IntEnum
from pulse import ICON_DIR
from dataclasses import dataclass

from pulse.interface.user_input.project.print_message import PrintMessageInput


window_title = "Error"


class Workspace(IntEnum):
    GEOMETRY = 0 
    STRUCTURAL_SETUP = 1
    ACOUSTIC_SETUP = 2
    RESULTS = 3


@dataclass
class VisualizationFilter:
    points: bool = False
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False

    @classmethod
    def all_false(cls):
        # It is dumb, but it works
        args = [False] * 7
        return cls(*args)
    
    @classmethod
    def all_true(cls):
        # It is dumb, but it works
        args = [True] * 7
        return cls(*args)

@dataclass
class SelectionFilter:
    nodes: bool = False
    entities: bool = False
    elements: bool = False

    @classmethod
    def all_false(cls):
        # It is dumb, but it works
        args = [False] * 3
        return cls(*args)
    
    @classmethod
    def all_true(cls):
        # It is dumb, but it works
        args = [True] * 3
        return cls(*args)


# Abandon this
@dataclass
class PlotFilter:
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    raw_lines: bool = False



def check_inputs(lineEdit, label, only_positive=True, zero_included=False, title=None):

        if title is None:
            title = "Invalid input"

        if lineEdit.text() != "":

            try:

                str_value = lineEdit.text().replace(",", ".")
                out = float(str_value)

                if only_positive:

                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([window_title, title, message])
                            return None
                    else:

                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([window_title, title, message])
                            return None

            except Exception as error_log:

                message = f"Wrong input for {label}.\n\n"
                message += str(error_log)
                PrintMessageInput([window_title, title, message])
                return None

        else:

            if zero_included:
                return float(0)
            else: 
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([window_title, title, message])
                return None

        return out
    
def get_icons_path(filename):
    path = ICON_DIR / filename
    if path.exists():
        return str(path)
    
def rotation_matrices(ax, ay, az):
    sin = np.sin([ax, ay, az])
    cos = np.cos([ax, ay, az])

    rx = np.array(
        [
            [1, 0, 0, 0],
            [0, cos[0], -sin[0], 0],
            [0, sin[0], cos[0], 0],
            [0, 0, 0, 1],
        ]
    )

    ry = np.array(
        [
            [cos[1], 0, sin[1], 0],
            [0, 1, 0, 0],
            [-sin[1], 0, cos[1], 0],
            [0, 0, 0, 1],
        ]
    )

    rz = np.array(
        [
            [cos[2], -sin[2], 0, 0],
            [sin[2], cos[2], 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    return rx, ry, rz
