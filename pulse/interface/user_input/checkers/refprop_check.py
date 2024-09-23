from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput

import os
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class CheckREFPROP:

    def __init__(self):
        super().__init__()

        self.check_external_dependency()

    def check_external_dependency(self):

        from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

        refProp_path = self.get_refprop_path()

        if refProp_path is None:
            return True

        if os.path.exists(refProp_path):
            
            self.refprop = REFPROPFunctionLibrary(refProp_path)
            if self.check_refprop_version():
                return True

    def get_refprop_path(self):

        refProp_path = None
        try:
            refProp_path = os.environ['RPPREFIX']
        except:
            pass

        if refProp_path is None:
            try:
                refProp_path = app().config.get_refprop_path_from_file()
            except:
                pass

        if refProp_path is None:

            caption = 'Search for the REFPROP folder'
            initial_path = str(Path().home())

            folder_path = app().main_window.file_dialog.get_existing_directory(caption, initial_path)
            
            if folder_path == "":
                return None

            if os.path.exists(folder_path):

                if os.path.basename(folder_path) in ["REFPROP", "Refprop", "refprop"]:
                    app().config.write_refprop_path_in_file(folder_path)
                    refProp_path = folder_path

                else:
                    title = "Invalid folder selected"
                    message = f"The selected folder path {folder_path} does not match with the REFPROP installation folder. "
                    message += "As suggestion, try to find the default installation folder in 'C:/Program Files (x86)/REFPROP'. "
                    message += "You should select the valid REFPROP installation folder to proceed."
                    PrintMessageInput([window_title_1, title, message])

        return refProp_path

    def check_refprop_version(self):

        version = self.refprop.RPVersion()

        if version[:3] != "10.":
            title = "Invalid REFPROP version detected"
            message = "The installed REFPROP version is incompatible with the OpenPulse requirements. It is recommended "
            message += "to install a newer REFPROP version to maintain the compatibility with the application.\n\n"
            message += f"Current version: {version}\n"
            message +=  "Required version: >= 10.0"
            PrintMessageInput([window_title_2, title, message])
            return True
        
        else:
            title = "REFPROP version detected"
            message = f"The current REFPROP version {version} installed "
            message += "in the computer meets the OpenPulse requirements."
            PrintMessageInput([window_title_2, title, message], auto_close=True)
            return False