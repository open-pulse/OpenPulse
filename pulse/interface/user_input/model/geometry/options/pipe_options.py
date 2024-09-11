from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import Pipe, Bend

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class PipeOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = Pipe
        self.cross_section_info = dict()
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_bent_pipe(xyz, **kwargs)

    def attach_callback(self):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return
        self.pipeline.connect_bent_pipes(**kwargs)

    def configure_structure(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_constant_section_pipe_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.cross_section_info = self.cross_section_widget.pipe_section_info
        self.configure_section_of_selected()
        self.update_permissions()

    def configure_section_of_selected(self):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, Pipe | Bend):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)

    def update_permissions(self):
        if self.cross_section_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)
    
    def _get_kwargs(self):
        if not self.cross_section_info:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            diameter = parameters[0],
            thickness = parameters[1],
            curvature_radius = self._get_bending_radius(parameters[0]),
            extra_info = self._get_extra_info(),
        )

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
            cross_section_info = deepcopy(self.cross_section_info),
            current_material_info = self.geometry_designer_widget.current_material_info,
        )
