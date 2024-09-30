
from opps.io.pcf.pcf_exporter import PCFExporter
from opps.io.pcf.pcf_handler import PCFHandler
from opps.model import Pipe, Bend, Flange, Reducer, ExpansionJoint, Valve

from pulse import app

from pathlib import Path

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

        last_path = app().config.get_last_folder_for("pcf folder")
        if last_path is None:
            last_path = str(Path().home())

        file_path, check = app().main_window.file_dialog.get_open_file_name(
                                                                            "Open PCF File", 
                                                                            last_path, 
                                                                            filter = "PCF File (*.pcf)"
                                                                            )

        if not check:
            return

        pipeline = app().project.pipeline
        pcf_handler = PCFHandler()
        pcf_handler.load(file_path, pipeline)

        for structure in pipeline.structures:
            if isinstance(structure, Pipe | Bend):
                structure.extra_info = dict(
                    structural_element_type = "pipe_1",
                    cross_section_info = dict(
                        section_type_label = "Pipe",
                        section_parameters = [structure.diameter, structure.thickness, 0, 0, 0, 0]
                    )
                )

            elif isinstance(structure, Reducer):
                structure.extra_info = dict(
                    structural_element_type = "pipe_1",
                    cross_section_info = dict(
                        section_type_label = "Reducer",
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
                        section_type_label = "Valve",
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

        last_path = app().config.get_last_folder_for("exported pcf folder")
        if last_path is None:
            last_path = str(Path().home())

        path, check = app().main_window.file_dialog.get_save_file_name( 
                                                                       'Export PCF file', 
                                                                       last_path, 
                                                                       'PCF File (*.pcf)'
                                                                       )

        if not check:
            return

        pipeline = app().project.pipeline
        pcf_exporter = PCFExporter()
        pcf_exporter.save(path, pipeline)
        app().main_window.update_plots()