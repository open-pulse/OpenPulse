from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget
import numpy as np

from opps.model import Point

from .structure_options import StructureOptions
from molde.stylesheets import set_qproperty


class PointOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()
        self.geometry_designer_widget = geometry_designer_widget

        self.structure_type = Point
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        if len(self.pipeline.selected_points) == 1:
            # Edit selected point
            self.pipeline.selected_points[0].set_coords(*xyz)
            self.pipeline.recalculate_curvatures()
        else:
            # Create new point
            self.pipeline.dismiss()
            self.pipeline.clear_selection()

            # If the point already exists ignore the command
            for point in self.pipeline.points:
                if np.all(point.coords() == xyz):
                    return

            self.pipeline.add_isolated_point(xyz)

    def attach_callback(self):
        pass

    def configure_structure(self):
        pass

    def update_permissions(self):
        set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
        self.geometry_designer_widget.configure_button.setEnabled(False)
        self.geometry_designer_widget.frame_bounding_box_sizes.setEnabled(True)
        self.geometry_designer_widget.attach_button.setEnabled(True)
        self.geometry_designer_widget.add_button.setEnabled(True)
        self.geometry_designer_widget.delete_button.setEnabled(True)
