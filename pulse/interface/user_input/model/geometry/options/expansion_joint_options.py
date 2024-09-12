from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import ExpansionJoint

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import ExpansionJointInput
from pulse import app


class ExpansionJointOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = ExpansionJoint
        self.expansion_joint_info = dict()
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return

        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_expansion_joint(xyz, **kwargs)

    def attach_callback(self):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return
        self.pipeline.connect_expansion_joints(**kwargs)

    def configure_structure(self):
        app().main_window.close_dialogs()
        expansion_joint_input = ExpansionJointInput(render_type="geometry")
        app().main_window.set_input_widget(None)

        if not expansion_joint_input.complete:
            self.expansion_joint_info = None
            return

        self.expansion_joint_info = expansion_joint_input.expansion_joint_info
        self.configure_section_of_selected()
        self.update_permissions()

    def update_permissions(self):
        if self.expansion_joint_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)

    def _get_kwargs(self) -> dict:
        if self.expansion_joint_info is None:
            return

        return dict(
            diameter = self.expansion_joint_info.get("effective_diameter", 0),
            thickness = 0,
            extra_info = self._get_extra_info(),
        )

    def _get_extra_info(self):
        return dict(
            structural_element_type = "expansion_joint",
            expansion_joint_info = deepcopy(self.expansion_joint_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
