
from pulse.interface.handler.pcf_exporter import PCFExporter
from pulse.interface.handler.pcf_handler import PCFHandler
from pulse.editor.structures import Pipe, Bend, Flange, Reducer, ExpansionJoint, Valve
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService

from pulse import app


class PCFFileIO:
    def __init__(self):
        super().__init__()

    def _initialize(self):
        self.complete = False

    def open_pcf(self):
        '''
        This function is absolutelly disgusting. I will refactor this next week, 
        but for now it will be like this just in order to make the bosses happy =)
        '''
        extensions = ["pcf"]
        file_path = FileDialogService.open_file(extensions, "Open PCF File", "pcf_folder")

        if file_path is None:
            return

        pipeline = app().project.pipeline
        pcf_handler = PCFHandler()
        pcf_handler.load(file_path, pipeline)

        for structure in pipeline.structures:
            if isinstance(structure, Pipe | Bend):
                structure.extra_info = dict(
                    structural_element_type = "pipe_1",
                    cross_section_info = dict(
                        section_type_label = "pipe",
                        section_parameters = [structure.diameter, structure.thickness, 0, 0, 0, 0]
                    )
                )

            elif isinstance(structure, Reducer):
                structure.extra_info = dict(
                    structural_element_type = "pipe_1",
                    cross_section_info = dict(
                        section_type_label = "reducer",
                        section_parameters = [
                            structure.initial_diameter, structure.thickness, 0, 0, 
                            structure.final_diameter, structure.thickness, 0, 0, 0, 0
                        ]
                    )
                )

            elif isinstance(structure, Flange):
                structure.extra_info = dict(
                    structural_element_type = "pipe_1",
                    cross_section_info = dict(
                        section_type_label = "Flange",  # talvez seja pipe
                        section_parameters = [structure.diameter, structure.thickness, 0, 0, 0, 0]
                    )
                )
            
            elif isinstance(structure, Valve):
                structure.extra_info = dict(
                    structural_element_type = "valve",
                    valve_info = dict(
                        acoustic_behavior=0,
                        valve_effective_diameter = structure.diameter,
                        valve_wall_thickness = structure.thickness,
                        flange_diameter = structure.flange_outer_diameter,
                        flange_length = structure.flange_length,
                        body_section_parameters = [structure.diameter, structure.thickness, 0, 0, 0, 0],
                        flange_section_parameters = [structure.flange_outer_diameter, 0.07, 0, 0, 0, 0],
                        valve_name = "valve_test",

                        # These values are arbitrary and are not reliable
                        valve_mass = 100,
                        stiffening_factor = 10,
                    ),
                    cross_section_info = dict(
                        section_type_label = "valve",
                    )
                )


            elif isinstance(structure, ExpansionJoint):
                structure.extra_info = dict(
                    structural_element_type = "expansion_joint",
                    expansion_joint_info = dict(
                        effective_diameter = structure.diameter,
                    )
                )

        pipeline.merge_coincident_points()
        app().main_window.geometry_widget.update_plot(reset_camera=True)

    def export_pcf(self):
        extensions = ["pcf"]
        path = FileDialogService.save_file(extensions, "Export PCF file", "exported_pcf_folder")

        if path is None:
            return

        pipeline = app().project.pipeline
        pcf_exporter = PCFExporter()
        pcf_exporter.save(path, pipeline)
        app().main_window.update_plots()