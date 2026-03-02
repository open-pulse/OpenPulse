from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.user_input.model.setup.nodes_input import NodesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np


class AcousticNodesInput(NodesInput):

    def __init__(self):
        super().__init__()
    
    def process_table_file_removal(self, table_names):
        super().process_table_file_removal("acoustic", table_names)
        
    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text
    
    def check_complex_entries(self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit, input_name: str):
        error_title = "Error"

        title = f"Invalid entry to the {input_name}"

        if lineEdit_real.text() != "":

            _str_real = lineEdit_real.text()
            str_real = _str_real.replace(",", ".")

            try:
                real_F = float(str_real)
            except Exception:
                self.hide()
                message = f"Wrong input for real part of {input_name}."
                PrintMessageInput([error_title, title, message])
                lineEdit_real.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            real_F = 0

        if lineEdit_imag.text() != "":

            _str_imag = lineEdit_imag.text()
            str_imag = _str_imag.replace(",", ".")

            try:
                imag_F = float(str_imag)
            except Exception:
                self.hide()
                message = f"Wrong input for imaginary part of {input_name}."
                PrintMessageInput([error_title, title, message])
                lineEdit_imag.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            self.hide()
            message = f"You must inform at least one {input_name} " 
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            app().main_window.set_input_widget(self)
            return True, None

        else:
            return False, real_F + 1j*imag_F
    
