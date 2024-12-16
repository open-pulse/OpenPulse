from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from pulse.editor.structures import ArcBend

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class ArcBendOptions(StructureOptions):
    structure_type = ArcBend

    def get_kwargs(self):
        if not self.structure_info:
            return

        parameters = self.structure_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            diameter = parameters[0],
            thickness = parameters[1],
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

    def update_permissions(self):
        if self.structure_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.set_bound_box_sizes_widgets_enabled(enable)
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

    def _get_extra_info(self):
        return dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.structure_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
