from pulse import app
from pulse.tools.utils import *

import os
import configparser
import numpy as np
from pathlib import Path
from pprint import pprint

# fmt: off
    
def translate_to_connection_point(points, connection_point):
    translated_points = list()
    for point in points:
        translated_point = point + connection_point
        translated_points.append(translated_point)
    return translated_points    
    
def rotation_matrix_y(angle):
    return np.array([[ np.cos(angle), 0, np.sin(angle)], 
                     [             0, 1,             0], 
                     [-np.sin(angle), 0, np.cos(angle)]], dtype=float)

def rotation_matrix_z(self, angle):
    return np.array([[ np.cos(angle), -np.sin(angle), 0],
                     [ np.sin(angle),  np.cos(angle), 0], 
                     [             0,              0, 1]], dtype=float)

def rotate_points(points, axis="along x-axis"):
    if axis == "along y-axis":
        matrix = rotation_matrix_z(np.pi/2)
    elif axis == "along z-axis":
        matrix = rotation_matrix_y(np.pi/2)
    else:
        matrix = np.identity(3)

    rotated_points = list()
    for point in points:
        rotated_point = matrix @ point
        rotated_points.append(rotated_point)
    
    return rotated_points

class SingleChamberPSD:
    def __init__(self, device_data : dict) -> None:
            
        self.unwrap_device_data(device_data)

    def unwrap_device_data(self, device_data : dict):

        self.connection_type = device_data["connection type"]
        self.connection_point = device_data["connecting coords"]
        self.axis = device_data["main axis"]

        [   self.inlet_pipe_length,
            self.inlet_pipe_diameter,
            self.inlet_pipe_wall_thickness,
            self.inlet_pipe_distance,
            self.inlet_pipe_angle   ] = device_data["pipe #1 parameters"]

        [   self.outlet_pipe_length,
            self.outlet_pipe_diameter,
            self.outlet_pipe_wall_thickness,
            self.outlet_pipe_distance,
            self.outlet_pipe_angle   ] = device_data["pipe #2 parameters"]

        [   self.main_chamber_length,
            self.main_chamber_diameter,
            self.main_chamber_wall_thickness   ] = device_data["volume #1 parameters"]

    def get_points(self):

        # P0 -> connection point between inlet pipe and main chamber
        # P1 -> connection point between outlet pipe and main chamber
        # Q0 -> start point of the main chamber
        # Q1 -> end point of the main chamber

        versor_x = np.array([1, 0, 0], dtype=float)
        versor_y = np.array([0, 1, 0], dtype=float)
        inlet = np.array([0, 0, 0], dtype=float)

        if self.connection_type == "discharge":
            P0 = inlet - versor_y * self.inlet_pipe_length
            Q0 = P0 - versor_x * self.inlet_pipe_distance
            P1 = Q0 + versor_x * self.outlet_pipe_distance
            Q1 = Q0 + versor_x * self.main_chamber_length
            outlet = P1 - versor_y * self.outlet_pipe_length

        else:
            P0 = inlet + versor_y * self.inlet_pipe_length
            Q0 = P0 - versor_x * self.inlet_pipe_distance
            P1 = Q0 + versor_x * self.outlet_pipe_distance
            Q1 = Q0 + versor_x * self.main_chamber_length
            outlet = P1 + versor_y * self.outlet_pipe_length

        base_points = [inlet, outlet, P0, P1, Q0, Q1]
        rot_points = rotate_points(base_points, axis=self.axis)
        inlet, outlet, P0, P1, Q0, Q1 = translate_to_connection_point(rot_points, self.connection_point)

        if np.linalg.norm(P0-Q0) > np.linalg.norm(P1-Q0):
            self.start_points = [inlet, outlet, Q0, P1, P0]
            self.end_points = [P0, P1, P1, P0, Q1]
        else:
            self.start_points = [inlet, outlet, Q0, P0, P1]
            self.end_points = [P0, P1, P0, P1, Q1]

    def get_section_parameters(self):
        self.section_parameters = list()
        self.section_parameters.append([self.inlet_pipe_diameter, self.inlet_pipe_wall_thickness, 0, 0, 0, 0])
        self.section_parameters.append([self.outlet_pipe_diameter, self.outlet_pipe_wall_thickness, 0, 0, 0, 0])
        self.section_parameters.append([self.main_chamber_diameter, self.main_chamber_wall_thickness, 0, 0, 0, 0])

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()
    
    def _initialize(self):
        self.pulsation_suppression_device = dict()
        self.psd_entity_data = dict()

    def add_pulsation_suppression_device(self, device_label, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                break

        if "volume #2 parameters" in suppression_device_data.keys():
            return
            self.psd_entity_data[device_label] = DualChambersPSD(suppression_device_data)
        else:
            self.psd_entity_data[device_label] = SingleChamberPSD(suppression_device_data)
        
        self.pulsation_suppression_device[device_label] = suppression_device_data
        self.write_suppression_device_data_in_file()

    def build_device(self, device_label):

        entity_path = self.file._entity_path
        config = configparser.ConfigParser()
        config.read(entity_path)

        line_tags = list()
        for section in config.sections():
            if "-" in section:
                tag = int(section.split("-")[0])
            else:
                tag = int(section)

            if tag in line_tags:
                continue
            line_tags.append(tag)

        if line_tags:
            shifted_line = max(line_tags) + 1
        else:
            shifted_line = 1

        device = self.psd_entity_data[device_label]
        device.get_points()
        device.get_section_parameters()

        for i in range(len(device.start_points)):

            section_parameters = device.section_parameters[i] if i < 2 else device.section_parameters[2]

            aux = { 
                    "start point" : list(np.round(device.start_points[i], 6)),
                    "end point" : list(np.round(device.end_points[i], 6)),
                    "section type" : "Pipe section",
                    "section parameters" : section_parameters,
                    "structural element type" : "pipe_1",
                    "psd label" : device_label
                    }

            tag = int(shifted_line + i)
            config[str(tag)] = aux

        with open(entity_path, 'w') as config_file:
            config.write(config_file)

        self.load_project()  

    def write_suppression_device_data_in_file(self):
    
        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.dat"

        config = configparser.ConfigParser()

        for key, data in self.pulsation_suppression_device.items():
            config[key] = data

        if list(config.sections()):
            with open(path, 'w') as config_file:
                config.write(config_file)
        else:
            os.remove(path)

    def load_suppression_device_data_from_file(self):
    
        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.dat"

        if os.path.exists(path):

            config = configparser.ConfigParser()
            config.read(path)

            list_data_keys = [  "connecting coords",
                                "volume #1 parameters",
                                "volume #2 parameters",
                                "pipe #1 parameters",
                                "pipe #2 parameters",
                                "pipe #3 parameters"  ]

            for tag in config.sections():

                aux = dict()
                section = config[tag]

                for key in section.keys():

                    if key in ["main axis", "connection type", "volumes connection"]:
                        aux[key] = section[key]

                    elif key == "volumes spacing":
                        aux[key] = float(section[key])

                    elif key in list_data_keys:
                        aux[key] = get_list_of_values_from_string(section[key], int_values=False)

                if aux:
                    self.pulsation_suppression_device[tag] = aux

    def delete_device_related_lines(self, device_label):

        entity_path = self.file._entity_path
        config = configparser.ConfigParser()
        config.read(entity_path)

        psd_lines= list()

        for section in config.sections():
            try:
                if config[section]["psd label"] == device_label:
                    config.remove_section(section)
                    psd_lines.append(int(section))
            except:
                pass
        
        with open(entity_path, 'w') as config_file:
            config.write(config_file)

    def remove_suppression_device(self, device_label):

        if device_label in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(device_label)

        self.write_suppression_device_data_in_file()
        self.delete_device_related_lines(device_label)
        self.load_project()

    def load_project(self):
        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_widget.initial_project_action(True)
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.plot_entities_with_cross_section()
        app().main_window.action_front_view_callback()

# fmt: on