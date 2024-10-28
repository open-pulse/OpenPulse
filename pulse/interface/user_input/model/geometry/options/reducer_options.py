from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget

from pulse.editor.structures import Reducer
from molde.stylesheets import set_qproperty
from .structure_options import StructureOptions

from copy import deepcopy


class ReducerOptions(StructureOptions):
    structure_type = Reducer

    def get_kwargs(self) -> dict:
        if self.structure_info is None:
            return

        parameters = self.structure_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            initial_diameter = parameters[0],
            final_diameter = parameters[4],
            thickness = parameters[1],
            initial_offset_y = parameters[2],
            initial_offset_z = parameters[3],
            final_offset_y = parameters[6],
            final_offset_z = parameters[7],
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(1, True)
        self.cross_section_widget.lineEdit_outside_diameter_initial.setFocus()
        self.load_data_from_pipe_section()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_variable_section_pipe_parameters():
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

        enable_attach = len(self.pipeline.selected_points) >= 2
        enable_add = len(self.pipeline.staged_structures) + len(self.pipeline.staged_points) >= 1
        enable_delete = len(self.pipeline.selected_structures) + len(self.pipeline.selected_points) >= 1

        self.geometry_designer_widget.configure_button.setEnabled(True)
        self.geometry_designer_widget.frame_bounding_box_sizes.setEnabled(enable)
        self.geometry_designer_widget.attach_button.setEnabled(enable_attach)
        self.geometry_designer_widget.add_button.setEnabled(enable_add)
        self.geometry_designer_widget.delete_button.setEnabled(enable_delete)

    def load_data_from_pipe_section(self):

        outside_diameter = self.cross_section_widget.lineEdit_outside_diameter.text()
        wall_thickness = self.cross_section_widget.lineEdit_wall_thickness.text()
        offset_y = self.cross_section_widget.lineEdit_offset_y.text()
        offset_z = self.cross_section_widget.lineEdit_offset_z.text()

        for i, value in enumerate([outside_diameter, wall_thickness, offset_y, offset_z]):
            self.cross_section_widget.left_variable_pipe_lineEdits[i].setText(value)

        for lineEdit in self.cross_section_widget.right_variable_pipe_lineEdits:
            lineEdit.setText("")

        if outside_diameter != "" and wall_thickness != "":
            self.cross_section_widget.lineEdit_outside_diameter_final.setFocus()

    def _get_extra_info(self):
        return dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.structure_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
