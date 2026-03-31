from pulse import app, version
from pulse.model import AnalysisID
from pulse.utils.common_utils import get_color_rgb, get_list_of_values_from_string

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.project.project import Project

from configparser import ConfigParser
from copy import deepcopy
from fileboxes import Filebox

import os
import h5py
import numpy as np

from pathlib import Path


class ProjectFile:
    
    def __init__(self, project: 'Project', path: str, override=False):
        super().__init__()

        self.project = project
        self.path = path

        self.filebox = Filebox(Path(path), override=override)

        self._initialize()
        self._default_filenames()

    def _initialize(self):
        self.project_folder_path = Path(os.path.dirname(self.path))

    def _default_filenames(self):

        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.json"
        self.material_library_filename = "material_library.json"

        self.nodal_properties_filename = "nodal_properties.json"
        self.element_properties_filename = "element_properties.json"
        self.line_properties_filename = "line_properties.json"

        self.mesh_data_filename = "mesh_data.hdf5"
        self.imported_table_data_filename = "imported_tables_data.hdf5"
        self.results_data_filename = "results_data.hdf5"
        self.psd_info_filename = "psd_info.json"
        self.pulsation_damper_info_filename = "pulsation_damper_info.json"
        self.valve_info_filename = "valve_info.json"

        self.thumbnail_filename = "thumbnail.png"

    def project_data_modified_callback(self):
        if app() is None:
            return

        app().main_window.project_data_modified = True

    def write_project_setup_in_file(self, data: dict, geometry_path=""):

        if geometry_path != "":
            basename = os.path.basename(geometry_path)
            internal_path = f"geometry_file/{basename}"

            try:
                self.filebox.remove("geometry_file")
            except:
                pass

            self.filebox.write_from_path(internal_path, geometry_path, encoding="iso-8859-1")

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            project_setup = dict()

        project_setup["mesher_setup"] = data
        project_setup["version"] = version()

        self.filebox.write(self.project_setup_filename, project_setup)
        self.project_data_modified_callback()

    def read_geometry_from_file(self):

        data = self.filebox.read(self.project_setup_filename)

        if "mesher_setup" in data.keys():
            project_setup = data["mesher_setup"]

            if "geometry_filename" in project_setup.keys():

                geometry_filename = project_setup["geometry_filename"]
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

    def write_model_setup_in_file(self, project_setup: dict):
        self.filebox.write(self.project_setup_filename, project_setup)
        self.project_data_modified_callback()

    def read_imported_table_from_file(self, folder_name: str, file_name: str):
        internal_path = f"imported_tables/{folder_name}/{file_name}"
        return self.filebox.read(internal_path)

    def create_temporary_folder(self, folder_name: str) -> Path:
        dirname = self.project_folder_path / folder_name
        if not dirname.exists():
            os.makedirs(dirname)
        return dirname

    def write_material_library_in_file(self, config):
        self.filebox.write(self.material_library_filename, config)
        self.project_data_modified_callback()

    def read_material_library_from_file(self) -> dict:
        self.backward_compatibility_for_materials_data_file()
        return self.filebox.read(self.material_library_filename)

    def write_fluid_library_in_file(self, config):
        self.filebox.write(self.fluid_library_filename, config)
        self.project_data_modified_callback()

    def read_fluid_library_from_file(self) -> dict:
        self.backward_compatibility_for_fluids_data_file()
        return self.filebox.read(self.fluid_library_filename)

    def write_psd_data_in_file(self, psds_data: dict):
        if psds_data:
            self.filebox.write(self.psd_info_filename, psds_data)
        else:
            self.filebox.remove(self.psd_info_filename)
        self.project_data_modified_callback()

    def read_psd_data_from_file(self):
        return self.filebox.read(self.psd_info_filename)

    def write_pulsation_damper_data_in_file(self, damper_data: dict):
        if damper_data:
            self.filebox.write(self.pulsation_damper_info_filename, damper_data)
        else:
            self.filebox.remove(self.pulsation_damper_info_filename)
        self.project_data_modified_callback()

    def read_pulsation_damper_data_from_file(self):
        return self.filebox.read(self.pulsation_damper_info_filename)

    def write_valve_info_in_file(self, valve_info: dict):
        if valve_info:
            self.filebox.write(self.valve_info_filename, valve_info)
        else:
            self.filebox.remove(self.valve_info_filename)
        self.project_data_modified_callback()

    def read_valves_info_from_file(self):
        return self.filebox.read(self.valve_info_filename)

    def write_analysis_setup_in_file(self, analysis_setup: dict):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return
       
        _analysis_setup = dict()
        for key, data in analysis_setup.items():

            if isinstance(data, np.ndarray):
                if data.size == 0:
                    continue

                data = list(data)

            _analysis_setup[key] = data

        project_setup["analysis_setup"] = _analysis_setup 
        self.filebox.write(self.project_setup_filename, project_setup)

        self.project_data_modified_callback()

    def read_analysis_setup_from_file(self):

        project_setup = self.filebox.read(self.project_setup_filename)
        if not isinstance(project_setup, dict):
            return dict()

        return project_setup.get("analysis_setup", dict())

    def write_inertia_load_in_file(self, inertia_load: dict):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return   

        project_setup["inertia_load"] = inertia_load         
        self.filebox.write(self.project_setup_filename, project_setup)

        self.project_data_modified_callback()

    def read_inertia_load_from_file(self):

        project_setup = self.filebox.read(self.project_setup_filename)

        if project_setup is None:
            return

        inertia_load = None
        if "inertia_load" in project_setup.keys():
            inertia_load = project_setup["inertia_load"]

        return inertia_load

    def write_nodal_properties_in_file(self):

        nodal_properties = self.project.model.properties.nodal_properties
        data = normalize_mesh(nodal_properties)

        if nodal_properties:
            self.filebox.write(self.nodal_properties_filename, data)
        else:
            self.filebox.remove(self.nodal_properties_filename)

        self.project_data_modified_callback()

    def read_nodal_properties_from_file(self):

        data = self.filebox.read(self.nodal_properties_filename)

        if data is None:
            return dict()
        
        return denormalize_mesh(data)
    
    def write_element_properties_in_file(self):

        element_properties = self.project.model.properties.element_properties
        data = normalize_mesh(element_properties)

        if element_properties:
            self.filebox.write(self.element_properties_filename, data)
        else:
            self.filebox.remove(self.element_properties_filename)

        self.project_data_modified_callback()

    def read_element_properties_from_file(self):

        data = self.filebox.read(self.element_properties_filename)

        if data is None:
            return dict()

        return denormalize_mesh(data)

    def write_line_properties_in_file(self):

        line_properties = self.project.model.properties.line_properties
        data = normalize_lines(line_properties)

        self.filebox.write(self.line_properties_filename, data)
        self.project_data_modified_callback()

    def read_line_properties_from_file(self):
        return self.filebox.read(self.line_properties_filename)

    def write_imported_table_data_in_file(self):

        self.filebox.remove(self.imported_table_data_filename)
        acoustic_imported_tables = self.project.model.properties.acoustic_imported_tables
        structural_imported_tables = self.project.model.properties.structural_imported_tables

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

                    self.project_data_modified_callback()

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
        thumbnail = self.project.thumbnail
        if thumbnail is None:
            return
        self.filebox.write(self.thumbnail_filename, thumbnail)
        self.project_data_modified_callback()

    def read_thumbnail(self):
        return self.filebox.read(self.thumbnail_filename)
    
    def write_results_data_in_file(self):

        self.remove_results_data_from_project_file()

        with self.filebox.open(self.results_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

                analysis_id = self.project.analysis_id
                acoustic_solver = self.project.acoustic_solver
                structural_solver = self.project.structural_solver

                if analysis_id == AnalysisID.STRUCTURAL_MODAL:
                    if structural_solver.modal_shapes is not None:
                        natural_frequencies = structural_solver.natural_frequencies
                        modal_shape = structural_solver.modal_shapes
                        f.create_dataset("modal_structural/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_structural/modal_shape", data=modal_shape, dtype=float)

                if analysis_id == AnalysisID.ACOUSTIC_MODAL:
                    if acoustic_solver.modal_shapes is not None:
                        natural_frequencies = acoustic_solver.natural_frequencies
                        modal_shape = acoustic_solver.modal_shapes
                        complex_natural_frequencies = acoustic_solver.complex_natural_frequencies 
                        if isinstance(complex_natural_frequencies, np.ndarray):
                            f.create_dataset("modal_acoustic/natural_frequencies", data=complex_natural_frequencies, dtype=complex)
                        else:
                            f.create_dataset("modal_acoustic/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_acoustic/modal_shape", data=modal_shape, dtype=complex)

                if analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
                    if acoustic_solver.solution is not None:
                        frequencies = acoustic_solver.frequencies
                        solution = acoustic_solver.solution
                        f.create_dataset("harmonic_acoustic/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_acoustic/solution", data=solution, dtype=complex)

                if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
                    if structural_solver.solution is not None:
                        frequencies = structural_solver.frequencies
                        solution = structural_solver.solution
                        f.create_dataset("harmonic_structural/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_structural/solution", data=solution, dtype=complex)

                if analysis_id == AnalysisID.STRUCTURAL_STATIC:
                    if structural_solver.solution is not None:
                        solution = structural_solver.solution
                        f.create_dataset("static_structural/solution", data=solution, dtype=complex)

                self.project_data_modified_callback()

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
        self.project_data_modified_callback()

    def remove_element_properties_from_project_file(self):
        self.filebox.remove(self.element_properties_filename)
        self.project_data_modified_callback()

    def remove_line_properties_from_project_file(self):
        self.filebox.remove(self.line_properties_filename)
        self.project_data_modified_callback()

    def remove_mesh_data_from_project_file(self):
        self.filebox.remove(self.mesh_data_filename)
        self.project_data_modified_callback()

    def remove_results_data_from_project_file(self):
        self.filebox.remove(self.results_data_filename)
        self.project_data_modified_callback()

    # def remove_table_from_project_file(self, folder_name: str, file_name: str):
    #     internal_path = f"imported_tables/{folder_name}/{file_name}"
    #     self.filebox.remove(internal_path)
    #     self.project_data_modified_callback()

    def check_pipeline_data(self):
        
        project_setup = self.read_project_setup_from_file()
        if project_setup is None:
            return False

        mesher_setup = project_setup["mesher_setup"]
        import_type = mesher_setup["import_type"]

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

        if "mesher_setup" in project_setup.keys():

            data = project_setup["mesher_setup"]

            if project_name is not None:
                data['project_name'] = project_name

            if import_type is not None:
                data['import_type'] = import_type

            if length_unit is not None:
                data['length_unit'] = length_unit

            if element_size is not None:
                data['element_size'] = element_size

            if geometry_tolerance is not None:
                data['geometry_tolerance'] = geometry_tolerance

            if geometry_filename is not None:
                data['geometry_filename'] = geometry_filename

            self.write_project_setup_in_file(data)
            # self.load(self._project_ini_file_path)

    def load_analysis_file(self):
        return self.read_analysis_setup_from_file()
    
    def load_thumbnail(self):
        thumbnail = self.read_thumbnail()
        if thumbnail is not None:
            self.project.thumbnail = thumbnail

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
        # cache_lines = list()

        for str_line_id, data in line_data.items():
            tag += 1

            # if int(str_line_id) not in cache_lines:
            #     tag += 1
            #     cache_lines.append(int(str_line_id))

            aux[tag] = data

        self.project.model.properties.line_properties.clear()

        for line_id, _data in aux.items():

            _data: dict
            for property, values in _data.items():
                self.project.model.properties._set_line_property(property, values, line_id)

        if aux:
            app().project.file.write_line_properties_in_file()

    def backward_compatibility_for_fluids_data_file(self):
        filename = deepcopy(str(self.fluid_library_filename))
        cpath = Path(self.path) / filename.replace(".json", ".config")
        if not cpath.exists():
            return

        fluid_data = self.convert_fluid_data_from_configparser_to_dictionary(cpath, remove_after_convert=False)
        if fluid_data:
            self.write_fluid_library_in_file(fluid_data)

    def backward_compatibility_for_materials_data_file(self):
        filename = deepcopy(str(self.material_library_filename))
        cpath = Path(self.path) / filename.replace(".json", ".config")
        if not cpath.exists():
            return

        material_data = self.convert_material_data_from_configparser_to_dictionary(cpath, remove_after_convert=False)
        if material_data:
            self.write_material_library_in_file(material_data)

    def convert_fluid_data_from_configparser_to_dictionary(self, path: Path, remove_after_convert: bool=False) -> dict:

        if not path.exists():
            return dict()

        with open(path) as file:
            config_string = file.read()
            config = ConfigParser()
            config.read_string(config_string)

        fluid_data = dict()

        for tag in config.sections():

            section = config[tag]
            keys = section.keys()

            identifier = int(section.get('identifier', -1))

            fluid_parameters = {
                "name" : section.get("name", ""),
                "identifier" : identifier,
                "fluid_density" : float(section.get('fluid_density', -1)),
                "speed_of_sound" : float(section.get('speed_of_sound', -1)),
                "isentropic_exponent" : float(section.get('isentropic_exponent', -1)),
                "thermal_conductivity" : float(section.get('thermal_conductivity', -1)),
                "specific_heat_Cp" : float(section.get('specific_heat_Cp', -1)),
                "dynamic_viscosity" : float(section.get('dynamic_viscosity', -1)),
                "temperature" : float(section.get('temperature', -1)),
                "pressure" : float(section.get('pressure', -1)),
                "molar_mass" : float(section.get('molar_mass', -1)),
                "color" : get_color_rgb(section.get('color')),
                }

            if 'key_mixture' in keys:
                fluid_parameters["key_mixture"] = section.get('key_mixture')

            if 'molar_fractions' in keys:
                str_molar_fractions = section.get('molar_fractions')
                molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
                fluid_parameters["molar_fractions"] = molar_fractions

            fluid_data[identifier] = fluid_parameters

        if remove_after_convert:
            path.unlink()

        return fluid_data

    def convert_material_data_from_configparser_to_dictionary(self, path: Path, remove_after_convert: bool=False) -> dict:

        if not path.exists():
            return dict()

        with open(path) as file:
            config_string = file.read()
            config = ConfigParser()
            config.read_string(config_string)

        material_library_data = dict()

        for tag in config.sections():

            section = config[tag]
            identifier = int(section.get('identifier', -1))

            material_parameters = {
                "name" : section.get("name", ""),
                "identifier" : identifier,
                "material_density" : float(section.get('material_density', -1)),
                "poisson_ratio" : float(section.get('poisson_ratio', -1)),
                "elasticity_modulus" : float(section.get('elasticity_modulus', -1)),
                "thermal_expansion_coefficient" : float(section.get('thermal_expansion_coefficient', -1)),
                "color" : get_color_rgb(section.get('color')),
                }

            material_library_data[identifier] = material_parameters

        if remove_after_convert:
            path.unlink()

        return material_library_data

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


def normalize_lines(line_properties: dict):
    """
    Sadly json doesn't accepts tuple keys,
    so we need to convert it to a string like:
    "property id" = value
    """
    output = dict()
    for tag, line_data in line_properties.items():

        aux = dict()
        line_data: dict
       
        for prop_key, prop_data in line_data.items():
            if prop_key in ["fluid", "material",  "cross_section"]:
                continue

            if prop_key != "expansion_joint_info":
                aux[prop_key] = prop_data
        
            else:

                if not isinstance(prop_data, dict):
                    continue
                
                aux_ej_data = dict()
                for _key, _data in prop_data.items():
                    if isinstance(_data, list | tuple):
                        if any(isinstance(x, np.ndarray) for x in _data):
                            continue

                    aux_ej_data[_key] = _data

                aux[prop_key] = aux_ej_data

        if aux:
            output[tag] = aux

    return output