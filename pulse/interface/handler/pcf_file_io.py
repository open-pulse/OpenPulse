
from opps.io.pcf.pcf_exporter import PCFExporter
from opps.io.pcf.pcf_handler import PCFHandler

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
        from opps.model import Pipe, Bend, Flange

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
                if structure.start_diameter == structure.end_diameter:
                    section_label = 'Pipe'
                    start_thickness = structure.start_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 0, 0]
                else:
                    section_label = 'Reducer'  
                    start_thickness = structure.start_diameter * 0.05
                    end_thickness = structure.end_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 
                                          structure.end_diameter, end_thickness, 0, 0, 0, 0]

            elif isinstance(structure, Flange):
                section_label = 'Pipe'
                thickness = structure.diameter * 0.05
                section_parameters = [structure.diameter, thickness, 0, 0, 0, 0]

            cross_section_info = {
                                  'section_type_label': section_label, 
                                  'section_parameters': section_parameters
                                  }

            # There are no beams in pcf files, therefore it is pipe_1
            structure.extra_info["structural_element_type"] = "pipe_1"
            structure.extra_info["cross_section_info"] = cross_section_info

        # TODO: the method 'process_geometry_callback' does not exist anymore
        # app().main_window.geometry_input_wigdet.process_geometry_callback()

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