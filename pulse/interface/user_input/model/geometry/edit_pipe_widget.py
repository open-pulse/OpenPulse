from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

from opps.model import Pipe

from pathlib import Path
import numpy as np

class EditPipeWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "model/geometry/edit_pipe2.ui", self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

        self._initialize()
        self._define_qt_variables()
        self._create_connections()        

    def _initialize(self):
        self.cross_section_widget = CrossSectionWidget()
        self.material_widget = MaterialInputs()

    def _define_qt_variables(self):
        # QLineEdit
        self.coord_x_end : QLineEdit
        self.coord_y_end : QLineEdit
        self.coord_z_end : QLineEdit
        self.coord_x_start : QLineEdit
        self.coord_y_start : QLineEdit
        self.coord_z_start : QLineEdit
        # QPushButton
        self.change_material_button : QPushButton
        self.change_section_button : QPushButton
        self.remove_segment_button : QPushButton

    def _create_connections(self):
        self.change_material_button.clicked.connect(self.show_material_widget)
        self.change_section_button.clicked.connect(self.show_cross_section_widget)
        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material)

    def show_cross_section_widget(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.setVisible(True)
        # section_type = self.comboBox_section_type.currentIndex()
        # self.cross_section_widget.set_inputs_to_geometry_creator(section_type=section_type)            

    def show_material_widget(self):
        self.material_widget._add_icon_and_title()
        self.material_widget.setVisible(True)
        self.material_widget.reset()
        self.material_widget.load_data_from_materials_library()

    def define_cross_section(self):
        is_pipe = (self.cross_section_widget.tabWidget_general.currentIndex() == 0)
        is_constant_section = (self.cross_section_widget.tabWidget_pipe_section.currentIndex() == 0)

        if is_pipe and is_constant_section:
            self.cross_section_widget.get_straight_pipe_parameters()
            section_parameters = list(self.cross_section_widget.section_parameters.values())
            self.cross_section_info = { "section label" : "pipe (constant)",
                                        "section parameters" : section_parameters }
            diameter = self.cross_section_widget.section_parameters["outer_diameter"]
            self.geometry_widget.update_default_diameter(diameter)

        elif is_pipe and not is_constant_section:
            self.cross_section_widget.get_variable_section_pipe_parameters()
            section_parameters =self.cross_section_widget.variable_parameters
            self.cross_section_info = { "section label" : "pipe (variable)",
                                        "section parameters" : section_parameters }

        else:  # is beam
            self.cross_section_widget.get_beam_section_parameters()
            section_label = self.cross_section_widget.section_label
            section_parameters = self.cross_section_widget.section_parameters
            self.cross_section_info = { "section label" : "beam",
                                        "beam section type" : section_label,
                                        "section parameters" : section_parameters }
        
        # just being consistent with the material name
        self.cross_section_widget.setVisible(False)
        # self._update_permissions()
        # self.update_segment_information_text()

    def define_material(self):
        self.current_material_index = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        # self._update_permissions()
        # self.update_segment_information_text()

    def update(self):
        super().update()
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            self.reset_lineEdits()
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Pipe):
            self.reset_lineEdits()
            return

        start_coords = np.round(structure.start.coords(), 6)
        self.coord_x_start.setText(str(start_coords[0]))
        self.coord_y_start.setText(str(start_coords[1]))
        self.coord_z_start.setText(str(start_coords[2]))

        end_coords = np.round(structure.end.coords(), 6)
        self.coord_x_end.setText(str(end_coords[0]))
        self.coord_y_end.setText(str(end_coords[1]))
        self.coord_z_end.setText(str(end_coords[2]))

    def reset_lineEdits(self):

        self.coord_x_start.setText("")
        self.coord_y_start.setText("")
        self.coord_z_start.setText("")

        self.coord_x_end.setText("")
        self.coord_y_end.setText("")
        self.coord_z_end.setText("")