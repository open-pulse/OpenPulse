from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.mass_spring_damper_input_ui import MassSpringDamperInput_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.common import get_spectral_data_from_array, get_table_name, update_analysis_setup_in_file


import os
import numpy as np
from pathlib import Path


error_title ="Error"


class MassSpringDamperInput(MassSpringDamperInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.keep_window_open = True
        self.lumped_element_applied = False

        self.reset_table_variables()

    def reset_table_variables(self):

        self.imported_Mx_values = None
        self.imported_My_values = None
        self.imported_Mz_values = None
        self.imported_Jx_values = None
        self.imported_Jy_values = None
        self.imported_Jz_values = None
        
        self.imported_Kx_values = None
        self.imported_Ky_values = None
        self.imported_Kz_values = None
        self.imported_Krx_values = None
        self.imported_Kry_values = None
        self.imported_Krz_values = None

        self.imported_Cx_values = None
        self.imported_Cy_values = None
        self.imported_Cz_values = None
        self.imported_Crx_values = None
        self.imported_Cry_values = None
        self.imported_Crz_values = None

        self.Mx_table_path = None
        self.My_table_path = None
        self.Mz_table_path = None
        self.Jx_table_path = None
        self.Jy_table_path = None
        self.Jz_table_path = None

        self.Kx_table_path = None
        self.Ky_table_path = None
        self.Kz_table_path = None
        self.Krx_table_path = None
        self.Kry_table_path = None
        self.Krz_table_path = None

        self.Cx_table_path = None
        self.Cy_table_path = None
        self.Cz_table_path = None
        self.Crx_table_path = None
        self.Cry_table_path = None
        self.Crz_table_path = None

    def _define_qt_variables(self):
        self._create_lists_of_lineEdits()

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
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

    def check_entries(self, lineEdit: QLineEdit, label: str):

        str_value = lineEdit.text()
        if str_value != "":
            try:
                str_value = str_value.replace(",", ".")
                value = float(str_value)
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for {label}."
                PrintMessageInput([error_title, title, message])
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
            PrintMessageInput([error_title, title, message]) 
            return

        self.actions_to_finalize()

    def load_table(self, line_edit : QLineEdit, dof_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                path_imported_table = line_edit.text()

            else:

                last_path = app().main_window.config.get_last_folder_for("imported_table_folder")
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

            line_edit.setText(path_imported_table)         
            imported_data = np.loadtxt(path_imported_table, delimiter=",")
        
            if imported_data.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None
            
            app().main_window.config.write_last_folder_path_in_file("imported_table_folder", path_imported_table)

            return imported_data, path_imported_table

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            line_edit.setFocus()
            return None, None

    def load_Mx_table(self):
        self.imported_Mx_values, self.Mx_table_path = self.load_table(self.lineEdit_path_table_Mx, "Mx")
        if self.Mx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Mx)

    def load_My_table(self):
        self.imported_My_values, self.My_table_path = self.load_table(self.lineEdit_path_table_My, "My")
        if self.My_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_My)

    def load_Mz_table(self):
        self.imported_Mz_values, self.Mz_table_path = self.load_table(self.lineEdit_path_table_Mz, "Mz")
        if self.Mz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Mz)

    def load_Jx_table(self):
        self.imported_Jx_values, self.Jx_table_path = self.load_table(self.lineEdit_path_table_Jx, "Jx")
        if self.Jx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Jx)

    def load_Jy_table(self):
        self.imported_Jy_values, self.Jy_table_path = self.load_table(self.lineEdit_path_table_Jy, "Jy")
        if self.Jy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Jy)

    def load_Jz_table(self):
        self.imported_Jz_values, self.Jz_table_path = self.load_table(self.lineEdit_path_table_Jz, "Jz")
        if self.Jz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Jz)

    def load_Kx_table(self):
        self.imported_Kx_values, self.Kx_table_path = self.load_table(self.lineEdit_path_table_Kx, "Kx")
        if self.Kx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Kx)

    def load_Ky_table(self):
        self.imported_Ky_values, self.Ky_table_path = self.load_table(self.lineEdit_path_table_Ky, "Ky")
        if self.Ky_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Ky)

    def load_Kz_table(self):
        self.imported_Kz_values, self.Kz_table_path = self.load_table(self.lineEdit_path_table_Kz, "Kz")
        if self.Kz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Kz)

    def load_Krx_table(self):
        self.imported_Krx_values, self.Krx_table_path = self.load_table(self.lineEdit_path_table_Krx, "Krx")
        if self.Krx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Krx)

    def load_Kry_table(self):
        self.imported_Kry_values, self.Kry_table_path = self.load_table(self.lineEdit_path_table_Kry, "Kry")
        if self.Kry_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Kry)

    def load_Krz_table(self):
        self.imported_Krz_values, self.Krz_table_path = self.load_table(self.lineEdit_path_table_Krz, "Krz")
        if self.Krz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Krz)

    def load_Cx_table(self):
        self.imported_Cx_values, self.Cx_table_path = self.load_table(self.lineEdit_path_table_Cx, "Cx")
        if self.Cx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Cx)

    def load_Cy_table(self):
        self.imported_Cy_values, self.Cy_table_path = self.load_table(self.lineEdit_path_table_Cy, "Cy")
        if self.Cy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Cy)

    def load_Cz_table(self):
        self.imported_Cz_values, self.Cz_table_path = self.load_table(self.lineEdit_path_table_Cz, "Cz")
        if self.Cz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Cz)

    def load_Crx_table(self):
        self.imported_Crx_values, self.Crx_table_path = self.load_table(self.lineEdit_path_table_Crx, "Crx")
        if self.Crx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Crx)

    def load_Cry_table(self):
        self.imported_Cry_values, self.Cry_table_path = self.load_table(self.lineEdit_path_table_Cry, "Cry")
        if self.Cry_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Cry)

    def load_Crz_table(self):
        self.imported_Crz_values, self.Crz_table_path = self.load_table(self.lineEdit_path_table_Crz, "Crz")
        if self.Crz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_Crz)

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(_frequencies)

        # real values vector
        real_values = imported_values[:, 1]
        
        # imaginary values vector
        imag_values = imported_values[:, 2]

        # array to be saved
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False

    def check_table_values_for_lumped_masses(self, node_ids: list):

        values = list()
        table_paths = list()
        lumped_labels = ["Mx", "My", "Mz", "Jx", "Jy", "Jz"]
        
        for label in lumped_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_path_table_{label}")

                _imported_values, _table_path = self.load_table(line_edit, label, direct_load = True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

            _imported_values_attr = getattr(self, imported_values_name)
            values.append(get_spectral_data_from_array(_imported_values_attr))

        for node_id in node_ids:

            table_names = list()

            for label in lumped_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"lumped_{label}", node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) != 6:

                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                _data = {
                    "coords" : list(coords),
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    "values" : values,
                    }

                self.properties._set_nodal_property("lumped_masses", _data, node_id)

    def check_table_values_for_lumped_stiffness(self, node_ids: list):

        values = list()
        table_paths = list()
        lumped_labels = ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]
        
        for label in lumped_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_path_table_{label}")

                _imported_values, _table_path = self.load_table(line_edit, label, direct_load = True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

            _imported_values_attr = getattr(self, imported_values_name)
            values.append(get_spectral_data_from_array(_imported_values_attr))

        for node_id in node_ids:

            table_names = list()

            for label in lumped_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"lumped_{label}", node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

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

    def check_table_values_for_lumped_dampings(self, node_ids: list):

        values = list()
        table_paths = list()
        lumped_labels = ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]

        for label in lumped_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_path_table_{label}")

                _imported_values, _table_path = self.load_table(line_edit, label, direct_load = True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

            _imported_values_attr = getattr(self, imported_values_name)
            values.append(get_spectral_data_from_array(_imported_values_attr))

        for node_id in node_ids:

            table_names = list()

            for label in lumped_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"lumped_{label}", node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

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

        if self.check_table_values_for_lumped_masses(node_ids):
            return

        if self.check_table_values_for_lumped_stiffness(node_ids):
            return

        if self.check_table_values_for_lumped_dampings(node_ids):
            return

        if not self.lumped_element_applied:
            title = "Additional inputs required"
            message = "Choose at least one external element table " 
            message += "file to proceed with model assignment."
            PrintMessageInput([error_title, title, message]) 
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

        app().project.file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        for _property in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:
            table_names = self.properties.get_nodal_related_table_names(_property, node_ids)
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().project.file.write_imported_table_data_in_file()

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
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
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
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)