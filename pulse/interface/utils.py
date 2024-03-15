
import os
from pathlib import Path

from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title = "Error"

def check_inputs(lineEdit, label, only_positive=True, zero_included=False):
        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if only_positive:
                    if zero_included:
                        if out < 0:
                            title = "INPUT CROSS-SECTION ERROR"
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([window_title, title, message])
                            return None
                    else:
                        if out <= 0:
                            title = "INPUT CROSS-SECTION ERROR"
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([window_title, title, message])
                            return None
            except Exception as _err:
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Wrong input for {label}.\n\n"
                message += str(_err)
                PrintMessageInput([window_title, title, message])
                return None
        else:
            if zero_included:
                return float(0)
            else: 
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([window_title, title, message])
                return None
        return out
    
def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))