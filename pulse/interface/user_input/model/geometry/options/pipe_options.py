from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from copy import deepcopy

from pulse import app
from pulse.editor.structures import Bend, Pipe

from .structure_options import StructureOptions


class PipeOptions(StructureOptions):
    structure_type = Pipe

    def get_kwargs(self):
        if not self.structure_info:
            return

        parameters = self.structure_info.get("section_parameters")
        if parameters is None:
            return

        nps = self.cross_section_widget.nps
        if nps:
            bending_radius_base = nps
        else:
            bending_radius_base = parameters[0]  # outside diameter

        return dict(
            diameter=parameters[0],
            thickness=parameters[1],
            offset_y=parameters[2],
            offset_z=parameters[3],
            curvature_radius=self._get_bending_radius(bending_radius_base),
            extra_info=self._get_extra_info(),
        )

    def attach_callback(self):
        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        if self._can_add_bend():
            self.pipeline.add_bend(**kwargs)
        else:
            self.pipeline.connect_structures(Pipe, **kwargs)
            self.pipeline.commit()

    def update_permissions(self):
        super().update_permissions()
        if self.structure_info and self._can_add_bend():
            self.geometry_designer_widget.attach_button.setEnabled(True)

    def configure_structure(self):
        self.cross_section_widget.set_inputs_to_geometry_creator()
        self.cross_section_widget.hide_all_tabs()
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.load_data_from_reducer_section()
        self.cross_section_dialog.load_active_sections("pipe")
        self.cross_section_dialog.exec()

        if not self.cross_section_dialog.complete:
            return

        self.cross_section_dialog.reset()
        if self.cross_section_widget.get_constant_section_pipe_parameters():
            self.configure_structure()
            return

        self.structure_info = self.cross_section_widget.pipe_section_info.as_dict()

        self.configure_section_of_selected()
        self.update_permissions()

    def configure_section_of_selected(self):
        kwargs = self.get_kwargs()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, Pipe | Bend):
                continue

            extra_info: dict = kwargs.get("extra_info")

            fluid_id = structure.extra_info.get("fluid_id")
            if isinstance(fluid_id, int):
                extra_info.update({"fluid_id" : fluid_id})

            material_id = structure.extra_info.get("material_id")
            if isinstance(material_id, int):
                extra_info.update({"material_id" : material_id})

            for k, v in kwargs.items():
                setattr(structure, k, v)

    def load_data_from_reducer_section(self):

        outside_diameter = self.cross_section_widget.lineEdit_outside_diameter_final.text()
        if outside_diameter != "":
            self.cross_section_widget.lineEdit_outside_diameter.setText(outside_diameter)

        wall_thickness = self.cross_section_widget.lineEdit_wall_thickness_final.text()
        if wall_thickness != "":
            self.cross_section_widget.lineEdit_wall_thickness.setText(wall_thickness)

        offset_y = self.cross_section_widget.lineEdit_offset_y_final.text()
        if offset_y != "":
            self.cross_section_widget.lineEdit_offset_y.setText(offset_y)

        offset_z = self.cross_section_widget.lineEdit_offset_z_final.text()
        if offset_z != "":
            self.cross_section_widget.lineEdit_offset_z.setText(offset_z)

        for lineEdit in self.cross_section_widget.left_variable_pipe_lineEdits:
            lineEdit.clear()

        for lineEdit in self.cross_section_widget.right_variable_pipe_lineEdits:
            lineEdit.clear()

    def _get_bending_radius(self, diameter):
        geometry_input_widget = app().main_window.geometry_input_wigdet
        bending_option = geometry_input_widget.bending_options_combobox.currentText().lower()
        custom_bending_radius = geometry_input_widget.bending_radius_line_edit.text().lower().replace(",", ".")

        if bending_option == "long radius":
            return 1.5 * diameter

        elif bending_option == "short radius":
            return diameter

        elif bending_option == "user-defined":
            try:
                return float(custom_bending_radius)
            except Exception:
                return 0

        else:
            return 0

    def _get_extra_info(self):
        return dict(
            structural_element_type="pipe_1",
            cross_section_info=deepcopy(self.structure_info),
            material_id=self.geometry_designer_widget.current_material_id,
        )

    def _can_add_bend(self) -> bool:
        if len(self.pipeline.selected_points) != 1:
            return False

        point = self.pipeline.selected_points[0]
        tangencies = self.pipeline.main_editor.get_point_tangency(point)
        return len(tangencies) == 2
