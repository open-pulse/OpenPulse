from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from copy import deepcopy


from pulse import app
from pulse.editor.structures import Valve
from pulse.interface.user_input.model.setup.structural.valves_input import ValvesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

from .structure_options import StructureOptions

window_title = "Error"


class ValveOptions(StructureOptions):
    structure_type = Valve

    def get_kwargs(self) -> dict:
        if self.structure_info is None:
            return

        return dict(
            diameter=self.structure_info.get("valve_effective_diameter", 0),
            flange_outer_diameter=self.structure_info.get("flange_section_parameters", [0])[0],
            flange_length=self.structure_info.get("flange_length"),
            thickness=0,
            extra_info=self._get_extra_info(),
        )

    def configure_structure(self):
        app().main_window.close_dialogs()
        self.valve_input = ValvesInput(render_type="geometry")
        self.load_data_from_pipe_section()
        self.valve_input.exec_callback()
        app().main_window.set_input_widget(None)

        if not self.valve_input.complete:
            self.structure_info = dict()
            return

        self.structure_info = self.valve_input.valve_info
        self.configure_section_of_selected()
        self.update_permissions()

    def load_data_from_pipe_section(self):

        try:

            section_parameters = self.cross_section_widget.pipe_section_info.get("section_parameters")
            if section_parameters is None:
                return

            outside_diameter = section_parameters[0]
            wall_thickness = section_parameters[1]
            effective_diameter = outside_diameter - 2 * wall_thickness

            self.valve_input.lineEdit_valve_effective_diameter.setText(f"{round(effective_diameter, 6)}")
            self.valve_input.lineEdit_valve_wall_thickness.setText(f"{round(wall_thickness, 6)}")

        except Exception as error_log:
            title = "Error while tranfering pipe data"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])

    def _get_extra_info(self):
        return dict(
            structural_element_type="valve",
            valve_info=deepcopy(self.structure_info),
            cross_section_info={"section_type_label": "valve"},
            material_id=self.geometry_designer_widget.current_material_id,
        )
