from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import IBeam

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class IBeamOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = IBeam
        self.cross_section_info = dict()
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return
        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_i_beam(xyz, **kwargs)

    def attach_callback(self):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return
        self.pipeline.connect_i_beams(**kwargs)

    def configure_structure(self):
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
        self.cross_section_widget.tabWidget_beam_section.setTabVisible(3, True)
        self.cross_section_widget.lineEdit_height_I_section.setFocus()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_beam_section_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.cross_section_info = self.cross_section_widget.beam_section_info
        self.configure_section_of_selected()
        self.update_permissions()

    def update_permissions(self):
        if self.cross_section_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)

    def _get_kwargs(self) -> dict:
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            height = parameters[0],
            width_1 = parameters[1],
            width_2 = parameters[3],
            thickness_1 = parameters[2],
            thickness_2 = parameters[4],
            thickness_3 = parameters[5],
            extra_info = self._get_extra_info(),
        )

    def _get_extra_info(self):
        return dict(
            structural_element_type = "beam_1",
            cross_section_info = deepcopy(self.cross_section_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
