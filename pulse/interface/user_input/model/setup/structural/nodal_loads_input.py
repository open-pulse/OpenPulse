#fmt: off

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np
from pathlib import Path

window_title = "Error"

class NodalLoadsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/set_nodal_loads_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

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

        self.list_Nones = [None, None, None, None, None, None]
        self.load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])

        self.reset_table_variables()
        self.before_run = app().project.get_pre_solution_model_checks()

    def reset_table_variables(self):

        self.fx_table_values = None
        self.fy_table_values = None
        self.fz_table_values = None
        self.mx_table_values = None
        self.my_table_values = None
        self.mz_table_values = None

        self.fx_array = None
        self.fy_array = None
        self.fz_array = None
        self.mx_array = None
        self.my_array = None
        self.mz_array = None

        self.fx_table_path = None
        self.fy_table_path = None
        self.fz_table_path = None
        self.mx_table_path = None
        self.my_table_path = None
        self.mz_table_path = None

        self.fx_table_name = None
        self.fy_table_name = None
        self.fz_table_name = None
        self.mx_table_name = None
        self.my_table_name = None
        self.mz_table_name = None

    def _define_qt_variables(self):

        # QLineEdit   
        self.lineEdit_node_ids: QLineEdit
        self.lineEdit_real_fx: QLineEdit
        self.lineEdit_real_fy: QLineEdit
        self.lineEdit_real_fz: QLineEdit
        self.lineEdit_real_mx: QLineEdit
        self.lineEdit_real_my: QLineEdit
        self.lineEdit_real_mz: QLineEdit
        self.lineEdit_imag_fx: QLineEdit
        self.lineEdit_imag_fy: QLineEdit
        self.lineEdit_imag_fz: QLineEdit
        self.lineEdit_imag_mx: QLineEdit
        self.lineEdit_imag_my: QLineEdit
        self.lineEdit_imag_mz: QLineEdit
        #
        self.lineEdit_path_table_fx: QLineEdit
        self.lineEdit_path_table_fy: QLineEdit
        self.lineEdit_path_table_fz: QLineEdit
        self.lineEdit_path_table_mx: QLineEdit
        self.lineEdit_path_table_my: QLineEdit
        self.lineEdit_path_table_mz: QLineEdit
        self._create_list_lineEdits()

        # QPushButton
        self.pushButton_cancel_tab0: QPushButton
        self.pushButton_cancel_tab1: QPushButton
        self.pushButton_load_fx_table: QPushButton
        self.pushButton_load_fy_table: QPushButton
        self.pushButton_load_fz_table: QPushButton
        self.pushButton_load_mx_table: QPushButton
        self.pushButton_load_my_table: QPushButton
        self.pushButton_load_mz_table: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_constant_value_confirm: QPushButton
        self.pushButton_table_values_confirm: QPushButton

        # QTabWidget
        self.tabWidget_nodal_loads: QTabWidget

        # QTreeWidget
        self.treeWidget_nodal_info: QTreeWidget

    def _create_list_lineEdits(self):

        self.list_lineEdit_constant_values = [  [self.lineEdit_real_fx, self.lineEdit_imag_fx],
                                                [self.lineEdit_real_fy, self.lineEdit_imag_fy],
                                                [self.lineEdit_real_fz, self.lineEdit_imag_fz],
                                                [self.lineEdit_real_mx, self.lineEdit_imag_mx],
                                                [self.lineEdit_real_my, self.lineEdit_imag_my],
                                                [self.lineEdit_real_mz, self.lineEdit_imag_mz]  ]

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_fx,
                                            self.lineEdit_path_table_fy,
                                            self.lineEdit_path_table_fz,
                                            self.lineEdit_path_table_mx,
                                            self.lineEdit_path_table_my,
                                            self.lineEdit_path_table_mz ]

    def _create_connections(self):
        #
        self.pushButton_cancel_tab0.clicked.connect(self.close)
        self.pushButton_cancel_tab1.clicked.connect(self.close)
        self.pushButton_constant_value_confirm.clicked.connect(self.constant_values_attribution_callback)
        self.pushButton_load_fx_table.clicked.connect(self.load_fx_table)
        self.pushButton_load_fy_table.clicked.connect(self.load_fy_table)
        self.pushButton_load_fz_table.clicked.connect(self.load_fz_table)
        self.pushButton_load_mx_table.clicked.connect(self.load_mx_table)
        self.pushButton_load_my_table.clicked.connect(self.load_my_table)
        self.pushButton_load_mz_table.clicked.connect(self.load_mz_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_table_values_confirm.clicked.connect(self.table_values_attribution_callback)
        #
        self.tabWidget_nodal_loads.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) == 1:
                for (property, *args), data in self.properties.nodal_properties.items():
                    if property == "nodal_loads" and selected_nodes == args:

                        values = data["values"]
        
                        if "table_paths" in data.keys():
                            table_paths = data["table_paths"]
                            for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                                table_path = table_paths[index]
                                if table_path is not None:                   
                                    lineEdit_table.setText(table_path)

                        else:
                            for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                                if values[index] is not None:
                                    lineEdit_real.setText(str(np.real(values[index])))
                                    lineEdit_imag.setText(str(np.imag(values[index])))

    def _config_widgets(self):
        for i, w in enumerate([80, 60]):
            self.treeWidget_nodal_info.setColumnWidth(i, w)
            self.treeWidget_nodal_info.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title, title, message])
                stop = True
                return stop, None
        else:
            _real = 0

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title, title, message])
                stop = True
                return stop, None
        else:
            _imag = 0
        
        if _real == 0 and _imag == 0:
            return stop, None
        else:
            return stop, _real + 1j*_imag

    def constant_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        stop, Fx = self.check_complex_entries(self.lineEdit_real_fx, self.lineEdit_imag_fx, "Fx")
        if stop:
            return

        stop, Fy = self.check_complex_entries(self.lineEdit_real_fy, self.lineEdit_imag_fy, "Fy")
        if stop:
            return
 
        stop, Fz = self.check_complex_entries(self.lineEdit_real_fz, self.lineEdit_imag_fz, "Fz")
        if stop:
            return

        stop, Mx = self.check_complex_entries(self.lineEdit_real_mx, self.lineEdit_imag_mx, "Mx")
        if stop:
            return

        stop, My = self.check_complex_entries(self.lineEdit_real_my, self.lineEdit_imag_my, "My")
        if stop:
            return

        stop, Mz = self.check_complex_entries(self.lineEdit_real_mz, self.lineEdit_imag_mz, "Mz")
        if stop:
            return

        nodal_loads = [Fx, Fy, Fz, Mx, My, Mz]
        
        if nodal_loads.count(None) != 6:

            self.remove_conflicting_excitations(node_ids)

            real_values = [value if value is None else np.real(value) for value in nodal_loads]
            imag_values = [value if value is None else np.imag(value) for value in nodal_loads]

            for node_id in node_ids:

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "values" : nodal_loads,
                        "real_values" : real_values,
                        "imag_values" : imag_values
                        }

                self.properties._set_nodal_property("nodal_loads", data, node_id)

            self.actions_to_finalize()
            # self.close()

            print(f"[Set Nodal loads] - defined at node(s) {node_ids}")

        else:    
    
            title = "Additional inputs required"
            message = "You must to inform at least one nodal load " 
            message += "before confirming the input!"
            PrintMessageInput([window_title, title, message]) 
            
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
                PrintMessageInput([window_title, title, message])
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
                PrintMessageInput([window_title, title, message])
                return None, None

            else:

                frequency_setup = { "f_min" : f_min,
                                    "f_max" : f_max,
                                    "f_step" : f_step }

                app().project.model.set_frequency_setup(frequency_setup)
            
            return imported_values, path_imported_table

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title, title, message])
            lineEdit.setFocus()
            return None, None

    def load_fx_table(self):
        self.fx_table_values, self.fx_table_path = self.load_table(self.lineEdit_path_table_fx, "Fx")
        if self.fx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_fx)

    def load_fy_table(self):
        self.fy_table_values, self.fy_table_path = self.load_table(self.lineEdit_path_table_fy, "Fy")
        if self.fy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_fy)

    def load_fz_table(self):
        self.fz_table_values, self.fz_table_path = self.load_table(self.lineEdit_path_table_fz, "Fz")
        if self.fz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_fz)

    def load_mx_table(self):
        self.mx_table_values, self.mx_table_path = self.load_table(self.lineEdit_path_table_mx, "Mx")
        if self.mx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_mx)

    def load_my_table(self):
        self.my_table_values, self.my_table_path = self.load_table(self.lineEdit_path_table_my, "My")
        if self.my_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_my)

    def load_mz_table(self):
        self.mz_table_values, self.mz_table_path = self.load_table(self.lineEdit_path_table_mz, "Mz")
        if self.mz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_mz)

    def lineEdit_reset(self, lineEdit : QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus() 

    def save_tables_files(self, load_label: str, node_id: int, values: np.ndarray):

        table_name = f"nodal_load_{load_label}_node_{node_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        self.remove_conflicting_excitations(node_ids)

        if self.fx_table_path is None:
            self.fx_table_values, self.fx_table_path = self.load_table(self.lineEdit_path_table_fx, "Fx", direct_load=True)

        if self.fy_table_path is None:
            self.fy_table_values, self.fy_table_path = self.load_table(self.lineEdit_path_table_fy, "Fy", direct_load=True)

        if self.fz_table_path is None:
            self.fz_table_values, self.fz_table_path = self.load_table(self.lineEdit_path_table_fz, "Fz", direct_load=True)           

        if self.mx_table_path is None:
            self.mx_table_values, self.mx_table_path = self.load_table(self.lineEdit_path_table_mx, "Mx", direct_load=True)            

        if self.my_table_path is None:
            self.my_table_values, self.my_table_path = self.load_table(self.lineEdit_path_table_my, "My", direct_load=True)             

        if self.mz_table_path is None:
            self.mz_table_values, self.mz_table_path = self.load_table(self.lineEdit_path_table_mz, "Mz", direct_load=True)              

        for node_id in node_ids:

            if self.fx_table_path is not None:
                self.fx_table_name, self.fx_array = self.save_tables_files("Fx", node_id, self.fx_table_values)

            if self.fy_table_path is not None:
                self.fy_table_name, self.fy_array = self.save_tables_files("Fy", node_id, self.fy_table_values)

            if self.fz_table_path is not None:
                self.fz_table_name, self.fz_array = self.save_tables_files("Fz", node_id, self.fz_table_values)

            if self.mx_table_path is not None:
                self.mx_table_name, self.mx_array = self.save_tables_files("Mx", node_id, self.mx_table_values)

            if self.my_table_path is not None:
                self.my_table_name, self.my_array = self.save_tables_files("My", node_id, self.my_table_values)

            if self.mz_table_path is not None:
                self.mz_table_name, self.mz_array = self.save_tables_files("Mz", node_id, self.mz_table_values)

            table_names = [   self.fx_table_name, self.fy_table_name, self.fz_table_name, 
                            self.mx_table_name, self.my_table_name, self.mz_table_name  ]

            table_paths = [ self.fx_table_path, self.fy_table_path, self.fz_table_path, 
                            self.mx_table_path, self.my_table_path, self.mz_table_path ]

            nodal_loads = [ self.fx_table_values, self.fy_table_values, self.fz_table_values, 
                            self.mx_table_values, self.my_table_values, self.mz_table_values ]

            if (table_names).count(None) == 6:
                title = "Additional inputs required"
                message = "You must inform at least one nodal load "
                message += "table path before confirming the input!"
                PrintMessageInput([window_title, title, message]) 
                return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                    "coords" : list(coords),
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    "values" : nodal_loads
                    }

            self.properties._set_nodal_property("nodal_loads", data, node_id)

        app().pulse_file.write_nodal_properties_in_file()

        self.actions_to_finalize()
        # self.close()

        print(f"[Set Nodal loads] - defined at node(s) {node_ids}")

    def text_label(self, mask):

        text = ""
        labels = self.load_labels[mask]

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

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():

            if property == "nodal_loads":
                values = data["values"]
                constrained_dofs_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(args[0]), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.tabWidget_nodal_loads.setTabVisible(2, False)
        for (property, *_) in self.properties.nodal_properties.keys():
            if property == "nodal_loads":
                self.tabWidget_nodal_loads.setCurrentIndex(0)
                self.tabWidget_nodal_loads.setTabVisible(2, True)
                return

    def tab_event_callback(self):

        self.lineEdit_node_ids.setText("")
        self.pushButton_remove.setDisabled(True)

        if self.tabWidget_nodal_loads.currentIndex() == 2:
            self.lineEdit_node_ids.setDisabled(True)
            items = self.treeWidget_nodal_info.selectedItems()
            if items == list():
                self.lineEdit_node_ids.setText("")
            else:
                self.on_click_item(items[0])

        else:
            self.lineEdit_node_ids.setEnabled(True)
            self.selection_callback()

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_double_click_item(self, item):
        # self.on_click_item(item)
        self.lineEdit_node_ids.setText(item.text(0))
        self.get_nodal_info(item)

    def get_nodal_info(self, item):
        try:

            loads_info = dict()
            selected_node = int(item.text(0))

            for (property, *args), data in self.properties.nodal_properties.items():
                if property == "nodal_loads" and selected_node == args[0]:

                    values = data["values"]
                    nodal_loads_mask = [False if bc is None else True for bc in values]

                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.load_labels[i]
                            loads_info[selected_node, dof_label] = values[i]

            if len(loads_info):

                self.hide()
                header_labels = ["Node ID", "DOF label", "Value"]
                GetInformationOfGroup(  group_label = "Nodal loads",
                                        selection_label = "Node ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
                                        data = data  )

        except Exception as error_log:
            title = "Error while gathering nodal loads information"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return

        self.show()

    def remove_conflicting_excitations(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["prescribed_dofs"]:
                table_names = self.properties.get_nodal_related_table_names(label, node_id)
                self.properties._remove_nodal_property(label, node_id)

                self.process_table_file_removal(table_names)

        app().pulse_file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("nodal_loads", node_ids)
        self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_callback(self):

        if  self.lineEdit_node_ids.text() != "":

            str_nodes = self.lineEdit_node_ids.text()
            stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            self.remove_table_files_from_nodes(node_ids[0])
            self.properties._remove_nodal_property("nodal_loads", node_ids[0])

            self.actions_to_finalize()
            # self.close()

    def reset_callback(self):

        self.hide()

        title = "Resetting of prescribed dofs"
        message = "Would you like to remove all prescribed dofs from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            
            node_ids = list()
            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "nodal_loads":
                    node_ids.append(args[0])

            for node_id in node_ids:
                self.remove_table_files_from_nodes(node_id)

            self.properties._reset_nodal_property("nodal_loads")

            self.actions_to_finalize()
            # self.close()

    def actions_to_finalize(self):
        app().pulse_file.write_nodal_properties_in_file()
        self.load_nodes_info()
        app().main_window.update_plots(reset_camera=False)

    def reset_input_fields(self):
        self.lineEdit_node_ids.setText("")
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")
        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_nodal_loads.currentIndex() == 0:
                self.constant_values_attribution_callback()
            elif self.tabWidget_nodal_loads.currentIndex() == 1:
                self.table_values_attribution_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

#fmt: on