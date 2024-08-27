from PyQt5.QtWidgets import QAction, QComboBox, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.model.cross_section import CrossSection
from pulse.tools.utils import *

from collections import defaultdict

window_title = "Error"

class SetCrossSectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/cross_section/set_cross_section.ui"
        uic.loadUi(ui_path, self)

        self.pipe_to_beam = kwargs.get("pipe_to_beam", False)
        self.beam_to_pipe = kwargs.get("beam_to_pipe", False)
        self.lines_to_update_cross_section = kwargs.get("lines_to_update_cross_section", list())

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.preprocessor
        self.before_run = app().project.get_pre_solution_model_checks()

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

        self.section_id = None

        self.complete = False
        self.stop = False
        self.flip = False
  
        self.section_data_lines = dict()

    def _define_qt_variables(self):

        # QAction
        self.action_all_lines = QAction(self)
        # self.action_all_lines.setVisible(False)
        self.action_all_lines.setShortcut("Ctrl+A")
        self.action_all_lines.triggered.connect(self.select_all_lines_callback)
        self.addAction(self.action_all_lines)

        # QComboBox
        self.comboBox_attribution_type : QComboBox

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
            
    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.lineEdit_selected_id.editingFinished.connect(self.update_highlights)
        #
        self.pushButton_confirm_pipe.clicked.connect(self.pipe_section_attribution_callback)
        self.pushButton_confirm_beam.clicked.connect(self.beam_section_attribution_callback)
        self.pushButton_flip_element_ids_initial.clicked.connect(self.flip_element_ids)
        self.pushButton_flip_element_ids_final.clicked.connect(self.flip_element_ids)
        self.pushButton_load_section_info.clicked.connect(self.load_section_info)
        #
        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        #
        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.single_click_item_callback)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.double_click_item_callback)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.attribution_type_callback()

    def selection_callback(self):

        self.input_widget.reset_all_input_texts()
        self.comboBox_attribution_type.blockSignals(True)

        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:
            self.write_ids(selected_lines)
            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if self.check_if_lines_belongs_to_psd(selected_lines):
                return

            if len(selected_lines) == 1:

                line_id = selected_lines[0]
                element_type = self.properties._get_property("structural_element_type", line_id=line_id)

                if element_type is None:
                    return

                section_parameters = self.properties._get_property("section_parameters", line_id=line_id)
                section_type = self.properties._get_property("section_type_label", line_id=line_id)

                if element_type == "pipe_1":
                    self.tabWidget_general.setCurrentIndex(0)
                    if len(section_parameters) == 6:
                        self.update_section_entries(section_type,
                                                    section_parameters)
                    else:
                        self.update_section_entries(section_type,
                                                    section_parameters,
                                                    variable_section=True)

                elif element_type == "beam_1":
                    self.tabWidget_general.setCurrentIndex(1)
                    self.update_section_entries(section_type,
                                                section_parameters)

        self.comboBox_attribution_type.blockSignals(False)

    def update_section_entries(self, section_type: str, section_parameters: list, variable_section=False):

        if variable_section:

            self.update_variable_section_element_ids()
            self.tabWidget_pipe_section.setCurrentIndex(1) 

            for index, lineEdit in enumerate(self.input_widget.list_pipe_section_entries[6:-2]):
                lineEdit.setText(str(section_parameters[index]))
            
            return

        if 'Pipe' in section_type:

            outside_diameter = section_parameters[0]
            thickness = section_parameters[1]
            offset_y = section_parameters[2]
            offset_z = section_parameters[3]
            insulation_thickness = section_parameters[4]
            insulation_density = section_parameters[5]

            self.tabWidget_pipe_section.setCurrentIndex(0)
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

        elif section_type == 'Rectangular section':
            [base, height, base_in, height_in, offset_y, offset_z] = section_parameters
            self.tabWidget_beam_section.setCurrentIndex(0)
            self.input_widget.lineEdit_base_rectangular_section.setText(str(base))
            self.input_widget.lineEdit_height_rectangular_section.setText(str(height))
            self.input_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
            if base_in != 0 and height_in != 0:
                self.input_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 

        elif section_type == 'Circular section':
            [outside_diameter_beam, thickness, offset_y, offset_z] = section_parameters
            self.tabWidget_beam_section.setCurrentIndex(1)
            self.input_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
            self.input_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
            if thickness != 0:
                self.input_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))

        elif section_type == 'C-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
            self.tabWidget_beam_section.setCurrentIndex(2)
            self.input_widget.lineEdit_height_C_section.setText(str(h))
            self.input_widget.lineEdit_w1_C_section.setText(str(w1))
            self.input_widget.lineEdit_tw_C_section.setText(str(tw))
            self.input_widget.lineEdit_w2_C_section.setText(str(w2))
            self.input_widget.lineEdit_t1_C_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_C_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_C_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_C_section.setText(str(offset_z))             

        elif section_type == 'I-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
            self.tabWidget_beam_section.setCurrentIndex(3)
            self.input_widget.lineEdit_height_I_section.setText(str(h))
            self.input_widget.lineEdit_w1_I_section.setText(str(w1))
            self.input_widget.lineEdit_tw_I_section.setText(str(tw))
            self.input_widget.lineEdit_w2_I_section.setText(str(w2))
            self.input_widget.lineEdit_t1_I_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_I_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_I_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_I_section.setText(str(offset_z))

        elif section_type == 'T-section':
            [h, w1, t1, tw, offset_y, offset_z] = section_parameters
            self.tabWidget_beam_section.setCurrentIndex(4)
            self.input_widget.lineEdit_height_T_section.setText(str(h))
            self.input_widget.lineEdit_w1_T_section.setText(str(w1))
            self.input_widget.lineEdit_tw_T_section.setText(str(tw))
            self.input_widget.lineEdit_t1_T_section.setText(str(t1))
            self.input_widget.lineEdit_offsety_T_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_T_section.setText(str(offset_z))

        else:
            self.tabWidget_beam_section.setCurrentIndex(5)

    def update_variable_section_element_ids(self):
        lines_id = app().main_window.list_selected_lines()
        if len(lines_id) == 1:

            line_id = lines_id[0]
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_pipe_section.setCurrentIndex(1)

            element_ids = app().project.model.mesh.line_to_elements[line_id]
            self.input_widget.lineEdit_element_id_initial.setText(str(element_ids[0]))
            self.input_widget.lineEdit_element_id_final.setText(str(element_ids[-1]))

    def load_existing_sections(self):

        self.treeWidget_sections_parameters_by_lines.clear()
        self.section_data_lines = app().loader.get_cross_sections_from_file()

        if len(self.section_data_lines) == 0:
            self.tabWidget_general.setTabVisible(2, False)
            return      

        for section_id, section_data in self.section_data_lines.items():

            [element_type, section_parameters, section_type, _] = section_data

            if section_parameters:

                str_parameters = str(section_parameters)[1:-1]
                new = QTreeWidgetItem([str(section_id), element_type, section_type, str_parameters])
                for i in range(4):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)

    def _config_treeWidget(self):
        #
        self.pushButton_load_section_info.setDisabled(True)
        #
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,100)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(2,100)

    def initial_condition(self):

        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentIndex(1)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_general.setTabEnabled(1, False)
        
        if self.lines_to_update_cross_section:
            self.comboBox_attribution_type.setCurrentIndex(1)
            self.write_ids(self.lines_to_update_cross_section)
        
    def write_ids(self,  selected_ids : list):
        text = ", ".join([str(i) for i in selected_ids])
        self.lineEdit_selected_id.setText(text)

    def single_click_item_callback(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        if int(key) in self.section_data_lines.keys():
            self.section_id = int(key)
            self.pushButton_load_section_info.setDisabled(False)

    def double_click_item_callback(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        if int(key) in self.section_data_lines.keys():
            self.section_id = int(key)
            self.load_section_info()

    def load_section_info(self):

        self.input_widget.reset_all_input_texts()

        if self.section_id is None:
            return

        [element_type, section_parameters, section_type, line_ids] = self.section_data_lines[self.section_id]
        app().main_window.set_selection(lines = line_ids)

        if element_type == "pipe_1":
            self.tabWidget_general.setCurrentIndex(0)

            if len(section_parameters) == 6:
                self.update_section_entries(section_type,
                                            section_parameters,
                                            variable_section=False)

            elif len(section_parameters) == 10:
                self.update_section_entries(section_type,
                                            section_parameters,
                                            variable_section=True)

                if len(line_ids) == 1:
                    line_elements = app().project.model.mesh.line_to_elements[line_ids[0]]
                    self.input_widget.lineEdit_element_id_initial.setText(str(line_elements[0]))
                    self.input_widget.lineEdit_element_id_final.setText(str(line_elements[-1]))

        elif element_type == "beam_1":
            self.tabWidget_general.setCurrentIndex(1)

            self.update_section_entries(section_type,
                                        section_parameters,
                                        variable_section=False)    

    def check_if_lines_belongs_to_psd(self, line_ids: list):

        device_related_lines =app().loader.get_psd_related_lines()

        for psd_lines in device_related_lines.values():
            for line_id in line_ids:
                if line_id in psd_lines:
                    self.lineEdit_selected_id.setText("")
                    title = "PSD cross-section edition not allowed"
                    message = "The PSD line sections could not be edited in the cross-section setup interface. "
                    message += "You must switch to the PSD configuration interface for this specific section editing."
                    PrintMessageInput([window_title_2, title, message])
                    return True

    def select_all_lines_callback(self):
        self.comboBox_attribution_type.setCurrentIndex(0)

    def update_highlights(self):

        lineEdit = self.lineEdit_selected_id.text()
        selection_index = self.comboBox_attribution_type.currentIndex()
        if lineEdit != "":

            if selection_index == 1:
                _stop, _lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
                if _stop:
                    return

                app().main_window.set_selection(lines = _lines_typed)

    def flip_element_ids(self):
        self.flip = not self.flip
        temp_initial = self.input_widget.lineEdit_element_id_initial.text()
        temp_final = self.input_widget.lineEdit_element_id_final.text()
        self.input_widget.lineEdit_element_id_initial.setText(temp_final)
        self.input_widget.lineEdit_element_id_final.setText(temp_initial)

    def attribution_type_callback(self):
        
        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            self.selection_callback()

        self.lineEdit_selected_id.setEnabled(bool(index))

    def tabEvent_cross_section(self):
        if self.tabWidget_general.currentIndex() == 2:
            self.comboBox_attribution_type.setDisabled(True)
        else:
            self.comboBox_attribution_type.setDisabled(False)

    def pipe_section_attribution_callback(self):

        if self.comboBox_attribution_type.currentIndex() == 0:
            line_ids = list(app().project.model.mesh.lines_from_model.keys())

        else:

            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return

        if self.check_if_lines_belongs_to_psd(line_ids):
            return

        self.preprocessor.set_structural_element_type_by_lines(line_ids, "pipe_1")
        self.preprocessor.set_capped_end_by_lines(line_ids, True)
        self.preprocessor.add_valve_by_lines(line_ids, None)
        self.preprocessor.add_expansion_joint_by_lines(line_ids, None)
        self.preprocessor.set_structural_element_wall_formulation_by_lines(line_ids, "thin_wall")
        self.preprocessor.set_structural_element_force_offset_by_lines(line_ids, 1)

        self.properties._set_line_property("structural_element_type", "pipe_1", line_ids)
        self.properties._remove_line_property("section_properties", line_ids)
        self.properties._remove_line_property("wall_formulation", line_ids)
        self.properties._remove_line_property("force_offset", line_ids)
        self.properties._remove_line_property("capped_end", line_ids)
        self.properties._remove_line_property("expansion_joint", line_ids=line_ids)
        self.properties._remove_line_property("valve_name", line_ids=line_ids)
        self.properties._remove_line_property("flange_section_parameters", line_ids=line_ids)
        self.properties._remove_line_property("valve_info", line_ids=line_ids)

        self.remove_table_files_from_expansion_joints(line_ids)

        if self.tabWidget_pipe_section.currentIndex() == 0:
            if self.input_widget.get_constant_section_pipe_parameters():
                return
        else:
            if self.input_widget.get_beam_section_parameters():
                return

        section_info = self.input_widget.pipe_section_info
        cross_section = CrossSection(pipe_section_info=section_info)

        self.properties._set_multiple_line_properties(section_info, line_ids)
        self.properties._set_line_property("cross_section", cross_section, line_ids)

        if self.tabWidget_pipe_section.currentIndex() == 0:
            self.preprocessor.set_cross_section_by_lines(line_ids, cross_section)

        elif self.tabWidget_pipe_section.currentIndex() == 1:
            self.preprocessor.set_variable_cross_section_by_line(line_ids, section_info)

        self.actions_to_finalize()

    def beam_section_attribution_callback(self):
        
        if self.comboBox_attribution_type.currentIndex() == 0:
            line_ids = list(app().project.model.mesh.lines_from_model.keys())

        else:
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return True        

        if self.check_if_lines_belongs_to_psd(line_ids):
            return

        if self.tabWidget_general.currentIndex() == 1:

            if self.input_widget.get_beam_section_parameters():
                return

            self.preprocessor.set_structural_element_type_by_lines(line_ids, "beam_1")
            self.properties._set_line_property("structural_element_type", "beam_1", line_ids)

            section_info = self.input_widget.beam_section_info
            cross_section = CrossSection(beam_section_info=section_info)

            self.preprocessor.set_cross_section_by_lines(line_ids, cross_section)
            self.preprocessor.set_capped_end_by_lines(line_ids, False)
            self.preprocessor.set_structural_element_wall_formulation_by_lines(line_ids, None)
            self.preprocessor.set_structural_element_force_offset_by_lines(line_ids, True)
            self.preprocessor.add_valve_by_lines(line_ids, None)
            self.preprocessor.add_expansion_joint_by_lines(line_ids, None)

            self.properties._set_multiple_line_properties(section_info, line_ids)
            self.properties._remove_line_property("wall_formulation", line_ids)
            self.properties._remove_line_property("force_offset", line_ids)
            self.properties._remove_line_property("capped_end", line_ids)
            self.properties._remove_line_property("expansion_joint", line_ids=line_ids)
            self.properties._remove_line_property("valve_name", line_ids=line_ids)
            self.properties._remove_line_property("flange_section_parameters", line_ids=line_ids)
            self.properties._remove_line_property("valve_info", line_ids=line_ids)

            self.remove_acoustic_related_data_from_lines(line_ids)
            self.remove_table_files_from_expansion_joints(line_ids)

            self.actions_to_finalize()

    def actions_to_finalize(self):
        import matplotlib.pyplot as plt

        plt.close()
        self.complete = True
        app().pulse_file.write_line_properties_in_file()
        app().project.enhance_pipe_sections_appearance()

        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
        geometry_handler.process_pipeline()

        app().main_window.update_plots()
        self.close()

    def remove_acoustic_related_data_from_lines(self, line_ids: list):
        """
        """
        self.properties._remove_line_property("fluid", line_ids=line_ids)
        self.properties._remove_line_property("fluid_id", line_ids=line_ids)
        self.properties._remove_line_property("acoustic_element_type", line_ids=line_ids)
        self.properties._remove_line_property("proportinal_damping", line_ids=line_ids)
        self.properties._remove_line_property("volume_flow", line_ids=line_ids)

        aux_e = self.properties.element_properties.copy()
        aux_n = self.properties.nodal_properties.copy()

        remove_data_from_nodes = defaultdict(list)
        remove_data_from_elements = defaultdict(list)

        for line_id in line_ids:
            line_elements = self.preprocessor.mesh.line_to_elements[line_id]
            for element_id in line_elements:
                for key in aux_e.items():
                    for property in ["perforated_plate"]:
                        if key == (property, element_id):
                            self.properties._remove_element_property(property, element_id)
                            remove_data_from_elements[property].append(element_id)

            line_nodes = self.preprocessor.line_to_nodes[line_id]
            for node_id in line_nodes:
                for key in aux_n.items():
                    for property in ["acoustic_pressure", "volume_velocity", "specific_impedance", "radiation_impedance", "compressor_excitation"]:
                        if key == (property, node_id):
                            self.properties._remove_nodal_property(property, node_id)
                            remove_data_from_nodes[property].append(node_id)

        for property, element_ids in remove_data_from_elements.items(): 
            table_names = self.properties.get_element_related_table_names(property, element_ids)
            self.process_table_file_removal(table_names)
        
        for property, node_ids in remove_data_from_nodes.items(): 
            table_names = self.properties.get_nodal_related_table_names(property, node_ids)
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_table_files_from_expansion_joints(self, line_ids: list):
        table_names = list()
        for line_id, data in self.properties.line_properties.items():
            data: dict
            if "expansion_joint" in data.keys():
                ej_data = data["expansion_joint"]
                if line_id in line_ids and "table_names" in ej_data.keys():
                    table_names.append(ej_data["table_names"])

        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.pipe_section_attribution_callback()
            if self.tabWidget_general.currentIndex() == 1:
                self.beam_section_attribution_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()