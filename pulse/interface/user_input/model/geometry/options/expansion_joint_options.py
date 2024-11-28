from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from pulse.editor.structures import ExpansionJoint

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import ExpansionJointInput

window_title = "Error"

class ExpansionJointOptions(StructureOptions):
    structure_type = ExpansionJoint

    def get_kwargs(self) -> dict:
        if self.structure_info is None:
            return

        return dict(
            diameter = self.structure_info.get("effective_diameter", 0),
            thickness = 0,
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        app().main_window.close_dialogs()
        self.expansion_joint_input = ExpansionJointInput(render_type="geometry")
        self.load_data_from_pipe_section()
        self.expansion_joint_input.exec_callback()
        app().main_window.set_input_widget(None)

        if not self.expansion_joint_input.complete:
            self.structure_info = None
            return

        self.structure_info = self.expansion_joint_input.expansion_joint_info
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

    def load_data_from_pipe_section(self):

        outside_diameter = self.cross_section_widget.lineEdit_outside_diameter.text()
        wall_thickness = self.cross_section_widget.lineEdit_wall_thickness.text()

        try:

            section_parameters = self.cross_section_widget.pipe_section_info["section_parameters"]
            outside_diameter = section_parameters[0]
            wall_thickness = section_parameters[1]
            effective_diameter = outside_diameter - 2 * wall_thickness

            self.expansion_joint_input.lineEdit_effective_diameter.setText(f"{round(effective_diameter, 6)}")
            # self.expansion_joint_input.lineEdit_wall_thickness.setText(f"{round(wall_thickness, 6)}")
        
        except Exception as error_log:
            title = "Error while tranfering pipe data"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])

    def _get_extra_info(self):
        return dict(
            structural_element_type = "expansion_joint",
            expansion_joint_info = deepcopy(self.structure_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
