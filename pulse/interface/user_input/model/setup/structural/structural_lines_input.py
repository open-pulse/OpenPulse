from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.user_input.model.setup.lines_input import LinesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput


class StructuralLinesInput(LinesInput):
    def __init__(self):
        super().__init__()

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        message = ""
        title = f"Invalid entry to the '{label}'"
        str_value = lineEdit.text()

        if str_value != "":

            try:

                str_value = str_value.replace(",", ".")
                if _float:
                    value = float(str_value)
                else:
                    value = int(str_value) 

                if value <= 0:
                    message = f"You cannot input a non-positive value to the '{label}'."

            except Exception as _log_error:
                message = f"You have typed an invalid value to the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        else:
            message = f"An empty entry has been detected at the '{label}' input field. " 
            message += "You should to enter a positive value to proceed."

        if message != "":
            PrintMessageInput(["Error", title, message])
            return True, None
        else:
            return False, value
    
    def process_table_file_removal(self, table_names: list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().project.file.write_imported_table_data_in_file()
 
