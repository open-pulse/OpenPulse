from PyQt5.QtWidgets import QAction, QComboBox, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.setup.cross_section.cross_section_inputs import CrossSectionWidget
from pulse.preprocessing.cross_section import CrossSection
from pulse.tools.utils import *

import configparser
import matplotlib.pyplot as plt

window_title = "Error"

class SetCrossSectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/cross_section/set_cross_section.ui"
        uic.loadUi(ui_path, self)

        self.pipe_to_beam = kwargs.get("pipe_to_beam", False)
        self.beam_to_pipe = kwargs.get("beam_to_pipe", False)

        self.lines_to_update_cross_section = kwargs.get("lines_to_update_cross_section", list())
        self.elements_to_update_cross_section = kwargs.get("elements_to_update_cross_section", list())

        app().main_window.set_input_widget(self)
        self.project = app().project

        self.preprocessor = self.project.preprocessor
        self.file = self.project.file
       
        self.input_widget = CrossSectionWidget()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_treeWidget()
        self.selection_callback()
        self.load_existing_sections()
        self.initial_condition()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.section_id_by_lines = None
        self.section_id_by_elements = None
        self.section_type = None
        self.section_parameters = None
        self.section_info = None
        self._element_type = None
        self._section_parameters = None

        self.complete = False
        self.stop = False
        self.flip = False

        self.currentTab = 0
        self.list_elements = list()
        self.section_data_lines = dict()
        self.section_data_elements = dict()
        self.remove_expansion_joint_tables_files = True

        self.structural_elements = self.project.preprocessor.structural_elements
        self.lines_from_model = self.project.preprocessor.lines_from_model

        self.before_run = self.project.get_pre_solution_model_checks()

        self.psd_lines = self.project.PSD.get_device_related_lines()

    def _define_qt_variables(self):

        # QAction
        self.action_all_lines = QAction(self)
        # self.action_all_lines.setVisible(False)
        self.action_all_lines.setShortcut("Ctrl+A")
        self.action_all_lines.triggered.connect(self.select_all_lines_callback)
        self.addAction(self.action_all_lines)

        # QComboBox
        self.comboBox_selection : QComboBox

        # QFrame
        self.main_frame : QFrame

        # QGridLayout
        self.grid_layout = self.main_frame.layout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.input_widget)

        # QLabel
        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        
        # QLineEdit
        self.lineEdit_selected_id = self.findChild(QLineEdit, 'lineEdit_selected_id')
        self.lineEdit_selected_id.setEnabled(True)

        # QPushButton
        self.pushButton_confirm_pipe = self.findChild(QPushButton, 'pushButton_confirm_pipe')
        self.pushButton_confirm_beam = self.findChild(QPushButton, 'pushButton_confirm_beam')
        self.pushButton_flip_element_ids_initial = self.findChild(QPushButton, 'pushButton_flip_element_ids_initial')
        self.pushButton_flip_element_ids_final = self.findChild(QPushButton, 'pushButton_flip_element_ids_final')
        self.pushButton_load_section_info = self.findChild(QPushButton, "pushButton_load_section_info")
        self.pushButton_plot_pipe_cross_section = self.findChild(QPushButton, 'pushButton_plot_pipe_cross_section')
        self.pushButton_plot_beam_cross_section = self.findChild(QPushButton, 'pushButton_plot_beam_cross_section')
        self.pushButton_select_standard_section = self.findChild(QPushButton, 'pushButton_select_standard_section')
        self.pushButton_select_standard_section_initial = self.findChild(QPushButton, 'pushButton_select_standard_section_initial')
        self.pushButton_select_standard_section_final = self.findChild(QPushButton, 'pushButton_select_standard_section_final')
        self.pushButton_check_if_section_is_normalized = self.findChild(QPushButton, 'pushButton_check_if_section_is_normalized')

        # QTabWidget
        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_pipe_section = self.findChild(QTabWidget, 'tabWidget_pipe_section')
        self.tabWidget_beam_section = self.findChild(QTabWidget, 'tabWidget_beam_section')
        self.tabWidget_sections_data = self.findChild(QTabWidget, 'tabWidget_sections_data')

        # QTreeWidget
        self.treeWidget_sections_parameters_by_lines = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_lines')
        self.treeWidget_sections_parameters_by_elements = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_elements')  
            
    def _create_connections(self):
        #
        self.comboBox_selection.currentIndexChanged.connect(self.update_selection)
        #
        self.lineEdit_selected_id.editingFinished.connect(self.update_highlights)
        #
        self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe)
        self.pushButton_confirm_beam.clicked.connect(self.confirm_beam)
        self.pushButton_flip_element_ids_initial.clicked.connect(self.flip_element_ids)
        self.pushButton_flip_element_ids_final.clicked.connect(self.flip_element_ids)
        self.pushButton_load_section_info.clicked.connect(self.load_section_info)
        #
        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        self.tabWidget_pipe_section.currentChanged.connect(self.tabEvent_pipe)
        #
        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_elements.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_element)
        self.treeWidget_sections_parameters_by_elements.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_element)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:
            selected_ids = selected_lines

        elif selected_elements:
            selected_ids = selected_elements

        else:
            return

        if selected_ids:
            self.write_ids(selected_ids)

        self.input_widget.reset_all_input_texts()
        self.update_line_and_element_ids(selected_lines, selected_elements)

        if len(selected_lines) == 1:   
            self.selection = self.lines_from_model[selected_lines[0]]
            element_type = self.selection.structural_element_type
            if element_type is None:
                for element_id in self.preprocessor.line_to_elements[selected_lines[0]]:
                    element = self.structural_elements[element_id]
                    element_type = element.element_type
                    if element_type in ["pipe_1", "beam_1"]:
                        break
            _variable_cross_section_data = self.selection.variable_cross_section_data

        elif len(selected_elements) == 1:
            self.selection = self.structural_elements[selected_elements[0]]
            element_type = self.selection.element_type
            _variable_cross_section_data = None

        else:
            return

        if _variable_cross_section_data is None:
            if self.selection.cross_section is not None:

                cross = self.selection.cross_section
                self.section_label = cross.section_info["section_type_label"]
                self.section_parameters = cross.section_info["section_parameters"]
                        
                if element_type == 'pipe_1':
                    self.tabWidget_general.setCurrentIndex(0)
                    self.tabWidget_pipe_section.setCurrentIndex(0)
                                
                elif element_type in ['beam_1']:
                    self.tabWidget_general.setCurrentIndex(1)

                self.update_section_entries()

        else:

            if element_type == 'pipe_1':
                self.tabWidget_general.setCurrentIndex(0)
                if self.selection.variable_cross_section_data:
                    self.tabWidget_pipe_section.setCurrentIndex(1)
                    self.update_section_entries(variable_section=True)

            # elif element_type in ['beam_1']:
            #     self.tabWidget_general.setCurrentIndex(1)

        self.update_tabs()

    def load_existing_sections(self):

        self.section_id_data_lines = dict()
        self.section_id_data_elements = dict()
        self.treeWidget_sections_parameters_by_lines.clear()
        self.treeWidget_sections_parameters_by_elements.clear()
        self.section_data_lines, self.section_data_elements = self.file.get_cross_sections_from_file()

        if len(self.section_data_elements) + len(self.section_data_lines) == 0:
            self.tabWidget_general.setTabVisible(2, False)

        elif len(self.section_data_lines) == 0:
            self.tabWidget_sections_data.setTabVisible(0, False)

        elif len(self.section_data_elements) == 0:
            self.tabWidget_sections_data.setTabVisible(1, False)

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_lines.items():
            if section_parameters:
                self.section_id_data_lines[section_id] = [tag_type, tags]
                str_parameters = str(section_parameters)[1:-1]
                new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_elements.items():
            if section_parameters:
                self.section_id_data_elements[section_id] = [tag_type, tags]
                str_parameters = str(section_parameters)[1:-1]
                new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_sections_parameters_by_elements.addTopLevelItem(new)

    def _config_treeWidget(self):
        #
        self.pushButton_load_section_info.setDisabled(True)
        #
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,120)
        #
        self.treeWidget_sections_parameters_by_elements.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_elements.setColumnWidth(1,120)

    def initial_condition(self):

        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentIndex(1)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_general.setTabEnabled(1, False)
        
        if self.lines_to_update_cross_section:
            # self.label_selected_id.setText("Lines IDs:")
            self.comboBox_selection.setCurrentIndex(1)
            self.write_ids(self.lines_to_update_cross_section)

        elif self.elements_to_update_cross_section:
            # self.label_selected_id.setText("Elements IDs:")
            self.comboBox_selection.setCurrentIndex(2)
            self.write_ids(self.elements_to_update_cross_section)

        else:
            return

        self.update_selection()
        
    def write_ids(self,  selected_ids : list):
        text = ", ".join([str(i) for i in selected_ids])
        self.lineEdit_selected_id.setText(text)

    def on_click_treeWidget_section_parameters_by_line(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_lines = int(key)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                self.pushButton_load_section_info.setDisabled(False)
                [self._element_type, self._section_parameters, *args] = self.section_data_lines[int(key)]

    def on_doubleClick_treeWidget_section_parameters_by_line(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_lines = int(key)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                [self._element_type, self._section_parameters, *args] = self.section_data_lines[int(key)]
                self.load_section_info()

    def on_click_treeWidget_section_parameters_by_element(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_elements = int(key)
        if key != "":
            if int(key) in self.section_data_elements.keys():
                self.pushButton_load_section_info.setDisabled(False)
                [self._element_type, self._section_parameters, *args] = self.section_data_elements[int(key)]

    def on_doubleClick_treeWidget_section_parameters_by_element(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_elements = int(key)
        if key != "":
            if int(key) in self.section_data_elements.keys():
                [self._element_type, self._section_parameters, *args] = self.section_data_elements[int(key)]
                self.load_section_info()

    def load_section_info(self):
        self.input_widget.reset_all_input_texts()
        if self._element_type is not None:
            if self._element_type == "pipe_1":

                if len(self._section_parameters) == 6:
                    for index, lineEdit in enumerate(self.input_widget.list_constant_pipe_entries):
                        lineEdit.setText(str(self._section_parameters[index]))
                    self.tabWidget_general.setCurrentIndex(0)
                    self.tabWidget_pipe_section.setCurrentIndex(0)

                elif len(self._section_parameters) == 10:
                    for index, lineEdit in enumerate(self.input_widget.list_variable_pipe_entries):
                        lineEdit.setText(str(self._section_parameters[index]))
                    self.tabWidget_general.setCurrentIndex(0)
                    self.tabWidget_pipe_section.setCurrentIndex(1)
            
            elif "beam_1" in self._element_type:
                
                section_type = self._element_type.split("beam_1 - ")[1]
                self.tabWidget_general.setCurrentIndex(1)
                
                if section_type == "Rectangular section":
                    self.tabWidget_beam_section.setCurrentIndex(0)
                    [base, height, base_in, height_in, offset_y, offset_z] = self._section_parameters
                    self.section_type = 1
                    self.input_widget.lineEdit_base_rectangular_section.setText(str(base))
                    self.input_widget.lineEdit_height_rectangular_section.setText(str(height))
                    self.input_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
                    if base_in != 0 and height_in != 0:
                        self.input_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 

                if section_type == "Circular section":
                    self.tabWidget_beam_section.setCurrentIndex(1)
                    [outside_diameter_beam, thickness, offset_y, offset_z] = self._section_parameters
                    self.section_type = 2
                    self.input_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
                    self.input_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
                    if thickness != 0:
                        self.input_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))

                if section_type == "C-section":
                    self.tabWidget_beam_section.setCurrentIndex(2)
                    [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 3
                    self.input_widget.lineEdit_height_C_section.setText(str(h))
                    self.input_widget.lineEdit_w1_C_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_C_section.setText(str(tw))
                    self.input_widget.lineEdit_w2_C_section.setText(str(w2))
                    self.input_widget.lineEdit_t1_C_section.setText(str(t1))   
                    self.input_widget.lineEdit_t2_C_section.setText(str(t2))
                    self.input_widget.lineEdit_offsety_C_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_C_section.setText(str(offset_z))  

                if section_type == "I-section":
                    self.tabWidget_beam_section.setCurrentIndex(3)
                    [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 4
                    self.input_widget.lineEdit_height_I_section.setText(str(h))
                    self.input_widget.lineEdit_w1_I_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_I_section.setText(str(tw))
                    self.input_widget.lineEdit_w2_I_section.setText(str(w2))
                    self.input_widget.lineEdit_t1_I_section.setText(str(t1))   
                    self.input_widget.lineEdit_t2_I_section.setText(str(t2))
                    self.input_widget.lineEdit_offsety_I_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_I_section.setText(str(offset_z))

                if section_type == "T-section":
                    self.tabWidget_beam_section.setCurrentIndex(4)
                    [h, w1, t1, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 5
                    self.input_widget.lineEdit_height_T_section.setText(str(h))
                    self.input_widget.lineEdit_w1_T_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_T_section.setText(str(tw))
                    self.input_widget.lineEdit_t1_T_section.setText(str(t1))
                    self.input_widget.lineEdit_offsety_T_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_T_section.setText(str(offset_z))

                if section_type == "Generic section":
                    self.tabWidget_beam_section.setCurrentIndex(5)
        
        if self.section_id_by_lines in self.section_id_data_lines.keys():

            [tag_type, lines] = self.section_id_data_lines[self.section_id_by_lines]

            str_lines = str(lines)
            if tag_type == "line ids":

                self.comboBox_selection.setCurrentIndex(1)
                app().main_window.set_selection(lines = lines)

                if len(self._section_parameters) == 10:
                    if len(lines) == 1:
                        line_elements = self.project.preprocessor.line_to_elements[lines[0]]
                        self.input_widget.lineEdit_element_id_initial.setText(str(line_elements[0]))
                        self.input_widget.lineEdit_element_id_final.setText(str(line_elements[-1]))

        if self.section_id_by_elements in self.section_id_data_elements.keys():
            [tag_type, lines] = self.section_id_data_elements[self.section_id_by_elements]
            str_lines = str(lines)
            if tag_type == "element ids":
                self.comboBox_selection.setCurrentIndex(2)
                app().main_window.set_selection(lines = lines)

        self.lineEdit_selected_id.setText(str_lines[1:-1])
        
        self.section_id_by_lines = None
        self.section_id_by_elements = None
        self._element_type = None
        self._section_parameters = None

    def check_variable_section_pipe(self):
        
        if self.input_widget.get_variable_section_pipe_parameters():
            return

        section_info = self.input_widget.pipe_section_info
        self.project.set_variable_cross_section_by_line(self.lines_typed[0], section_info)
        # self.project.add_cross_sections_expansion_joints_valves_in_file(self.list_elements)
        self.project.set_structural_element_type_by_lines(self.lines_typed[0], self.element_type)
        self.file.modify_variable_cross_section_in_file(self.lines_typed[0], section_info)
        # self.project.set_variable_cross_section_by_line(self.lines_typed[0], section_info)
        self.project._set_variable_cross_section_to_selected_line(self.lines_typed[0], section_info)
        self.project.reset_number_sections_by_line(self.lines_typed[0])
        self.actions_to_finalize()

    def update_section_entries(self, variable_section=False):
 
        if variable_section:

            self.update_variable_section_element_ids()   
            section_parameters = self.selection.variable_cross_section_data["section_parameters"]

            for index, lineEdit in enumerate(self.input_widget.list_pipe_section_entries[6:-2]):
                lineEdit.setText(str(section_parameters[index]))
            
            return

        if 'Pipe section' in self.section_label:

            outside_diameter = self.section_parameters[0]
            thickness = self.section_parameters[1]
            offset_y = self.section_parameters[2] 
            offset_z = self.section_parameters[3]
            insulation_thickness = self.section_parameters[4]
            insulation_density = self.section_parameters[5]

            self.section_type = 0
            self.input_widget.lineEdit_outside_diameter.setText(str(outside_diameter))
            self.input_widget.lineEdit_wall_thickness.setText(str(thickness))

            if offset_y != 0:
                self.input_widget.lineEdit_offset_y.setText(str(offset_y))

            if offset_z != 0:
                self.input_widget.lineEdit_offset_z.setText(str(offset_z))

            if insulation_density != 0:
                self.input_widget.lineEdit_insulation_density.setText(str(insulation_density))

            if insulation_thickness != 0:
                self.input_widget.lineEdit_insulation_thickness.setText(str(insulation_thickness))

        elif self.section_label == 'Rectangular section':
            [base, height, base_in, height_in, offset_y, offset_z] = self.section_parameters
            self.section_type = 1
            self.input_widget.lineEdit_base_rectangular_section.setText(str(base))
            self.input_widget.lineEdit_height_rectangular_section.setText(str(height))
            self.input_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
            if base_in != 0 and height_in != 0:
                self.input_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 
        
        elif self.section_label == 'Circular section':
            [outside_diameter_beam, thickness, offset_y, offset_z] = self.section_parameters
            self.section_type = 2
            self.input_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
            self.input_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
            if thickness != 0:
                self.input_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))
        
        elif self.section_label == 'C-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 3
            self.input_widget.lineEdit_height_C_section.setText(str(h))
            self.input_widget.lineEdit_w1_C_section.setText(str(w1))
            self.input_widget.lineEdit_tw_C_section.setText(str(tw))
            self.input_widget.lineEdit_w2_C_section.setText(str(w2))
            self.input_widget.lineEdit_t1_C_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_C_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_C_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_C_section.setText(str(offset_z))             
        
        elif self.section_label == 'I-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 4
            self.input_widget.lineEdit_height_I_section.setText(str(h))
            self.input_widget.lineEdit_w1_I_section.setText(str(w1))
            self.input_widget.lineEdit_tw_I_section.setText(str(tw))
            self.input_widget.lineEdit_w2_I_section.setText(str(w2))
            self.input_widget.lineEdit_t1_I_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_I_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_I_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_I_section.setText(str(offset_z))
        
        elif self.section_label == 'T-section':
            [h, w1, t1, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 5
            self.input_widget.lineEdit_height_T_section.setText(str(h))
            self.input_widget.lineEdit_w1_T_section.setText(str(w1))
            self.input_widget.lineEdit_tw_T_section.setText(str(tw))
            self.input_widget.lineEdit_t1_T_section.setText(str(t1))
            self.input_widget.lineEdit_offsety_T_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_T_section.setText(str(offset_z))  

    def update_variable_section_element_ids(self):
        lines_id = app().main_window.list_selected_lines()
        if len(lines_id) > 0:
            line_id = lines_id[0]
            # entity = self.lines_from_model[line_id]
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_pipe_section.setCurrentIndex(1)
            if len(lines_id) == 1:
                self.list_elements = self.project.preprocessor.line_to_elements[line_id]
                self.input_widget.lineEdit_element_id_initial.setText(str(self.list_elements[0]))
                self.input_widget.lineEdit_element_id_final.setText(str(self.list_elements[-1]))
    
    def update_tabs(self):
        if self.tabWidget_general.currentIndex() == 0:
            if self.tabWidget_pipe_section.currentIndex() == 1:
                return
       
        if self.section_type == 0:
            self.tabWidget_pipe_section.setCurrentIndex(0)
            return

        for i in range(6):
            if i+1 == self.section_type:
                self.tabWidget_beam_section.setCurrentIndex(i)

    def check_if_lines_belongs_to_psd(self, lines):
        for psd_lines in self.psd_lines.values():
            for line in lines:
                if line in psd_lines:
                    self.lineEdit_selected_id.setText("")
                    title = "PSD cross-section edition not allowed"
                    message = "The PSD line sections could not be edited in the cross-section setup interface. "
                    message += "You must switch to the PSD configuration interface for this specific section editing."
                    PrintMessageInput([window_title_2, title, message])
                    return True

    def update_line_and_element_ids(self, lines_id, elements_id):

        if self.check_if_lines_belongs_to_psd(lines_id):
            return

        self.comboBox_selection.blockSignals(True)
        if lines_id:
            self.label_selected_id.setText("Lines IDs:")
            self.comboBox_selection.setCurrentIndex(1)

        elif elements_id:
            self.label_selected_id.setText("Elements IDs:")
            self.comboBox_selection.setCurrentIndex(2)

        self.comboBox_selection.blockSignals(False)

    def select_all_lines_callback(self):

        self.comboBox_selection.setCurrentIndex(0)
        self.label_selected_id.setText("Lines IDs:")
        self.lineEdit_selected_id.setText("All lines")

    def update_highlights(self):

        lineEdit = self.lineEdit_selected_id.text()
        selection_index = self.comboBox_selection.currentIndex()
        if lineEdit != "":

            if selection_index == 1:
                _stop, _lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
                if _stop:
                    return
                app().main_window.set_selection(lines = _lines_typed)

            if selection_index == 2:
                _stop, _elements_typed = self.before_run.check_selected_ids(lineEdit, "elements")
                if _stop:
                    return
                app().main_window.set_selection(elements = _elements_typed) 

    def flip_element_ids(self):
        self.flip = not self.flip
        temp_initial = self.input_widget.lineEdit_element_id_initial.text()
        temp_final = self.input_widget.lineEdit_element_id_final.text()
        self.input_widget.lineEdit_element_id_initial.setText(temp_final)
        self.input_widget.lineEdit_element_id_final.setText(temp_initial)

    def update_selection(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)

        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        elif selection_index == 1:
            self.label_selected_id.setText("Lines IDs:")
                    
        elif selection_index == 2:
            self.label_selected_id.setText("Elements IDs:")
    
    def tabEvent_cross_section(self):
        if self.tabWidget_general.currentIndex() == 0:
            if self.tabWidget_pipe_section.currentIndex() == 1:
                self.tabEvent_pipe()
            for i in range(2):
                self.tabWidget_pipe_section.setTabEnabled(i, True)
        else:
            self.comboBox_selection.setDisabled(True)
            for i in range(6):
                self.tabWidget_beam_section.setTabEnabled(i, True)

    def tabEvent_pipe(self):
        self.comboBox_selection.setDisabled(False)
        if self.tabWidget_pipe_section.currentIndex() == 0:
            self.pushButton_plot_pipe_cross_section.setDisabled(False)

        if self.tabWidget_pipe_section.currentIndex() == 1:
            self.pushButton_plot_pipe_cross_section.setDisabled(True)
            self.comboBox_selection.setCurrentIndex(1)
            self.comboBox_selection.setDisabled(True)
            self.update_variable_section_element_ids()

    def actions_to_finalize(self):

        plt.close()
        self.complete = True
        app().main_window.update_plots()

        build_data = self.file.get_pipeline_data_from_file()
        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(self.file.length_unit)
        geometry_handler.process_pipeline(build_data)

        self.close()

    def load_project(self):
        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_ui.initial_project_action(True)
        self.complete = True

    def check_constant_pipe(self, plot=False):

        if self.input_widget.get_constant_pipe_parameters():
            return

        self.section_label = self.input_widget.section_label
        self.section_parameters = self.input_widget.section_parameters
        self.section_properties = self.input_widget.section_properties
        self.pipe_section_info = self.input_widget.pipe_section_info

        if plot:
            return
        
        self.cross_section = CrossSection(pipe_section_info=self.pipe_section_info)

        self.set_cross_sections()
        self.actions_to_finalize()

    def confirm_pipe(self):
        
        self.element_type = 'pipe_1'
        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 2:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.elements_typed = self.before_run.check_selected_ids(lineEdit, "elements")
            if self.stop:
                return

        elif selection_index == 1:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True 

        if self.tabWidget_pipe_section.currentIndex() == 0:
            self.check_constant_pipe()

        elif self.tabWidget_pipe_section.currentIndex() == 1:
            self.check_variable_section_pipe()

    def confirm_beam(self):
        self.element_type = 'beam_1'
        self.check_beam()

    def check_beam(self):

        selection_index = self.comboBox_selection.currentIndex()
        
        if selection_index == 0:
            self.lines_typed = list(self.preprocessor.lines_from_model.keys())

        elif selection_index == 1:
            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True        

        if self.tabWidget_general.currentIndex() == 1:

            if self.input_widget.get_beam_section_parameters():
                return

            self.section_label = self.input_widget.section_label
            self.section_parameters = self.input_widget.section_parameters
            self.section_properties = self.input_widget.section_properties

            self.beam_section_info = {  "section_type_label" : self.section_label,
                                        "section_parameters" : self.section_parameters,
                                        "section_properties" : self.section_properties  }

            self.cross_section = CrossSection(beam_section_info=self.beam_section_info)

            self.set_cross_sections()
            self.project.set_capped_end_by_lines(self.lines_typed, False)
            self.project.set_structural_element_wall_formulation_by_lines(self.lines_typed, None)

        self.actions_to_finalize()

    def set_cross_sections(self):
        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 1:

            if self.check_if_lines_belongs_to_psd(self.lines_typed):
                return

            if self.remove_expansion_joint_tables_files:
                self.process_expansion_joint_table_files_removal(self.lines_typed)

            for line_id in self.lines_typed:
                self.project.reset_number_sections_by_line(line_id)

            self.project.add_valve_by_line(line_id, None, reset_cross=False)
            self.project._set_expansion_joint_to_selected_lines(self.lines_typed, None)

            self.project.set_cross_section_by_lines(self.lines_typed, self.cross_section)
            self.project.set_structural_element_type_by_lines(self.lines_typed, self.element_type)

            if len(self.lines_typed) < 20:
                print("[Set Cross-section] - defined at the {} lines".format(self.lines_typed))
            else:
                print("[Set Cross-section] - defined at {} selected lines".format(len(self.lines_typed)))

        elif selection_index == 2:

            self.project.set_cross_section_by_elements(self.elements_typed, self.cross_section)
            self.project.add_cross_sections_expansion_joints_valves_in_file(self.elements_typed)
            # self.preprocessor.set_structural_element_type_by_element(self.elements_typed, self.element_type)
            
            if len(self.elements_typed) < 20:
                print("[Set Cross-section] - defined at the {} elements".format(self.elements_typed))
            else:
                print("[Set Cross-section] - defined at {} selected elements".format(len(self.elements_typed)))

        else:

            line_ids = list(self.preprocessor.lines_from_model.keys())
            if self.check_if_lines_belongs_to_psd(line_ids):
                return

            if self.remove_expansion_joint_tables_files:
                self.process_expansion_joint_table_files_removal(line_ids)

            self.project.add_valve_by_line(line_ids, None, reset_cross=False)
            self.project._set_expansion_joint_to_selected_lines(line_ids, None)

            self.project.set_cross_section_by_lines(line_ids, self.cross_section)
            self.project.set_structural_element_type_to_all(self.element_type)
            
            print("[Set Cross-section] - defined at all lines") 
        
        self.preprocessor.add_lids_to_variable_cross_sections()

    def process_expansion_joint_table_files_removal(self, list_line_ids):

        config = configparser.ConfigParser()
        config.read(self.project.file._pipeline_path)
        sections = config.sections()

        for section in sections:
            if "-" in section:
                line_id = int(section.split("-")[0])
            else:
                line_id = int(section)

            if line_id in list_line_ids:
                if "expansion joint stiffness" in config[section].keys():
                    str_joint_stiffness = config[section]['expansion joint stiffness']
                    _, joint_table_names, _ = self.project.file._get_expansion_joint_stiffness_from_string(str_joint_stiffness)
                    if joint_table_names is not None:
                        for table_name in joint_table_names:
                            self.project.remove_structural_table_files_from_folder(table_name, "expansion_joints_files")
   
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.confirm_pipe()
            if self.tabWidget_general.currentIndex() == 1:
                self.confirm_beam()

        elif event.key() == Qt.Key_Escape:
            self.close()