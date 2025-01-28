from PySide6.QtWidgets import QCheckBox, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QEvent, QObject, Signal

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from molde import load_ui

import os
import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class ElasticNodalLinksInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/elastic_nodal_links_input.ui"
        load_ui(ui_path, self, UI_DIR)

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
        self.link_applied = False
        
        self.reset_table_variables()

    def reset_table_variables(self):

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
        self.checkBox_link_stiffness: QCheckBox
        self.checkBox_link_dampings: QCheckBox

        # QFrame
        self.selection_frame: QFrame

        # QLineEdit
        self.lineEdit_selection: QLineEdit
        self.lineEdit_first_node_id: QLineEdit
        self.lineEdit_last_node_id: QLineEdit

        self.lineEdit_Kx: QLineEdit
        self.lineEdit_Ky: QLineEdit
        self.lineEdit_Kz: QLineEdit
        self.lineEdit_Krx: QLineEdit
        self.lineEdit_Kry: QLineEdit
        self.lineEdit_Krz: QLineEdit

        self.lineEdit_Cx: QLineEdit
        self.lineEdit_Cy: QLineEdit
        self.lineEdit_Cz: QLineEdit
        self.lineEdit_Crx: QLineEdit
        self.lineEdit_Cry: QLineEdit
        self.lineEdit_Crz: QLineEdit

        self.lineEdit_path_table_Kx: QLineEdit
        self.lineEdit_path_table_Ky: QLineEdit
        self.lineEdit_path_table_Kz: QLineEdit
        self.lineEdit_path_table_Krx: QLineEdit
        self.lineEdit_path_table_Kry: QLineEdit
        self.lineEdit_path_table_Krz: QLineEdit

        self._create_lists_of_lineEdits()

        # QPushButton
        self.pushButton_load_Kx_table: QPushButton
        self.pushButton_load_Ky_table: QPushButton
        self.pushButton_load_Kz_table: QPushButton
        self.pushButton_load_Krx_table: QPushButton
        self.pushButton_load_Kry_table: QPushButton
        self.pushButton_load_Krz_table: QPushButton 

        self.lineEdit_path_table_Cx: QLineEdit
        self.lineEdit_path_table_Cy: QLineEdit
        self.lineEdit_path_table_Cz: QLineEdit
        self.lineEdit_path_table_Crx: QLineEdit
        self.lineEdit_path_table_Cry: QLineEdit
        self.lineEdit_path_table_Crz: QLineEdit

        self.pushButton_load_Cx_table: QPushButton
        self.pushButton_load_Cy_table: QPushButton
        self.pushButton_load_Cz_table: QPushButton
        self.pushButton_load_Crx_table: QPushButton
        self.pushButton_load_Cry_table: QPushButton
        self.pushButton_load_Crz_table: QPushButton

        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget
        self.tabWidget_inputs: QTabWidget
        self.tabWidget_remove: QTabWidget
        self.tabWidget_constant_values: QTabWidget
        self.tabWidget_table_values: QTabWidget
        
        # QTreeWidget
        self.treeWidget_structural_stiffness_links: QTreeWidget
        self.treeWidget_structural_damping_links: QTreeWidget

    def _create_lists_of_lineEdits(self):

        self.lineEdits_constant_values_stiffness = [self.lineEdit_Kx,
                                                    self.lineEdit_Ky,
                                                    self.lineEdit_Kz,
                                                    self.lineEdit_Krx,
                                                    self.lineEdit_Kry,
                                                    self.lineEdit_Krz]

        self.lineEdits_constant_values_dampings = [self.lineEdit_Cx,
                                                   self.lineEdit_Cy,
                                                   self.lineEdit_Cz,
                                                   self.lineEdit_Crx,
                                                   self.lineEdit_Cry,
                                                   self.lineEdit_Crz]

        self.lineEdits_table_values_stiffness = [self.lineEdit_path_table_Kx,
                                                 self.lineEdit_path_table_Ky,
                                                 self.lineEdit_path_table_Kz,
                                                 self.lineEdit_path_table_Krx,
                                                 self.lineEdit_path_table_Kry,
                                                 self.lineEdit_path_table_Krz]

        self.lineEdits_table_values_dampings = [self.lineEdit_path_table_Cx,
                                                self.lineEdit_path_table_Cy,
                                                self.lineEdit_path_table_Cz,
                                                self.lineEdit_path_table_Crx,
                                                self.lineEdit_path_table_Cry,
                                                self.lineEdit_path_table_Crz]

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        for i, w in enumerate([120, 200]):
            self.treeWidget_structural_stiffness_links.setColumnWidth(i, w)
            self.treeWidget_structural_damping_links.setColumnWidth(i, w)
            self.treeWidget_structural_stiffness_links.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_structural_damping_links.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_first_node_clicked(self):
        self.current_lineEdit = self.lineEdit_first_node_id

    def lineEdit_last_node_clicked(self):
        self.current_lineEdit = self.lineEdit_last_node_id

    def _create_connections(self):
        #
        self.clickable(self.lineEdit_first_node_id).connect(self.lineEdit_first_node_clicked)
        self.clickable(self.lineEdit_last_node_id).connect(self.lineEdit_last_node_clicked)
        self.current_lineEdit = self.lineEdit_first_node_id
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        self.pushButton_load_Cx_table.clicked.connect(self.load_Cx_table)
        self.pushButton_load_Cy_table.clicked.connect(self.load_Cy_table)
        self.pushButton_load_Cz_table.clicked.connect(self.load_Cz_table)
        self.pushButton_load_Crx_table.clicked.connect(self.load_Crx_table)
        self.pushButton_load_Cry_table.clicked.connect(self.load_Cry_table)
        self.pushButton_load_Crz_table.clicked.connect(self.load_Crz_table)

        self.pushButton_load_Kx_table.clicked.connect(self.load_Kx_table)
        self.pushButton_load_Ky_table.clicked.connect(self.load_Ky_table)
        self.pushButton_load_Kz_table.clicked.connect(self.load_Kz_table)
        self.pushButton_load_Krx_table.clicked.connect(self.load_Krx_table)
        self.pushButton_load_Kry_table.clicked.connect(self.load_Kry_table)
        self.pushButton_load_Krz_table.clicked.connect(self.load_Krz_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_structural_stiffness_links.itemClicked.connect(self.on_click_item_stiffness)
        self.treeWidget_structural_damping_links.itemClicked.connect(self.on_click_item_damping)
        self.treeWidget_structural_stiffness_links.itemDoubleClicked.connect(self.on_double_click_item_stiffness)
        self.treeWidget_structural_damping_links.itemDoubleClicked.connect(self.on_double_click_item_damping)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:

            if len(selected_nodes) == 1:
                self.current_lineEdit.setText(str(selected_nodes[0]))

            elif len(selected_nodes) == 2:
                first_node = min(selected_nodes)
                last_node = max(selected_nodes)
                sorted_nodes = [first_node, last_node]
                self.lineEdit_first_node_id.setText(str(first_node))
                self.lineEdit_last_node_id.setText(str(last_node))

                ss_link_data = self.properties._get_property("structural_stiffness_links", node_ids=sorted_nodes)
                if isinstance(ss_link_data, dict):

                    self.reset_stiffness_input_fields()
                    self.reset_dampings_input_fields()

                    if "table_paths" in ss_link_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in ss_link_data["table_paths"]:
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_stiffness[i]
                                lineEdit.setText(table_path)

                    else:

                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(0)
                        for i, value in enumerate(ss_link_data["real_values"]):
                            if value is not None:
                                lineEdit = self.lineEdits_constant_values_stiffness[i]
                                lineEdit.setText(f"{value : .3e}")

                sd_link_data = self.properties._get_property("structural_damping_links", node_ids=sorted_nodes)
                if isinstance(sd_link_data, dict):

                    if "table_paths" in sd_link_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(1)
                        for i, table_path in enumerate(sd_link_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_dampings[i]
                                lineEdit.setText(table_path)

                    else:

                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(1)
                        for i, value in sd_link_data["real_values"]:
                            if value is not None:
                                lineEdit = self.lineEdits_constant_values_dampings[i]
                                lineEdit.setText(f"{value : .3e}")

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)

        else:
            self.selection_frame.setDisabled(False)

        self.cache_tab = self.tabWidget_main.currentIndex()

    def check_all_nodes(self):

        first_node = self.lineEdit_first_node_id.text()
        stop, node_id = self.before_run.check_selected_ids(first_node, "nodes", single_id=True)
        if stop:
            return True
        temp_node_id1 = node_id
        
        last_node = self.lineEdit_last_node_id.text()
        stop, node_id = self.before_run.check_selected_ids(last_node, "nodes", single_id=True)
        if stop:
            return True           
        temp_node_id2 = node_id

        if temp_node_id1 == temp_node_id2:
            title = "invalid pair of nodes selected"
            message = "The selected nodes must differ. Try to choose another pair of nodes."
            PrintMessageInput([window_title_1, title, message])
            return True

        if temp_node_id2 > temp_node_id1:
            node_id1 = temp_node_id1
            node_id2 = temp_node_id2
        else:
            node_id2 = temp_node_id1
            node_id1 = temp_node_id2

        return False, (node_id1, node_id2)

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

    def check_constant_stiffness_links(self, node_ids: list):

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

            self.link_applied = True

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            coords = list()
            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))

            data = {
                    "coords" : coords,
                    "values" : values,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            self.properties._set_nodal_property("structural_stiffness_links", data, node_ids)

    def check_constant_dampings_links(self, node_ids: list):
        
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

            self.link_applied = True

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            coords = list()
            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))

            data = {
                    "coords" : coords,
                    "values" : values,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            self.properties._set_nodal_property("structural_damping_links", data, node_ids)

    def attribute_callback(self):

        stop, node_ids = self.check_all_nodes()
        if stop:
            return True

        self.remove_conflicting_data(node_ids)

        if self.tabWidget_inputs.currentIndex() == 0:
            self.check_constant_stiffness_links(node_ids)
            self.check_constant_dampings_links(node_ids)

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.check_tables_stiffiness_links(node_ids)
            self.check_tables_dampings_links(node_ids)

        if not self.link_applied:
            title = 'No inputs entered for the structural stiffness or damping links'
            message = "Define at least one value or table of values to the stiffness " 
            message += "or damping links to proceed with the structural link attribution."
            PrintMessageInput([window_title_1, title, message])
            return

        self.reset_nodes_input_fields()
        self.actions_to_finalize()
        # self.close()

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                path_imported_table = lineEdit.text()

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
        
            app().main_window.config.write_last_folder_path_in_file("imported_table_folder", path_imported_table)

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

    def check_tables_stiffiness_links(self, node_ids: list):

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

                self.link_applied = True

                coords = list()
                for node_id in node_ids:
                    node = app().project.model.preprocessor.nodes[node_id]
                    coords.extend(list(np.round(node.coordinates, 5)))

                data = {
                        "coords" : coords,
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        "values" : values
                        }

                self.properties._set_nodal_property("structural_stiffness_links", data, node_ids)

    def check_tables_dampings_links(self, node_ids: list):

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

                self.link_applied = True

                coords = list()
                for node_id in node_ids:
                    node = app().project.model.preprocessor.nodes[node_id]
                    coords.extend(list(np.round(node.coordinates, 5)))

                data = {
                        "coords" : coords,
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        "values" : values
                        }

                self.properties._set_nodal_property("structural_damping_links", data, node_ids)
  
    def actions_to_finalize(self):
        app().pulse_file.write_nodal_properties_in_file()
        app().main_window.update_plots()
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

    def load_elastic_links_stiffness_info(self):

        self.treeWidget_structural_stiffness_links.clear()
        stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "structural_stiffness_links":

                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, stiffness_labels))]
            
                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_structural_stiffness_links.addTopLevelItem(item)

    def load_elastic_links_damping_info(self):

        self.treeWidget_structural_damping_links.clear()
        damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "structural_damping_links":

                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, damping_labels))]
            
                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_structural_damping_links.addTopLevelItem(item)

    def load_nodes_info(self):

        self.load_elastic_links_stiffness_info()
        self.load_elastic_links_damping_info()

        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)

        self.checkBox_link_stiffness.setChecked(True)
        self.checkBox_link_dampings.setChecked(True)

        for (_property, *args) in self.properties.nodal_properties.keys():
            if _property == "structural_stiffness_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(0, True)
                self.checkBox_link_stiffness.setChecked(True)
                break

        for (_property, *args) in self.properties.nodal_properties.keys():
            if _property == "structural_damping_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(1, True)
                self.checkBox_link_dampings.setChecked(True)
                break

    def on_click_item_stiffness(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property("structural_stiffness_links", node_ids=node_ids)
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            # self.lineEdit_first_node_id.setText(str(node_ids[0]))
            # self.lineEdit_last_node_id.setText(str(node_ids[1]))
            self.pushButton_remove.setDisabled(False)

    def on_click_item_damping(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property("structural_damping_links", node_ids=node_ids)
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            # self.lineEdit_first_node_id.setText(str(node_ids[0]))
            # self.lineEdit_last_node_id.setText(str(node_ids[1]))
            self.pushButton_remove.setDisabled(False)

    def on_double_click_item_stiffness(self, item):
        self.on_click_item_stiffness(item)

    def on_double_click_item_damping(self, item):
        self.on_click_item_damping(item)

    def remove_conflicting_data(self, node_ids: int | list | tuple, selected_property = None):

        if selected_property is None:
            properties = ["structural_stiffness_links", "structural_damping_links"]

        elif isinstance(selected_property, str):
            properties = [selected_property]

        for node_id in node_ids:
            for _property in properties:
                table_names = self.properties.get_nodal_related_table_names(_property, node_id)
                self.properties._remove_nodal_property(_property, node_id)
                self.process_table_file_removal(table_names)

        app().pulse_file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        for _property in ["structural_stiffness_links", "structural_damping_links"]:
            table_names = self.properties.get_nodal_related_table_names(_property, node_ids)
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_callback(self):

        _first_node = self.lineEdit_first_node_id.text()
        _last_node = self.lineEdit_last_node_id.text()

        if _first_node != "" and _last_node != "":

            node_id1 = int(_first_node)
            node_id2 = int(_last_node)
            node_ids = [node_id1, node_id2]

            if self.checkBox_link_stiffness.isChecked():
                self.properties._remove_nodal_property("structural_stiffness_links", node_ids=node_ids)
                self.remove_conflicting_data(node_ids, selected_property="structural_stiffness_links")

            if self.checkBox_link_dampings.isChecked():
                self.properties._remove_nodal_property("structural_damping_links", node_ids=node_ids)
                self.remove_conflicting_data(node_ids, selected_property="structural_damping_links")

        self.reset_nodes_input_fields()
        self.reset_stiffness_input_fields()
        self.reset_dampings_input_fields()
        self.actions_to_finalize()

    def reset_callback(self):
        
        self.hide()

        title = "Resetting of structural links"
        message = "Would you like to remove all structural links from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            
            link_nodes = list()
            for (_property, *args) in self.properties.nodal_properties.keys():
                if _property in ["structural_stiffness_links", "structural_damping_links"]:
                    link_nodes.append(args)

            for node_ids in link_nodes:

                if self.checkBox_link_stiffness.isChecked():
                    self.properties._remove_nodal_property("structural_stiffness_links", node_ids=node_ids)
                    self.remove_conflicting_data(node_ids, selected_property="structural_stiffness_links")

                if self.checkBox_link_dampings.isChecked():
                    self.properties._remove_nodal_property("structural_damping_links", node_ids=node_ids)
                    self.remove_conflicting_data(node_ids, selected_property="structural_damping_links")

            self.reset_nodes_input_fields()
            self.reset_stiffness_input_fields()
            self.reset_dampings_input_fields()
            self.actions_to_finalize()

    def reset_nodes_input_fields(self):
        self.lineEdit_first_node_id.setText("")
        self.lineEdit_last_node_id.setText("")

    def reset_stiffness_input_fields(self):
        for lineEdit in self.lineEdits_constant_values_stiffness:    
            lineEdit.setText("")
        for lineEdit in self.lineEdits_table_values_stiffness:
            lineEdit.setText("")

    def reset_dampings_input_fields(self):
        for lineEdit in self.lineEdits_constant_values_dampings:    
            lineEdit.setText("")
        for lineEdit in self.lineEdits_table_values_dampings:
            lineEdit.setText("")
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)