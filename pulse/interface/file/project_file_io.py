from pulse import app
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.material import Material
from pulse.preprocessing.cross_section import get_beam_section_properties
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

from fileboxes import Filebox

import os
import io
import h5py
import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class ProjectFileIO:
    
    def __init__(self, path : str, override=False):
        super().__init__()

        self.path = path
        self.vibra_file = Filebox(Path(path), override=override)

        # self.model = app().main_window.project.model
        # self.properties = self.model.properties

        self._initialize()
        self._default_filenames()
        self._default_foldernames()

    def _initialize(self):
        self.project_folder_path = Path(os.path.dirname(self.path))

    def _default_filenames(self):
        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.config"
        self.material_library_filename = "material_library.config"
        self.pipeline_filename = "pipeline.dat"
        self.model_properties = "model_properties.json"
        self.mesh_data_filename = "mesh_data.hdf5"
        self.results_data_filename = "results_data.hdf5"
        self.thumbnail_filename = "thumbnail.png"

    def _default_foldernames(self):
        pass

    def write_project_setup_in_file(self, data : dict, geometry_path=""):

        if geometry_path != "":
            basename = os.path.basename(geometry_path)
            internal_path = f"geometry_file/{basename}"

            try:
                self.vibra_file.remove("geometry_file")
            except:
                pass

            self.vibra_file.write_from_path(internal_path, geometry_path, encoding="iso-8859-1")

        try:

            project_setup = self.vibra_file.read(self.project_setup_filename)
            if project_setup is None:
                project_setup = dict()

            project_setup["project"] = data

            self.vibra_file.write(self.project_setup_filename, project_setup)
            app().main_window.project_data_modified = True

        except Exception as error_log:
            print(str(error_log))

    def read_geometry_from_file(self):

        data = self.vibra_file.read(self.project_setup_filename)

        if "project" in data.keys():
            project_setup = data["project"]

            if "geometry_filename" in project_setup.keys():

                geometry_filename = project_setup["geometry_filename"]
                dirname = self.project_folder_path / "geometry" 
                temp_path = dirname / geometry_filename
                internal_path = f"geometry_file/{geometry_filename}"

                print(temp_path, internal_path)

                if os.path.exists(dirname):
                    for filename in os.listdir(dirname).copy():
                        file_path = dirname / filename
                        os.remove(file_path)
                else:
                    os.mkdir(dirname)

                self.vibra_file.read_to_path(internal_path, temp_path)

            return str(temp_path)
    
    def read_project_setup_from_file(self):
        return self.vibra_file.read(self.project_setup_filename)
    
    def write_analysis_setup_in_file(self, analysis_setup):

        project_setup = self.vibra_file.read(self.project_setup_filename)
        if project_setup is None:
            return   

        aux = dict()
        for key, data in analysis_setup.items():
            if key == "frequencies":
                continue
            # if isinstance(data, np.ndarray):
            #     data = list(data)
            aux[key] = data

        project_setup["analysis_setup"] = aux         
        self.vibra_file.write(self.project_setup_filename, project_setup)
        app().main_window.project_data_modified = True

    def read_analysis_setup_from_file(self):

        analysis_setup = None
        project_setup = self.vibra_file.read(self.project_setup_filename)

        if project_setup is None:
            return

        if "analysis_setup" in project_setup.keys():
            analysis_setup = project_setup["analysis_setup"]

        return analysis_setup

    def write_model_setup_in_file(self, project_setup : dict):
        self.vibra_file.write(self.project_setup_filename, project_setup)
        app().main_window.project_data_modified = True

    def read_model_setup_from_file(self):
        return self.vibra_file.read(self.project_setup_filename)

    def write_pipeline_data_in_file(self, pipeline_data):
        self.vibra_file.write(self.pipeline_filename, pipeline_data)
        app().main_window.project_data_modified = True

    def read_pipeline_data_from_file(self):
        return self.vibra_file.read(self.pipeline_filename)

    def write_material_library_in_file(self, config):
        self.vibra_file.write(self.material_library_filename, config)
        app().main_window.project_data_modified = True

    def read_material_library_from_file(self):
        return self.vibra_file.read(self.material_library_filename)

    def write_fluid_library_in_file(self, config):
        self.vibra_file.write(self.fluid_library_filename, config)
        app().main_window.project_data_modified = True

    def read_fluid_library_from_file(self):
        return self.vibra_file.read(self.fluid_library_filename)

    def write_model_properties_in_file(self):

        try:

            def normalize(prop: dict):
                """
                Sadly json doesn't accepts tuple keys,
                so we need to convert it to a string like:
                "property id" = value
                """
                output = dict()
                for (property, tag), data in prop.items():

                    key = f"{property} {tag}"

                    if property in ["fluid", "material"]:
                        if isinstance(data, (Fluid, Material)):
                            output[key] = data.identifier
                    else:
                        output[key] = data

                return output

            data = dict(
                        # global_properties = normalize(self.properties.global_properties),
                        volume_properties = normalize(self.properties.volume_properties),
                        surface_properties = normalize(self.properties.surface_properties),
                        line_properties = normalize(self.properties.line_properties),
                        element_properties = normalize(self.properties.element_properties),
                        nodal_properties = normalize(self.properties.nodal_properties),
                        )

            self.vibra_file.write(self.model_properties, data)
            app().main_window.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting model properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])


    def read_model_properties_from_file(self):

        def denormalize(prop: dict):
            new_prop = dict()
            for key, val in prop.items():
                p, i = key.split()
                p = p.strip()
                i = int(i)
                new_prop[p, i] = val
            return new_prop

        data = self.vibra_file.read(self.model_properties)

        if data is None:
            return dict()

        model_properties = dict(
                                # global_properties = denormalize(data["global_properties"]),
                                volume_properties = denormalize(data["volume_properties"]),
                                surface_properties = denormalize(data["surface_properties"]),
                                line_properties = denormalize(data["line_properties"]),
                                element_properties = denormalize(data["element_properties"]),
                                nodal_properties = denormalize(data["nodal_properties"])
                                )

        return model_properties
    
    def write_thumbnail(self):
        thumbnail = app().main_window.project.thumbnail
        if thumbnail is None:
            return
        self.vibra_file.write(self.thumbnail_filename, thumbnail)
        app().main_window.project_data_modified = True

    def read_thumbnail(self):
        return self.vibra_file.read(self.thumbnail_filename)
    
    def write_results_data_in_file(self):
        with self.vibra_file.open(self.results_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

                acoustic_modal_solver = app().main_window.project.acoustic_modal_solver
                if acoustic_modal_solver is not None:
                    if acoustic_modal_solver.modal_shape is not None:
                        natural_frequencies = acoustic_modal_solver.natural_frequencies
                        modal_shape = acoustic_modal_solver.modal_shape
                        f.create_dataset("modal_acoustic/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_acoustic/modal_shape", data=modal_shape, dtype=float)
                
                structural_modal_solver = app().main_window.project.structural_modal_solver
                if structural_modal_solver is not None:
                    if structural_modal_solver.modal_shape is not None:
                        natural_frequencies = structural_modal_solver.natural_frequencies
                        modal_shape = structural_modal_solver.modal_shape
                        f.create_dataset("modal_structural/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_structural/modal_shape", data=modal_shape, dtype=float)

                acoustic_harmonic_solver = app().main_window.project.acoustic_harmonic_solver
                if acoustic_harmonic_solver is not None:
                    if acoustic_harmonic_solver.solution is not None:
                        frequencies = acoustic_harmonic_solver.frequencies
                        solution = acoustic_harmonic_solver.solution
                        f.create_dataset("harmonic_acoustic/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_acoustic/solution", data=solution, dtype=complex)
                
                structural_harmonic_solver = app().main_window.project.structural_harmonic_solver
                if structural_harmonic_solver is not None:
                    if structural_harmonic_solver.solution is not None:
                        frequencies = acoustic_harmonic_solver.frequencies
                        solution = acoustic_harmonic_solver.solution
                        f.create_dataset("harmonic_structural/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_structural/solution", data=solution, dtype=complex)

                app().main_window.project_data_modified = True

    def read_results_data_from_file(self):
        
        results_data = dict()

        try:

            with self.vibra_file.open(self.results_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        aux = dict()
                        for key, values in f.get(group).items():

                            try:
                                aux[key] = np.array(values)
                            except:
                                continue

                        if aux:
                            results_data[group] = aux

        except:
            return dict()

        return results_data
    
    def remove_model_properties_from_project_file(self):
        self.vibra_file.remove(self.model_properties)

    def remove_mesh_data_from_project_file(self):
        self.vibra_file.remove(self.mesh_data_filename)

    def remove_results_data_from_project_file(self):
        self.vibra_file.remove(self.results_data_filename)

    def check_pipeline_data(self):
        
        project_data = self.read_project_setup_from_file()
        if project_data is None:
            return False

        project_setup = project_data["project"]
        import_type = project_setup["import_type"]

        pipeline_data = self.read_pipeline_data_from_file()
        if pipeline_data is None:
            return False

        if len(pipeline_data.sections()):
            for tag in pipeline_data.sections():
                if import_type == 0:
                    return True
                else:
                    if "-" in tag:
                        continue
                    keys_to_check = ["start coords", "end coords"]
                    for key in keys_to_check:
                        if key not in pipeline_data[tag].keys():
                            return False
            return True
        else:
            return False

    def get_pipeline_data_from_file(self) -> dict:
        '''
        This method returns the all required data to build pipeline segments.
        '''

        pipeline_data = dict()
        config = self.read_pipeline_data_from_file()

        for section in config.sections():

            if "-" in section:
                continue

            tag = int(section)
            keys = config[section].keys()
            aux = dict()

            if "start coords" in keys:
                start_coords = config[section]["start coords"]
                aux["start_coords"] = get_list_of_values_from_string(start_coords, int_values=False)

            if "end coords" in keys:
                end_coords = config[section]["end coords"]
                aux["end_coords"] = get_list_of_values_from_string(end_coords, int_values=False)

            if "corner coords" in keys:
                corner_coords = config[section]["corner coords"]
                aux["corner_coords"] = get_list_of_values_from_string(corner_coords, int_values=False)

            if "curvature radius" in keys:
                curvature_radius = config[section]["curvature radius"]
                aux["curvature_radius"] = float(curvature_radius)

            if 'structural element type' in keys:
                structural_element_type = config[section]["structural element type"]
                aux["structural_element_type"] = structural_element_type
            else:
                structural_element_type = "pipe_1"

            if 'section type' in keys:
                section_type_label = config[section]["section type"]
                aux["section_type_label"] = section_type_label

            if 'section parameters' in keys:
                section_parameters = config[section]["section parameters"]
                aux["section_parameters"] = get_list_of_values_from_string(section_parameters, int_values=False)

            if structural_element_type == "beam_1":
                if 'section properties' in keys:
                    section_properties = config[section]["section properties"]
                    aux["section_properties"] = get_list_of_values_from_string(section_properties, int_values=False)
                else:
                    aux["section_properties"] = get_beam_section_properties(section_type_label, aux["section_parameters"])

            if 'material id' in keys:
                try:
                    aux["material_id"] = int(config[section]["material id"])
                except:
                    pass

            if 'psd label' in keys:
                aux["psd_label"] = config[section]["psd label"]

            if 'link type' in keys:
                aux["link type"] = config[section]["link type"]

            is_bend = ('corner coords' in keys) and ('curvature radius' in keys)
            if is_bend:
                pipeline_data[tag, "Bend"] = aux

            else:
                pipeline_data[tag, "Pipe"] = aux

        return pipeline_data

    def modify_project_attributes(self, **kwargs):

        project_name = kwargs.get('project_name', None)
        import_type = kwargs.get('import_type', None)
        length_unit = kwargs.get('length_unit', None)
        element_size = kwargs.get('element_size', None)
        geometry_tolerance = kwargs.get('geometry_tolerance', None)
        geometry_filename = kwargs.get('geometry_filename', None)
        
        project_setup = self.read_project_setup_from_file()
        if project_setup is None:
            return
        
        if "project" in project_setup.keys():

            data = project_setup["project"]
            
            if project_name is not None:
                data['name'] = project_name

            if import_type is not None:
                data['import type'] = str(import_type)

            if length_unit is not None:
                data['length unit'] = length_unit

            if element_size is not None:
                data['element size'] = str(element_size)
                # if 'element size' in data.keys(): 
                #     read_element_size = data['element size']
                #     if read_element_size != str(element_size):
                #         data['element size'] = str(element_size)
                # else:
                #     data['element size'] = str(element_size)
            
            if geometry_tolerance is not None:
                data['geometry tolerance'] = str(geometry_tolerance)

            if geometry_filename is not None:
                data['geometry file'] = geometry_filename

            self.write_project_setup_in_file(data)
            # self.load(self._project_ini_file_path)