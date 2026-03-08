from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QEvent, QObject, Signal

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.elastic_nodal_links_input_ui import ElasticNodalLinksInput_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.common import get_spectral_data_from_array, get_table_name, update_analysis_setup_in_file


import os
import numpy as np
from pathlib import Path


error_title = "Error"


class ElasticNodalLinksInput(ElasticNodalLinksInput_UI):
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

        self.complete = False
        self.keep_window_open = True
        self.link_applied = False
        
        self.reset_table_variables()

    def reset_table_variables(self):

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

    def _define_qt_variables(self):
        self._create_lists_of_lineEdits()

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
            self.treeWidget_stiffness_nodal_links.setColumnWidth(i, w)
            self.treeWidget_damping_nodal_links.setColumnWidth(i, w)
            self.treeWidget_stiffness_nodal_links.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_damping_nodal_links.headerItem().setTextAlignment(i, Qt.AlignCenter)

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
        self.pushButton_exit.clicked.connect(self.close)
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
        self.treeWidget_stiffness_nodal_links.itemClicked.connect(self.on_click_item_stiffness)
        self.treeWidget_damping_nodal_links.itemClicked.connect(self.on_click_item_damping)
        self.treeWidget_stiffness_nodal_links.itemDoubleClicked.connect(self.on_double_click_item_stiffness)
        self.treeWidget_damping_nodal_links.itemDoubleClicked.connect(self.on_double_click_item_damping)
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

                ss_link_data = self.properties._get_property("stiffness_nodal_links", node_ids=sorted_nodes)
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

                sd_link_data = self.properties._get_property("damping_nodal_links", node_ids=sorted_nodes)
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
            PrintMessageInput([error_title, title, message])
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
                PrintMessageInput([error_title, title, message])
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

            self.properties._set_nodal_property("stiffness_nodal_links", data, node_ids)

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

            self.properties._set_nodal_property("damping_nodal_links", data, node_ids)

    def attribute_callback(self):

        stop, node_ids = self.check_all_nodes()
        if stop:
            return True

        self.remove_conflicting_data(node_ids)

        if self.tabWidget_inputs.currentIndex() == 0:
            self.check_constant_stiffness_links(node_ids)
            self.check_constant_dampings_links(node_ids)

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.check_tables_for_stiffness_links(node_ids)
            self.check_tables_for_dampings_links(node_ids)

        if not self.link_applied:
            title = 'No inputs entered for the structural stiffness or damping links'
            message = "Define at least one value or table of values to the stiffness " 
            message += "or damping links to proceed with the structural link attribution."
            PrintMessageInput([error_title, title, message])
            return

        self.reset_nodes_input_fields()
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

    def check_tables_for_stiffness_links(self, node_ids: list):

        values = list()
        table_paths = list()

        for label in ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]:

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

            for label in ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]:

                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"stiffness_link_{label}", node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

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

                self.properties._set_nodal_property("stiffness_nodal_links", data, node_ids)

    def check_tables_for_dampings_links(self, node_ids: list):

        values = list()
        table_paths = list()

        for label in ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]:

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

            for label in ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]:

                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"stiffness_link_{label}", node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

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

                self.properties._set_nodal_property("damping_nodal_links", data, node_ids)
  
    def actions_to_finalize(self):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
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

        self.treeWidget_stiffness_nodal_links.clear()
        stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "stiffness_nodal_links":

                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, stiffness_labels))]
            
                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_stiffness_nodal_links.addTopLevelItem(item)

    def load_elastic_links_damping_info(self):

        self.treeWidget_damping_nodal_links.clear()
        damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "damping_nodal_links":

                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, damping_labels))]
            
                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_damping_nodal_links.addTopLevelItem(item)

    def load_nodes_info(self):

        self.load_elastic_links_stiffness_info()
        self.load_elastic_links_damping_info()

        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)

        self.checkBox_link_stiffness.setChecked(True)
        self.checkBox_link_dampings.setChecked(True)

        for (_property, *args) in self.properties.nodal_properties.keys():
            if _property == "stiffness_nodal_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(0, True)
                self.checkBox_link_stiffness.setChecked(True)
                break

        for (_property, *args) in self.properties.nodal_properties.keys():
            if _property == "damping_nodal_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(1, True)
                self.checkBox_link_dampings.setChecked(True)
                break

    def on_click_item_stiffness(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property("stiffness_nodal_links", node_ids=node_ids)
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            # self.lineEdit_first_node_id.setText(str(node_ids[0]))
            # self.lineEdit_last_node_id.setText(str(node_ids[1]))
            self.pushButton_remove.setDisabled(False)

    def on_click_item_damping(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property("damping_nodal_links", node_ids=node_ids)
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
            properties = ["stiffness_nodal_links", "damping_nodal_links"]

        elif isinstance(selected_property, str):
            properties = [selected_property]

        for node_id in node_ids:
            for _property in properties:
                table_names = self.properties.get_nodal_related_table_names(_property, node_id)
                self.properties._remove_nodal_property(_property, node_id)
                self.process_table_file_removal(table_names)

        app().project.file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        for _property in ["stiffness_nodal_links", "damping_nodal_links"]:
            table_names = self.properties.get_nodal_related_table_names(_property, node_ids)
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().project.file.write_imported_table_data_in_file()

    def remove_callback(self):

        _first_node = self.lineEdit_first_node_id.text()
        _last_node = self.lineEdit_last_node_id.text()

        if _first_node != "" and _last_node != "":

            node_id1 = int(_first_node)
            node_id2 = int(_last_node)
            node_ids = [node_id1, node_id2]

            if self.checkBox_link_stiffness.isChecked():
                self.properties._remove_nodal_property("stiffness_nodal_links", node_ids=node_ids)
                self.remove_conflicting_data(node_ids, selected_property="stiffness_nodal_links")

            if self.checkBox_link_dampings.isChecked():
                self.properties._remove_nodal_property("damping_nodal_links", node_ids=node_ids)
                self.remove_conflicting_data(node_ids, selected_property="damping_nodal_links")

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
                if _property in ["stiffness_nodal_links", "damping_nodal_links"]:
                    link_nodes.append(args)

            for node_ids in link_nodes:

                if self.checkBox_link_stiffness.isChecked():
                    self.properties._remove_nodal_property("stiffness_nodal_links", node_ids=node_ids)
                    self.remove_conflicting_data(node_ids, selected_property="stiffness_nodal_links")

                if self.checkBox_link_dampings.isChecked():
                    self.properties._remove_nodal_property("damping_nodal_links", node_ids=node_ids)
                    self.remove_conflicting_data(node_ids, selected_property="damping_nodal_links")

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
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)