from typing import TYPE_CHECKING

from pulse import TEMP_PROJECT_DIR, app
from pulse.model import AnalysisID
from pulse.model.data_classes.project_setup_data_classes import ImportType, MesherSetup, ProjectSetup
from pulse.utils.common_utils import get_color_rgb, get_list_of_values_from_string

if TYPE_CHECKING:
    from pulse.project.project import Project

import json
import os
import shutil
import zipfile
from configparser import ConfigParser
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

import h5py
import numpy as np
from PIL import Image


class ProjectFile:

    def __init__(self, project: 'Project', path: str | Path = TEMP_PROJECT_DIR):
        super().__init__()

        self.project = project
        self.path = Path(path)

        self._initialize()
        self._default_filenames()

    def _initialize(self):
        self.project_folder_path = self.path

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

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _file_path(self, filename: str) -> Path:
        return self.path / filename

    def _read_file(self, filename: str):
        """Read a file from the project directory. Returns a Python object."""
        path = self._file_path(filename)
        if not path.exists() or path.stat().st_size == 0:
            return None

        suffix = path.suffix.lower()
        if suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif suffix == ".config":
            config = ConfigParser()
            config.read(str(path))
            return config
        elif suffix == ".png":
            return Image.open(path).copy()
        return path.read_bytes()

    def _write_file(self, filename: str, data):
        """Write a Python object to a file in the project directory."""
        path = self._file_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        suffix = path.suffix.lower()
        if suffix == ".json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        elif suffix == ".config":
            with open(path, "w", encoding="utf-8") as f:
                data.write(f)
        elif suffix == ".png":
            data.save(path)
        else:
            path.write_bytes(data)

    @contextmanager
    def _open_file(self, filename: str, mode: str = "r"):
        """Yield the Path for a file inside the project directory (for h5py use)."""
        path = self._file_path(filename)
        if "w" in mode:
            path.parent.mkdir(parents=True, exist_ok=True)
        yield path

    def _remove_file(self, filename: str):
        """Remove a file or directory from the project directory."""
        path = self._file_path(filename)
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    def _copy_to_dir(self, internal_path: str, source_path: str):
        """Copy an external file into the project directory."""
        dest = self._file_path(internal_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest)

    def _copy_from_dir(self, internal_path: str, dest_path):
        """Copy a file from the project directory to an external path."""
        src = self._file_path(internal_path)
        shutil.copy2(src, dest_path)

    # ── Archive / extract ─────────────────────────────────────────────────────

    def archive_to_file(self, dest_path: str | Path):
        """Archive all files in the project directory to a .pulse zip file."""
        dest_path = Path(dest_path)
        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in self.path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.path)
                    zf.write(file_path, arcname)

    def extract_from_file(self, source_path: str | Path):
        """Extract a .pulse zip file into the project directory (clears it first)."""
        source_path = Path(source_path)
        if self.path.exists():
            for item in list(self.path.iterdir()):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        self.path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(source_path, "r") as zf:
            zf.extractall(self.path)

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def project_data_modified_callback(self):
        if app() is None:
            return

        app().main_window.project_data_modified = True

    # ── Project setup ─────────────────────────────────────────────────────────

    def write_project_setup_in_file(self, project_setup: dict):
        geometry_path = project_setup.get("geometry_path_source", "")

        if geometry_path != "":
            basename = os.path.basename(geometry_path)
            internal_path = f"geometry_file/{basename}"

            try:
                self._remove_file("geometry_file")
            except Exception:
                pass

            self._copy_to_dir(internal_path, geometry_path)

        self._write_file(self.project_setup_filename, project_setup)
        self.project_data_modified_callback()

    def read_geometry_from_file(self):

        project_setup = self._read_file(self.project_setup_filename)
        if not isinstance(project_setup, dict):
            return ""
        
        geometry_filename = project_setup.get("geometry_filename")
        geometry_path = self.path / f"geometry_file/{geometry_filename}"

        if geometry_path.exists():
            return str(geometry_path)

    def read_project_setup_from_file(self):
        return self._read_file(self.project_setup_filename)
    
    def read_mesher_setup_from_file(self) -> None | MesherSetup:
        project_setup = self._read_file(self.project_setup_filename)
        if not isinstance(project_setup, dict):
            return

        mesh_setup = project_setup.get("mesher_setup")
        if mesh_setup is None:
            return

        return MesherSetup(**mesh_setup)
    
    def write_model_setup_in_file(self, project_setup: dict):
        self._write_file(self.project_setup_filename, project_setup)
        self.project_data_modified_callback()

    def read_imported_table_from_file(self, folder_name: str, file_name: str):
        internal_path = f"imported_tables/{folder_name}/{file_name}"
        return self._read_file(internal_path)

    def create_temporary_folder(self, folder_name: str) -> Path:
        dirname = self.project_folder_path / folder_name
        if not dirname.exists():
            os.makedirs(dirname)
        return dirname

    # ── Libraries ─────────────────────────────────────────────────────────────

    def write_material_library_in_file(self, config):
        self._write_file(self.material_library_filename, config)
        self.project_data_modified_callback()

    def read_material_library_from_file(self) -> dict:
        self.backward_compatibility_for_materials_data_file()
        return self._read_file(self.material_library_filename)

    def write_fluid_library_in_file(self, config):
        self._write_file(self.fluid_library_filename, config)
        self.project_data_modified_callback()

    def read_fluid_library_from_file(self) -> dict:
        self.backward_compatibility_for_fluids_data_file()
        return self._read_file(self.fluid_library_filename)

    # ── PSD / damper / valve ──────────────────────────────────────────────────

    def write_psd_data_in_file(self, psds_data: dict):
        if psds_data:
            self._write_file(self.psd_info_filename, psds_data)
        else:
            self._remove_file(self.psd_info_filename)
        self.project_data_modified_callback()

    def read_psd_data_from_file(self):
        return self._read_file(self.psd_info_filename)

    def write_pulsation_damper_data_in_file(self, damper_data: dict):
        if damper_data:
            self._write_file(self.pulsation_damper_info_filename, damper_data)
        else:
            self._remove_file(self.pulsation_damper_info_filename)
        self.project_data_modified_callback()

    def read_pulsation_damper_data_from_file(self):
        return self._read_file(self.pulsation_damper_info_filename)

    def write_valve_info_in_file(self, valve_info: dict):
        if valve_info:
            self._write_file(self.valve_info_filename, valve_info)
        else:
            self._remove_file(self.valve_info_filename)
        self.project_data_modified_callback()

    def read_valves_info_from_file(self):
        return self._read_file(self.valve_info_filename)

    # ── Analysis setup ────────────────────────────────────────────────────────

    def write_analysis_setup_in_file(self, analysis_setup: dict):

        project_setup = self._read_file(self.project_setup_filename)
        if project_setup is None:
            return

        _analysis_setup = dict()
        for key, data in analysis_setup.items():

            if isinstance(data, np.ndarray):
                if data.size == 0:
                    continue

                data = list(data)

            _analysis_setup[key] = data

        project_setup.update({"analysis_setup" : _analysis_setup})

        self._write_file(self.project_setup_filename, project_setup)
        self.project_data_modified_callback()

    def read_analysis_setup_from_file(self):

        project_setup = self._read_file(self.project_setup_filename)
        if not isinstance(project_setup, dict):
            return

        return project_setup.get("analysis_setup", dict())

    def write_inertia_load_in_file(self, inertia_load: dict):

        project_setup = self._read_file(self.project_setup_filename)
        if project_setup is None:
            return

        project_setup["inertia_load"] = inertia_load
        self._write_file(self.project_setup_filename, project_setup)

        self.project_data_modified_callback()

    def read_inertia_load_from_file(self):

        project_setup = self._read_file(self.project_setup_filename)

        if project_setup is None:
            return

        inertia_load = None
        if "inertia_load" in project_setup.keys():
            inertia_load = project_setup["inertia_load"]

        return inertia_load

    # ── Mesh properties ───────────────────────────────────────────────────────

    def write_nodal_properties_in_file(self):

        nodal_properties = self.project.model.properties.nodal_properties
        data = normalize_mesh(nodal_properties)

        if nodal_properties:
            self._write_file(self.nodal_properties_filename, data)
        else:
            self._remove_file(self.nodal_properties_filename)

        self.project_data_modified_callback()

    def read_nodal_properties_from_file(self):

        data = self._read_file(self.nodal_properties_filename)

        if data is None:
            return dict()

        return denormalize_mesh(data)

    def write_element_properties_in_file(self):

        element_properties = self.project.model.properties.element_properties
        data = normalize_mesh(element_properties)

        if element_properties:
            self._write_file(self.element_properties_filename, data)
        else:
            self._remove_file(self.element_properties_filename)

        self.project_data_modified_callback()

    def read_element_properties_from_file(self):

        data = self._read_file(self.element_properties_filename)

        if data is None:
            return dict()

        return denormalize_mesh(data)

    def write_line_properties_in_file(self):

        line_properties = self.project.model.properties.line_properties
        data = normalize_lines(line_properties)

        self._write_file(self.line_properties_filename, data)
        self.project_data_modified_callback()

    def read_line_properties_from_file(self):
        return self._read_file(self.line_properties_filename)

    # ── Imported tables ───────────────────────────────────────────────────────

    def write_imported_table_data_in_file(self):

        self._remove_file(self.imported_table_data_filename)
        acoustic_imported_tables = self.project.model.properties.acoustic_imported_tables
        structural_imported_tables = self.project.model.properties.structural_imported_tables

        if acoustic_imported_tables or structural_imported_tables:

            with self._open_file(self.imported_table_data_filename, "w") as internal_file:
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
            with self._open_file(self.imported_table_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        aux = dict()
                        for key, values in f.get(group).items():

                            try:
                                aux[key] = np.array(values)
                            except Exception:
                                continue

                        if aux:
                            tables_data[group] = aux

        except Exception:
            return dict()

        return tables_data

    # ── Thumbnail ─────────────────────────────────────────────────────────────

    def write_thumbnail(self):
        thumbnail = self.project.thumbnail
        if thumbnail is None:
            return
        self._write_file(self.thumbnail_filename, thumbnail)
        self.project_data_modified_callback()

    def read_thumbnail(self):
        return self._read_file(self.thumbnail_filename)

    # ── Results ───────────────────────────────────────────────────────────────

    def write_results_data_in_file(self):

        self.remove_results_data_from_project_file()

        with self._open_file(self.results_data_filename, "w") as internal_file:
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

            with self._open_file(self.results_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        aux = dict()
                        for key, values in f.get(group).items():

                            try:
                                aux[key] = np.array(values)
                            except Exception:
                                continue

                        if aux:
                            results_data[group] = aux

        except Exception:
            return dict()

        return results_data

    # ── Remove helpers ────────────────────────────────────────────────────────

    def remove_nodal_properties_from_project_file(self):
        self._remove_file(self.nodal_properties_filename)
        self.project_data_modified_callback()

    def remove_element_properties_from_project_file(self):
        self._remove_file(self.element_properties_filename)
        self.project_data_modified_callback()

    def remove_line_properties_from_project_file(self):
        self._remove_file(self.line_properties_filename)
        self.project_data_modified_callback()

    def remove_mesh_data_from_project_file(self):
        self._remove_file(self.mesh_data_filename)
        self.project_data_modified_callback()

    def remove_results_data_from_project_file(self):
        self._remove_file(self.results_data_filename)
        self.project_data_modified_callback()

    # ── Checks and misc ───────────────────────────────────────────────────────

    def check_pipeline_data(self):

        project_setup = self.read_project_setup_from_file()
        if not isinstance(project_setup, dict):
            return False

        lines_data = self.read_line_properties_from_file()
        if lines_data is None:
            return False

        if not lines_data:
            return False

        import_type = project_setup.get("import_type")

        for line_data in lines_data.values():
            line_data: dict
            if import_type == ImportType.CAD_FILE:
                return True
            
            keys_to_check = ["start_coords", "end_coords"]
            for key in keys_to_check:
                coords = line_data.get(key)
                if coords is None:
                    return False

        return True

    def modify_project_attributes(self, new_project_setup: ProjectSetup):
        project_setup = self.read_project_setup_from_file()
        if not isinstance(project_setup, dict):
            project_setup = dict()

        # update the project_setup to maintain the analysis_setup
        project_setup.update(new_project_setup.as_dict())
        self.write_project_setup_in_file(project_setup)

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

        for str_line_id, data in line_data.items():
            tag += 1
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

        fluid_data = self.convert_fluid_data_from_configparser_to_dictionary(cpath, remove_after_convert=True)
        if fluid_data:
            self.write_fluid_library_in_file(fluid_data)

    def backward_compatibility_for_materials_data_file(self):
        filename = deepcopy(str(self.material_library_filename))
        cpath = Path(self.path) / filename.replace(".json", ".config")
        if not cpath.exists():
            return

        material_data = self.convert_material_data_from_configparser_to_dictionary(cpath, remove_after_convert=True)
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
                "density" : float(section.get('density', -1)),
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
                "density" : float(section.get('density', -1)),
                "poisson_ratio" : float(section.get('poisson_ratio', -1)),
                "elasticity_modulus" : 1e9 * float(section.get('elasticity_modulus', -1)),
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
