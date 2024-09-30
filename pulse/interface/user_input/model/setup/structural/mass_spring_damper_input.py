from PyQt5.QtWidgets import QCheckBox, QDialog, QFrame, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np
from pathlib import Path

window_title_1 ="Error"
window_title_2 ="Warning"

class MassSpringDamperInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/setup/structural/mass_spring_damper_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties

        self.before_run = app().project.get_pre_solution_model_checks()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.selection_callback()
        self.load_nodes_info()
               
        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.complete = False
        self.keep_window_open = True
        self.lumped_element_applied = False

        self.reset_table_variables()

    def reset_table_variables(self):

        self.Mx_table_name = None
        self.My_table_name = None
        self.Mz_table_name = None
        self.Jx_table_name = None
        self.Jy_table_name = None
        self.Jz_table_name = None

        self.Mx_table_path = None
        self.My_table_path = None
        self.Mz_table_path = None
        self.Jx_table_path = None
        self.Jy_table_path = None
        self.Jz_table_path = None

        self.Mx_table_values = None
        self.My_table_values = None
        self.Mz_table_values = None
        self.Jx_table_values = None
        self.Jy_table_values = None
        self.Jz_table_values = None

        self.Kx_table_name = None
        self.Ky_table_name = None
        self.Kz_table_name = None
        self.Krx_table_name = None
        self.Kry_table_name = None
        self.Krz_table_name = None

        self.Kx_table_path = None
        self.Ky_table_path = None
        self.Kz_table_path = None
        self.Krx_table_path = None
        self.Kry_table_path = None
        self.Krz_table_path = None

        self.Kx_table_values = None
        self.Ky_table_values = None
        self.Kz_table_values = None
        self.Krx_table_values = None
        self.Kry_table_values = None
        self.Krz_table_values = None

        self.Cx_table_name = None
        self.Cy_table_name = None
        self.Cz_table_name = None
        self.Crx_table_name = None
        self.Cry_table_name = None
        self.Crz_table_name = None

        self.Cx_table_path = None
        self.Cy_table_path = None
        self.Cz_table_path = None
        self.Crx_table_path = None
        self.Cry_table_path = None
        self.Crz_table_path = None

        self.Cx_table_values = None
        self.Cy_table_values = None
        self.Cz_table_values = None
        self.Crx_table_values = None
        self.Cry_table_values = None
        self.Crz_table_values = None

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_remove_mass : QCheckBox
        self.checkBox_remove_spring : QCheckBox
        self.checkBox_remove_damper : QCheckBox

        self.lineEdit_node_ids : QLineEdit

        # QFrame
        self.selection_frame : QFrame

        # QLineEdit
        self.lineEdit_path_table_Kx : QLineEdit
        self.lineEdit_path_table_Ky : QLineEdit
        self.lineEdit_path_table_Kz : QLineEdit
        self.lineEdit_path_table_Krx : QLineEdit
        self.lineEdit_path_table_Kry : QLineEdit
        self.lineEdit_path_table_Krz : QLineEdit

        self.lineEdit_path_table_Cx : QLineEdit
        self.lineEdit_path_table_Cy : QLineEdit
        self.lineEdit_path_table_Cz : QLineEdit
        self.lineEdit_path_table_Crx : QLineEdit
        self.lineEdit_path_table_Cry : QLineEdit
        self.lineEdit_path_table_Crz : QLineEdit

        self.lineEdit_Mx : QLineEdit
        self.lineEdit_My : QLineEdit
        self.lineEdit_Mz : QLineEdit
        self.lineEdit_Jx : QLineEdit
        self.lineEdit_Jy : QLineEdit
        self.lineEdit_Jz : QLineEdit

        self.lineEdit_Kx : QLineEdit
        self.lineEdit_Ky : QLineEdit
        self.lineEdit_Kz : QLineEdit
        self.lineEdit_Krx : QLineEdit
        self.lineEdit_Kry : QLineEdit
        self.lineEdit_Krz : QLineEdit

        self.lineEdit_Cx : QLineEdit
        self.lineEdit_Cy : QLineEdit
        self.lineEdit_Cz : QLineEdit
        self.lineEdit_Crx : QLineEdit
        self.lineEdit_Cry : QLineEdit
        self.lineEdit_Crz : QLineEdit

        self.lineEdit_path_table_Mx : QLineEdit
        self.lineEdit_path_table_My : QLineEdit
        self.lineEdit_path_table_Mz : QLineEdit
        self.lineEdit_path_table_Jx : QLineEdit
        self.lineEdit_path_table_Jy : QLineEdit
        self.lineEdit_path_table_Jz : QLineEdit

        self._create_lists_of_lineEdits()

        # QPushButton       
        self.pushButton_attribute : QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        self.pushButton_load_Mx_table : QPushButton
        self.pushButton_load_My_table : QPushButton
        self.pushButton_load_Mz_table : QPushButton
        self.pushButton_load_Jx_table : QPushButton
        self.pushButton_load_Jy_table : QPushButton
        self.pushButton_load_Jz_table : QPushButton

        self.pushButton_load_Kx_table : QPushButton
        self.pushButton_load_Ky_table : QPushButton
        self.pushButton_load_Kz_table : QPushButton
        self.pushButton_load_Krx_table : QPushButton
        self.pushButton_load_Kry_table : QPushButton
        self.pushButton_load_Krz_table : QPushButton         

        self.pushButton_load_Cx_table : QPushButton
        self.pushButton_load_Cy_table : QPushButton
        self.pushButton_load_Cz_table : QPushButton
        self.pushButton_load_Crx_table : QPushButton
        self.pushButton_load_Cry_table : QPushButton
        self.pushButton_load_Crz_table : QPushButton
        
        # QTabWidget
        self.tabWidget_main : QTabWidget
        self.tabWidget_inputs : QTabWidget
        self.tabWidget_main : QTabWidget

        self.tabWidget_external_elements : QTabWidget
        self.tabWidget_constant_values : QTabWidget
        self.tabWidget_table_values : QTabWidget
        self.tabWidget_remove : QTabWidget

        # QTreeWidget
        self.treeWidget_springs : QTreeWidget
        self.treeWidget_dampers : QTreeWidget
        self.treeWidget_masses : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        self.pushButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.pushButton_load_My_table.clicked.connect(self.load_My_table)
        self.pushButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.pushButton_load_Jx_table.clicked.connect(self.load_Jx_table)
        self.pushButton_load_Jy_table.clicked.connect(self.load_Jy_table)
        self.pushButton_load_Jz_table.clicked.connect(self.load_Jz_table)

        self.pushButton_load_Kx_table.clicked.connect(self.load_Kx_table)
        self.pushButton_load_Ky_table.clicked.connect(self.load_Ky_table)
        self.pushButton_load_Kz_table.clicked.connect(self.load_Kz_table)
        self.pushButton_load_Krx_table.clicked.connect(self.load_Krx_table)
        self.pushButton_load_Kry_table.clicked.connect(self.load_Kry_table)
        self.pushButton_load_Krz_table.clicked.connect(self.load_Krz_table)

        self.pushButton_load_Cx_table.clicked.connect(self.load_Cx_table)
        self.pushButton_load_Cy_table.clicked.connect(self.load_Cy_table)
        self.pushButton_load_Cz_table.clicked.connect(self.load_Cz_table)
        self.pushButton_load_Crx_table.clicked.connect(self.load_Crx_table)
        self.pushButton_load_Cry_table.clicked.connect(self.load_Cry_table)
        self.pushButton_load_Crz_table.clicked.connect(self.load_Crz_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_masses.itemClicked.connect(self.on_click_item_masses)
        self.treeWidget_masses.itemDoubleClicked.connect(self.on_doubleclick_item_masses)
        #
        self.treeWidget_springs.itemClicked.connect(self.on_click_item_springs)
        self.treeWidget_springs.itemDoubleClicked.connect(self.on_doubleclick_item_springs)
        #
        self.treeWidget_dampers.itemClicked.connect(self.on_click_item_dampings)
        self.treeWidget_dampers.itemDoubleClicked.connect(self.on_doubleclick_item_dampings)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            self.reset_input_fields_masses()
            self.reset_input_fields_stiffness()
            self.reset_input_fields_dampings()

            if len(selected_nodes) == 1:

                node_id = selected_nodes[0]
                lm_data = self.properties._get_property("lumped_masses", node_ids=node_id)
                if isinstance(lm_data, dict):

                    # Lumped masses/inertias
                    if "table_names" in lm_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(lm_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_masses[i]
                                lineEdit.setText(table_path)

                        else:

                            self.tabWidget_inputs.setCurrentIndex(0)
                            self.tabWidget_constant_values.setCurrentIndex(1)
                            for i, value in enumerate(lm_data["values"]):
                                if value is not None:
                                    lineEdit = self.constant_values_lumped_masses[i]
                                    lineEdit.setText(f"{value : .3e}")
     
                ls_data = self.properties._get_property("lumped_stiffness", node_ids=node_id)
                if isinstance(ls_data, dict):

                    # Lumped stiffness
                    if "table_names" in ls_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(ls_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_stiffness[i]
                                lineEdit.setText(table_path)

                        else:

                            self.tabWidget_inputs.setCurrentIndex(0)
                            self.tabWidget_constant_values.setCurrentIndex(1)
                            for i, value in enumerate(ls_data["values"]):
                                if value is not None:
                                    lineEdit = self.constant_values_lumped_stiffness[i]
                                    lineEdit.setText(f"{value : .3e}")

                ld_data = self.properties._get_property("lumped_dampings", node_ids=node_id)
                if isinstance(ld_data, dict):

                    # Lumped dampings
                    if "table_names" in ld_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(ld_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_dampings[i]
                                lineEdit.setText(table_path)

                        else:

                            self.tabWidget_inputs.setCurrentIndex(0)
                            self.tabWidget_constant_values.setCurrentIndex(1)
                            for i, value in enumerate(ld_data["values"]):
                                if value is not None:
                                    lineEdit = self.constant_values_lumped_dampings[i]
                                    lineEdit.setText(f"{value : .3e}")

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        for i, w in enumerate([100, 150]):
            self.treeWidget_masses.setColumnWidth(i, w)
            self.treeWidget_springs.setColumnWidth(i, w)
            self.treeWidget_dampers.setColumnWidth(i, w)
            self.treeWidget_masses.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_springs.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_dampers.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_lists_of_lineEdits(self):

        self.constant_values_lumped_masses = [  self.lineEdit_Mx,
                                                self.lineEdit_My,
                                                self.lineEdit_Mz,
                                                self.lineEdit_Jx,
                                                self.lineEdit_Jy,
                                                self.lineEdit_Jz  ]

        self.constant_values_lumped_stiffness = [   self.lineEdit_Kx,
                                                    self.lineEdit_Ky,
                                                    self.lineEdit_Kz,
                                                    self.lineEdit_Krx,
                                                    self.lineEdit_Kry,
                                                    self.lineEdit_Krz   ]

        self.constant_values_lumped_dampings = [self.lineEdit_Cx,
                                                self.lineEdit_Cy,
                                                self.lineEdit_Cz,
                                                self.lineEdit_Crx,
                                                self.lineEdit_Cry,
                                                self.lineEdit_Crz]

        self.table_values_lumped_masses = [ self.lineEdit_path_table_Mx,
                                            self.lineEdit_path_table_My,
                                            self.lineEdit_path_table_Mz,
                                            self.lineEdit_path_table_Jx,
                                            self.lineEdit_path_table_Jy,
                                            self.lineEdit_path_table_Jz ]

        self.table_values_lumped_stiffness = [  self.lineEdit_path_table_Kx,
                                                self.lineEdit_path_table_Ky,
                                                self.lineEdit_path_table_Kz,
                                                self.lineEdit_path_table_Krx,
                                                self.lineEdit_path_table_Kry,
                                                self.lineEdit_path_table_Krz  ]

        self.table_values_lumped_dampings = [   self.lineEdit_path_table_Cx,
                                                self.lineEdit_path_table_Cy,
                                                self.lineEdit_path_table_Cz,
                                                self.lineEdit_path_table_Crx,
                                                self.lineEdit_path_table_Cry,
                                                self.lineEdit_path_table_Crz   ]

    def attribute_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return True

        self.remove_conflicting_data(node_ids)

        if self.tabWidget_inputs.currentIndex() == 0:
            self.check_constant_values_inputs(node_ids)

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.check_table_values_inputs(node_ids)

        self.actions_to_finalize()
        # self.close()

    def check_entries(self, lineEdit: QLineEdit, label: str):

        str_value = lineEdit.text()
        if str_value != "":
            try:
                str_value = str_value.replace(",", ".")
                value = float(str_value)
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for {label}."
                PrintMessageInput([window_title_1, title, message])
                return True, None
        else:
            value = 0

        if value == 0:
            return False, None
        else:
            return False, value

    def check_constant_values_lumped_masses(self, node_ids: list):

        stop, Mx = self.check_entries(self.lineEdit_Mx, "Mx")
        if stop:
            return True

        stop, My = self.check_entries(self.lineEdit_My, "My")
        if stop:
            return True
      
        stop, Mz = self.check_entries(self.lineEdit_Mz, "Mz")
        if stop:
            return True
     
        stop, Jx = self.check_entries(self.lineEdit_Jx, "Jx")
        if stop:
            return True
     
        stop, Jy = self.check_entries(self.lineEdit_Jy, "Jy")
        if stop:
            return True
     
        stop, Jz = self.check_entries(self.lineEdit_Jz, "Jz")
        if stop:
            return True

        values = [Mx, My, Mz, Jx, Jy, Jz]
        
        if values.count(None) != 6:

            self.lumped_element_applied = True

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            for node_id in node_ids:

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "values" : values,
                        "real_values" : real_values,
                        "imag_values" : imag_values
                        }

                self.properties._set_nodal_property("lumped_masses", data, node_id)

    def check_constant_values_lumped_stiffness(self, node_ids: list):

        stop, Kx = self.check_entries(self.lineEdit_Kx, "Kx")
        if stop:
            return True

        stop, Ky = self.check_entries(self.lineEdit_Ky, "Ky")
        if stop:
            return True
   
        stop, Kz = self.check_entries(self.lineEdit_Kz, "Kz")
        if stop:
            return True
 
        stop, Krx = self.check_entries(self.lineEdit_Krx, "Krx")
        if stop:
            return True

        stop, Kry = self.check_entries(self.lineEdit_Kry, "Kry")
        if stop:
            return True
 
        stop, Krz = self.check_entries(self.lineEdit_Krz, "Krz")
        if stop:
            return True

        values = [Kx, Ky, Kz, Krx, Kry, Krz]
        
        if values.count(None) != 6:

            self.lumped_element_applied = True

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            for node_id in node_ids:

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "values" : values,
                        "real_values" : real_values,
                        "imag_values" : imag_values
                        }

                self.properties._set_nodal_property("lumped_stiffness", data, node_id)

    def check_constant_values_lumped_dampings(self, node_ids: list):

        stop, Cx = self.check_entries(self.lineEdit_Cx, "Cx")
        if stop:
            return True

        stop, Cy = self.check_entries(self.lineEdit_Cy, "Cy")
        if stop:
            return True

        stop, Cz = self.check_entries(self.lineEdit_Cz, "Cz")
        if stop:
            return True

        stop, Crx = self.check_entries(self.lineEdit_Crx, "Crx")
        if stop:
            return True

        stop, Cry = self.check_entries(self.lineEdit_Cry, "Cry")
        if stop:
            return True

        stop, Crz = self.check_entries(self.lineEdit_Crz, "Crz")
        if stop:
            return True

        values = [Cx, Cy, Cz, Crx, Cry, Crz]

        if values.count(None) != 6:

            self.lumped_element_applied = True

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            for node_id in node_ids:

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "values" : values,
                        "real_values" : real_values,
                        "imag_values" : imag_values
                        }

                self.properties._set_nodal_property("lumped_dampings", data, node_id)

    def check_constant_values_inputs(self, node_ids: list):

        if self.check_constant_values_lumped_masses(node_ids):
            return

        if self.check_constant_values_lumped_stiffness(node_ids):
            return

        if self.check_constant_values_lumped_dampings(node_ids):
            return
            
        if not self.lumped_element_applied:
            title = "Additional inputs required"
            message = "You must inform at least one external element\n"
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message]) 
            return

        self.actions_to_finalize()

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                path_imported_table = lineEdit.text()

            else:

                last_path = app().main_window.config.get_last_folder_for("imported table folder")
                if last_path is None:
                    last_path = str(Path().home())

                caption = f"Choose a table to import the {dof_label} nodal load"
                path_imported_table, check = app().main_window.file_dialog.get_open_file_name(
                                                                                                caption, 
                                                                                                last_path, 
                                                                                                'Table File (*.csv; *.dat; *.txt)'
                                                                                              )

                if not check:
                    return None, None

            if path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(path_imported_table)
            lineEdit.setText(path_imported_table)         
            imported_file = np.loadtxt(path_imported_table, delimiter=",")
        
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([window_title_1, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:,1] + 1j*imported_file[:,2]

            self.frequencies = imported_file[:,0]
            f_min = self.frequencies[0]
            f_max = self.frequencies[-1]
            f_step = self.frequencies[1] - self.frequencies[0] 
            
            app().main_window.config.write_last_folder_path_in_file("imported table folder", path_imported_table)

            if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

                self.lineEdit_reset(lineEdit)

                title = "Project frequency setup cannot be modified"
                message = f"The following imported table of values has a frequency setup\n"
                message += "different from the others already imported ones. The current\n"
                message += "project frequency setup is not going to be modified."
                message += f"\n\n{imported_filename}"
                PrintMessageInput([window_title_1, title, message])
                return None, None

            else:

                frequency_setup = { "f_min" : f_min,
                                    "f_max" : f_max,
                                    "f_step" : f_step }

                app().project.model.set_frequency_setup(frequency_setup)
            
            return imported_values, path_imported_table

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def load_Mx_table(self):
        self.Mx_table_values, self.Mx_table_path = self.load_table(self.lineEdit_path_table_Mx, "Mx")
        if (self.Mx_table_values, self.Mx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Mx)

    def load_My_table(self):
        self.My_table_values, self.My_table_path = self.load_table(self.lineEdit_path_table_My, "My")
        if (self.My_table_values, self.My_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_My)

    def load_Mz_table(self):
        self.Mz_table_values, self.Mz_table_path = self.load_table(self.lineEdit_path_table_Mz, "Mz")
        if (self.Mz_table_values, self.Mz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Mz)
    
    def load_Jx_table(self):
        self.Jx_table_values, self.Jx_table_path = self.load_table(self.lineEdit_path_table_Jx, "Jx")
        if (self.Jx_table_values, self.Jx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Jx)

    def load_Jy_table(self):
        self.Jy_table_values, self.Jy_table_path = self.load_table(self.lineEdit_path_table_Jy, "Jy")
        if (self.Jy_table_values, self.Jy_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Jy)

    def load_Jz_table(self):
        self.Jz_table_values, self.Jz_table_path = self.load_table(self.lineEdit_path_table_Jz, "Jz")
        if (self.Jz_table_values, self.Jz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Jz)

    def load_Kx_table(self):
        self.Kx_table_values, self.Kx_table_path = self.load_table(self.lineEdit_path_table_Kx, "Kx")
        if (self.Kx_table_values, self.Kx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Kx)

    def load_Ky_table(self):
        self.Ky_table_values, self.Ky_table_path = self.load_table(self.lineEdit_path_table_Ky, "Ky")
        if (self.Ky_table_values, self.Ky_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Ky)

    def load_Kz_table(self):
        self.Kz_table_values, self.Kz_table_path = self.load_table(self.lineEdit_path_table_Kz, "Kz")
        if (self.Kz_table_values, self.Kz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Kz)

    def load_Krx_table(self):
        self.Krx_table_values, self.Krx_table_path = self.load_table(self.lineEdit_path_table_Krx, "Krx")
        if (self.Krx_table_values, self.Krx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Krx)

    def load_Kry_table(self):
        self.Kry_table_values, self.Kry_table_path = self.load_table(self.lineEdit_path_table_Kry, "Kry")
        if (self.Kry_table_values, self.Kry_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Kry)

    def load_Krz_table(self):
        self.Krz_table_values, self.Krz_table_path = self.load_table(self.lineEdit_path_table_Krz, "Krz")
        if (self.Krz_table_values, self.Krz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Krz)

    def load_Cx_table(self):
        self.Cx_table_values, self.Cx_table_path = self.load_table(self.lineEdit_path_table_Cx, "Cx")
        if (self.Cx_table_values, self.Cx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Cx)

    def load_Cy_table(self):
        self.Cy_table_values, self.Cy_table_path = self.load_table(self.lineEdit_path_table_Cy, "Cy")
        if (self.Cy_table_values, self.Cy_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Cy)

    def load_Cz_table(self):
        self.Cz_table_values, self.Cz_table_path = self.load_table(self.lineEdit_path_table_Cz, "Cz")
        if (self.Cz_table_values, self.Cz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Cz)

    def load_Crx_table(self):
        self.Crx_table_values, self.Crx_table_path = self.load_table(self.lineEdit_path_table_Crx, "Crx")
        if (self.Crx_table_values, self.Crx_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Crx)

    def load_Cry_table(self):
        self.Cry_table_values, self.Cry_table_path = self.load_table(self.lineEdit_path_table_Cry, "Cry")
        if (self.Cry_table_values, self.Cry_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Cry)

    def load_Crz_table(self):
        self.Crz_table_values, self.Crz_table_path = self.load_table(self.lineEdit_path_table_Crz, "Crz")
        if (self.Crz_table_values, self.Crz_table_path).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Crz)

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_tables_files(self, lumped_label: str, _label: str, node_id: int, values: np.ndarray):

        table_name = f"{lumped_label}_{_label}_node_{node_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def check_table_values_lumped_masses(self, node_ids: list):

        if self.Mx_table_path is None:
            self.Mx_table_values, self.Mx_table_path = self.load_table(self.lineEdit_path_table_Mx, "Mx", direct_load=True)

        if self.My_table_path is None:
            self.My_table_values, self.My_table_path = self.load_table(self.lineEdit_path_table_My, "My", direct_load=True)

        if self.Mz_table_path is None:
            self.Mz_table_values, self.Mz_table_path = self.load_table(self.lineEdit_path_table_Mz, "Mz", direct_load=True)

        if self.Jx_table_path is None:
            self.Jx_table_values, self.Jx_table_path = self.load_table(self.lineEdit_path_table_Jx, "Jx", direct_load=True)

        if self.Jy_table_path is None:
            self.Jy_table_values, self.Jy_table_path = self.load_table(self.lineEdit_path_table_Jy, "Jy", direct_load=True)

        if self.Jz_table_path is None:
            self.Jz_table_values, self.Jz_table_path = self.load_table(self.lineEdit_path_table_Jz, "Jz", direct_load=True)

        for node_id in node_ids:

            if self.Mx_table_name is not None:
                self.Mx_table_name, self.Mx_array = self.save_tables_files("Mx", node_id, self.Mx_table_values)

            if self.My_table_name is not None:
                self.My_table_name, self.My_array = self.save_tables_files("My", node_id, self.My_table_values)

            if self.My_table_name is not None:
                self.My_table_name, self.My_array = self.save_tables_files("My", node_id, self.My_table_values)

            if self.Jx_table_name is not None:
                self.Jx_table_name, self.Jx_array = self.save_tables_files("Jx", node_id, self.Jx_table_values)

            if self.Jy_table_name is not None:
                self.Jy_table_name, self.Jy_array = self.save_tables_files("Jy", node_id, self.Jy_table_values)

            if self.Jz_table_name is not None:
                self.Jz_table_name, self.Jz_array = self.save_tables_files("Jz", node_id, self.Jz_table_values)

            table_names = [ self.Mx_table_name, self.My_table_name, self.Mz_table_name, 
                            self.Jx_table_name, self.Jy_table_name, self.Jz_table_name  ]

            table_paths = [ self.Mx_table_path, self.My_table_path, self.Mz_table_path, 
                            self.Jx_table_path, self.Jy_table_path, self.Jz_table_path ]

            values = [  self.Mx_table_values, self.My_table_values, self.Mz_table_values, 
                        self.Jx_table_values, self.Jy_table_values, self.Jz_table_values  ]

            if (table_names).count(None) != 6:
                
                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                _data = {
                        "coords" : list(coords),
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        "values" : values
                        }

                self.properties._set_nodal_property("lumped_masses", _data, node_id)

    def check_table_values_lumped_stiffness(self, node_ids: list):

        if self.Kx_table_path is None:
            self.Kx_table_values, self.Kx_table_path = self.load_table(self.lineEdit_path_table_Kx, "Kx", direct_load=True)

        if self.Ky_table_path is None:
            self.Ky_table_values, self.Ky_table_path = self.load_table(self.lineEdit_path_table_Ky, "Ky", direct_load=True)

        if self.Kz_table_path is None:
            self.Kz_table_values, self.Kz_table_path = self.load_table(self.lineEdit_path_table_Kz, "Kz", direct_load=True)

        if self.Krx_table_path is None:
            self.Krx_table_values, self.Krx_table_path = self.load_table(self.lineEdit_path_table_Krx, "Krx", direct_load=True)

        if self.Kry_table_path is None:
            self.Kry_table_values, self.Kry_table_path = self.load_table(self.lineEdit_path_table_Kry, "Kry", direct_load=True)

        if self.Krz_table_path is None:
            self.Krz_table_values, self.Krz_table_path = self.load_table(self.lineEdit_path_table_Krz, "Krz", direct_load=True)

        for node_id in node_ids:

            if self.Kx_table_name is not None:
                self.Kx_table_name, self.Kx_array = self.save_tables_files("Kx", node_id, self.Kx_table_values)

            if self.Ky_table_name is not None:
                self.Ky_table_name, self.Ky_array = self.save_tables_files("Ky", node_id, self.Ky_table_values)

            if self.Ky_table_name is not None:
                self.Ky_table_name, self.Ky_array = self.save_tables_files("Ky", node_id, self.Ky_table_values)

            if self.Krx_table_name is not None:
                self.Krx_table_name, self.Krx_array = self.save_tables_files("Krx", node_id, self.Krx_table_values)

            if self.Kry_table_name is not None:
                self.Kry_table_name, self.Kry_array = self.save_tables_files("Kry", node_id, self.Kry_table_values)

            if self.Krz_table_name is not None:
                self.Krz_table_name, self.Krz_array = self.save_tables_files("Krz", node_id, self.Krz_table_values)

            table_names = [ self.Kx_table_name, self.Ky_table_name, self.Kz_table_name, 
                            self.Krx_table_name, self.Kry_table_name, self.Krz_table_name  ]

            table_paths = [ self.Kx_table_path, self.Ky_table_path, self.Kz_table_path, 
                            self.Krx_table_path, self.Kry_table_path, self.Krz_table_path ]

            values = [  self.Kx_table_values, self.Ky_table_values, self.Kz_table_values, 
                        self.Krx_table_values, self.Kry_table_values, self.Krz_table_values  ]
            
            if (table_names).count(None) != 6:
                
                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        "values" : values
                        }

                self.properties._set_nodal_property("lumped_stiffness", data, node_id)

    def check_table_values_lumped_dampings(self, node_ids: list):


        if self.Cx_table_path is None:
            self.Cx_table_values, self.Cx_table_path = self.load_table(self.lineEdit_path_table_Cx, "Cx", direct_load=True)

        if self.Cy_table_path is None:
            self.Cy_table_values, self.Cy_table_path = self.load_table(self.lineEdit_path_table_Cy, "Cy", direct_load=True)

        if self.Cz_table_path is None:
            self.Cz_table_values, self.Cz_table_path = self.load_table(self.lineEdit_path_table_Cz, "Cz", direct_load=True)

        if self.Crx_table_path is None:
            self.Crx_table_values, self.Crx_table_path = self.load_table(self.lineEdit_path_table_Crx, "Crx", direct_load=True)

        if self.Cry_table_path is None:
            self.Cry_table_values, self.Cry_table_path = self.load_table(self.lineEdit_path_table_Cry, "Cry", direct_load=True)

        if self.Crz_table_path is None:
            self.Crz_table_values, self.Crz_table_path = self.load_table(self.lineEdit_path_table_Crz, "Crz", direct_load=True)

        for node_id in node_ids:

            if self.Cx_table_name is not None:
                self.Cx_table_name, self.Cx_array = self.save_tables_files("Cx", node_id, self.Cx_table_values)

            if self.Cy_table_name is not None:
                self.Cy_table_name, self.Cy_array = self.save_tables_files("Cy", node_id, self.Cy_table_values)

            if self.Cy_table_name is not None:
                self.Cy_table_name, self.Cy_array = self.save_tables_files("Cy", node_id, self.Cy_table_values)

            if self.Crx_table_name is not None:
                self.Crx_table_name, self.Crx_array = self.save_tables_files("Crx", node_id, self.Crx_table_values)

            if self.Cry_table_name is not None:
                self.Cry_table_name, self.Cry_array = self.save_tables_files("Cry", node_id, self.Cry_table_values)

            if self.Crz_table_name is not None:
                self.Crz_table_name, self.Crz_array = self.save_tables_files("Crz", node_id, self.Crz_table_values)

            table_names = [ self.Cx_table_name, self.Cy_table_name, self.Cz_table_name, 
                            self.Crx_table_name, self.Cry_table_name, self.Crz_table_name  ]

            table_paths = [ self.Cx_table_path, self.Cy_table_path, self.Cz_table_path, 
                            self.Crx_table_path, self.Cry_table_path, self.Crz_table_path ]

            values = [  self.Cx_table_values, self.Cy_table_values, self.Cz_table_values, 
                        self.Crx_table_values, self.Cry_table_values, self.Crz_table_values  ]

            if (table_names).count(None) != 6:
                
                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        "values" : values
                        }

                self.properties._set_nodal_property("lumped_dampings", data, node_id)

    def check_table_values_inputs(self, node_ids: list):

        if self.check_table_values_lumped_masses(node_ids):
            return

        if self.check_table_values_lumped_stiffness(node_ids):
            return

        if self.check_table_values_lumped_dampings(node_ids):
            return

        if not self.lumped_element_applied:
            title = "Additional inputs required"
            message = "You must inform at least one external element\n" 
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message]) 
            return

        self.actions_to_finalize()

    def remove_conflicting_data(self, node_ids: int | list | tuple, selected_property = None):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if selected_property is None:
            properties = ["lumped_masses", "lumped_stiffness", "lumped_dampings"]

        elif isinstance(selected_property, str):
            properties = [selected_property]

        for node_id in node_ids:
            for _property in properties:
                table_names = self.properties.get_nodal_related_table_names(_property, node_id)
                self.properties._remove_nodal_property(_property, node_id)
                self.process_table_file_removal(table_names)

        app().pulse_file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        for _property in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:
            table_names = self.properties.get_nodal_related_table_names(_property, node_ids)
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_callback(self):

        if self.lineEdit_node_ids.text() != "":

            node_id = int(self.lineEdit_node_ids.text())

            if self.checkBox_remove_mass.isChecked():
                self.properties._remove_nodal_property("lumped_masses", node_ids=node_id)
                self.remove_conflicting_data(node_id, selected_property="lumped_masses")

            if self.checkBox_remove_spring.isChecked():
                self.properties._remove_nodal_property("lumped_stiffness", node_ids=node_id)
                self.remove_conflicting_data(node_id, selected_property="lumped_stiffness")

            if self.checkBox_remove_damper.isChecked():
                self.properties._remove_nodal_property("lumped_dampings", node_ids=node_id)
                self.remove_conflicting_data(node_id, selected_property="lumped_dampings")

        self.actions_to_finalize()

    def reset_callback(self):
        
        self.hide()

        title = "Resetting of lumped elements"
        message = "Would you like to remove all lumped elements from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            
            node_ids = list()
            for (_property, *args) in self.properties.nodal_properties.keys():
                if _property in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:
                    node_ids.append(args[0])

            for node_id in node_ids:
                if self.checkBox_remove_mass.isChecked():
                    self.properties._remove_nodal_property("lumped_masses", node_id)
                    self.remove_conflicting_data(node_id, selected_property="lumped_masses")

                if self.checkBox_remove_spring.isChecked():
                    self.properties._remove_nodal_property("lumped_stiffness", node_id)
                    self.remove_conflicting_data(node_id, selected_property="lumped_stiffness")

                if self.checkBox_remove_damper.isChecked():
                    self.properties._remove_nodal_property("lumped_dampings", node_id)
                    self.remove_conflicting_data(node_id, selected_property="lumped_dampings")

            self.actions_to_finalize()
    
    def update_tabs_visibility(self):
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)
        for (_property, *args) in self.properties.nodal_properties.keys():
            if _property in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:
                self.tabWidget_main.setTabVisible(1, True)
                return

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)

        else:
            if self.cache_tab == 1:
                self.lineEdit_node_ids.setText("")
            self.selection_frame.setDisabled(False)
            self.selection_callback()

        self.cache_tab = self.tabWidget_main.currentIndex()

    def actions_to_finalize(self):
        app().pulse_file.write_nodal_properties_in_file()
        app().main_window.update_plots(reset_camera=False)
        self.load_nodes_info()

    def text_label(self, mask, load_labels):
        
        text = ""
        labels = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)
        return text

    def load_nodes_info(self):

        self.treeWidget_masses.clear()
        self.treeWidget_springs.clear()
        self.treeWidget_dampers.clear()

        m_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
        k_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])
        c_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])

        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "lumped_stiffness":

                node_id = args[0]
                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(k_mask, k_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_springs.addTopLevelItem(item)

            if property == "lumped_dampings":

                node_id = args[0]
                c_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(c_mask, c_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_dampers.addTopLevelItem(item)

            if property == "lumped_masses":

                node_id = args[0]
                m_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(m_mask, m_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_masses.addTopLevelItem(item)

        self.update_tabs_visibility()

    def on_click_item_masses(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_masses(self, item):
        self.on_click_item_masses(item)

    def on_click_item_springs(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_springs(self, item):
        self.on_click_item_springs(item)

    def on_click_item_dampings(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_dampings(self, item):
        self.on_click_item_dampings(item)

    def reset_input_fields_masses(self):
        for lineEdit_constant_masses in self.constant_values_lumped_masses:    
            lineEdit_constant_masses.setText("")
        for lineEdit_table_masses in self.table_values_lumped_masses:
            lineEdit_table_masses.setText("")

    def reset_input_fields_stiffness(self):
        for lineEdit_constant_stiffness in self.constant_values_lumped_stiffness:    
            lineEdit_constant_stiffness.setText("")
        for lineEdit_table_stiffness in self.table_values_lumped_stiffness:
            lineEdit_table_stiffness.setText("")

    def reset_input_fields_dampings(self):
        for lineEdit_constant_dampings in self.constant_values_lumped_dampings:    
            lineEdit_constant_dampings.setText("")
        for lineEdit_table_dampings in self.table_values_lumped_dampings:
            lineEdit_table_dampings.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)