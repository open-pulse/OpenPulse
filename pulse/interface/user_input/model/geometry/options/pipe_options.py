from copy import deepcopy

from opps.model import Pipe, Bend

from .structure_options import StructureOptions
from pulse import app


class PipeOptions(StructureOptions):
    def __init__(self) -> None:
        super().__init__(self)
    
        self.structure_type = Pipe
        self.add_function = self.pipeline.add_bent_pipe
        self.attach_function = self.pipeline.connect_bent_pipes
        self.cross_section_info = None
        self.user_defined_bending_radius = 0

    def get_parameters(self):
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        kwargs = dict()
        kwargs["diameter"] = parameters[0]
        kwargs["thickness"] = parameters[1]
        kwargs["curvature_radius"] = self.get_bending_radius(parameters[0])
        kwargs["extra_info"] = dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.cross_section_info),
        )
        return kwargs

    def get_bending_radius(self, diameter):
        geometry_input_widget = app().main_window.geometry_input_wigdet
        bending_option = geometry_input_widget.bending_options_combobox.currentText()
        custom_bending_radius = geometry_input_widget.bending_radius_line_edit.text()

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

    def update_permissions(self):
        pass