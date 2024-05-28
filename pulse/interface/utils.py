
import os
from pathlib import Path
from pulse import ICON_DIR

from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title = "Error"

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