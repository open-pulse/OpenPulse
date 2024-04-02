from PyQt5.QtWidgets import QComboBox, QDialog, QFileDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.interface.user_input.model.setup.general.set_cross_section import SetCrossSectionInput
from pulse.preprocessing.cross_section import CrossSection
from pulse.tools.utils import get_new_path

import os
import numpy as np
import configparser

window_title_1 = "Error"
window_title_2 = "Warning"

class ExpansionJointInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/expansion_joint_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_treeWidgets_info()
        self.update()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")
    
    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        
        self.structural_elements = self.preprocessor.structural_elements
        self.element_size = self.project.file._element_size

        self.userPath = os.path.expanduser('~')     
        self.imported_data_path = self.project.file._imported_data_folder_path
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.expansion_joints_folder_path = get_new_path(self.structural_folder_path, "expansion_joints_files")

        self._entity_path = self.project.file._entity_path
        self._project_path = self.project.file._project_path
        self.stop = False
        self.complete = False

        self.Kx_table = None
        self.Kyz_table = None
        self.Krx_table = None
        self.Kryz_table = None

        self.Kx_filename = None
        self.Kyz_filename = None
        self.Krx_filename = None
        self.Kryz_filename = None

        self.Kx_basename = None
        self.Kyz_basename = None
        self.Krx_basename = None
        self.Kryz_basename = None

        self.allow_to_update = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection_type : QComboBox
        self.comboBox_axial_stop_rod : QComboBox

        # QFrame
        self.selection_frame : QFrame

        # QLabel
        self.label_selected_id : QLabel
        self.label_selection : QLabel
        self.label_axial_lock_criteria : QLabel

        # QLineEdit 
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_selection : QLineEdit
        #
        self.lineEdit_effective_diameter : QLineEdit
        self.lineEdit_joint_mass : QLineEdit
        self.lineEdit_joint_length : QLineEdit
        self.lineEdit_axial_locking_criteria : QLineEdit
        #
        self.lineEdit_axial_stiffness : QLineEdit
        self.lineEdit_transversal_stiffness : QLineEdit
        self.lineEdit_torsional_stiffness : QLineEdit
        self.lineEdit_angular_stiffness : QLineEdit
        #
        self.lineEdit_path_table_axial_stiffness : QLineEdit
        self.lineEdit_path_table_transversal_stiffness : QLineEdit
        self.lineEdit_path_table_torsional_stiffness : QLineEdit
        self.lineEdit_path_table_angular_stiffness : QLineEdit
        self._create_lists_of_lineEdits()

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_load_table_axial_stiffness : QPushButton
        self.pushButton_load_table_transversal_stiffness : QPushButton
        self.pushButton_load_table_torsional_stiffness : QPushButton
        self.pushButton_load_table_angular_stiffness : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget
        self.tabWidget_inputs : QTabWidget

        # QTreeWidget
        self.treeWidget_expansion_joint_by_lines : QTreeWidget
        self.treeWidget_expansion_joint_by_elements : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_axial_stop_rod.currentIndexChanged.connect(self.axial_stop_rod_callback)
        self.comboBox_selection_type.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_confirm.clicked.connect(self.add_expansion_joint)
        self.pushButton_remove.clicked.connect(self.remove_selected_expansion_joint)
        self.pushButton_reset.clicked.connect(self.reset_expansion_joints)
        #
        self.pushButton_load_table_axial_stiffness.clicked.connect(self.load_Kx_table)
        self.pushButton_load_table_transversal_stiffness.clicked.connect(self.load_Kyz_table)
        self.pushButton_load_table_torsional_stiffness.clicked.connect(self.load_Krx_table)
        self.pushButton_load_table_angular_stiffness.clicked.connect(self.load_Kryz_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_expansion_joint_by_lines.itemClicked.connect(self.on_click_item_lines)
        self.treeWidget_expansion_joint_by_elements.itemClicked.connect(self.on_click_item_elements)
        self.treeWidget_expansion_joint_by_lines.itemDoubleClicked.connect(self.on_doubleclick_item_lines)
        self.treeWidget_expansion_joint_by_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elements)

    def _config_widgets(self):
        self.treeWidget_expansion_joint_by_lines.setColumnWidth(0, 70)
        self.treeWidget_expansion_joint_by_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_elements.setColumnWidth(0, 70)
        self.treeWidget_expansion_joint_by_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def _create_lists_of_lineEdits(self):
        self.list_lineEdits = [ self.lineEdit_effective_diameter,
                                self.lineEdit_joint_mass,
                                self.lineEdit_joint_length,
                                self.lineEdit_axial_locking_criteria,
                                self.lineEdit_axial_stiffness,
                                self.lineEdit_transversal_stiffness,
                                self.lineEdit_torsional_stiffness,
                                self.lineEdit_angular_stiffness,
                                self.lineEdit_path_table_axial_stiffness,
                                self.lineEdit_path_table_transversal_stiffness,
                                self.lineEdit_path_table_torsional_stiffness,
                                self.lineEdit_path_table_angular_stiffness ]

    def axial_stop_rod_callback(self):
        if self.comboBox_axial_stop_rod.currentIndex() == 0:
            self.label_axial_lock_criteria.setDisabled(True)
            self.lineEdit_axial_locking_criteria.setText("")
            self.lineEdit_axial_locking_criteria.setDisabled(True)
        else:
            self.label_axial_lock_criteria.setDisabled(False)
            self.lineEdit_axial_locking_criteria.setDisabled(False)

    def selection_type_callback(self):

        line_id = self.opv.getListPickedLines()
        node_id = self.opv.getListPickedPoints()
        element_id = self.opv.getListPickedElements()

        self.lineEdit_selected_id.setText("")

        if self.comboBox_selection_type.currentIndex() == 0:

            self.label_selected_id.setText("Line ID:")
            self.lineEdit_joint_length.setDisabled(True)
            
            if not self.opv.change_plot_to_entities_with_cross_section:
                self.opv.plot_entities_with_cross_section()
                if line_id:
                    self.opv.opvRenderer.highlight_lines(line_id)

        elif self.comboBox_selection_type.currentIndex() == 1:

            self.label_selected_id.setText("Node ID:")
            self.lineEdit_joint_length.setDisabled(False)

            if not self.opv.change_plot_to_mesh:
                self.opv.plot_mesh()
                if node_id:
                    self.opv.opvRenderer.highlight_elements(node_id)

        elif self.comboBox_selection_type.currentIndex() == 2:

            self.label_selected_id.setText("Element ID:")
            self.lineEdit_joint_length.setDisabled(False)

            if not self.opv.change_plot_to_mesh:
                self.opv.plot_mesh()
                if element_id:
                    self.opv.opvRenderer.highlight_elements(element_id)

        if self.allow_to_update:
            self.update()

    def update(self):

        line_id = self.opv.getListPickedLines()
        node_id = self.opv.getListPickedPoints()
        element_id = self.opv.getListPickedElements()

        if line_id:
            element_id = list()
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(0)

        elif node_id:
            node_id = list()
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(1)

        elif element_id:
            line_id = list()
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(2)

        else:
            return

        self.allow_to_update = True

        try:

            if line_id:

                if self.write_ids(line_id):
                    self.lineEdit_selected_id.setText("")
                    return

                if len(line_id) == 1:
                    length, _ = self.preprocessor.get_line_length(line_id[0])
                    self.lineEdit_joint_length.setText(str(round(length, 8)))
                else:
                    self.lineEdit_joint_length.setText("multiple")

            elif node_id:
                if self.write_ids(node_id):
                    self.lineEdit_selected_id.setText("")
                    return

            elif element_id:

                if self.write_ids(element_id):
                    self.lineEdit_selected_id.setText("")
                    return

            self.load_input_fields()

        except Exception as log_error:
            title = "Error in 'update' function"
            message = str(log_error) 
            PrintMessageInput([window_title_1, title, message])

    def get_expansion_joint_length(self, selected_id):
        
        _stop = False
        if isinstance(selected_id, int):
            if self.comboBox_selection_type.currentIndex() == 0:
        
                _stop, _line_id = self.before_run.check_input_LineID(str(selected_id), single_ID=True)

                if not _stop:
                    self.joint_elements = self.preprocessor.line_to_elements[_line_id]
                    joint_length, _ = self.preprocessor.get_line_length(_line_id) 
                    self.lineEdit_joint_length.setText(str(round(joint_length, 6)))
                    self.list_table_names_from_selection = self.get_list_tables_names_from_selected_lines(selected_id)

            else:

                if self.check_input_parameters(self.lineEdit_joint_length, 'Expansion joint length'):
                    self.lineEdit_joint_length.setFocus()
                    _stop = True

                else:
 
                    input_length = self.value
                    self.joint_nodes, self.joint_elements = self.get_nodes_and_elements_according_joint_length(selected_id, 
                                                                                                               input_length)

                    if self.joint_elements is None:
                        _stop = True

                    else:

                        self.list_table_names_from_selection = self.get_list_tables_names_from_selected_elements(self.joint_elements)

                        joint_length = 0
                        for _id in self.joint_elements:
                            joint_length += self.preprocessor.structural_elements[_id].length

            if _stop:
                return None
            else:
                return round(joint_length, 6)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)
        else:
            self.lineEdit_selection.setText("")
            self.selection_frame.setDisabled(False)

    def check_selection_type(self):

        _stop = False
        lineEdit_selection = self.lineEdit_selected_id.text()

        if self.comboBox_selection_type.currentIndex() == 0:
            _stop, self.selected_lines = self.before_run.check_input_LineID(lineEdit_selection)

            for line_id in self.selected_lines:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type in ["beam_1"]:
                    _stop = True
                    break
            
            if len(self.selected_lines) == 1:
                joint_length, _ = self.preprocessor.get_line_length(self.selected_lines[0]) 
                self.lineEdit_joint_length.setText(str(round(joint_length, 6)))

            self.joint_elements = self.preprocessor.line_to_elements[line_id]

        elif self.comboBox_selection_type.currentIndex() == 1:  
            _stop, self.selected_nodes = self.before_run.check_input_NodeID(lineEdit_selection)

        elif self.comboBox_selection_type.currentIndex() == 2:
            _stop, self.selected_elements = self.before_run.check_input_ElementID(lineEdit_selection)

            for element_id in self.selected_elements:
                element = self.structural_elements[element_id]
                if element.element_type in ["beam_1"]:
                    _stop = True
                    break

        if _stop:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_joint_length.setText("")
            self.lineEdit_selected_id.setFocus()
            return True

        return False

    def reset_all_lineEdits(self):
        for lineEdit in self.list_lineEdits:
            lineEdit.setText("")

    def load_input_fields(self):

        lines_id = self.opv.getListPickedLines()
        elements_id = self.opv.getListPickedElements()

        if len(lines_id) == 1:

            entity = self.preprocessor.dict_tag_to_entity[lines_id[0]]
            if entity.expansion_joint_parameters is None:
                return
            else:
                parameters = entity.expansion_joint_parameters

        elif len(elements_id) == 1:
            
            element = self.preprocessor.structural_elements[elements_id[0]]
            if element.expansion_joint_parameters is None:
                return
            else:
                parameters = element.expansion_joint_parameters

        else:
            return

        self.reset_all_lineEdits()

        try:

            [joint_data, joint_stiffness, joint_tables]  = parameters      

            self.lineEdit_joint_length.setText(str(round(joint_data[0], 6)))
            self.lineEdit_effective_diameter.setText(str(joint_data[1]))
            self.lineEdit_joint_mass.setText(str(joint_data[2]))
            self.lineEdit_axial_locking_criteria.setText(str(joint_data[3]))

            self.comboBox_axial_stop_rod.setCurrentIndex(int(joint_data[4]))

            if isinstance(joint_stiffness[0], np.ndarray):
                table_path_axial = get_new_path(self.expansion_joints_folder_path, joint_tables[0])
                self.lineEdit_path_table_axial_stiffness.setText(table_path_axial)
                self.tabWidget_inputs.setCurrentIndex(1)

            else:
                self.lineEdit_axial_stiffness.setText(f"{joint_stiffness[0] : .3e}")
                self.tabWidget_inputs.setCurrentIndex(0)

            if isinstance(joint_stiffness[1], np.ndarray):
                table_path_transversal = get_new_path(self.expansion_joints_folder_path, joint_tables[1])
                self.lineEdit_path_table_transversal_stiffness.setText(table_path_transversal)
                self.tabWidget_inputs.setCurrentIndex(1)

            else:    
                self.lineEdit_transversal_stiffness.setText(f"{joint_stiffness[1] : .3e}")
                self.tabWidget_inputs.setCurrentIndex(0)

            if isinstance(joint_stiffness[2], np.ndarray):
                table_path_torsional = get_new_path(self.expansion_joints_folder_path, joint_tables[2])
                self.lineEdit_path_table_torsional_stiffness.setText(table_path_torsional)
                self.tabWidget_inputs.setCurrentIndex(1)

            else:                
                self.lineEdit_torsional_stiffness.setText(f"{joint_stiffness[2] : .3e}")
                self.tabWidget_inputs.setCurrentIndex(0)

            if isinstance(joint_stiffness[3], np.ndarray):
                table_path_angular = get_new_path(self.expansion_joints_folder_path, joint_tables[3])
                self.lineEdit_path_table_angular_stiffness.setText(table_path_angular)
                self.tabWidget_inputs.setCurrentIndex(1)

            else:
                self.lineEdit_angular_stiffness.setText(f"{joint_stiffness[3] : .3e}")
                self.tabWidget_inputs.setCurrentIndex(0)

        except Exception as error_log:
            title = "Error while loading info from entity"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def get_nodes_and_elements_according_joint_length(self, selected_id, input_length):

        if self.comboBox_selection_type.currentIndex() == 1:
            _nodes, _elements = self.preprocessor.get_neighbor_nodes_and_elements_by_node(selected_id, input_length)

        elif self.comboBox_selection_type.currentIndex() == 2:
            _nodes, _elements = self.preprocessor.get_neighbor_nodes_and_elements_by_element(selected_id, input_length)

        list_lines = list()
        for element_id in _elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            if line_id not in list_lines:
                list_lines.append(line_id)

        if len(list_lines) > 1:
            title = "Expansion joint: multiple lines in the list of elements"
            message = "Multiples lines have been detected in the current list of elements. It's recommended "
            message += "to reduces the joint length and/or choose another center node or element to avoid this "
            message += "problem. All elements from the expansion joint should belong to the same line. "
            PrintMessageInput([window_title_2, title, message])
            return None, None
        else:
            return _nodes, _elements

    def check_input_parameters(self, lineEdit, label, _float=True):
        message = ""
        title = f"Invalid entry to the '{label}'"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value <= 0:
                    message = f"You cannot input a non-positive value to the '{label}'."
                else:
                    self.value = value
            except Exception as _log_error:
                message = f"You have typed an invalid value to the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        else:
            message = f"An empty entry has been detected at the '{label}' input field. " 
            message += "You should to enter a positive value to proceed."
            self.value = None

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False
    
    def check_initial_inputs(self):
                
        if self.check_selection_type():
            return True

        if self.check_input_parameters(self.lineEdit_effective_diameter, 'Effective diameter'):
            self.lineEdit_effective_diameter.setFocus()
            return True
        else:
            self.effective_diameter = self.value
        
        if self.check_input_parameters(self.lineEdit_joint_mass, 'Joint mass'):
            self.lineEdit_joint_mass.setFocus()
            return True
        else:
            self.joint_mass = self.value

        if self.check_input_parameters(self.lineEdit_axial_locking_criteria, 'Axial locking criteria'):
            self.lineEdit_axial_locking_criteria.setFocus()
            return True
        else:
            self.axial_locking_criteria = self.value

        self.add_rods_key = int(self.comboBox_axial_stop_rod.currentIndex())

    def check_constant_values_to_stiffness(self):
        
        self.list_stiffness = list()

        if self.check_input_parameters(self.lineEdit_axial_stiffness, 'Axial stiffness'):
            self.lineEdit_axial_stiffness.setFocus()
            return True
        else:
            self.axial_stiffness = self.value

        if self.check_input_parameters(self.lineEdit_transversal_stiffness, 'Transversal stiffness'):
            self.lineEdit_transversal_stiffness.setFocus()
            return True
        else:
            self.transversal_stiffness = self.value

        if self.check_input_parameters(self.lineEdit_torsional_stiffness, 'Torsional stiffness'):
            self.lineEdit_torsional_stiffness.setFocus()
            return True
        else:
            self.torsional_stiffness = self.value

        if self.check_input_parameters(self.lineEdit_angular_stiffness, 'Angular stiffness'):
            self.lineEdit_angular_stiffness.setFocus()
            return True
        else:
            self.angular_stiffness = self.value

    def get_selected_ids(self):
        if self.comboBox_selection_type.currentIndex() == 0:
            selected_ids = self.selected_lines
        else:
            selected_ids = self.selected_elements
        return selected_ids

    def process_valve_inputs(self, data_type):

        if self.check_initial_inputs():
            return

        if data_type == "constant values":
            if self.check_constant_values_to_stiffness():
                return

        elif data_type == "table of values":
            if self.check_table_of_values():
                return

        else:
            return

        for tag in self.get_selected_ids():

            _joint_length = self.get_expansion_joint_length(tag)

            if _joint_length is None:
                continue

            joint_parameters = [_joint_length,
                                self.effective_diameter,  
                                self.joint_mass, 
                                self.axial_locking_criteria,
                                self.add_rods_key]

            if data_type == "constant values":

                joint_stiffness = [ self.axial_stiffness,
                                    self.transversal_stiffness,
                                    self.torsional_stiffness,
                                    self.angular_stiffness ]

                table_names = [None, None, None, None]

            elif data_type == "table of values":

                joint_stiffness = [self.Kx, self.Kyz, self.Krx, self.Kryz]

                table_names = [ self.Kx_basename, 
                                self.Kyz_basename, 
                                self.Krx_basename, 
                                self.Kryz_basename ]

            expansion_joint_data = [joint_parameters, joint_stiffness, table_names]

            if self.comboBox_selection_type.currentIndex() == 0:

                self.process_table_file_removal(self.list_table_names_from_selection)
                self.project.add_valve_by_line(tag, None)
                self.project.set_cross_section_by_lines(tag, None)

                cross_sections = get_list_cross_sections_to_plot_expansion_joint(self.joint_elements, joint_parameters[1])
                self.preprocessor.set_cross_section_by_element(self.joint_elements, cross_sections)
                self.project.add_expansion_joint_by_line(tag, expansion_joint_data)

            else:

                if self.check_previous_attributions_to_elements(self.joint_elements):
                    return

                self.project.add_valve_by_elements(self.joint_elements, None, reset_cross=False)
                elements_to_change = self.get_list_of_elements_to_update_cross_section()
                # lines_to_change = self.get_list_of_lines_to_update_cross_section()

                if elements_to_change:
                    self.setVisible(False)
                    read = SetCrossSectionInput(beam_to_pipe = True, 
                                                elements_to_update_cross_section = elements_to_change)
                    if not read.complete:
                        self.opv.setInputObject(self)
                        self.setVisible(True)
                        return
                else:
                    self.process_table_file_removal(self.list_table_names_from_selection)

                self.remove_expansion_joint_already_added_to_elements(self.joint_elements)            
                self.project.add_expansion_joint_by_elements(self.joint_elements, 
                                                             expansion_joint_data)

    def get_list_of_lines_to_update_cross_section(self):
        list_lines = []
        for element_id in self.joint_elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            if entity.structural_element_type in ["expansion_joint"]:
                if line_id not in list_lines:
                    list_lines.append(line_id)
            list_elements_from_line = self.preprocessor.line_to_elements[line_id]
            for element_id_from_line in list_elements_from_line:
                element = self.structural_elements[element_id_from_line]
                if element.element_type in [None, "beam_1"] or element.cross_section in [None]:
                    if line_id not in list_lines:
                        list_lines.append(line_id)
            
        return list_lines

    def get_list_of_elements_to_update_cross_section(self):

        list_lines = list()
        for element_id in self.joint_elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            if line_id not in list_lines:
                list_lines.append(line_id)
                
        list_elements = list()
        for _line_id in list_lines:
            list_elements_from_line = self.preprocessor.line_to_elements[_line_id]
            for element_id_from_line in list_elements_from_line:
                element = self.structural_elements[element_id_from_line]
                if element.element_type in [None, "beam_1"] or element.cross_section is None:
                    if element_id_from_line not in list_elements:
                        list_elements.append(element_id_from_line)

        return list_elements
    
    def get_list_of_lines_to_update_cross_section(self):

        list_lines = list()
        for element_id in self.joint_elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            for element_id_from_line in self.preprocessor.line_to_elements[line_id]:
                element = self.structural_elements[element_id_from_line]
                if element.element_type in [None, "beam_1"] or element.cross_section is None:
                    if line_id not in list_lines:
                        list_lines.append(line_id)

        return list_lines

    def get_pipe_cross_section_from_neighbors(self, line_id, list_elements):

        line_elements = self.preprocessor.line_to_elements[line_id]
        lower_id = list_elements[0] - 1
        upper_id = list_elements[-1] + 1

        cross = None
        structural_element_type = None

        try:
            if lower_id in line_elements:
                element = self.structural_elements[lower_id]
                cross = element.cross_section
                structural_element_type = element.element_type
            
            elif upper_id in line_elements:
                element = self.structural_elements[upper_id]
                cross = element.cross_section
                structural_element_type = element.element_type
        except:
            pass

        return cross, structural_element_type

    def remove_expansion_joint_already_added_to_elements(self, list_elements):

        changed = False
        temp_dict = self.preprocessor.group_elements_with_expansion_joints.copy()

        for key, [joint_elements, _] in temp_dict.items():

            joint_detected = False
            for element_id in joint_elements:
                if element_id in list_elements:
                    line_id = self.preprocessor.elements_to_line[element_id]
                    joint_detected = True
                    break

            if joint_detected:

                cross, etype = self.get_pipe_cross_section_from_neighbors(line_id, joint_elements)
                self.preprocessor.set_structural_element_type_by_element(joint_elements, etype)

                self.project.set_structural_element_type_by_lines(line_id, cross)
                self.project.set_cross_section_by_lines(line_id, cross)

                # self.project.add_expansion_joint_by_elements(   joint_elements, 
                #                                                 None, 
                #                                                 update_element_type = False, 
                #                                                 reset_cross = False   )
                # self.project.set_cross_section_by_elements(joint_elements, cross)

                if key in self.preprocessor.group_elements_with_expansion_joints.keys():
                    self.preprocessor.group_elements_with_expansion_joints.pop(key)

                changed = True

        return changed

    def load_table(self, lineEdit, stiffness_label, direct_load=False):
        title = "Error reached while loading table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the {} nodal load'.format(stiffness_label)
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)   
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
                
            if imported_file.shape[1] < 3:
                title = f"Error while loading {stiffness_label} table"
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have only two columns to the frequencies and values."
                PrintMessageInput([window_title_1, title, message])
                return None, None
        
            imported_values = imported_file[:,1]

            if imported_file.shape[1] >= 3:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                       
                if self.project.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                    self.stop = True
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                    self.stop = False

            return imported_values, imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def load_Kx_table(self):
        stiffness_label = "Axial stiffness"
        self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_axial_stiffness, stiffness_label)
        if self.stop:
            self.stop = False
            self.Kx_table, self.Kx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_axial_stiffness)

    def load_Kyz_table(self):
        stiffness_label = "Transversal stiffness"
        self.Kyz_table, self.Kyz_filename = self.load_table(self.lineEdit_path_table_transversal_stiffness, stiffness_label)
        if self.stop:
            self.stop = False
            self.Kyz_table, self.Kyz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_transversal_stiffness)

    def load_Krx_table(self):
        stiffness_label = "Torsional stiffness"
        self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_torsional_stiffness, stiffness_label)
        if self.stop:
            self.stop = False
            self.Krx_table, self.Krx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_torsional_stiffness)

    def load_Kryz_table(self):
        stiffness_label = "Angular stiffness"
        self.Kryz_table, self.Kryz_filename = self.load_table(self.lineEdit_path_table_angular_stiffness, stiffness_label)
        if self.stop:
            self.stop = False
            self.Kryz_table, self.Kryz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_angular_stiffness)

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_tables_files(self, values, filename, stiffness_label, linear=True):

        real_values = np.real(values)
        imag_values = np.imag(values)
        abs_values = np.abs(values)
        data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
        self.project.create_folders_structural("expansion_joints_files")
        line_id, table_index = self.get_line_and_table_index()

        header = f"OpenPulse - imported table for Expansion joint {stiffness_label} @ line {line_id} - table #{table_index}\n"     
        header += f"\nSource filename: {filename}\n"

        if linear:
            header += "\nFrequency [Hz], real[N/m], imaginary[N/m], absolute[N/m]"
        else:
            header += "\nFrequency [Hz], real[N.m/rad], imaginary[N.m/rad], absolute[N.m/rad]"

        basename = f"expansion_joint_{stiffness_label}_line_{line_id}_table#{table_index}.dat" 

        if basename in self.list_table_names_from_selection:
            self.list_table_names_from_selection.remove(basename)

        new_path_table = get_new_path(self.expansion_joints_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def check_message_empty_table_selection(self, label):
        title = 'None table selected to expansion joint stiffness'
        message = f"Please, define a table of values to the {label} "
        message += f"before confirming the attribution."
        PrintMessageInput([window_title_2, title, message])

    def check_table_of_values(self):

        self.loaded_stiffness = None
        try:
            Kx = Kyz = Krx = Kryz = None
            stiffness_label = "Axial stiffness"
            if self.lineEdit_path_table_axial_stiffness.text() != "":
                
                if self.Kx_table is None:
                    lineEdit = self.lineEdit_path_table_axial_stiffness
                    self.Kx_table, self.Kx_filename = self.load_table(lineEdit, stiffness_label, direct_load=True)
                
                if self.Kx_table is not None:
                    self.Kx, self.Kx_basename = self.save_tables_files( self.Kx_table, 
                                                                        self.Kx_filename, 
                                                                        "axial_stiffness" )
            else:
                self.check_message_empty_table_selection(stiffness_label)
                return True

            stiffness_label = "Transversal stiffness"
            if self.lineEdit_path_table_transversal_stiffness.text() != "":
                if self.Kyz_table is None:
                    lineEdit = self.lineEdit_path_table_transversal_stiffness
                    self.Kyz_table, self.Kyz_filename = self.load_table(lineEdit, stiffness_label, direct_load=True)
                
                if self.Kyz_table is not None:
                    self.Kyz, self.Kyz_basename = self.save_tables_files(self.Kyz_table,
                                                                         self.Kyz_filename, 
                                                                         "transversal_stiffness")
            else:
                self.check_message_empty_table_selection(stiffness_label)
                return True

            stiffness_label = "Torsional stiffness"
            if self.lineEdit_path_table_torsional_stiffness.text() != "":
                if self.Krx_table is None:
                    lineEdit = self.lineEdit_path_table_torsional_stiffness
                    self.Krx_table, self.Krx_filename = self.load_table(lineEdit, stiffness_label, direct_load=True)
                
                if self.Krx_table is not None:
                    self.Krx, self.Krx_basename = self.save_tables_files(self.Krx_table, 
                                                                         self.Krx_filename, 
                                                                         "torsional_stiffness")
            else:
                self.check_message_empty_table_selection(stiffness_label)
                return True

            stiffness_label = "Angular stiffness"
            if self.lineEdit_path_table_angular_stiffness.text() != "":
                if self.Kryz_table is None:
                    lineEdit = self.lineEdit_path_table_angular_stiffness
                    self.Kryz_table, self.Kryz_filename = self.load_table(lineEdit, stiffness_label, direct_load=True)

                if self.Kryz_table is not None:
                    self.Kryz, self.Kryz_basename = self.save_tables_files(self.Kryz_table, 
                                                                           self.Kryz_filename, 
                                                                           "angular_stiffness")
            else:
                self.check_message_empty_table_selection(stiffness_label)
                return True

            self.loaded_stiffness_tables = [Kx, Kyz, Krx, Kryz]
            self.basenames = [  self.Kx_basename, self.Kyz_basename, self.Krx_basename, self.Kryz_basename  ]

            return False

        except Exception as log_error:
            title = "Error while loading stiffness table of values"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return True

    def get_line_and_table_index(self):
        if self.comboBox_selection_type.currentIndex() == 0:
            line_id = self.selected_lines
            table_index = 1
        else:
            line_id = self.preprocessor.elements_to_line[self.joint_elements[0]]
            if line_id in self.preprocessor.number_expansion_joints_by_lines.keys():
                table_index = self.preprocessor.number_expansion_joints_by_lines[line_id] + 1
            else:
                table_index = 1

        return line_id, table_index

    def add_expansion_joint(self):

        if self.tabWidget_inputs.currentIndex() == 0:
            data_type = "constant values"

        elif self.tabWidget_inputs.currentIndex() == 1: 
            data_type = "table of values"

        self.process_valve_inputs(data_type)
        self.update_plots()
        self.close()

    def get_list_tables_names_from_selected_lines(self, list_line_ids):

        if isinstance(list_line_ids, int):
            list_line_ids = [list_line_ids]

        table_names_from_lines = list()
        for line_id in list_line_ids:
            list_elements = self.preprocessor.line_to_elements[line_id]
            table_names = self.get_list_tables_names_from_selected_elements(list_elements)
            for table_name in table_names:
                if table_name not in table_names_from_lines:
                    table_names_from_lines.append(table_name)

        return table_names_from_lines

    def get_list_tables_names_from_selected_elements(self, list_element_ids):

        if isinstance(list_element_ids, int):
            list_element_ids = [list_element_ids]

        table_names_from_elements = list()
        for element_id in list_element_ids:
            element = self.preprocessor.structural_elements[element_id]
            for table_name in element.joint_stiffness_table_names:
                if table_name not in table_names_from_elements:
                    table_names_from_elements.append(table_name)

        return table_names_from_elements

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="expansion_joints_files")

    def remove_all_table_files_from_nodes(self, list_node_ids):
        list_table_names = self.get_list_tables_names_from_selected_nodes(list_node_ids)
        self.process_table_file_removal(list_table_names)

    def check_previous_attributions_to_elements(self, list_elements):
        for element_id in list_elements:
            element = self.structural_elements[element_id]
            if element.element_type == "valve":
                title = "Valve detected in the elements selection"
                message = "In the present element list, at least one 'valve' element was found. "
                message += "To avoid unwanted valve setup modifications, we recommend removing any " 
                message += "already existing valve in the vicinity of the 'expansion joint' elements."
                PrintMessageInput([window_title_2, title, message])
                return True
        return False

    def skip_treeWidget_row(self, treeWidget):
        new = QTreeWidgetItem(["", ""])
        new.setTextAlignment(0, Qt.AlignCenter)
        new.setTextAlignment(1, Qt.AlignCenter)
        treeWidget.addTopLevelItem(new)
    
    def load_expansion_joint_by_line_info(self):
        self.treeWidget_expansion_joint_by_lines.clear()
        for line_id, parameters in self.preprocessor.dict_lines_with_expansion_joints.items():

            if get_string_from_joint_paramters(parameters):
                str_joint_data = f"{str(parameters[0])[1:-1]}, {'Table, Table, Table, Table'}"
            
            else:
                str_joint_data = ""
                for value in parameters[0]:
                    str_joint_data += f"{value}, "
                for value in parameters[1]:
                    str_joint_data += f"{value : .2e}, "

            new = QTreeWidgetItem([str(line_id), str_joint_data[:-2]])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_expansion_joint_by_lines.addTopLevelItem(new)

    def load_expansion_joint_by_elements_info(self):
        self.treeWidget_expansion_joint_by_elements.clear()
        for group_id, [_, parameters] in self.preprocessor.group_elements_with_expansion_joints.items():
           
            if get_string_from_joint_paramters(parameters):
                str_joint_data = f"{str(parameters[0])[1:-1]}, {'Table, Table, Table, Table'}"

            else:
                str_joint_data = ""
                for value in parameters[0]:
                    str_joint_data += f"{value}, "
                for value in parameters[1]:
                    str_joint_data += f"{value : .2e}, "

            new = QTreeWidgetItem([str(group_id), str_joint_data[:-2]])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_expansion_joint_by_elements.addTopLevelItem(new)

    def load_treeWidgets_info(self):

        self.load_expansion_joint_by_line_info()
        self.load_expansion_joint_by_elements_info()
        self.tabWidget_main.setTabVisible(1, False)

        if self.preprocessor.dict_lines_with_expansion_joints:
            self.tabWidget_main.setTabVisible(1, True)

        if self.preprocessor.group_elements_with_expansion_joints:
            self.tabWidget_main.setTabVisible(1, True)

    def on_click_item_lines(self, item):
        self.label_selection.setText("Line ID:")
        self.lineEdit_selection.setText(item.text(0))
        self.lineEdit_selection.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_click_item_elements(self, item):
        self.label_selection.setText("Element ID:")
        self.lineEdit_selection.setText(item.text(0))
        self.lineEdit_selection.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_doubleclick_item_elements(self, item):
        self.on_click_item_elements(item)
        self.get_information(item)

    def on_doubleclick_item_lines(self, item):
        self.on_click_item_lines(item)
        self.get_information(item)

    def get_information(self, item):
        try:

            if self.lineEdit_selection.text() != "":
                return        

                data = dict()
                for line in self.get_list_typed_entries(item.text(1)):
                    data[line] = ["Enabled"]

                if len(data):
                    self.close()
                    header_labels = ["Lines", "Stress stiffening effect"]
                    GetInformationOfGroup(  group_label = "Stress stiffening effect",
                                            selection_label = "Line ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 140],
                                            data = data  )

                # GetInformationOfGroup(self.project, selection)

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def remove_selected_expansion_joint(self):
        if self.label_selection.text() == "Line ID:":
            self.remove_selected_expansion_joint_by_line()
        else:
            self.remove_selected_expansion_joint_by_group_elements

    def restore_the_cross_section(self, input_elements):

        lists_element_indexes = list()
        first_element_id = min(input_elements)
        last_element_id = max(input_elements)
        lists_element_indexes.append([  first_element_id - 1, 
                                        first_element_id + 1,
                                        last_element_id - 1,  
                                        last_element_id + 1  ])

        line_id = self.preprocessor.elements_to_line[input_elements[0]]
        first_element_id_from_line = self.preprocessor.line_to_elements[line_id][0]
        last_element_id_from_line = self.preprocessor.line_to_elements[line_id][-1]
        lists_element_indexes.append([  first_element_id_from_line - 1, 
                                        first_element_id_from_line + 1, 
                                        last_element_id_from_line - 1,  
                                        last_element_id_from_line + 1  ])

        for element_indexes in lists_element_indexes:
            for element_id in element_indexes:
                if element_id not in input_elements:
                    cross = self.structural_elements[element_id].cross_section
                    element_type = self.structural_elements[element_id].element_type
                    if element_type == 'pipe_1' and cross is not None:
                        self.project.set_cross_section_by_elements(input_elements, cross)
                        self.project.add_cross_sections_expansion_joints_valves_in_file(input_elements)
                        return

    def remove_selected_expansion_joint_by_line(self):

        if self.lineEdit_selection.text() == "":
            title = "Empty selection in expansion joint"
            message = "Please, select an expansion joint in the list "
            message += "before confirm the joint removal."
            PrintMessageInput([window_title_2, title, message])
            return

        line_id = int(self.lineEdit_selection.text())
        self.reset_all_lineEdits()

        if line_id in list(self.preprocessor.dict_lines_with_expansion_joints.keys()):
            joint_elements = self.preprocessor.line_to_elements[line_id]
            self.remove_expansion_joint_by_line(line_id)
            self.restore_the_cross_section(joint_elements)
            self.update_plots()

    def remove_selected_expansion_joint_by_group_elements(self):

        if self.lineEdit_selection.text() == "":
            title = "Empty selection in expansion joint"
            message = "Please, select an expansion joint in the list "
            message += "before confirm the joint removal."
            PrintMessageInput([window_title_2, title, message])
            return

        selected_group = self.lineEdit_selection.text()
        self.remove_expansion_joint_by_group_of_elements(selected_group)
        self.update_plots()

    def remove_expansion_joint_by_line(self, line_id):
        self.remove_table_files_from_imported_data_folder_by_line(line_id)
        self.project.add_expansion_joint_by_line(line_id, None)
        joint_elements = self.preprocessor.line_to_elements[line_id]
        self.restore_the_cross_section(joint_elements)

    def remove_expansion_joint_by_group_of_elements(self, selected_group):

        if selected_group in self.preprocessor.group_elements_with_expansion_joints.keys():
            [joint_elements, _] = self.preprocessor.group_elements_with_expansion_joints[selected_group]
            list_lines = list()
            for element_id in joint_elements:
                line_id = self.preprocessor.elements_to_line[element_id]
                if line_id not in list_lines:
                    list_lines.append(line_id)

        self.remove_table_files_from_imported_data_folder_by_elements(joint_elements)
        
        for line_id in list_lines:

            cross, etype = self.get_pipe_cross_section_from_neighbors(line_id, joint_elements)
            self.preprocessor.set_structural_element_type_by_element(joint_elements, etype)
            self.project.set_cross_section_by_elements(joint_elements, cross)

            self.project.add_expansion_joint_by_elements(   joint_elements, 
                                                            None,  
                                                            update_element_type = False,
                                                            reset_cross = False  )

            if selected_group in self.preprocessor.group_elements_with_expansion_joints.keys():
                self.preprocessor.group_elements_with_expansion_joints.pop(selected_group)

            self.restore_the_cross_section(joint_elements)

    def reset_expansion_joints(self):

        self.setVisible(False)
        title = "Resetting of expansion joints"
        message = "Would you like to remove all expansion joints from the model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            self.setVisible(True)
            return

        temp_dict_1 = self.preprocessor.dict_lines_with_expansion_joints.copy()
        for line_id in temp_dict_1.keys():
            self.remove_expansion_joint_by_line(line_id)

        temp_dict_2 = self.preprocessor.group_elements_with_expansion_joints.copy()
        for group in temp_dict_2.keys(): 
            self.remove_expansion_joint_by_group_of_elements(group)

        self.update_plots()
        self.close()

    def update_plots(self):
        self.load_treeWidgets_info()
        # self.opv.opvRenderer.plot()
        # self.opv.opvAnalysisRenderer.plot()
        self.opv.plot_entities_with_cross_section() 
    
    def remove_table_files_from_imported_data_folder_by_elements(self, list_elements):

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_table_names = []
        list_joint_stiffness = []
        for section in sections:
            keys = list(config[section].keys())
            if 'list of elements' in keys:
                str_list_elements_from_file = config[section]['list of elements']
                if str_list_elements_from_file == str(list_elements):
                    if 'expansion joint stiffness' in keys:
                        read_joint_stiffness = config[section]['expansion joint stiffness']
                        list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
                        cache_section = section

        if list_joint_stiffness == []:
            return

        for stiffness_value in list_joint_stiffness:
            try:
                float(stiffness_value)
                return
            except:
                break

        list_table_multiple_joints = []
        list_table_names = list_joint_stiffness

        for section in sections:
            if section != cache_section:
                keys = list(config[section].keys())
                if 'expansion joint stiffness' in keys:
                    read_table_names = config[section]['expansion joint stiffness']
                    for table_name in list_table_names:
                        if table_name in read_table_names:
                            list_table_multiple_joints.append(table_name)

        if len(list_table_multiple_joints)==0:
            for table_name in list_table_names:
                self.project.remove_structural_table_files_from_folder(table_name, folder_name="expansion_joints_files")
            # self.confirm_table_file_removal(list_table_names)

    def remove_table_files_from_imported_data_folder_by_line(self, line_id):

        str_line_id = str(line_id)
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_table_names = []
        list_joint_stiffness = []
        if str_line_id in sections:
            keys = list(config[str_line_id].keys())
            if 'expansion joint stiffness' in keys:
                read_joint_stiffness = config[str_line_id]['expansion joint stiffness']
                list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
                cache_section = str_line_id
        
        if list_joint_stiffness == []:
            return

        for stiffness_value in list_joint_stiffness:
            try:
                float(stiffness_value)
                return
            except:
                break
        
        list_table_multiple_joints = []
        list_table_names = list_joint_stiffness

        for section in sections:
            if section != cache_section:
                keys = list(config[section].keys())
                if 'expansion joint stiffness' in keys:
                    read_table_names = config[section]['expansion joint stiffness']
                    for table_name in list_table_names:
                        if table_name in read_table_names:
                            list_table_multiple_joints.append(table_name)

        if len(list_table_multiple_joints)==0:
            for table_name in list_table_names:
                self.project.remove_structural_table_files_from_folder(table_name, folder_name="expansion_joints_files")
            # self.confirm_table_file_removal(list_table_names)

    def confirm_table_file_removal(self, list_tables):

        title = "Removal of imported table files"
        
        message = "Would you like to remove the following unused imported table from the project folder?\n\n"
        for table in list_tables:
            message += f"{table}\n"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            return

        if read._continue:
            for table_name in list_tables:
                self.project.remove_structural_table_files_from_folder(table_name, folder_name="expansion_joints_files")
            # self.project.remove_structural_empty_folders(folder_name="expansion_joints_tables")             

    def write_ids(self, list_selected_ids):
        text = ""
        for _id in list_selected_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text[:-2])  
        if self.check_selection_type():
            return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_expansion_joint()
        if event.key() == Qt.Key_Escape:
            self.close()

def get_list_cross_sections_to_plot_expansion_joint(list_elements, effective_diameter):

    """"
        This auxiliary function returns a list of cross-sections 
        from the expansion joint.
    """

    list_cross_sections = list()
    flanges_elements = [    list_elements[0],
                            list_elements[1],
                            list_elements[-2],
                            list_elements[-1]  ]

    for element in list_elements:

        if element in flanges_elements:
            plot_key = "flanges"
        else:
            if np.remainder(element, 2) == 0:
                plot_key = "minor"
            else:
                plot_key = "major"

        expansion_joint_info = [    "Expansion joint section", 
                                    plot_key,
                                    effective_diameter ]

        cross = CrossSection(expansion_joint_info = expansion_joint_info)
        list_cross_sections.append(cross)

    return list_cross_sections 

def get_string_from_joint_paramters(parameters):
    for parameter in parameters:
        for value in parameter:
            if isinstance(value, np.ndarray):
                return True
    return False

    