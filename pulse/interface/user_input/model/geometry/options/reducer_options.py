from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import Reducer

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class ReducerOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = Reducer
        self.cross_section_info: dict = self.cross_section_widget.pipe_section_info
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return
        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_reducer_eccentric(
            xyz,
            initial_diameter = parameters[0],
            final_diameter = parameters[4],
            thickness = parameters[1],
            initial_offset_y = parameters[2],
            initial_offset_z = parameters[3],
            final_offset_y = parameters[6],
            final_offset_z = parameters[7],
            extra_info = self._get_extra_info(),
        )

    def attach_callback(self):
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        self.pipeline.connect_reducer_eccentrics(
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
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(1, True)
        self.cross_section_widget.lineEdit_outside_diameter_initial.setFocus()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_variable_section_pipe_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.cross_section_info = self.cross_section_widget.pipe_section_info
        self.update_permissions()

    def update_permissions(self):
        if self.cross_section_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)

    def _get_extra_info(self):
        return dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.cross_section_info),
            current_material_info = self.geometry_designer_widget.current_material_info,
        )
