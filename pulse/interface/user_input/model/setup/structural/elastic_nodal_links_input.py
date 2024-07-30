from PyQt5.QtWidgets import QDialog, QFileDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.tools.utils import get_new_path, remove_bc_from_file

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class ElasticNodalLinksInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/elastic_nodal_links_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        app().main_window.input_ui.set_input_widget(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.update()
        self.load_treeWidgets_info()
        
        while self.keep_window_open:
            self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.nodes = self.preprocessor.nodes

        self.structural_bc_info_path = self.project.file._node_structural_path
        # self.imported_data_path = project.file._imported_data_folder_path 
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.elastic_links_files_folder_path = get_new_path(self.structural_folder_path, "elastic_links_files")
        
        self.userPath = os.path.expanduser('~')       
        self.stop = False
        self.complete = False

        self.current_selection = None
        
        self.Kx_table = None
        self.Ky_table = None
        self.Kz_table = None
        self.Krx_table = None
        self.Kry_table = None
        self.Krz_table = None

        self.Kx_filename = None
        self.Ky_filename = None
        self.Kz_filename = None
        self.Krx_filename = None
        self.Kry_filename = None
        self.Krz_filename = None

        self.Kx_basename = None
        self.Ky_basename = None
        self.Kz_basename = None
        self.Krx_basename = None
        self.Kry_basename = None
        self.Krz_basename = None

        self.Cx_table = None
        self.Cy_table = None
        self.Cz_table = None
        self.Crx_table = None
        self.Cry_table = None
        self.Crz_table = None

        self.Cx_filename = None
        self.Cy_filename = None
        self.Cz_filename = None
        self.Crx_filename = None
        self.Cry_filename = None
        self.Crz_filename = None

        self.Cx_basename = None
        self.Cy_basename = None
        self.Cz_basename = None
        self.Crx_basename = None
        self.Cry_basename = None
        self.Crz_basename = None

        self.flag_stiffness_parameters = False
        self.flag_damping_parameters = False

    def _define_qt_variables(self):

        # QFrame
        self.selection_frame : QFrame

        # QLineEdit
        self.lineEdit_selection : QLineEdit
        self.lineEdit_first_node_id : QLineEdit
        self.lineEdit_last_node_id : QLineEdit

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

        self.lineEdit_path_table_Kx : QLineEdit
        self.lineEdit_path_table_Ky : QLineEdit
        self.lineEdit_path_table_Kz : QLineEdit
        self.lineEdit_path_table_Krx : QLineEdit
        self.lineEdit_path_table_Kry : QLineEdit
        self.lineEdit_path_table_Krz : QLineEdit

        # QPushButton
        self.pushButton_load_Kx_table : QPushButton
        self.pushButton_load_Ky_table : QPushButton
        self.pushButton_load_Kz_table : QPushButton
        self.pushButton_load_Krx_table : QPushButton
        self.pushButton_load_Kry_table : QPushButton
        self.pushButton_load_Krz_table : QPushButton 

        self.lineEdit_path_table_Cx : QLineEdit
        self.lineEdit_path_table_Cy : QLineEdit
        self.lineEdit_path_table_Cz : QLineEdit
        self.lineEdit_path_table_Crx : QLineEdit
        self.lineEdit_path_table_Cry : QLineEdit
        self.lineEdit_path_table_Crz : QLineEdit

        self.pushButton_load_Cx_table : QPushButton
        self.pushButton_load_Cy_table : QPushButton
        self.pushButton_load_Cz_table : QPushButton
        self.pushButton_load_Crx_table : QPushButton
        self.pushButton_load_Cry_table : QPushButton
        self.pushButton_load_Crz_table : QPushButton

        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget
        self.tabWidget_inputs : QTabWidget
        self.tabWidget_constant_values : QTabWidget
        self.tabWidget_table_values : QTabWidget
        
        # QTreeWidget
        self.treeWidget_nodal_links_stiffness : QTreeWidget
        self.treeWidget_nodal_links_damping : QTreeWidget

    def _create_connections(self):
        #
        self.clickable(self.lineEdit_first_node_id).connect(self.lineEdit_first_node_clicked)
        self.clickable(self.lineEdit_last_node_id).connect(self.lineEdit_last_node_clicked)
        self.current_lineEdit = self.lineEdit_first_node_id
        self._create_lists_of_lineEdits()
        #
        self.pushButton_confirm.clicked.connect(self.add_elastic_link)
        self.pushButton_remove.clicked.connect(self.remove_selected_elastic_link)
        self.pushButton_reset.clicked.connect(self.reset_elastic_links)

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

        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)

        self.treeWidget_nodal_links_stiffness.itemClicked.connect(self.on_click_item_stiffness)
        self.treeWidget_nodal_links_damping.itemClicked.connect(self.on_click_item_damping)
        self.treeWidget_nodal_links_stiffness.itemDoubleClicked.connect(self.on_doubleclick_item_stiffness)
        self.treeWidget_nodal_links_damping.itemDoubleClicked.connect(self.on_doubleclick_item_damping)

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
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        self.treeWidget_nodal_links_stiffness.setColumnWidth(0, 120)
        self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_nodal_links_damping.setColumnWidth(0, 120)
        self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = pyqtSignal()

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

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)

        else:
            if self.cache_tab == 1:
                self.lineEdit_selection.setText("")
            self.selection_frame.setDisabled(False)

        self.cache_tab = self.tabWidget_main.currentIndex()

    def check_all_nodes(self):

        lineEdit_nodeID = self.lineEdit_first_node_id.text()
        self.stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True
        temp_nodeID_1 = self.nodeID
        
        lineEdit_nodeID = self.lineEdit_last_node_id.text()
        self.stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True           
        temp_nodeID_2 = self.nodeID

        if temp_nodeID_1 == temp_nodeID_2:
            title = "ERROR IN NODES SELECTION"
            message = "The selected nodes must differ. Try to choose another pair of nodes."
            PrintMessageInput([window_title_1, title, message])
            return True

        if temp_nodeID_2 > temp_nodeID_1:
            self.nodeID_1 = temp_nodeID_1
            self.nodeID_2 = temp_nodeID_2
        else:
            self.nodeID_2 = temp_nodeID_1
            self.nodeID_1 = temp_nodeID_2

        return False
        
    def check_input_parameters(self, lineEdit, label, _float=True):
        title = "Invalid input"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            self.value = None
        return False

    def check_constant_inputs(self):

        self.parameters_K = None
        self.parameters_C = None

        if self.check_all_nodes():
            return True

        if self.check_input_parameters(self.lineEdit_Kx, 'Kx'):
            return True
        else:
            Kx = self.value

        if self.check_input_parameters(self.lineEdit_Ky, 'Ky'):
            return True
        else:
            Ky = self.value

        if self.check_input_parameters(self.lineEdit_Kz, 'Kz'):
            return True
        else:
            Kz = self.value

        if self.check_input_parameters(self.lineEdit_Krx, 'Krx'):
            return True
        else:
            Krx = self.value

        if self.check_input_parameters(self.lineEdit_Kry, 'Kry'):
            return True
        else:
            Kry = self.value

        if self.check_input_parameters(self.lineEdit_Krz, 'Krz'):
            return True
        else:
            Krz = self.value
        
        if self.check_input_parameters(self.lineEdit_Cx, 'Cx'):
            return True
        else:
            Cx = self.value

        if self.check_input_parameters(self.lineEdit_Cy, 'Cy'):
            return True
        else:
            Cy = self.value

        if self.check_input_parameters(self.lineEdit_Cz, 'Cz'):
            return True
        else:
            Cz = self.value

        if self.check_input_parameters(self.lineEdit_Crx, 'Crx'):
            return True
        else:
            Crx = self.value

        if self.check_input_parameters(self.lineEdit_Cry, 'Cry'):
            return True
        else:
            Cry = self.value

        if self.check_input_parameters(self.lineEdit_Crz, 'Crz'):
            return True
        else:
            Crz = self.value

        list_K = [Kx, Ky, Kz, Krx, Kry, Krz]
        list_C = [Cx, Cy, Cz, Crx, Cry, Crz] 
                
        if list_K.count(None) != 6:
            self.parameters_K = list_K

        if list_C.count(None) != 6:
            self.parameters_C = list_C

        if list_K.count(None) == 6 and list_C.count(None) == 6:
            title = 'Empty inputs for stiffness and damping'
            message = "Please insert at least a stiffness or damping "
            message += "value before confirming the attribution."
            PrintMessageInput([window_title_1, title, message])

    def add_elastic_link(self):

        if self.tabWidget_inputs.currentIndex() == 0:
            self.constant_input_confirm()

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.table_input_confirm()

        self.opv.updateRendererMesh()
        self.close()

    def constant_input_confirm(self):

        if self.check_constant_inputs():
            return

        table_names = [None, None, None, None, None, None]

        if self.parameters_K is not None:
            self.remove_elastic_link_stiffness_table_files()
            data = [self.parameters_K, table_names]
            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, 
                                                          self.nodeID_2, 
                                                          data,
                                                          False)

        if self.parameters_C is not None:
            self.remove_elastic_link_damping_table_files()
            data = [self.parameters_C, table_names]
            self.project.add_elastic_nodal_link_damping(self.nodeID_1, 
                                                        self.nodeID_2, 
                                                        data, 
                                                        False)

    def load_table(self, lineEdit, _label, direct_load=False):
        title = "Error reached while loading table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the {} nodal load'.format(_label)
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None
            
            self.imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)                        
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The imported \n"
                message += "data must have two columns of values."
                PrintMessageInput([window_title_1, title, message])
                lineEdit.setFocus()
                return None, None

            if imported_file.shape[1] >= 3:
                self.imported_values = imported_file[:,1]
                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]

                if self.project.change_project_frequency_setup(self.imported_filename, list(self.frequencies)):
                    self.stop = True
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                    self.stop = False
            
                return self.imported_values, self.imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def load_Kx_table(self):
        self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_Kx, "Kx")
        if self.stop:
            self.stop = False
            self.Kx_table, self.Kx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kx)

    def load_Ky_table(self):
        self.Ky_table, self.Ky_filename = self.load_table(self.lineEdit_path_table_Ky, "Ky")
        if self.stop:
            self.stop = False
            self.Ky_table, self.Ky_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Ky)

    def load_Kz_table(self):
        self.Kz_table, self.Kz_filename = self.load_table(self.lineEdit_path_table_Kz, "Kz")
        if self.stop:
            self.stop = False
            self.Kz_table, self.Kz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kz)

    def load_Krx_table(self):
        self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_Krx, "Krx")
        if self.stop:
            self.stop = False
            self.Krx_table, self.Krx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Krx)

    def load_Kry_table(self):
        self.Kry_table, self.Kry_filename = self.load_table(self.lineEdit_path_table_Kry, "Kry")
        if self.stop:
            self.stop = False
            self.Kry_table, self.Kry_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kry)

    def load_Krz_table(self):
        self.Krz_table, self.Krz_filename = self.load_table(self.lineEdit_path_table_Krz, "Krz")
        if self.stop:
            self.stop = False
            self.Krz_table, self.Krz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Krz)

    def load_Cx_table(self):
        self.Cx_table, self.Cx_filename = self.load_table(self.lineEdit_path_table_Cx, "Cx")
        if self.stop:
            self.stop = False
            self.Cx_table, self.Cx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cx)

    def load_Cy_table(self):
        self.Cy_table, self.Cy_filename = self.load_table(self.lineEdit_path_table_Cy, "Cy")
        if self.stop:
            self.stop = False
            self.Cy_table, self.Cy_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cy)

    def load_Cz_table(self):
        self.Cz_table, self.Cz_filename = self.load_table(self.lineEdit_path_table_Cz, "Cz")
        if self.stop:
            self.stop = False
            self.Cz_table, self.Cz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cz)

    def load_Crx_table(self):
        self.Crx_table, self.Crx_filename = self.load_table(self.lineEdit_path_table_Crx, "Crx")
        if self.stop:
            self.stop = False
            self.Crx_table, self.Crx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Crx)

    def load_Cry_table(self):
        self.Cry_table, self.Cry_filename = self.load_table(self.lineEdit_path_table_Cry, "Cry")
        if self.stop:
            self.stop = False
            self.Cry_table, self.Cry_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cry)

    def load_Crz_table(self):
        self.Crz_table, self.Crz_filename = self.load_table(self.lineEdit_path_table_Crz, "Crz")
        if self.stop:
            self.stop = False
            self.Crz_table, self.Crz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Crz)

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_tables_files(self, values, filename, _label, unit_label):

        real_values = np.real(values)
        data = np.array([self.frequencies, real_values]).T
        self.project.create_folders_structural("elastic_links_files")

        if _label in ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]:
            header = f"OpenPulse - stiffness elastic link - imported table for {_label}  @ "
            basename = f"elastic_link_stiffness_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_2}.dat"
            values_label = "Stiffness values"

        else:
            header = f"OpenPulse - damping elastic link - imported table for {_label} @ "
            basename = f"elastic_link_damping_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_2}.dat"
            values_label = "Damping values"
            
        header += f"linked nodes {self.nodeID_1}-{self.nodeID_2}\n"
        header += f"\nSource filename: {filename}\n"
        header += f"\nFrequency [Hz], {values_label} [{unit_label}]"
        # basename = filename + f"_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_1}.dat"
    
        new_path_table = get_new_path(self.elastic_links_files_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def check_table_for_elastic_link_stiffness(self):

        Kx = Ky = Kz = None
        if self.lineEdit_path_table_Kx.text() != "":
            if self.Kx_table is None:
                if self.Kx_filename is None:
                    self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_Kx, "Kx", direct_load=True)
            if self.Kx_table is not None:
                Kx, self.Kx_basename = self.save_tables_files(self.Kx_table, self.Kx_filename, "Kx", "N/m")

        if self.lineEdit_path_table_Ky.text() != "":
            if self.Ky_table is None:
                if self.Ky_filename is None:
                    self.Ky_table, self.Ky_filename = self.load_table(self.lineEdit_path_table_Ky, "Ky", direct_load=True)
            if self.Ky_table is not None:
                Ky, self.Ky_basename = self.save_tables_files(self.Ky_table, self.Ky_filename, "Ky", "N/m")

        if self.lineEdit_path_table_Kz.text() != "":
            if self.Kz_table is None:
                if self.Kz_filename is None:
                    self.Kz_table, self.Kz_filename = self.load_table(self.lineEdit_path_table_Kz, "Kz", direct_load=True)
            if self.Kz_table is not None:
                Kz, self.Kz_basename = self.save_tables_files(self.Kz_table, self.Kz_filename, "Kz", "N/m")

        Krx = Kry = Krz = None
        if self.lineEdit_path_table_Krx.text() != "":
            if self.Krx_table is None:
                if self.Krx_filename is None:
                    self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_Krx, "Krx", direct_load=True)
            if self.Krx_table is not None:
                Krx, self.Krx_basename = self.save_tables_files(self.Krx_table, self.Krx_filename, "Krx", "N.m/rad")

        if self.lineEdit_path_table_Kry.text() != "":
            if self.Kry_table is None:
                if self.Kry_filename is None:
                    self.Kry_table, self.Kry_filename = self.load_table(self.lineEdit_path_table_Kry, "Kry", direct_load=True)
            if self.Kry_table is not None:
                Kry, self.Kry_basename = self.save_tables_files(self.Kry_table, self.Kry_filename, "Kry", "N.m/rad")

        if self.lineEdit_path_table_Krz.text() != "":
            if self.Krz_table is None:
                if self.Krz_filename is None:
                    self.Krz_table, self.Krz_filename = self.load_table(self.lineEdit_path_table_Krz, "Krz", direct_load=True)
            if self.Krz_table is not None:
                Krz, self.Krz_basename = self.save_tables_files(self.Krz_table, self.Krz_filename, "Krz", "N.m/rad")
        
        stiffness_parameters = [Kx, Ky, Kz, Krx, Kry, Krz]

        if sum([0 if bc is None else 1 for bc in stiffness_parameters]) != 0:
            self.flag_stiffness_parameters = True
            self.K_basenames = [self.Kx_basename, self.Ky_basename, self.Kz_basename, 
                                self.Krx_basename, self.Kry_basename, self.Krz_basename]
            self.stiffness_parameters = stiffness_parameters
            data = [stiffness_parameters, self.K_basenames]

            key = f"{self.nodeID_1}-{self.nodeID_2}"
            for node_id in [self.nodeID_1, self.nodeID_2]:
                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_elastic_link_stiffness:
                    if key in node.elastic_nodal_link_stiffness.keys():
                        list_table_names = node.elastic_nodal_link_stiffness[key][1]
                        for basename in self.K_basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, self.nodeID_2, data, True)
            return False
        else:
            return True

    def check_table_for_elastic_link_damping(self):
 
        Cx = Cy = Cz = None
        if self.lineEdit_path_table_Cx.text() != "":
            if self.Cx_table is None:
                if self.Cx_filename is None:
                    self.Cx_table, self.Cx_filename = self.load_table(self.lineEdit_path_table_Cx, "Cx", direct_load=True)
            if self.Cx_table is not None:
                Cx, self.Cx_basename = self.save_tables_files(self.Cx_table, self.Cx_filename, "Cx", "N.s/m")
    
        if self.lineEdit_path_table_Cy.text() != "":
            if self.Cy_table is None:
                if self.Cy_filename is None:
                    self.Cy_table, self.Cy_filename = self.load_table(self.lineEdit_path_table_Cy, "Cy", direct_load=True)
            if self.Cy_table is not None:
                Cy, self.Cy_basename = self.save_tables_files(self.Cy_table, self.Cy_filename, "Cy", "N.s/m")

        if self.lineEdit_path_table_Cz.text() != "":
            if self.Cz_table is None:
                if self.Cz_filename is None:
                    self.Cz_table, self.Cz_filename = self.load_table(self.lineEdit_path_table_Cz, "Cz", direct_load=True)
            if self.Cz_table is not None:
                Cz, self.Cz_basename = self.save_tables_files(self.Cz_table, self.Cz_filename, "Cz", "N.s/m")

        Crx = Cry = Crz = None
        if self.lineEdit_path_table_Crx.text() != "":
            if self.Crx_table is None:
                if self.Crx_filename is None:
                    self.Crx_table, self.Crx_filename = self.load_table(self.lineEdit_path_table_Crx, "Crx", direct_load=True)
            if self.Crx_table is not None:
                Crx, self.Crx_basename = self.save_tables_files(self.Crx_table, self.Crx_filename, "Crx", "N.m/rad/s")

        if self.lineEdit_path_table_Cry.text() != "":
            if self.Cry_table is None:
                if self.Cry_filename is None:
                    self.Cry_table, self.Cry_filename = self.load_table(self.lineEdit_path_table_Cry, "Cry", direct_load=True)
            if self.Cry_table is not None:
                Cry, self.Cry_basename = self.save_tables_files(self.Cry_table, self.Cry_filename, "Cry", "N.m/rad/s")

        if self.lineEdit_path_table_Crz.text() != "":
            if self.Crz_table is None:
                if self.Crz_filename is None:
                    self.Crz_table, self.Crz_filename = self.load_table(self.lineEdit_path_table_Crz, "Crz", direct_load=True)
            if self.Crz_table is not None:
                Crz, self.Crz_basename = self.save_tables_files(self.Crz_table, self.Crz_filename, "Crz", "N.m/rad/s")
                    
        damping_parameters = [Cx, Cy, Cz, Crx, Cry, Crz]
 
        if sum([0 if bc is None else 1 for bc in damping_parameters]):

            self.flag_damping_parameters = True
            self.C_basenames = [self.Cx_basename, self.Cy_basename, self.Cz_basename, 
                                self.Crx_basename, self.Cry_basename, self.Crz_basename]
            self.damping_parameters = damping_parameters
            data = [damping_parameters, self.C_basenames]
            
            key = f"{self.nodeID_1}-{self.nodeID_2}"

            for node_id in [self.nodeID_1, self.nodeID_2]:
                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_elastic_link_dampings:
                    if key in node.elastic_nodal_link_dampings.keys():
                        list_table_names = node.elastic_nodal_link_dampings[key][1]
                        for basename in self.C_basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

            self.project.add_elastic_nodal_link_damping(self.nodeID_1, self.nodeID_2, data, True)
            return False
        else:
            return True
  
    def table_input_confirm(self):

        if self.check_all_nodes():
            return True

        self.check_table_for_elastic_link_stiffness()
        self.check_table_for_elastic_link_damping()

        if not (self.flag_stiffness_parameters or self.flag_damping_parameters):
            title = 'NONE TABLE SELECTED FOR STIFFNESS OR DAMPING'
            message = "Please, define at least a table of values to the stiffness or damping" 
            message += "before confirming the elastic link attribution."
            PrintMessageInput([window_title_1, title, message])
            return

    def remove_elastic_link_stiffness_table_files(self):
        for node_id in [self.nodeID_1, self.nodeID_2]:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_elastic_link_stiffness:
                key = f"{self.nodeID_1}-{self.nodeID_2}"
                if key in node.elastic_nodal_link_stiffness.keys():
                    list_table_names = node.elastic_nodal_link_stiffness[key][1]
                    self.process_table_file_removal(list_table_names)

    def remove_elastic_link_damping_table_files(self):
        for node_id in [self.nodeID_1, self.nodeID_2]:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_elastic_link_dampings:
                key = f"{self.nodeID_1}-{self.nodeID_2}"
                if key in node.elastic_nodal_link_dampings.keys():
                    list_table_names = node.elastic_nodal_link_dampings[key][1]
                    self.process_table_file_removal(list_table_names)

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="elastic_links_files")

    def text_label(self, mask, load_labels):
        
        text = ""
        temp = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4])
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3])
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def skip_treeWidget_row(self, treeWidget):
        new = QTreeWidgetItem(["", "", ""])
        new.setTextAlignment(0, Qt.AlignCenter)
        new.setTextAlignment(1, Qt.AlignCenter)
        new.setTextAlignment(2, Qt.AlignCenter)
        treeWidget.addTopLevelItem(new)

    def load_elastic_links_stiffness_info(self):

        self.treeWidget_nodal_links_stiffness.clear()
        stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])
        self.pushButton_remove.setDisabled(True)

        for key in self.preprocessor.nodes_with_elastic_link_stiffness.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_stiffness[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, stiffness_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_stiffness.addTopLevelItem(new)

    def load_elastic_links_damping_info(self):

        self.treeWidget_nodal_links_damping.clear()
        damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 
        self.pushButton_remove.setDisabled(True)

        for key in self.preprocessor.nodes_with_elastic_link_dampings.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_dampings[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, damping_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_damping.addTopLevelItem(new)

    def load_treeWidgets_info(self):

        self.load_elastic_links_stiffness_info()
        self.load_elastic_links_damping_info()
        self.tabWidget_main.setTabVisible(1, False)

        if self.preprocessor.nodes_with_elastic_link_stiffness:
            self.tabWidget_main.setTabVisible(1, True)

        if self.preprocessor.nodes_with_elastic_link_dampings:
            self.tabWidget_main.setTabVisible(1, True)

    def on_click_item_stiffness(self, item):
        self.current_selection = "stiffness"
        self.pushButton_remove.setDisabled(False)
        self.lineEdit_selection.setText(item.text(0))

    def on_click_item_damping(self, item):
        self.current_selection = "damping"
        self.pushButton_remove.setDisabled(False)
        self.lineEdit_selection.setText(item.text(0))

    def on_doubleclick_item_stiffness(self, item):
        self.on_click_item_stiffness(item)
        self.get_information()

    def on_doubleclick_item_damping(self, item):
        self.on_click_item_damping(item)
        self.get_information()

    def remove_selected_elastic_link(self):
        if self.lineEdit_selection.text() != "":
            selection = self.lineEdit_selection.text()
            if self.current_selection == "stiffness":
                self.remove_selected_link_stiffness(selection)
            elif self.current_selection == "damping":
                self.remove_selected_link_damping(selection)

    def remove_selected_link_stiffness(self, selection, reset=False):

        str_ids = selection.split("-")
        self.nodeID_1, self.nodeID_2 = [int(str_id) for str_id in str_ids]
    
        key_strings = ["connecting stiffness", "connecting torsional stiffness"]

        # remove_bc_from_file([selection], self.structural_bc_info_path, key_strings, message, equals_keys=True)
        self.project.file.filter_bc_data_from_dat_file([selection], key_strings, self.structural_bc_info_path)
        self.remove_elastic_link_stiffness_table_files()
        self.preprocessor.add_elastic_nodal_link(self.nodeID_1, self.nodeID_2, None, _stiffness=True)

        if not reset:
            self.load_elastic_links_stiffness_info()
            self.opv.updateRendererMesh()
            self.lineEdit_selection.setText("")

    def remove_selected_link_damping(self, selection, reset=False):

        str_ids = selection.split("-")
        self.nodeID_1, self.nodeID_2 = [int(str_id) for str_id in str_ids]

        key_strings = ["connecting damping", "connecting torsional damping"]
        message = None

        # remove_bc_from_file([selection], self.structural_bc_info_path, key_strings, message, equals_keys=True)
        self.project.file.filter_bc_data_from_dat_file([selection], key_strings, self.structural_bc_info_path)
        self.remove_elastic_link_damping_table_files()
        self.preprocessor.add_elastic_nodal_link(self.nodeID_1, self.nodeID_2, None, _damping=True)

        if not reset:
            self.load_elastic_links_damping_info()
            self.opv.updateRendererMesh()
            self.lineEdit_selection.setText("")

    def reset_elastic_links(self):

        self.hide()

        title = "Resetting of elastic links"
        message = "Would you like to remove all nodal elastic links from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            temp_dict_stiffness = self.preprocessor.nodes_with_elastic_link_stiffness.copy()
            for key in temp_dict_stiffness.keys():
                self.remove_selected_link_stiffness(key, reset=True)

            temp_dict_damping = self.preprocessor.nodes_with_elastic_link_dampings.copy()
            for key in temp_dict_damping.keys():
                self.remove_selected_link_damping(key, reset=True)

            self.close()
            self.opv.updateRendererMesh()

    def get_information(self):
        try:
            if self.lineEdit_selection.text() != "":

                key = self.lineEdit_selection.text()
                node_ids = [int(node) for node in key.split("-")]

                if self.current_selection == "stiffness":
                    group_label = "Stiffness elastic link"
                    labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])
                    mask, values = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_stiffness[key]

                elif self.current_selection == "damping":
                    group_label = "Damping elastic link"
                    header_labels = ["Nodes", "Damping elastic link"]
                    labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
                    mask, values = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_damping[key]
                else:
                    return

                header_labels = ["Nodes", self.text_label(mask, labels)]
                # print(self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_stiffness[key])

                data = dict()
                for node_id in node_ids:
                    # filtered_values = [list(np.array(values)[mask])]
                    # data[node_id] = [f"{value : .3e}" if isinstance(value, float) else str(value) for value in filtered_values]
                    data[node_id] = [list(np.array(values)[mask])]

                if len(data):

                    self.setVisible(False)
                    GetInformationOfGroup(  group_label = group_label,
                                            selection_label = "Node ID:",
                                            header_labels = header_labels,
                                            column_widths = [80, 90],
                                            data = data  )

            else:
                title = "Invalid selection"
                message = "Please, select an elastic link in the list to get the information."
                PrintMessageInput([window_title_2, title, message])

        except Exception as error_log:
            title = "Error while getting information of selected elastic link"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

        self.setVisible(True)

    def reset_nodes_input_fields(self):
        self.lineEdit_selection.setText("")
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

    def update(self):

        try:
        
            key = None
            nodes_ids = self.opv.getListPickedPoints()

            if nodes_ids:

                if len(nodes_ids) == 1:
                    self.current_lineEdit.setText(str(nodes_ids[0]))

                elif len(nodes_ids) == 2:
                    first_node = min(nodes_ids)
                    last_node = max(nodes_ids)
                    key = f"{first_node}-{last_node}"
                    self.write_ids(nodes_ids)
                    x = 1

            else:
                return

            self.reset_stiffness_input_fields()
            self.reset_dampings_input_fields()
            node = self.preprocessor.nodes[nodes_ids[0]]

            #Elastic link stiffness
            if node.there_are_elastic_nodal_link_stiffness:
                if key in node.elastic_nodal_link_stiffness.keys():
                    if node.loaded_table_for_elastic_link_stiffness:
                        table_names = node.elastic_nodal_link_stiffness[key][1]
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for index, lineEdit_table in enumerate(self.lineEdits_table_values_stiffness):
                            if table_names[index] is not None:
                                table_name = get_new_path(self.elastic_links_files_folder_path, table_names[index])
                                lineEdit_table.setText(table_name)

                    else:

                        elastic_link_stiffness = node.elastic_nodal_link_stiffness[key][1]
                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(0)
                        for index, lineEdit_constant in enumerate(self.lineEdits_constant_values_stiffness):
                            value = elastic_link_stiffness[index]
                            if value is not None:
                                lineEdit_constant.setText(f"{value : .3e}")

            #Elastic link dampings
            if node.there_are_elastic_nodal_link_dampings:
                if key in node.elastic_nodal_link_dampings.keys():
                    if node.loaded_table_for_elastic_link_dampings:
                        table_names = node.elastic_nodal_link_dampings[key][1]
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(1)
                        for index, lineEdit_table in enumerate(self.lineEdits_table_values_dampings):
                            if table_names[index] is not None:
                                table_name = get_new_path(self.elastic_links_files_folder_path, table_names[index])
                                lineEdit_table.setText(table_name)

                    else:

                        elastic_link_dampings = node.elastic_nodal_link_dampings[key][1]
                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(1)
                        for index, lineEdit_constant in enumerate(self.lineEdits_constant_values_dampings):
                            value = elastic_link_dampings[index]
                            if value is not None:
                                lineEdit_constant.setText(f"{value : .3e}")

        except Exception as error_log:
            title = "Error in 'update' function"
            message = str(error_log)
            # TODO: disable the 'messages' until solve the 'update' function recursive callback problem in opvRenderer
            # PrintMessageInput([window_title_1, title, message])

    def write_ids(self, list_node_ids):

        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)

        if len(list_node_ids) == 2:
            self.lineEdit_first_node_id.setText(str(min(list_node_ids[-2:])))
            self.lineEdit_last_node_id.setText(str(max(list_node_ids[-2:])))

        elif len(list_node_ids) == 1:
            self.lineEdit_first_node_id.setText(str(list_node_ids[-1]))
            self.lineEdit_last_node_id.setText("")
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_elastic_link()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)           

    # def remove_table_files(self, values):          
    #     for value in values:
    #         if value != 'None' and ".dat" in value:
    #             self.path_of_selected_table = get_new_path(self.elastic_links_tables_folder_path, value)
    #             # self.get_path_of_selected_table(value)
    #             try:
    #                 os.remove(self.path_of_selected_table)
    #             except:
    #                 pass

    # def remove_elastic_link_stiffness_from_file(self, section_key):

    #     path = self.project.file._node_structural_path
    #     config = configparser.ConfigParser()
    #     config.read(path)

    #     keys = list(config[section_key].keys())
    #     if "connecting stiffness" in keys and "connecting torsional stiffness" in keys:
    #         values_stiffness = config[section_key]["connecting stiffness"][1:-1].split(",")
    #         self.remove_table_files(values_stiffness)
    #         values_torsional_stiffness = config[section_key]["connecting torsional stiffness"][1:-1].split(",")
    #         self.remove_table_files(values_torsional_stiffness)
    #         config.remove_option(section=section_key, option="connecting stiffness")
    #         config.remove_option(section=section_key, option="connecting torsional stiffness")
    #         if len(list(config[section_key].keys())) == 0:
    #             config.remove_section(section=section_key)
    #     with open(path, 'w') as config_file:
    #         config.write(config_file)

    # def remove_elastic_link_damping_from_file(self, section_key):

    #     path = self.project.file._node_structural_path
    #     config = configparser.ConfigParser()
    #     config.read(path)        

    #     keys = list(config[section_key].keys())
    #     if "connecting damping" in keys and "connecting torsional damping" in keys:
    #         values_damping = config[section_key]["connecting damping"][1:-1].split(",")
    #         self.remove_table_files(values_damping)
    #         values_torsional_damping = config[section_key]["connecting torsional damping"][1:-1].split(",")
    #         self.remove_table_files(values_torsional_damping)
    #         config.remove_option(section=section_key, option="connecting damping")
    #         config.remove_option(section=section_key, option="connecting torsional damping")
    #         if len(list(config[section_key].keys())) == 0:
    #             config.remove_section(section=section_key)    
    #     with open(path, 'w') as config_file:
    #         config.write(config_file)