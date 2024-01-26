from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QRect

from pulse.utils import *
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

import gmsh
import sys
import os

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class EditImportedGeometryInput(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.file = project.file
        self.geometry_path = self.file._geometry_path
        self.project_ini_file_path = self.file._project_ini_file_path
        
        self.geometry_basename = "" 
        self.complete = False
        if os.path.exists(self.geometry_path):
            if os.path.basename(self.geometry_path) != "":
                self.geometry_basename = os.path.basename(self.geometry_path)
                self.call_gmsh(self.geometry_path)
    
    def call_gmsh(self, path):
       
        gmsh.initialize('', False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        
        try:
            gmsh.option.setNumber("General.NumThreads", 4)
        except:
            pass

        gmsh.open(str(self.geometry_path))
        # gmsh.option.setString("General.OCCTargetUnit", "m")

        gmsh.model.occ.synchronize()

        if '-nopopup' not in sys.argv:
            gmsh.option.setNumber('General.FltkColorScheme', 1)
            gmsh.fltk.run()

        title = f"Additional confirmation required"
        message = "Do you really want to confirm the current geometry edition?\n\n"
        message += "\n\nPress the Confirm and save button to proceed with the edtion and save the modified geometry "
        message += "into the project file, otherwise, press Cancel or Close buttons to abort the current operation."
        
        buttons_config = {"left_button_label" : "Cancel", 
                          "right_button_label" : "Confirm and save", 
                          "right_button_size" : 220}

        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            gmsh.finalize()
            return
        
        if read._continue:

            filename = self.geometry_basename.split(".")[0]
            self.new_basename = filename + ".step"
            self.new_geometry_path = get_new_path(self.file._project_path, self.new_basename)
            
            if os.path.exists(self.file._geometry_path):
                os.remove(self.file._geometry_path)

            gmsh.write(self.new_geometry_path)
            gmsh.finalize()

            # self.geometry_entities_path = self.file.get_geometry_entities_path()
            # if os.path.exists(self.geometry_entities_path):
            #     os.remove(self.geometry_entities_path)

            if os.path.exists(self.file._entity_path):
                os.remove(self.file._entity_path)
            
            self.project.edit_project_geometry(self.new_basename)
            self.project.initial_load_project_actions(self.project_ini_file_path)
            self.complete = True

        return True