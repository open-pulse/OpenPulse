
from pulse import app
from pulse.utils.text_utils import pascal_to_spaced_case

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


class StructureOptions:
    structure_type = None

    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget"):
        self.pipeline = app().project.pipeline
        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget
        self.structure_info = dict()

    @classmethod
    def name(cls):
        return pascal_to_spaced_case(cls.__name__).strip().removesuffix("Options")
    
    def xyz_callback(self, xyz: tuple[float, float, float]):
        if self.structure_type is None:
            return

        kwargs = self.get_kwargs()
        if kwargs is None:
            return        

        if self.pipeline.staged_structures or self.pipeline.staged_points:
            self.geometry_designer_widget.load_tmp_camera()
        else:
            self.geometry_designer_widget.save_tmp_camera()

        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_structure_deltas(self.structure_type, xyz, **kwargs)

    def attach_callback(self):
        if self.structure_type is None:
            return

        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        self.pipeline.connect_structures(self.structure_type, **kwargs)
        self.pipeline.commit()

    def configure_structure(self):
        raise NotImplementedError(f"Method configure_structure not implemented on {self.__class__.__name__}")

    def replace_selection(self):
        if self.structure_type is None:
            return

        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        self.pipeline.dismiss()
        self.pipeline.replace_selection_by(self.structure_type, **kwargs)
        self.pipeline.commit()

    def configure_section_of_selected(self):
        if self.structure_type is None:
            return

        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, self.structure_type):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)

    def update_permissions(self, enable=True):
        enable_attach = len(self.pipeline.selected_points) >= 2
        enable_add = (
            len(self.pipeline.selected_structures)
            + len(self.pipeline.staged_structures)
            + len(self.pipeline.staged_points)
            >= 1
        )
        enable_delete = (
            len(self.pipeline.selected_structures)
            + len(self.pipeline.selected_points)
            >= 1
        )
        self.geometry_designer_widget.attach_button.setEnabled(enable_attach and enable)
        self.geometry_designer_widget.add_button.setEnabled(enable_add and enable)
        self.geometry_designer_widget.delete_button.setEnabled(enable_delete)
        self.geometry_designer_widget.configure_button.setEnabled(True)

    def get_kwargs(self) -> dict:
        raise NotImplementedError(f"Method get_kwargs not implemented on {self.__class__.__name__}")