from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from pulse.editor.structures import Pipe, Bend

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class PipeOptions(StructureOptions):
    structure_type = Pipe

    def get_kwargs(self):
        if not self.structure_info:
            return

        parameters = self.structure_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            diameter = parameters[0],
            thickness = parameters[1],
            curvature_radius = self._get_bending_radius(parameters[0]),
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.load_data_from_reducer_section()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_constant_section_pipe_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.structure_info = self.cross_section_widget.pipe_section_info
        self.configure_section_of_selected()
        self.update_permissions()

    def configure_section_of_selected(self):
        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, Pipe | Bend):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)

    def update_permissions(self):
        if self.structure_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.frame_bounding_box_sizes.setEnabled(enable)
        super().update_permissions(enable)

    def load_data_from_reducer_section(self):

        outside_diameter = self.cross_section_widget.lineEdit_outside_diameter_final.text()
        if outside_diameter != "":
            self.cross_section_widget.lineEdit_outside_diameter.setText(outside_diameter)

        wall_thickness = self.cross_section_widget.lineEdit_wall_thickness_final.text()
        if wall_thickness != "":
            self.cross_section_widget.lineEdit_wall_thickness.setText(wall_thickness)

        offset_y = self.cross_section_widget.lineEdit_offset_y_final.text()
        if offset_y != "":
            self.cross_section_widget.lineEdit_offset_y.setText(offset_y)

        offset_z = self.cross_section_widget.lineEdit_offset_z_final.text()
        if offset_z != "":
            self.cross_section_widget.lineEdit_offset_z.setText(offset_z)

        for lineEdit in self.cross_section_widget.left_variable_pipe_lineEdits:
            lineEdit.setText("")

        for lineEdit in self.cross_section_widget.right_variable_pipe_lineEdits:
            lineEdit.setText("")

    def _get_bending_radius(self, diameter):
        geometry_input_widget = app().main_window.geometry_input_wigdet
        bending_option = geometry_input_widget.bending_options_combobox.currentText().lower()
        custom_bending_radius = geometry_input_widget.bending_radius_line_edit.text().lower()

        if (bending_option == "long radius"):
            return 1.5 * diameter

        elif (bending_option == "short radius"):
            return diameter

        elif bending_option == "user-defined":
            try:
                return float(custom_bending_radius)
            except:
                return 0

        else:
            return 0

    def _get_extra_info(self):
        return dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.structure_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
