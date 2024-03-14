from PyQt5.QtWidgets import QComboBox, QWidget, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.geometry.goemetry_editor_help import GeometryEditorHelp
from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs
from pulse.interface.user_input.project.print_message import PrintMessageInput

from opps.model import Point

import os
import numpy as np
from time import sleep
from pathlib import Path

class AddStructuresWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "model/geometry/add_widget.ui", self)

        self.geometry_widget = geometry_widget
        self.main_window = app().main_window
        self.project = app().project
        self.file = self.project.file

        self.cross_section_widget = CrossSectionWidget()
        self.material_widget = MaterialInputs()

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._update_permissions()
        self.reset_text_info()

    def _initialize(self):
        self.complete = False
        self.cross_section_info = None
        self.current_material_index = None
        self.bending_radius = 0
        self.bending_factor = 0
        self.segment_information = dict()

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_length_unit : QComboBox
        self.comboBox_bending_type : QComboBox

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        # QLabel
        self.label_unit_coord_x : QLabel
        self.label_unit_coord_y : QLabel
        self.label_unit_coord_z : QLabel
        self.label_unit_delta_x : QLabel
        self.label_unit_delta_y : QLabel
        self.label_unit_delta_z : QLabel
        self.label_unit_bending_radius : QLabel

        # QLineEdit
        self.lineEdit_coord_x : QLineEdit
        self.lineEdit_coord_y : QLineEdit
        self.lineEdit_coord_z : QLineEdit
        self.lineEdit_delta_x : QLineEdit
        self.lineEdit_delta_y : QLineEdit
        self.lineEdit_delta_z : QLineEdit
        self.lineEdit_bending_radius : QLineEdit
        
        # QPushButton
        self.pushButton_set_cross_section : QPushButton
        self.pushButton_set_material : QPushButton
        self.pushButton_add_segment : QPushButton
        # self.pushButton_quick_manual : QPushButton
        self.pushButton_remove_selection : QPushButton

    def _create_connections(self):
        self.comboBox_length_unit.currentIndexChanged.connect(self.update_legth_units)
        self.comboBox_bending_type.currentIndexChanged.connect(self.update_bending_type)
        self.update_legth_units()
        self.update_bending_type()

        self.lineEdit_delta_x.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_y.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_z.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_bending_radius.textEdited.connect(self.coords_modified_callback)
        self.reset_coords(0.)

        self.pushButton_add_segment.clicked.connect(self.create_segment_callback)
        # self.pushButton_quick_manual.clicked.connect(self.show_geometry_editor_help)
        self.pushButton_remove_selection.clicked.connect(self.remove_selection_callback)
        self.pushButton_set_cross_section.clicked.connect(self.show_cross_section_widget)
        self.pushButton_set_material.clicked.connect(self.show_material_widget)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material)
        self.main_window.geometry_widget.selection_changed.connect(self.selection_callback)

    def _update_permissions(self, force_disable=False):
        
        if force_disable:
            enable_pipe = False
        else:
            enable_pipe = self.cross_section_info is not None

        self.lineEdit_delta_x.setEnabled(enable_pipe)
        self.lineEdit_delta_y.setEnabled(enable_pipe)
        self.lineEdit_delta_z.setEnabled(enable_pipe)

        if enable_pipe:
            self.lineEdit_delta_x.setPlaceholderText("")
            self.lineEdit_delta_y.setPlaceholderText("")
            self.lineEdit_delta_z.setPlaceholderText("")
        else:
            self.lineEdit_delta_x.setPlaceholderText("Cross-section")
            self.lineEdit_delta_y.setPlaceholderText("was not")
            self.lineEdit_delta_z.setPlaceholderText("defined")

        pipeline = app().geometry_toolbox.pipeline
        enable_finalize = len(pipeline.structures) > 0

    def load_defined_unit(self):
        self.length_unit = self.file.length_unit
        if self.length_unit == "meter":
            self.comboBox_length_unit.setCurrentIndex(0)
        elif self.length_unit == "millimeter":
            self.comboBox_length_unit.setCurrentIndex(1)
        elif self.length_unit == "inch":
            self.comboBox_length_unit.setCurrentIndex(2)
        self.update_legth_units()

    def show_cross_section_widget(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()            
        self.cross_section_widget.setVisible(True)

    def show_material_widget(self):
        self.material_widget._initialize()
        self.material_widget._add_icon_and_title()
        self.material_widget.load_data_from_materials_library()
        self.material_widget.setVisible(True)

    def update_legth_units(self):
        index = self.comboBox_length_unit.currentIndex()
        if index == 0:
            unit_label = "m"
            self.length_unit = "meter"
        elif index == 1:
            unit_label = "mm"
            self.length_unit = "millimeter"
        else:
            unit_label = "in"
            self.length_unit = "inch"
        #
        self.label_unit_delta_x.setText(f"[{unit_label}]")
        self.label_unit_delta_y.setText(f"[{unit_label}]")
        self.label_unit_delta_z.setText(f"[{unit_label}]")
        self.label_unit_bending_radius.setText(f"[{unit_label}]")
        #
        self.label_unit_coord_x.setText(f"Coords. x [{unit_label}]")
        self.label_unit_coord_y.setText(f"Coords. y [{unit_label}]")
        self.label_unit_coord_z.setText(f"Coords. z [{unit_label}]")
        
    def update_bending_type(self):
        
        self.bending_factor = 0
        self.lineEdit_bending_radius.setText("")
        self.lineEdit_bending_radius.setDisabled(True)
        
        index = self.comboBox_bending_type.currentIndex()
        if index == 0:
            self.bending_factor = 1.5
            self.lineEdit_bending_radius.setText("1.5*D")
        
        elif index == 1:
            self.bending_factor = 1
            self.lineEdit_bending_radius.setText("1.0*D")
    
        elif index == 2:
            self.lineEdit_bending_radius.setDisabled(False)
            self.lineEdit_bending_radius.setFocus()

        self.coords_modified_callback()

    def get_segment_deltas(self):
        dx = float(self.lineEdit_delta_x.text() or 0)
        dy = float(self.lineEdit_delta_y.text() or 0)
        dz = float(self.lineEdit_delta_z.text() or 0)
        return dx, dy, dz

    def get_user_defined_radius(self):
        try:
            radius = float(self.lineEdit_bending_radius.text())
        except:
            return None
        
        if radius != 0:
            return radius
        else:
            return None

    def coords_modified_callback(self):
        self._disable_add_segment_button()
        try:
            dx, dy, dz = self.get_segment_deltas()
            if (dx, dy, dz) == (0, 0, 0):
                return
            self.pushButton_add_segment.setDisabled(False)
        except ValueError:
            return

        editor = app().geometry_toolbox.editor
        if self.comboBox_bending_type.currentIndex() == 2:
            radius = self.get_user_defined_radius()
            if radius is None:
                return
        else:
            radius = self.bending_factor * editor.default_initial_diameter

        editor.dismiss()
        editor.clear_selection()

        can_bend = (
            self.cross_section_info["section_type_label"] == "Pipe section"
            and len(self.cross_section_info["section_parameters"]) != 10
        )

        if can_bend:
            editor.add_bent_pipe((dx,dy,dz), radius)
        else:
            editor.add_pipe((dx,dy,dz))  # actually it is a beam =)

        self.geometry_widget.update_plot()

    def _disable_add_segment_button(self, _bool=True):
        self.pushButton_add_segment.setDisabled(_bool)
    
    def selection_callback(self): 
        editor = self.geometry_widget.editor
        if editor.selected_structures or editor.selected_points:
            if editor.selected_points:
                *_, _point = editor.selected_points
                if not isinstance(_point, Point):
                    return
                self.lineEdit_coord_x.setText(str(round(_point.x, 8)))
                self.lineEdit_coord_y.setText(str(round(_point.y, 8)))
                self.lineEdit_coord_z.setText(str(round(_point.z, 8)))

            self.pushButton_remove_selection.setDisabled(False)
        else:
            self.pushButton_remove_selection.setDisabled(True)

    def reset_coords(self, value=""):
        self.lineEdit_coord_x.setText(str(value))
        self.lineEdit_coord_y.setText(str(value))
        self.lineEdit_coord_z.setText(str(value))
        self.lineEdit_coord_x.setDisabled(True)
        self.lineEdit_coord_y.setDisabled(True)
        self.lineEdit_coord_z.setDisabled(True)

    def create_segment_callback(self):
        try:
            dx, dy, dz = self.get_segment_deltas()
        except ValueError:
            return

        if (dx, dy, dz) == (0, 0, 0):
            return

        # put usefull data inside the structures
        editor = app().geometry_toolbox.editor
        for structure in editor.staged_structures:

            if self.cross_section_info is None:
                return

            structure.extra_info["cross_section_info"] = self.cross_section_info

            if self.cross_section_info["section_type_label"] == "Pipe section":
                structure.extra_info["structural_element_type"] = "pipe_1"
            else:
                structure.extra_info["structural_element_type"] = "beam_1"

            if self.current_material_index is not None:
                structure.extra_info["material_info"] = self.current_material_index

        self.geometry_widget.commit_structure()
        self.reset_deltas()
        self._update_permissions()

    def remove_selection_callback(self):
        editor = app().geometry_toolbox.editor
        editor.delete_selection()
        app().update()
        self.selection_callback()

    def reset_deltas(self):
        self.lineEdit_delta_x.setText("")
        self.lineEdit_delta_y.setText("")
        self.lineEdit_delta_z.setText("")

    # def show_geometry_editor_help(self):
    #     GeometryEditorHelp()

    def define_cross_section(self):
        is_pipe = (self.cross_section_widget.tabWidget_general.currentIndex() == 0)
        is_constant_section = (self.cross_section_widget.tabWidget_pipe_section.currentIndex() == 0)

        if is_pipe and is_constant_section:
            if self.cross_section_widget.get_constant_pipe_parameters():
                return
            self.cross_section_info = self.cross_section_widget.pipe_section_info
            diameter = self.cross_section_widget.section_parameters[0]
            self.geometry_widget.update_default_diameter(diameter)

        elif is_pipe and not is_constant_section:
            if  self.cross_section_widget.get_variable_section_pipe_parameters():
                return
            self.cross_section_info = self.cross_section_widget.pipe_section_info
            diameter_initial = self.cross_section_widget.variable_parameters[0]
            diameter_final = self.cross_section_widget.variable_parameters[4]
            self.geometry_widget.update_default_diameter(diameter_initial, diameter_final)

        else:  # is beam
            self.cross_section_widget.get_beam_section_parameters()
            self.cross_section_info = self.cross_section_widget.beam_section_info
            # temporary strategy
            self.geometry_widget.update_default_diameter(0.02)
        
        # just being consistent with the material name
        self.cross_section_widget.setVisible(False)
        self._update_permissions()
        self.update_segment_information_text()
        self.coords_modified_callback()

    def define_material(self):
        self.current_material_index = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self._update_permissions()
        self.update_segment_information_text()

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

        message = "Segment information\n\n"

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

    def run_help(self):

        self.list_buttons_highlighted = list()
        self.list_lineEdits_highlighted = list()

        self.set_button_highlighted(self.pushButton_set_cross_section, True)
        self.main_window.positioning_cursor_on_widget(self.pushButton_set_cross_section)
        # sleep(2)
        self.set_button_highlighted(self.pushButton_set_material, True)
        self.main_window.positioning_cursor_on_widget(self.pushButton_set_material)
        # sleep(2)
        self.set_lineEdit_highlighted(self.lineEdit_delta_x, True)
        self.main_window.positioning_cursor_on_widget(self.lineEdit_delta_x)
        # sleep(2)
        self.set_lineEdit_highlighted(self.lineEdit_delta_y, True)
        self.main_window.positioning_cursor_on_widget(self.lineEdit_delta_y)
        # sleep(2)
        self.set_lineEdit_highlighted(self.lineEdit_delta_z, True)
        self.main_window.positioning_cursor_on_widget(self.lineEdit_delta_z)
        # sleep(2)
        self.set_button_highlighted(self.pushButton_add_segment, True)
        self.main_window.positioning_cursor_on_widget(self.pushButton_add_segment)
        # sleep(2)
        # self.revert_highlights()

    def set_button_highlighted(self, button, _bool):
        """
        """
        if _bool:
            key = "QPushButton{ border-radius: 6px; border-color: rgb(255, 0, 0); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240) }"
            key += "QPushButton:hover{ border-radius: 6px; border-color: rgb(255, 0, 0); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240) }"
            key += "QPushButton:disabled{ border-radius: 6px; border-color: rgb(255, 0, 0); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240) }"
        else:
            key = "QPushButton{ border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240) }"
            key += "QPushButton:hover{ border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100) }"
            key += "QPushButton:pressed{ border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255) }"    
            key += "QPushButton:disabled{ border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(150,150, 150); background-color: rgb(220, 220, 220) }"

        if isinstance(button, QPushButton):
            button.setStyleSheet(key)
            if _bool:
                self.list_buttons_highlighted.append(button)

    def set_lineEdit_highlighted(self, lineEdit, _bool):
        """
        """
        if _bool:
            key = "QLineEdit{ border-radius: 6px; border-color: rgb(0, 0, 250); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }"
            key = "QLineEdit:hover{ border-radius: 6px; border-color: rgb(0, 0, 250); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }"
            key += "QLineEdit:disabled{ border-radius: 6px; border-color: rgb(0, 0, 250); border-style: ridge; border-width: 2px; color: rgb(100, 100, 100); background-color: rgb(240, 240, 240) }"
        else:
            key = "QLineEdit{ color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }"
            key += "QLineEdit:disabled{ color: rgb(100, 100, 100); background-color: rgb(240, 240, 240) }"   

        if isinstance(lineEdit, QLineEdit):
            lineEdit.setStyleSheet(key)
            if _bool:
                self.list_lineEdits_highlighted.append(lineEdit)

    def revert_highlights(self):

        for button in self.list_buttons_highlighted:
            self.set_button_highlighted(button, False)

        for lineEdit in self.list_lineEdits_highlighted:
            self.set_lineEdit_highlighted(lineEdit, False)

        self.list_buttons_highlighted.clear()
        self.list_lineEdits_highlighted.clear()