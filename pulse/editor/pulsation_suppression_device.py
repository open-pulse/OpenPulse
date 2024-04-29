from pulse import app
from pulse.tools.utils import *

import os
import configparser
import numpy as np
from pathlib import Path
from pprint import pprint

class PSDSingleChamber:
    def __init__(self, 
                 connection_type, 
                 connection_point, 
                 axis, 
                 inlet_pipe_length, 
                 inlet_pipe_diameter, 
                 inlet_pipe_wall_thickness, 
                 inlet_pipe_distance, 
                 inlet_pipe_angle, 
                 outlet_pipe_length, 
                 outlet_pipe_diameter, 
                 outlet_pipe_wall_thickness, 
                 outlet_pipe_distance, 
                 outlet_pipe_angle, 
                 main_chamber_length, 
                 main_chamber_diameter, 
                 main_chamber_wall_thickness) -> None:
        
            self.connection_type = connection_type
            self.connection_point = connection_point
            self.axis = axis

            self.inlet_pipe_length = inlet_pipe_length
            self.inlet_pipe_diameter = inlet_pipe_diameter
            self.inlet_pipe_wall_thickness = inlet_pipe_wall_thickness
            self.inlet_pipe_distance = inlet_pipe_distance
            self.inlet_pipe_angle = inlet_pipe_angle

            self.outlet_pipe_length = outlet_pipe_length
            self.outlet_pipe_diameter = outlet_pipe_diameter
            self.outlet_pipe_wall_thickness = outlet_pipe_wall_thickness
            self.outlet_pipe_distance = outlet_pipe_distance
            self.outlet_pipe_angle = outlet_pipe_angle

            self.main_chamber_length = main_chamber_length
            self.main_chamber_diameter = main_chamber_diameter
            self.main_chamber_wall_thickness = main_chamber_wall_thickness

    def get_points(self):
        versor_x = np.array([1, 0, 0])
        versor_y = np.array([0, 1, 0])
        
        inlet = np.array([0, 0, 0])
        junction_0 = inlet - versor_y * self.inlet_pipe_length
        deadleg_0 = junction_0 - versor_x * self.inlet_pipe_distance
        junction_1 = deadleg_0 + versor_x * self.outlet_pipe_distance
        deadleg_1 = deadleg_0 + versor_x * self.main_chamber_length
        outlet = junction_1 - versor_y * self.outlet_pipe_length

        points = self.rotate_points([inlet, outlet, junction_0, junction_1, deadleg_0, deadleg_1])

        if self.connection_point == "discharge":
            inlet, outlet = outlet, inlet

        self.inlet, self.outlet, self.junction_0, self.junction_1, self.deadleg_0, self.deadleg_1 = self.translate_to_connection_point(points)


        return dict(
            inlet = inlet, 
            outlet = outlet, 
            junction_0 = junction_0, 
            junction_1 = junction_1, 
            deadleg_0 = deadleg_0, 
            deadleg_1 = deadleg_1,
        )     

    def rotate_points(self, points):
        if self.axis == "along y-axis":
            matrix = self.rotation_matrix_z(np.pi/2)
        elif self.axis == "along z-axis":
            matrix = self.rotation_matrix_y(np.pi/2)
        else:
            matrix = np.identity(3)

        rotated_points = []
        for point in points:
            rotated_point = matrix @ point
            rotated_points.append(rotated_point)
        
        return rotated_points
    
    def translate_to_connection_point(self, points):
        translated_points = []
        for point in points:
            translated_point = point + self.connection_point
            translated_points.append(translated_point)
        return translated_points    
        
    def rotation_matrix_y(self, angle):
        return np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
    
    def rotation_matrix_z(self, angle):
        return np.array([[np.cos(angle), -np.sin(angle), 0],[np.sin(angle), np.cos(angle), 0], [0, 0, 1] ])
    
class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()
    

    def _initialize(self):
        self.pulsation_suppression_device = dict()
        self.pulsation_suppression_devices = dict()

    def add_pulsation_suppression_device(self, device_label, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                break

        self.pulsation_suppression_devices[device_label] = PSDSingleChamber(
                                                                            suppression_device_data["connection type"],
                                                                            suppression_device_data["connecting coords"],
                                                                            suppression_device_data["main axis"],
                                                                            *suppression_device_data["pipe #1 parameters"],
                                                                            *suppression_device_data["pipe #2 parameters"],
                                                                            *suppression_device_data["volume #1 parameters"]
                                                                            )
        
        self.pulsation_suppression_device[device_label] = suppression_device_data
        self.write_suppression_device_data_in_file()

    def remove_suppression_device(self, device_label):

        if device_label in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(device_label)

        self.write_suppression_device_data_in_file()

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

    def write_psd_data_in_dat(self, device_tag, last_line_tag):
        device = self.pulsation_suppression_devices[device_tag]
        device.get_points()

        config = configparser.ConfigParser()
        config[str(last_line_tag + 1)] = {}
        config[str(last_line_tag + 1)] ["start point"] = str(list(device.deadleg_0))
        config[str(last_line_tag + 1)] ["end point"] = str(list(device.junction_0))
        config[str(last_line_tag + 1)] ["section type"] = "Pipe section"
        config[str(last_line_tag + 1)] ["section parameters"] = str([device.main_chamber_diameter, device.main_chamber_wall_thickness, 0, 0, 0, 0])
        config[str(last_line_tag + 1)] ["structural element type"] = "pipe_1'"
        config[str(last_line_tag + 1)] ["material id"] = "2"
        config[str(last_line_tag + 1)]["psd tag"] = device_tag
        config[str(last_line_tag + 1)]["psd part"] = "1"
        

        config[str(last_line_tag + 2)] = {}
        config[str(last_line_tag + 2)]["start point"] = str(list(device.inlet))
        config[str(last_line_tag + 2)]["end point"] = str(list(device.junction_0))
        config[str(last_line_tag + 2)]["section type"] = "Pipe section"
        config[str(last_line_tag + 2)]["section parameters"] = str([device.inlet_pipe_diameter, device.inlet_pipe_wall_thickness, 0, 0, 0, 0])
        config[str(last_line_tag + 2)]["structural element type"] = "pipe_2"
        config[str(last_line_tag + 2)]["material id"] = "2"
        config[str(last_line_tag + 2)]["psd tag"] = device_tag
        config[str(last_line_tag + 2)]["psd part"] = "2"
        

        config[str(last_line_tag + 3)] = {}
        config[str(last_line_tag + 3)]["start point"] = str(list(device.junction_0))
        config[str(last_line_tag + 3)]["end point"] = str(list(device.junction_1))
        config[str(last_line_tag + 3)]["section type"] = "Pipe section"
        config[str(last_line_tag + 3)]["section parameters"] = str([device.main_chamber_diameter, device.main_chamber_wall_thickness, 0, 0, 0, 0])
        config[str(last_line_tag + 3)]["structural element type"] = "pipe_1"
        config[str(last_line_tag + 3)]["material id"] = "2"
        config[str(last_line_tag + 3)]["psd tag"] = device_tag
        config[str(last_line_tag + 3)]["psd part"] = "3"
        

        config[str(last_line_tag + 4)] = {}
        config[str(last_line_tag + 4)]["start point"] = str(list(device.junction_1))
        config[str(last_line_tag + 4)]["end point"] = str(list(device.outlet))
        config[str(last_line_tag + 4)]["section type"] = "Pipe section"
        config[str(last_line_tag + 4)]["section parameters"] = str([device.outlet_pipe_diameter, device.outlet_pipe_wall_thickness, 0, 0, 0, 0])
        config[str(last_line_tag + 4)]["structural element type"] = "pipe_1"
        config[str(last_line_tag + 4)]["material id"] = "2"
        config[str(last_line_tag + 4)]["psd tag"] = device_tag
        config[str(last_line_tag + 4)]["psd part"] = "4"
        

        config[str(last_line_tag + 5)] = {}
        config[str(last_line_tag + 5)]["start point"] = str(list(device.junction_1))
        config[str(last_line_tag + 5)]["end point"] = str(list(device.deadleg_1))
        config[str(last_line_tag + 5)]["section type"] = "Pipe section"
        config[str(last_line_tag + 5)]["section parameters"] = str([device.main_chamber_diameter, device.main_chamber_wall_thickness, 0, 0, 0, 0])
        config[str(last_line_tag + 5)]["structural element type"] = "pipe_1"
        config[str(last_line_tag + 5)]["material id"] = "2"
        config[str(last_line_tag + 5)]["psd tag"] = device_tag
        config[str(last_line_tag + 5)]["psd part"] = "5"
        
    
        project_path = Path(self.file._project_path)
        path = project_path / "entity.dat"
        with open(path, 'w') as config_file:
            config.write(config_file)  
