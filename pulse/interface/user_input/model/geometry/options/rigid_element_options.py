from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from copy import deepcopy

from pulse.editor.structures.rigid_element import RigidElement

from .structure_options import StructureOptions


class RigidElementOptions(StructureOptions):
    structure_type = RigidElement

    def get_kwargs(self) -> dict:
        return dict(
            extra_info=self._get_extra_info(),
        )

    def configure_structure(self):
        pass

    def update_permissions(self):
        self.geometry_designer_widget.configure_button.setEnabled(False)
        self.geometry_designer_widget.set_material_button.setEnabled(False)
        self.geometry_designer_widget.set_bound_box_sizes_widgets_enabled(True)
        self.geometry_designer_widget.attach_button.setEnabled(True)
        self.geometry_designer_widget.add_button.setEnabled(True)
        self.geometry_designer_widget.delete_button.setEnabled(True)

    def _get_extra_info(self):
        return dict(
            structural_element_type="rigid_element",
            material_id=self.geometry_designer_widget.current_material_id,
        )
