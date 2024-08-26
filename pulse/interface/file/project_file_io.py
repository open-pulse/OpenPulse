from pulse import app
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


class ProjectFile:
    
    def __init__(self, path : str, override=False):
        super().__init__()

        self.path = path
        self.filebox = Filebox(Path(path), override=override)

        # self.model = app().project.model
        # self.properties = self.model.properties

        self._initialize()
        self._default_filenames()

    def _initialize(self):
        self.project_folder_path = Path(os.path.dirname(self.path))

    def _default_filenames(self):

        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.config"
        self.material_library_filename = "material_library.config"

        self.nodal_properties_filename = "nodal_properties.json"
        self.element_properties_filename = "element_properties.json"
        self.line_properties_filename = "line_properties.json"

        self.mesh_data_filename = "mesh_data.hdf5"
        self.imported_table_data_filename = "imported_tables_data.hdf5"
        self.results_data_filename = "results_data.hdf5"
        self.psd_info_filename = "psd_info.json"
        self.valve_info_filename = "valve_info.json"

        self.thumbnail_filename = "thumbnail.png"

    def write_project_setup_in_file(self, data : dict, geometry_path=""):

        if geometry_path != "":
            basename = os.path.basename(geometry_path)
            internal_path = f"geometry_file/{basename}"

            try:
                self.filebox.remove("geometry_file")
            except:
                pass

            self.filebox.write_from_path(internal_path, geometry_path, encoding="iso-8859-1")

        try:

            project_setup = self.filebox.read(self.project_setup_filename)
            if project_setup is None:
                project_setup = dict()

            project_setup["mesher setup"] = data

            self.filebox.write(self.project_setup_filename, project_setup)
            app().main_window.project_data_modified = True

        except Exception as error_log:
            print(str(error_log))

    def read_geometry_from_file(self):

        data = self.filebox.read(self.project_setup_filename)

        if "mesher setup" in data.keys():
            project_setup = data["mesher setup"]

            if "geometry filename" in project_setup.keys():

                geometry_filename = project_setup["geometry filename"]
                dirname = self.project_folder_path / "geometry" 
                temp_path = dirname / geometry_filename
                internal_path = f"geometry_file/{geometry_filename}"

                if os.path.exists(dirname):
                    for filename in os.listdir(dirname).copy():
                        file_path = dirname / filename
                        os.remove(file_path)
                else:
                    os.mkdir(dirname)

                self.filebox.read_to_path(internal_path, temp_path)

                return str(temp_path)
    
    def read_project_setup_from_file(self):
        return self.filebox.read(self.project_setup_filename)

    def write_model_setup_in_file(self, project_setup : dict):
        self.filebox.write(self.project_setup_filename, project_setup)
        app().main_window.project_data_modified = True

    def read_imported_table_from_file(self, folder_name : str, file_name : str):
        internal_path = f"imported_tables/{folder_name}/{file_name}"
        return self.filebox.read(internal_path)

    def create_temporary_folder(self, folder_name : str) -> Path:
        dirname = self.project_folder_path / folder_name
        if not dirname.exists():
            os.makedirs(dirname)
        return dirname

    # def write_imported_table_in_file(self, file_name : str, folder_name : str):

    #     suffix = f"imported_tables/{folder_name}"
    #     dirname = self.project_folder_path / suffix
    #     temp_path = dirname / file_name
    #     internal_path = f"imported_tables/{folder_name}/{file_name}"

    #     self.filebox.write_from_path(internal_path, temp_path)
    #     app().main_window.project_data_modified = True

    def write_material_library_in_file(self, config):
        self.filebox.write(self.material_library_filename, config)
        app().main_window.project_data_modified = True

    def read_material_library_from_file(self):
        return self.filebox.read(self.material_library_filename)

    def write_fluid_library_in_file(self, config):
        self.filebox.write(self.fluid_library_filename, config)
        app().main_window.project_data_modified = True

    def read_fluid_library_from_file(self):
        return self.filebox.read(self.fluid_library_filename)

    def write_psd_data_in_file(self, psds_data: dict):
        if psds_data:
            self.filebox.write(self.psd_info_filename, psds_data)
        else:
            self.filebox.remove(self.psd_info_filename)
        app().main_window.project_data_modified = True

    def read_psd_data_from_file(self):
        return self.filebox.read(self.psd_info_filename)

    def write_valve_info_in_file(self, valve_info: dict):
        if valve_info:
            self.filebox.write(self.valve_info_filename, valve_info)
        else:
            self.filebox.remove(self.valve_info_filename)
        app().main_window.project_data_modified = True

    def read_valves_info_from_file(self):
        return self.filebox.read(self.valve_info_filename)

    def write_analysis_setup_in_file(self, analysis_setup : dict):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return   

        project_setup["analysis setup"] = analysis_setup         
        self.filebox.write(self.project_setup_filename, project_setup)

        app().main_window.project_data_modified = True

    def read_analysis_setup_from_file(self):

        analysis_setup = None
        project_setup = self.filebox.read(self.project_setup_filename)

        if project_setup is None:
            return

        if "analysis setup" in project_setup.keys():
            analysis_setup = project_setup["analysis setup"]

        return analysis_setup

    def write_inertia_load_in_file(self, inertia_load : dict):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return   

        project_setup["inertia load"] = inertia_load         
        self.filebox.write(self.project_setup_filename, project_setup)

        app().main_window.project_data_modified = True

    def read_inertia_load_from_file(self):

        project_setup = self.filebox.read(self.project_setup_filename)

        if project_setup is None:
            return

        inertia_load = None
        if "inertia load" in project_setup.keys():
            inertia_load = project_setup["inertia load"]

        return inertia_load

    def write_nodal_properties_in_file(self):

        try:

            nodal_properties = app().project.model.properties.nodal_properties
            data = normalize_mesh(nodal_properties)

            if nodal_properties:
                self.filebox.write(self.nodal_properties_filename, data)
            else:
                self.filebox.remove(self.nodal_properties_filename)

            app().main_window.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting the nodal properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def read_nodal_properties_from_file(self):

        data = self.filebox.read(self.nodal_properties_filename)

        if data is None:
            return dict()
        
        return denormalize_mesh(data)
    
    def write_element_properties_in_file(self):

        try:

            element_properties = app().project.model.properties.element_properties
            data = normalize_mesh(element_properties)

            if element_properties:
                self.filebox.write(self.element_properties_filename, data)
            else:
                self.filebox.remove(self.element_properties_filename)

            app().main_window.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting element properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def read_element_properties_from_file(self):

        data = self.filebox.read(self.element_properties_filename)

        if data is None:
            return dict()

        return denormalize_mesh(data)

    def write_line_properties_in_file(self):

        try:

            line_properties = app().project.model.properties.line_properties
            data = normalize_lines(line_properties)

            self.filebox.write(self.line_properties_filename, data)
            app().main_window.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting line properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def read_line_properties_from_file(self):
        return self.filebox.read(self.line_properties_filename)

    def write_imported_table_data_in_file(self):

        self.filebox.remove(self.imported_table_data_filename)
        acoustic_imported_tables = app().project.model.properties.acoustic_imported_tables
        structural_imported_tables = app().project.model.properties.structural_imported_tables

        # print(acoustic_imported_tables)
        # print(structural_imported_tables)

        if acoustic_imported_tables or structural_imported_tables:

            with self.filebox.open(self.imported_table_data_filename, "w") as internal_file:
                with h5py.File(internal_file, "w") as f:

                    for group_label in ["acoustic", "structural"]:

                        if group_label == "acoustic":
                            imported_tables = acoustic_imported_tables
                        else:
                            imported_tables = structural_imported_tables

                        for table_name, data_array in imported_tables.items():

                            if table_name is None:
                                continue

                            data_name = f"{group_label}/{table_name}"
                            f.create_dataset(data_name, data=data_array, dtype=float)
                            # print(data_name, data_array.shape)
                            # print("arquivo foi atualizado")

                    app().main_window.project_data_modified = True

    def read_imported_table_data_from_file(self):

        try:
            tables_data = dict()
            with self.filebox.open(self.imported_table_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        aux = dict()
                        for key, values in f.get(group).items():

                            try:
                                aux[key] = np.array(values)
                            except:
                                continue

                        if aux:
                            tables_data[group] = aux

        except:
            return dict()

        return tables_data

    def write_thumbnail(self):
        thumbnail = app().project.thumbnail
        if thumbnail is None:
            return
        self.filebox.write(self.thumbnail_filename, thumbnail)
        app().main_window.project_data_modified = True

    def read_thumbnail(self):
        return self.filebox.read(self.thumbnail_filename)
    
    def write_results_data_in_file(self):
        with self.filebox.open(self.results_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

                acoustic_modal_solver = app().project.acoustic_modal_solver
                if acoustic_modal_solver is not None:
                    if acoustic_modal_solver.modal_shape is not None:
                        natural_frequencies = acoustic_modal_solver.natural_frequencies
                        modal_shape = acoustic_modal_solver.modal_shape
                        f.create_dataset("modal_acoustic/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_acoustic/modal_shape", data=modal_shape, dtype=float)
                
                structural_modal_solver = app().project.structural_modal_solver
                if structural_modal_solver is not None:
                    if structural_modal_solver.modal_shape is not None:
                        natural_frequencies = structural_modal_solver.natural_frequencies
                        modal_shape = structural_modal_solver.modal_shape
                        f.create_dataset("modal_structural/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_structural/modal_shape", data=modal_shape, dtype=float)

                acoustic_harmonic_solver = app().project.acoustic_harmonic_solver
                if acoustic_harmonic_solver is not None:
                    if acoustic_harmonic_solver.solution is not None:
                        frequencies = acoustic_harmonic_solver.frequencies
                        solution = acoustic_harmonic_solver.solution
                        f.create_dataset("harmonic_acoustic/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_acoustic/solution", data=solution, dtype=complex)
                
                structural_harmonic_solver = app().project.structural_harmonic_solver
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

            with self.filebox.open(self.results_data_filename) as internal_file:
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

    def remove_nodal_properties_from_project_file(self):
        self.filebox.remove(self.nodal_properties_filename)
        app().main_window.project_data_modified = True

    def remove_element_properties_from_project_file(self):
        self.filebox.remove(self.element_properties_filename)
        app().main_window.project_data_modified = True

    def remove_line_properties_from_project_file(self):
        self.filebox.remove(self.line_properties_filename)
        app().main_window.project_data_modified = True

    def remove_mesh_data_from_project_file(self):
        self.filebox.remove(self.mesh_data_filename)
        app().main_window.project_data_modified = True

    def remove_results_data_from_project_file(self):
        self.filebox.remove(self.results_data_filename)
        app().main_window.project_data_modified = True

    # def remove_table_from_project_file(self, folder_name : str, file_name : str):
    #     internal_path = f"imported_tables/{folder_name}/{file_name}"
    #     self.filebox.remove(internal_path)
    #     app().main_window.project_data_modified = True

    def check_pipeline_data(self):
        
        project_setup = self.read_project_setup_from_file()
        if project_setup is None:
            return False

        mesher_setup = project_setup["mesher setup"]
        import_type = mesher_setup["import type"]

        lines_data = self.read_line_properties_from_file()
        if lines_data is None:
            return False

        if lines_data:
            for line_id, data in lines_data.items():
                data: dict
                if import_type == 0:
                    return True
                else:
                    keys_to_check = ["start_coords", "end_coords"]
                    for key in keys_to_check:
                        if key not in data.keys():
                            return False
            return True
        else:
            return False

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

        if "mesher setup" in project_setup.keys():

            data = project_setup["mesher setup"]

            if project_name is not None:
                data['name'] = project_name

            if import_type is not None:
                data['import type'] = import_type

            if length_unit is not None:
                data['length unit'] = length_unit

            if element_size is not None:
                data['element size'] = element_size

            if geometry_tolerance is not None:
                data['geometry tolerance'] = geometry_tolerance

            if geometry_filename is not None:
                data['geometry file'] = geometry_filename

            self.write_project_setup_in_file(data)
            # self.load(self._project_ini_file_path)

    def load_analysis_file(self):
        return self.read_analysis_setup_from_file()
    
    def load_thumbnail(self):
        thumbnail = self.read_thumbnail()
        if thumbnail is not None:
            app().project.thumbnail = thumbnail

    def load_nodal_properties_from_file(self):
        return self.read_nodal_properties_from_file()

    def load_element_properties_from_file(self):
        return self.read_element_properties_from_file()

    def load_imported_table_data_from_file(self):
        return self.read_imported_table_data_from_file()
    
    def remove_line_gaps_from_line_properties_file(self):
        
        line_data = self.read_line_properties_from_file()

        tag = 0
        aux = dict()
        cache_lines = list()

        for str_line_id, data in line_data.items():
            tag += 1

            # if int(str_line_id) not in cache_lines:
            #     tag += 1
            #     cache_lines.append(int(str_line_id))

            aux[tag] = data

        app().project.model.properties.line_properties.clear()

        for line_id, _data in aux.items():

            _data: dict
            for property, values in _data.items():
                app().project.model.properties._set_line_property(property, values, line_id)

        if aux:
            app().pulse_file.write_line_properties_in_file()

def denormalize_mesh(prop: dict):

    new_prop = dict()
    for key, val in prop.items():

        if len(key.split()) == 2:
            p, id = key.split()
            p = p.strip()
            id = int(id)
            new_prop[p, id] = val

        elif len(key.split()) == 3:
            p, id_1, id_2 = key.split()
            id_1 = int(id_1)
            id_2 = int(id_2)
            new_prop[p, id_1, id_2] = val

    return new_prop

def normalize_mesh(prop: dict):
    """
    Sadly json doesn't accepts tuple keys,
    so we need to convert it to a string like:
    "property id" = value
    """
    output = dict()
    for (property, *args), data in prop.items():

        aux = dict()
        if len(args) == 1:
            key = f"{property} {args[0]}"
        elif len(args) == 2:
            key = f"{property} {args[0]} {args[1]}"

        if isinstance(data, dict):
            for _key, _data in data.items():
                if _key in ["values", "link_data"]:
                    continue
                aux[_key] = _data

        if aux:
            output[key] = aux

    return output


def normalize_lines(prop: dict):
    """
    Sadly json doesn't accepts tuple keys,
    so we need to convert it to a string like:
    "property id" = value
    """
    output = dict()
    for tag, data in prop.items():

        aux = dict()
        for property in data.keys():
            value = data[property]
            if property in ["fluid", "material",  "cross_section"]:
                continue
            else:
                aux[property] = value

        if aux:
            output[tag] = aux

    return output

