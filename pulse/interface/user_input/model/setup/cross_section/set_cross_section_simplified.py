from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.cross_section.set_cross_section_simplified_ui import SetCrossSectionSimplified_UI
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from itertools import count


class TabIndex(IntEnum):
    PIPE = 0
    BEAM = 1
    ACTIVE_SECTIONS = 2


class SectionsInfo(IntEnum):
    ID = 0
    SECTION_TYPE = 2
    SECTION_PARAMETERS = 3

class TabWidgetGeneral(IntEnum):
    PIPE = 0
    BEAM = 1
    ACTIVE_SECTIONS = 2

class TabWidgetBeams(IntEnum):
    RECTANGULAR_BEAM = 0
    CIRCULAR_BEAM = 1
    C_BEAM = 2
    I_BEAM = 3
    T_BEAM = 4
    


class SetCrossSectionSimplified(SetCrossSectionSimplified_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties
        self.pipeline = app().project.pipeline

        self._config_window()
        self.reset()
        self._define_qt_variables()
        self._create_connections()

        # while self.keep_window_open:
        #     self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Configure the cross-section")

    def reset(self):
        self.selected_column = None
        self.complete = False
        self.keep_window_open = True
        self.active_sections = dict()

    def _define_qt_variables(self):
        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_cross_section.setLayout(self.grid_layout)
        self._add_cross_section_widget()

        # QPushButton
        self.pushButton_exit_pipe = self.cross_section_widget.pushButton_exit_pipe
        self.pushButton_exit_beam = self.cross_section_widget.pushButton_exit_beam
        self.pushButton_confirm_beam = self.cross_section_widget.pushButton_confirm_beam
        self.pushButton_confirm_pipe = self.cross_section_widget.pushButton_confirm_pipe

    def _create_connections(self):
        self.pushButton_exit_pipe.clicked.connect(self.close)
        self.pushButton_exit_beam.clicked.connect(self.close)
        self.pushButton_confirm_beam.clicked.connect(self.attribute_callback)
        self.pushButton_confirm_pipe.clicked.connect(self.attribute_callback)
        self.cross_section_widget.pushButton_load_section_data.clicked.connect(self.load_section_data)
        self.cross_section_widget.pushButton_edit_section_data.clicked.connect(self.edit_section_data)
        self.cross_section_widget.treeWidget_lines_info.itemClicked.connect(self.single_click_item_callback)

    def _add_cross_section_widget(self):
        self.cross_section_widget = CrossSectionWidget(dialog=self)
        self.grid_layout.addWidget(self.cross_section_widget)

    def attribute_callback(self):
        self.complete = True
        self.close()

    def load_active_sections(self, section_type_to_filter: str):

        self.cross_section_widget.pushButton_edit_section_data.setDisabled(True)
        self.cross_section_widget.pushButton_load_section_data.setDisabled(True)

        self.cross_section_widget.treeWidget_lines_info.clear()
        self.cross_section_widget.tabWidget_general.setTabVisible(TabIndex.ACTIVE_SECTIONS, True)

        # hides the 'Element option' column
        self.cross_section_widget.treeWidget_lines_info.hideColumn(1)

        self.active_sections.clear()

        for structure in self.pipeline.structures:
            cross_section_info = structure.extra_info.get("cross_section_info")
            if not isinstance(cross_section_info, dict):
                continue

            section_type_label = cross_section_info.get("section_type_label")
            if section_type_label != section_type_to_filter:
                continue

            section_parameters = cross_section_info.get("section_parameters")
            if section_parameters in self.active_sections.values():
                continue

            # define a new section index
            section_id = self.get_section_index()

            # add the new section parameters
            self.active_sections[section_id] = section_parameters

            new = QTreeWidgetItem([
                str(section_id),
                "",
                section_type_label,
                str(section_parameters),
                ])

            for i in range(4):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.cross_section_widget.treeWidget_lines_info.addTopLevelItem(new)

        if not self.active_sections:
            self.cross_section_widget.tabWidget_general.setTabVisible(TabIndex.ACTIVE_SECTIONS, False)

    def get_section_index(self):
        for i in count(1):
            index = i
            if index in self.active_sections.keys():
                continue

            return index

    def load_section_data(self):
        selected_items = self.cross_section_widget.treeWidget_lines_info.selectedItems()
        if len(selected_items) != 1:
            return None, None

        index = selected_items[0].text(SectionsInfo.ID)
        section_type = selected_items[0].text(SectionsInfo.SECTION_TYPE)

        parameters = self.active_sections[int(index)]
        self.load_section_inputs(section_type, parameters)

        return section_type, parameters

    def load_section_inputs(self, section_type: str, parameters: list):

        if section_type is None:
            raise TypeError()

        if section_type == "pipe" or section_type == "reducer":
            self.update_pipe_section_entries(section_type, parameters)

        elif "beam" in section_type:
            self.cross_section_widget.tabWidget_general.setTabVisible(0, False)
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_general.setCurrentIndex(1)
            self.update_beam_section_entries(section_type, parameters)

    def edit_section_data(self):
        section_type, target_parameters = self.load_section_data()
        if section_type is None:
            return

        line_ids = list()       
        for structure in self.pipeline.structures:
            parameters = structure.extra_info["cross_section_info"]["section_parameters"]
            
            if parameters == target_parameters:
                line_ids.append(structure)

        if not line_ids:
            raise ValueError()

        self.pipeline.select_structures(line_ids)
        self.main_window.geometry_widget.update_plot()

    def single_click_item_callback(self, item):
        self.cross_section_widget.reset_all_input_texts()
        self.cross_section_widget.pushButton_edit_section_data.setEnabled(True)
        self.cross_section_widget.pushButton_load_section_data.setEnabled(True)

    def update_pipe_section_entries(self, section_type: str, section_parameters: list):

        if section_type == "pipe":
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_general.setCurrentIndex(0)

            outside_diameter = section_parameters[0]
            thickness = section_parameters[1]
            offset_y = section_parameters[2]
            offset_z = section_parameters[3]
            insulation_thickness = section_parameters[4]
            insulation_density = section_parameters[5]

            self.cross_section_widget.lineEdit_outside_diameter.setText(str(outside_diameter))
            self.cross_section_widget.lineEdit_wall_thickness.setText(str(thickness))

            if offset_y:
                self.cross_section_widget.lineEdit_offset_y.setText(str(offset_y))

            if offset_z:
                self.cross_section_widget.lineEdit_offset_z.setText(str(offset_z))

            if insulation_density:
                self.cross_section_widget.lineEdit_insulation_density.setText(str(insulation_density))

            if insulation_thickness:
                self.cross_section_widget.lineEdit_insulation_thickness.setText(str(insulation_thickness))

        elif section_type == "reducer":
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_general.setCurrentIndex(0)

            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, False)
            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_pipe_section.setCurrentIndex(1) 

            for index, lineEdit in enumerate(self.cross_section_widget.variable_pipe_entries_line_edits):
                lineEdit.setText(str(section_parameters[index]))

    def update_beam_section_entries(self, section_type: str, section_parameters: list):

        if section_type == "rectangular_beam":
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(TabWidgetBeams.RECTANGULAR_BEAM, True)
            self.cross_section_widget.tabWidget_beam_section.setCurrentIndex(TabWidgetBeams.RECTANGULAR_BEAM)

            [base, height, base_in, height_in, offset_y, offset_z] = section_parameters

            self.cross_section_widget.lineEdit_base_rectangular_section.setText(str(base))
            self.cross_section_widget.lineEdit_height_rectangular_section.setText(str(height))
            self.cross_section_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
            self.cross_section_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
            
            if base_in != 0 and height_in != 0:
                self.cross_section_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base - base_in) / 2, 4)))

        elif section_type == "circular_beam":
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(TabWidgetBeams.CIRCULAR_BEAM, True)
            self.cross_section_widget.tabWidget_beam_section.setCurrentIndex(TabWidgetBeams.CIRCULAR_BEAM)

            [outside_diameter_beam, thickness, offset_y, offset_z] = section_parameters
            self.cross_section_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
            self.cross_section_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
            self.cross_section_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
            
            if thickness != 0:
                self.cross_section_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))

        elif section_type == "c_beam":
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(TabWidgetBeams.C_BEAM, True)
            self.cross_section_widget.tabWidget_beam_section.setCurrentIndex(TabWidgetBeams.C_BEAM)

            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
            self.cross_section_widget.lineEdit_height_C_section.setText(str(h))
            self.cross_section_widget.lineEdit_w1_C_section.setText(str(w1))
            self.cross_section_widget.lineEdit_tw_C_section.setText(str(tw))
            self.cross_section_widget.lineEdit_w2_C_section.setText(str(w2))
            self.cross_section_widget.lineEdit_t1_C_section.setText(str(t1))
            self.cross_section_widget.lineEdit_t2_C_section.setText(str(t2))
            self.cross_section_widget.lineEdit_offsety_C_section.setText(str(offset_y))
            self.cross_section_widget.lineEdit_offsetz_C_section.setText(str(offset_z))

        elif section_type == "i_beam":
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(TabWidgetBeams.I_BEAM, True)
            self.cross_section_widget.tabWidget_beam_section.setCurrentIndex(TabWidgetBeams.I_BEAM)
            
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
            self.cross_section_widget.lineEdit_height_I_section.setText(str(h))
            self.cross_section_widget.lineEdit_w1_I_section.setText(str(w1))
            self.cross_section_widget.lineEdit_tw_I_section.setText(str(tw))
            self.cross_section_widget.lineEdit_w2_I_section.setText(str(w2))
            self.cross_section_widget.lineEdit_t1_I_section.setText(str(t1))
            self.cross_section_widget.lineEdit_t2_I_section.setText(str(t2))
            self.cross_section_widget.lineEdit_offsety_I_section.setText(str(offset_y))
            self.cross_section_widget.lineEdit_offsetz_I_section.setText(str(offset_z))

        elif section_type == "t_beam":
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(TabWidgetBeams.T_BEAM, True)
            self.cross_section_widget.tabWidget_beam_section.setCurrentIndex(TabWidgetBeams.T_BEAM)

            [h, w1, t1, tw, offset_y, offset_z] = section_parameters
            self.cross_section_widget.lineEdit_height_T_section.setText(str(h))
            self.cross_section_widget.lineEdit_w1_T_section.setText(str(w1))
            self.cross_section_widget.lineEdit_tw_T_section.setText(str(tw))
            self.cross_section_widget.lineEdit_t1_T_section.setText(str(t1))
            self.cross_section_widget.lineEdit_offsety_T_section.setText(str(offset_y))
            self.cross_section_widget.lineEdit_offsetz_T_section.setText(str(offset_z))
