from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget, QListWidget

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs

from opps.model import Pipe, Bend, Elbow

from pathlib import Path
import numpy as np


class EditBendWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/edit_bend.ui"
        uic.loadUi(ui_path, self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):
        self.cross_section_info = None
        self.current_material_index = None
        self.cross_section_widget = CrossSectionWidget()
        self.material_widget = MaterialInputs()

    def _define_qt_variables(self):
        # QLineEdit
        self.bend_radius : QLineEdit
        self.coord_x_end : QLineEdit
        self.coord_y_end : QLineEdit
        self.coord_z_end : QLineEdit
        self.coord_x_start : QLineEdit
        self.coord_y_start : QLineEdit
        self.coord_z_start : QLineEdit
        # QListWidget
        self.morph_list : QListWidget
        # QPushButton
        self.change_material_button : QPushButton
        self.change_section_button : QPushButton
        self.remove_bend_button : QPushButton

    def _create_connections(self):
        self.bend_radius.textEdited.connect(self.curvature_modified_callback)
        self.morph_list.itemClicked.connect(self.moph_list_callback)
        self.change_material_button.clicked.connect(self.show_material_widget)
        self.change_section_button.clicked.connect(self.show_cross_section_widget)
        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material)
        self.remove_bend_button.clicked.connect(self.remove_selection_callback)

    def remove_selection_callback(self):
        editor = app().geometry_toolbox.editor
        editor.delete_selection()
        app().update()

    def show_cross_section_widget(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.setVisible(True)           

    def show_material_widget(self):
        self.material_widget._add_icon_and_title()
        self.material_widget.setVisible(True)
        self.material_widget._initialize()
        self.material_widget.load_data_from_materials_library()

    def define_cross_section(self):
        is_pipe = (self.cross_section_widget.tabWidget_general.currentIndex() == 0)
        is_constant_section = (self.cross_section_widget.tabWidget_pipe_section.currentIndex() == 0)

        editor = self.geometry_widget.editor
        for structure in editor.selected_structures:
            if not isinstance(structure, (Pipe, Bend)):
                return

            if is_pipe and is_constant_section:
                self.cross_section_widget.get_constant_pipe_parameters()
                self.cross_section_info = self.cross_section_widget.pipe_section_info
                diameter = self.cross_section_widget.section_parameters[0]
                structure.set_diameter(diameter, diameter)
                self.geometry_widget.update_default_diameter(diameter)

            elif is_pipe and not is_constant_section:
                self.cross_section_widget.get_variable_section_pipe_parameters()
                self.cross_section_info = self.cross_section_widget.pipe_section_info
                diameter_initial = self.cross_section_widget.section_parameters[0]
                diameter_final = self.cross_section_widget.section_parameters[4]
                self.geometry_widget.update_default_diameter(diameter_initial)
                structure.set_diameter(diameter_initial, diameter_final)

            else:  # is beam
                self.cross_section_widget.get_beam_section_parameters()
                self.cross_section_info = self.cross_section_widget.beam_section_info
                # temporary strategy
                diameter = 0.01
                self.geometry_widget.update_default_diameter(diameter)
                structure.set_diameter(diameter, diameter)

        self.cross_section_widget.setVisible(False)
        self.update_pipe_cross_section()

    def define_material(self):
        self.current_material_index = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self.update_pipe_material()

    def curvature_modified_callback(self, text):
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            return

        try:
            curvature = float(text)
        except ValueError:
            return
        else:
            structure.curvature = curvature
            app().update()

    def moph_list_callback(self):
        items = self.morph_list.selectedItems()
        if not items:
            return
        first_item, *_ = items
        name = first_item.text().lower().strip()

        if name == "bend":
            _type = Bend
        elif name == "elbow":
            _type = Elbow
        else:
            return

        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            return
        
        new_structure = editor.morph(structure, _type)
        editor.select_structures([new_structure])
        app().update()

    def reset_lineEdits(self):
        self.bend_radius.setText("")
        self.coord_x_start.setText("")
        self.coord_y_start.setText("")
        self.coord_z_start.setText("")
        self.coord_x_end.setText("")
        self.coord_y_end.setText("")
        self.coord_z_end.setText("")

    def update(self):
        super().update()
        editor = self.geometry_widget.editor
        if not editor.selected_structures:
            self.reset_lineEdits()
            return

        *_, structure = editor.selected_structures
        if not isinstance(structure, Bend):
            self.reset_lineEdits()
            return
        
        bend_radius = np.round(structure.curvature, 8)
        self.bend_radius.setText(str(bend_radius))

        start_coords = np.round(structure.start.coords(), 6)
        self.coord_x_start.setText(str(start_coords[0]))
        self.coord_y_start.setText(str(start_coords[1]))
        self.coord_z_start.setText(str(start_coords[2]))

        end_coords = np.round(structure.end.coords(), 6)
        self.coord_x_end.setText(str(end_coords[0]))
        self.coord_y_end.setText(str(end_coords[1]))
        self.coord_z_end.setText(str(end_coords[2]))

    def update_pipe_cross_section(self):

        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)

        editor = self.geometry_widget.editor
        for structure in editor.selected_structures:
            if not isinstance(structure, (Bend, Pipe)):
                return
            
            if self.cross_section_info is None:
                return
            
            structure.extra_info["cross_section_info"] = self.cross_section_info
            if self.cross_section_info["section_type_label"] == "Pipe section":
                structure.extra_info["structural_element_type"] = "pipe_1"
            else:
                structure.extra_info["structural_element_type"] = "beam_1"
        
        self.update_segment_information_text()
        
        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)

    def update_pipe_material(self):

        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)

        editor = self.geometry_widget.editor
        for structure in editor.selected_structures:
            if not isinstance(structure, (Bend, Pipe)):
                return         
        
            if self.current_material_index is None:
                return

            structure.extra_info["material_info"] = self.current_material_index

        self.update_segment_information_text()

        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)
    
    def update_segment_information_text(self):
        
        section_label = ""
        section_parameters = ""
        if self.cross_section_info:
            section_label = self.cross_section_info["section_type_label"]
            section_parameters = self.cross_section_info["section_parameters"]

        material_id = ""
        material_data = None
        if self.current_material_index is not None:
            material_id = self.current_material_index
            material_data = self.file.get_material_properties(material_id)

        message = "Active configuration\n\n"

        if self.cross_section_info:
            # message = "Cross-section info:\n"
            if section_label == "Pipe section":
                if len(section_parameters) == 6:
                    message += f"Section type: {section_label} (constant)\n"
                else:
                    message += f"Section type: {section_label} (variable)\n"
            else:
                message += f"Section type: {section_label}\n"
            message += f"Section data: {section_parameters}\n\n"

        if material_data is not None:
            # message = "Material info:\n"
            message += f"Material name: {material_data[0]}\n"
            message += f"Material data: {material_data[1:]}\n\n"

        self.geometry_widget.set_info_text(message)

    def reset_text_info(self):
        self.geometry_widget.set_info_text("")