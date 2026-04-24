from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit

from pulse import app
from pulse.interface.ui_generated.model.setup.cross_section.cross_section_widget_ui import (
    CrossSectionWidget_UI,
)
from pulse.interface.user_input.model.setup.cross_section.cross_section_plotter import (
    CrossSectionPlotter,
)
from pulse.interface.user_input.model.setup.structural.get_standard_cross_section import (
    GetStandardCrossSection,
)
from pulse.interface.user_input.numeric_checks.validators import StrictDoubleValidator
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_sections.c_beam_cross_section import CBeamCrossSection
from pulse.model.cross_sections.circular_beam_cross_section import (
    CircularBeamCrossSection,
)
from pulse.model.cross_sections.generic_beam_cross_section import (
    GenericBeamCrossSection,
)
from pulse.model.cross_sections.i_beam_cross_section import IBeamCrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.cross_sections.rectangular_beam_cross_section import (
    RectangularBeamCrossSection,
)
from pulse.model.cross_sections.t_beam_cross_section import TBeamCrossSection
from pulse.model.cross_sections.variable_pipe_cross_section import (
    VariablePipeCrossSection,
)
from pulse.utils.interface_utils import check_inputs


class TabIndex(IntEnum):
    PIPE = 0
    BEAM = 1
    ACTIVE_SECTIONS = 2


class BeamType(IntEnum):
    RECTANGULAR_BEAM = 0
    CIRCULAR_BEAM = 1
    C_BEAM = 2
    I_BEAM = 3
    T_BEAM = 4
    GENERIC_BEAM = 5

error_title = "Error"


class CrossSectionWidget(CrossSectionWidget_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dialog = kwargs.get("dialog", None)

        self._initialize()
        self._configure_validators()
        self._create_connections()
        self.create_list_of_line_edits()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _add_icon_and_title(self):
        self._config_window()

    def _initialize(self):

        self.nps = 0.
        
        self.section_type = None
        self.section_type_label = None
        self.section_parameters = None
        self.section_properties = None
        self.beam_section_info = None
        self.pipe_section_info = None

        self.complete = False
 
        self.section_data_lines = dict()
        self.section_data_elements = dict()
        self.variable_parameters = list()

    def _configure_validators(self):

        positive_validators = StrictDoubleValidator(0, 1e8, 6)
        simetric_validators = StrictDoubleValidator(-1e8, 1e8, 6)

        for line_edit in self.findChildren(QLineEdit):

            obj_name = line_edit.objectName()
            if "element_id" in obj_name:
                continue

            if "offset" in obj_name:
                line_edit.setValidator(simetric_validators)
            else:
                line_edit.setValidator(positive_validators)

    def _create_connections(self):
        #
        self.pushButton_select_standard_section.clicked.connect(self.select_standard_section)
        self.pushButton_select_standard_section_initial.clicked.connect(self.select_standard_section_initial)
        self.pushButton_select_standard_section_final.clicked.connect(self.select_standard_section_final)
        self.pushButton_check_if_section_is_normalized.clicked.connect(self.check_if_section_is_normalized)
        self.pushButton_plot_pipe_cross_section.clicked.connect(self.plot_section)
        self.pushButton_plot_beam_cross_section.clicked.connect(self.plot_section)
        self.pushButton_invert_input_values.clicked.connect(self.invert_variable_section_values)
        #
        self.config_treeWidget()

    def create_list_of_line_edits(self):

        self.variable_pipe_entries_line_edits =   [   
            self.lineEdit_outside_diameter_initial,
            self.lineEdit_wall_thickness_initial,
            self.lineEdit_offset_y_initial,
            self.lineEdit_offset_z_initial,
            self.lineEdit_outside_diameter_final,
            self.lineEdit_wall_thickness_final,
            self.lineEdit_offset_y_final,
            self.lineEdit_offset_z_final,
            self.lineEdit_insulation_thickness_variable_section,
            self.lineEdit_insulation_density_variable_section,
            ]

        self.left_variable_pipe_lineEdits = [
            self.lineEdit_outside_diameter_initial,
            self.lineEdit_wall_thickness_initial,
            self.lineEdit_offset_y_initial,
            self.lineEdit_offset_z_initial,
            ]

        self.right_variable_pipe_lineEdits = [
            self.lineEdit_outside_diameter_final,
            self.lineEdit_wall_thickness_final,
            self.lineEdit_offset_y_final,
            self.lineEdit_offset_z_final,
            ]

    def reset_all_input_texts(self):
        for line_edit in self.findChildren(QLineEdit):
            line_edit.clear()

    def config_treeWidget(self):
        for i, width in enumerate([40, 120]):
            self.treeWidget_lines_info.setColumnWidth(0, width)
            self.treeWidget_lines_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def select_standard_section(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.nps = round(read.nps, 6)
            self.lineEdit_outside_diameter.setText(str(outside_diameter))
            self.lineEdit_wall_thickness.setText(str(thickness))

    def select_standard_section_initial(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.lineEdit_outside_diameter_initial.setText(str(outside_diameter))
            self.lineEdit_wall_thickness_initial.setText(str(thickness))

    def select_standard_section_final(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.lineEdit_outside_diameter_final.setText(str(outside_diameter))
            self.lineEdit_wall_thickness_final.setText(str(thickness))

    def set_inputs_to_geometry_creator(self):
        self.complete = False
        self.tabWidget_general.setTabVisible(TabIndex.ACTIVE_SECTIONS, False)
        self.label_element_id.setVisible(False)
        self.lineEdit_element_id_initial.setVisible(False)
        self.lineEdit_element_id_final.setVisible(False)
        # self.pushButton_invert_input_values.setVisible(False)

    def invert_variable_section_values(self):

        left_values = list()
        for i, lineEdit in enumerate(self.left_variable_pipe_lineEdits):
            left_values.append(lineEdit.text())
        
        right_values = list()
        for i, lineEdit in enumerate(self.right_variable_pipe_lineEdits):
            right_values.append(lineEdit.text())

        for i, value in enumerate(left_values):
            lineEdit = self.right_variable_pipe_lineEdits[i]
            lineEdit.setText(value)

        for i, value in enumerate(right_values):
            lineEdit = self.left_variable_pipe_lineEdits[i]
            lineEdit.setText(value)

    def hide_all_tabs(self):
        for i in range(self.tabWidget_general.count()):
            self.tabWidget_general.setTabVisible(i, False)

        for i in range(self.tabWidget_pipe_section.count()):
            self.tabWidget_pipe_section.setTabVisible(i, False)

        for i in range(self.tabWidget_beam_section.count()):
            self.tabWidget_beam_section.setTabVisible(i, False)

    def set_geometry_creator(self, geometry_creator):
        self.geometry_creator_input = geometry_creator

    def get_constant_section_pipe_parameters(self):

        self.section_type_label = None
        self.pipe_section_info = None
        self.section_parameters = list()

        outside_diameter = check_inputs(self.lineEdit_outside_diameter, 'outside diameter')
        if outside_diameter is None:
            self.lineEdit_outside_diameter.setFocus()
            return True
        self.section_parameters.append(outside_diameter)

        thickness = check_inputs(self.lineEdit_wall_thickness, 'wall thickness')
        if thickness is None:
            self.lineEdit_wall_thickness.setFocus()
            return True
        self.section_parameters.append(thickness)
        
        offset_y = check_inputs(self.lineEdit_offset_y, 'offset y', only_positive=False, zero_included=True)
        if offset_y is None:
            self.lineEdit_offset_y.setFocus()
            return True
        self.section_parameters.append(offset_y)

        offset_z = check_inputs(self.lineEdit_offset_z, 'offset z', only_positive=False, zero_included=True)
        if offset_z is None:
            self.lineEdit_offset_z.setFocus()
            return True
        self.section_parameters.append(offset_z)

        insulation_density = check_inputs(self.lineEdit_insulation_density, 'insulation density', zero_included=True)
        if insulation_density is None:
            self.lineEdit_insulation_density.setFocus()
            return True
        self.section_parameters.append(insulation_density)

        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness, 'insulation thickness', zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness.setFocus()
            return True
        self.section_parameters.append(insulation_thickness)

        message = ""
        if np.isclose(outside_diameter, 2*thickness, atol=1e-5) or 2*thickness > outside_diameter:
            message = "The pipe 'wall thickness' must be less than half of the outside diameter."
            self.lineEdit_wall_thickness.setFocus()

        if message != "":
            title = "Input cross-section error"
            PrintMessageInput([error_title, title, message]) 
            return True

        if len(self.section_parameters) == 6:
            
            self.section_type_label = "pipe"
            # self.pipe_section_info = {  "section_type_label" : self.section_type_label ,
            #                             "section_parameters" : self.section_parameters  }
            
            self.pipe_section_info = PipeCrossSection(*self.section_parameters)

    def get_variable_section_pipe_parameters(self):

        self.section_type_label = None
        self.pipe_section_info = None

        message = ""

        outside_diameter_initial = check_inputs(self.lineEdit_outside_diameter_initial, 'outside diameter (initial)')
        if outside_diameter_initial is None:
            self.lineEdit_outside_diameter_initial.setFocus()
            return True
        
        outside_diameter_final = check_inputs(self.lineEdit_outside_diameter_final, 'outside diameter (final)')
        if outside_diameter_final is None:
            self.lineEdit_outside_diameter_final.setFocus()
            return True

        thickness_initial = check_inputs(self.lineEdit_wall_thickness_initial, 'thickness (initial)')
        if thickness_initial is None:
            self.lineEdit_wall_thickness_initial.setFocus()
            return True
        
        thickness_final = check_inputs(self.lineEdit_wall_thickness_final, 'thickness (final)')
        if thickness_final is None:
            self.lineEdit_wall_thickness_final.setFocus()
            return True

        if np.isclose(outside_diameter_initial, 2*thickness_initial, atol=1e-5) or 2*thickness_initial > outside_diameter_initial:
            message = "The 'initial thickness' be less than half of the 'initial outside diameter'."

        if np.isclose(outside_diameter_final, 2*thickness_final, atol=1e-5) or 2*thickness_final > outside_diameter_final:
            message = "The 'final thickness' be less than half of the 'final outside diameter'."
        
        if message != "":
            title = "Input cross-section error"
            PrintMessageInput([error_title, title, message])
            return True

        offset_y_initial = check_inputs(self.lineEdit_offset_y_initial, 'offset y (initial)', only_positive=False, zero_included=True)
        if offset_y_initial is None:
            self.lineEdit_offset_y_initial.setFocus()
            return True

        offset_y_final = check_inputs(self.lineEdit_offset_y_final, 'offset y (final)', only_positive=False, zero_included=True)
        if offset_y_final is None:
            self.lineEdit_offset_y_final.setFocus()
            return True

        offset_z_initial = check_inputs(self.lineEdit_offset_z_initial, 'offset z (initial)', only_positive=False, zero_included=True)
        if offset_z_initial is None:
            self.lineEdit_offset_z_initial.setFocus()
            return True
        
        offset_z_final = check_inputs(self.lineEdit_offset_z_final, 'offset z (final)', only_positive=False, zero_included=True)
        if offset_z_final is None:
            self.lineEdit_offset_z_final.setFocus()
            return True
        
        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness_variable_section, 
                                            'insulation thickness (variable pipe section)',
                                            zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness_variable_section.setFocus()
            return True
        
        insulation_density = check_inputs(  self.lineEdit_insulation_density_variable_section, 
                                            'density thickness (variable pipe section)',
                                            zero_included=True  )
        if insulation_density is None:
            self.lineEdit_insulation_density_variable_section.setFocus()
            return True

        self.variable_parameters = [
            outside_diameter_initial,
            thickness_initial,
            offset_y_initial,
            offset_z_initial,
            outside_diameter_final,
            thickness_final,
            offset_y_final,
            offset_z_final,
            insulation_thickness,
            insulation_density,
        ]

        self.section_type_label = "reducer"
        # self.pipe_section_info = {  "section_type_label" : self.section_type_label ,
        #                             "section_parameters" : self.variable_parameters  }

        self.pipe_section_info = VariablePipeCrossSection(*self.variable_parameters)


    def get_beam_section_parameters(self):

        self.beam_section_info = None

        tab_index = self.tabWidget_beam_section.currentIndex()

        if tab_index == BeamType.RECTANGULAR_BEAM:

            self.section_type_label = "rectangular_beam"

            base = check_inputs(self.lineEdit_base_rectangular_section, 'base (Rectangular beam)')
            if base is None:
                self.lineEdit_base_rectangular_section.setFocus()
                return True
            
            height = check_inputs(self.lineEdit_height_rectangular_section, 'height (Rectangular beam)')
            if height is None:
                self.lineEdit_height_rectangular_section.setFocus()
                return True
            
            offset_y = check_inputs(self.lineEdit_offsety_rectangular_section, 'offset y (Rectangular beam)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_rectangular_section.setFocus()
                return True
            
            offset_z = check_inputs(self.lineEdit_offsetz_rectangular_section, 'offset z (Rectangular beam)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_rectangular_section.setFocus()
                return True
   
            if self.lineEdit_wall_thickness_rectangular_section.text() != "":
                
                thickness = check_inputs(self.lineEdit_wall_thickness_rectangular_section, 'wall thickness (Rectangular beam)')
                if thickness is None:
                    self.lineEdit_wall_thickness_rectangular_section.setFocus()
                    return True

                if thickness > np.min([(base/2), (height/2)]):
                    title = "Invalid cross-section parameters"
                    message = "For a rectangular cross-section, the wall thickness must be simultaneously "
                    message += "greater than half of the base and height section parameters."
                    PrintMessageInput([error_title, title, message])
                    return True             
                else:
                    base_in = base - 2*thickness
                    height_in = height - 2*thickness

            else:
                base_in = 0
                height_in = 0

            self.section_parameters = [base, height, base_in, height_in, offset_y, offset_z]
            self.beam_section_info = RectangularBeamCrossSection(*self.section_parameters)

        elif tab_index == BeamType.CIRCULAR_BEAM:

            self.section_type_label = "circular_beam"

            outside_diameter_beam = check_inputs(self.lineEdit_outside_diameter_circular_section, 'outside diameter (circular_beam)')
            if outside_diameter_beam is None:
                self.lineEdit_outside_diameter_circular_section.setFocus()
                return True
            
            offset_y = check_inputs(self.lineEdit_offsety_circular_section, 'offset y (circular_beam)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_circular_section.setFocus()
                return True
            
            offset_z = check_inputs(self.lineEdit_offsetz_circular_section, 'offset z (circular_beam)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_circular_section.setFocus()
                return True

            if self.lineEdit_wall_thickness_circular_section != "":
                thickness = check_inputs(self.lineEdit_wall_thickness_circular_section, 'wall thickness (circular_beam)', zero_included=True)
                if thickness is None:
                    self.lineEdit_wall_thickness_circular_section.setFocus()
                    return True
 
            if np.isclose(outside_diameter_beam, 2*thickness, atol=1e-5) or 2*thickness > outside_diameter_beam:
                title = "Invalid cross-section parameters"
                message = "For a circular cross-section, the wall thickness must be simultaneously "
                message += "greater than half of the base and height section parameters."
                PrintMessageInput([error_title, title, message])
                return True

            self.section_parameters = [outside_diameter_beam, thickness, offset_y, offset_z]
            self.beam_section_info = CircularBeamCrossSection(*self.section_parameters)

        elif tab_index == BeamType.C_BEAM:

            self.section_type_label = "c_beam"

            h = check_inputs(self.lineEdit_height_C_section, 'height (c-beam)')
            if h is None:
                self.lineEdit_height_C_section
                return True
            
            w1 = check_inputs(self.lineEdit_w1_C_section, 'w1 (c-beam)')
            if w1 is None:
                self.lineEdit_w1_C_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_C_section, 'tw (c-beam)')
            if tw is None:
                self.lineEdit_tw_C_section.setFocus()
                return True
            
            w2 = check_inputs(self.lineEdit_w2_C_section, 'w2 (c-beam)')
            if w2 is None:
                self.lineEdit_w2_C_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_C_section, 't1 (c-beam)')
            if t1 is None:
                self.lineEdit_t1_C_section.setFocus()
                return True

            t2 = check_inputs(self.lineEdit_t2_C_section, 't2 (c-beam)')
            if t2 is None:
                self.lineEdit_t2_C_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_C_section, 'offset y (c-beam)',only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_C_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_C_section, 'offset z (c-beam)', only_positive=False, zero_included=True)            
            if offset_z is None:
                self.lineEdit_offsetz_C_section.setFocus()
                return True

            if h < (t1 + t2):
                title = "Input cross-section error"
                message = "The height must be greater than t1+t2 summation."
                PrintMessageInput([error_title, title, message])
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]
            self.beam_section_info = CBeamCrossSection(*self.section_parameters)

        elif tab_index == BeamType.I_BEAM:

            self.section_type_label = "i_beam"

            h = check_inputs(self.lineEdit_height_I_section, 'height (i-beam)')
            if h is None:
                self.lineEdit_height_I_section.setFocus()
                return True

            w1 = check_inputs(self.lineEdit_w1_I_section, 'w1 (i-beam)')
            if w1 is None:
                self.lineEdit_w1_I_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_I_section, 'tw (i-beam)')
            if tw is None:
                self.lineEdit_tw_I_section.setFocus()
                return True

            w2 = check_inputs(self.lineEdit_w2_I_section, 'w2 (i-beam)')
            if w2 is None:
                self.lineEdit_w2_I_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_I_section, 't1 (i-beam)')
            if t1 is None:
                self.lineEdit_t1_I_section.setFocus()
                return True

            t2 = check_inputs(self.lineEdit_t2_I_section, 't2 (i-beam)')
            if t2 is None:
                self.lineEdit_t2_I_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_I_section, 'offset y (i-beam)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_I_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_I_section, 'offset z (i-beam)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_I_section.setFocus()
                return True

            if h < (t1 + t2):
                title = "Input cross-section error"
                message = "The height must be greater than t1+t2 summation."
                PrintMessageInput([error_title, title, message])
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]
            self.beam_section_info = IBeamCrossSection(*self.section_parameters)
            
        elif tab_index == BeamType.T_BEAM:

            self.section_type_label = "t_beam"

            h = check_inputs(self.lineEdit_height_T_section, 'height (t-beam)')
            if h is None:
                self.lineEdit_height_T_section.setFocus()
                return True

            w1 = check_inputs(self.lineEdit_w1_T_section, 'W1 (t-beam)')
            if w1 is None:
                self.lineEdit_w1_T_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_T_section, 'tw (t-beam)')
            if tw is None:
                self.lineEdit_tw_T_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_T_section, 't1 (t-beam)')
            if t1 is None:
                self.lineEdit_t1_T_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_T_section, 'offset y (t-beam)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_T_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_T_section, 'offset z (t-beam)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_T_section.setFocus()
                return True

            if h < t1:
                title = "Input cross-section error"
                message = "The height must be greater than t1."
                PrintMessageInput([error_title, title, message])
                return True

            self.section_parameters = [h, w1, t1, tw, offset_y, offset_z]
            self.beam_section_info = TBeamCrossSection(*self.section_parameters)

        elif tab_index == BeamType.GENERIC_BEAM:

            area = float(0)
            Iyy = float(0)
            Izz = float(0)
            Iyz = float(0)

            area = check_inputs(self.lineEdit_area, 'Area (generic beam)')
            if area is None:
                return True

            Iyy = check_inputs(self.lineEdit_Iyy, 'Iyy (generic beam)')
            if Iyy is None:
                return True

            Izz = check_inputs(self.lineEdit_Izz, 'Izz (generic beam)')
            if Izz is None:
                return True

            Iyz = check_inputs(self.lineEdit_Iyz, 'Iyz (generic beam)', only_positive=False, zero_included=True)
            if Iyz is None:
                return True

            shear_coefficient = check_inputs(self.lineEdit_shear_coefficient, 'Shear Coefficient (generic beam)', zero_included=True)
            if shear_coefficient is None:
                return True

            if shear_coefficient > 1:
                title = "Input cross-section error"
                message = "The shear factor must be less or equals to 1."
                PrintMessageInput([error_title, title, message]) 
                return True
            else:

                self.section_type_label = "generic_beam"
                self.section_parameters = None
                _section_properties = [area, Iyy, Izz, Iyz, shear_coefficient, 0, 0]

                self.beam_section_info = GenericBeamCrossSection(*_section_properties)

        return False

    def check_if_section_is_normalized(self):

        outside_diameter = check_inputs(self.lineEdit_outside_diameter, "'outside diameter (Pipe section)'")
        if outside_diameter is None:
            self.lineEdit_outside_diameter.setFocus()
            return

        thickness = check_inputs(self.lineEdit_wall_thickness, "'thickness (Pipe section)'")
        if thickness is None:
            self.lineEdit_wall_thickness.setFocus()
            return

        section_data = {
            "outside diameter" : outside_diameter,
            "wall thickness" : thickness,
            }

        GetStandardCrossSection(section_data=section_data)

    def plot_section(self):
        
        # hide the QDialog before showing the cross-section plotter
        if isinstance(self.dialog, QDialog):
            self.dialog.hide()

        plotter = CrossSectionPlotter()

        if self.tabWidget_general.currentIndex() == TabIndex.PIPE:
            if self.get_constant_section_pipe_parameters():
                self.show_dialog()
                return

        elif self.tabWidget_general.currentIndex() == TabIndex.BEAM:
            if self.get_beam_section_parameters():
                self.show_dialog()
                return

        if isinstance(self.pipe_section_info, PipeCrossSection):
            points = self.pipe_section_info.section_points_to_draw
            section_type_label = self.pipe_section_info.section_type_label

        elif isinstance(self.beam_section_info, RectangularBeamCrossSection | CircularBeamCrossSection | CBeamCrossSection | IBeamCrossSection | TBeamCrossSection):
            points = self.beam_section_info.section_points_to_draw
            section_type_label = self.beam_section_info.section_type_label

        else:
            return

        plotter.plot_cross_section(points, section_type_label)
        plotter.exec()

        self.show_dialog()

    def show_dialog(self):
        # show the QDialog after closing the cross-section plotter
        if isinstance(self.dialog, QDialog):
            self.dialog.show()

    def keyPressEvent(self, event):
        if isinstance(self.dialog, QDialog):
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.dialog.attribute_callback()

            elif event.key() == Qt.Key_Escape:
                self.dialog.close()