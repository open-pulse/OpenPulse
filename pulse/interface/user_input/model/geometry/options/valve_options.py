from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import Valve

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse.interface.user_input.model.setup.structural.valves_input import ValvesInput
from pulse import app


class ValveOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = Valve
        self.valve_info = dict()
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        if self.valve_info is None:
            print("no valve info")
            return
        
        print(self.valve_info.get("valve_effective_diameter", 0))
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_valve(
            xyz,
            diameter = self.valve_info.get("valve_effective_diameter", 0),
            thickness = 0,
            extra_info = self._get_extra_info(),
        )

    def attach_callback(self):
        if self.valve_info is None:
            return

        parameters = self.valve_info.get("section_parameters")
        if parameters is None:
            return

        self.pipeline.connect_valves(
            diameter = self.valve_info.get("valve_effective_diameter", 0),
            thickness = 0,
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        app().main_window.close_dialogs()
        valve_input = ValvesInput(render_type="geometry")
        app().main_window.set_input_widget(None)

        if not valve_input.complete:
            self.valve_info = dict()
            return

        self.valve_info = valve_input.valve_info
        self.update_permissions()

    def update_permissions(self):
        if self.valve_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)

    def _get_extra_info(self):
        return dict(
            structural_element_type = "valve",
            valve_info = deepcopy(self.valve_info),
            cross_section_info = {"section_type_label" : "Valve"},
            current_material_info = self.geometry_designer_widget.current_material_info,
        )
