from pulse import app
from pulse.tools.utils import *

import os
import configparser
import numpy as np
from pathlib import Path
from pprint import pprint

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()
    

    def _initialize(self):
        self.pulsation_suppression_device = dict()

    def add_pulsation_suppression_device(self, device_label, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                break

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
    
    def process_psd_data(self):
        # aqui colocar um if pra ver se ele tem 2 volumes ou nao
        self.devices = dict()
        for device, value in self.pulsation_suppression_device.items():
            inlet_pipe = dict()
            inlet_pipe = {"length": value["pipe #1 parameters"][0], 
                          "diameter": value["pipe #1 parameters"][1],
                          "wall thickness": value["pipe #1 parameters"][2],
                          "distance": value["pipe #1 parameters"][3],
                          "rotation_angle": value["pipe #1 parameters"][4]
                          }     
                   
            outlet_pipe = dict()            
            outlet_pipe = {"length": value["pipe #2 parameters"][0], 
                          "diameter": value["pipe #2 parameters"][1],
                          "wall thickness": value["pipe #2 parameters"][2],
                          "distance": value["pipe #2 parameters"][3],
                          "rotation_angle": value["pipe #2 parameters"][4]
                          }            
            
            main_chamber = dict()
            main_chamber = {"length": value["volume #1 parameters"][0], 
                          "diameter": value["volume #1 parameters"][1],
                          "wall thickness": value["volume #1 parameters"][2]
                            }
            
            
            lines = []
            points = []

            points.append(list(np.array(value["connecting coords"]) - np.array([inlet_pipe["distance"], inlet_pipe["length"], 0])))
            points.append(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
            lines.append(points)

            points.append(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
            points.append(list(np.array(value["connecting coords"])))
            lines.append(points)

            points.append(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
            points.append(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
            lines.append(points)

            points.append(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
            points.append(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"] - outlet_pipe["length"], 0])))
            lines.append(points)

            points.append(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
            points.append(list(np.array(value["connecting coords"]) + np.array([main_chamber["length"] - inlet_pipe["distance"], -inlet_pipe["length"], 0])))
            lines.append(points)

            self.devices[str(device)] = lines
            pprint(self.devices)

        def rotate_psd_device(self, angle, axis, device):
            
            if axis == "y":
                rotation_matrix = [[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]]
                for i in lines[i]:
                    for j in lines[i][j]:
                        lines[i][j] = np.dot(rotation_matrix, lines[i][j])
            if axis == "z":
                rotation_matrix = [[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]]
                for i in lines[i]:
                    for j in lines[i][j]:
                        lines[i][j] = np.dot(rotation_matrix, lines[i][j])

                



        def write_psd(self):
            for key, value in self.pulsation_suppression_device.items():
                config = configparser.ConfigParser()

                config["1"] = {}
                config["1"]["start point"] = str(list(np.array(value["connecting coords"]) - np.array([inlet_pipe["distance"], inlet_pipe["length"], 0])))
                config["1"]["end point"] = str(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
                config["1"]["section type"] = "Pipe section"
                config["1"]["section parameters"] = str([main_chamber["diameter"], main_chamber["wall thickness"], 0, 0, 0, 0])
                config["1"]["structural element type"] = "pipe_1"
                config["1"]["material id"] = "2"

                config["2"] = {}
                config["2"]["start point"] = str(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
                config["2"]["end point"] = str(list(np.array(value["connecting coords"]) ))
                config["2"]["section type"] = "Pipe section"
                config["2"]["section parameters"] = str([inlet_pipe["diameter"], inlet_pipe["wall thickness"], 0, 0, 0, 0])
                config["2"]["structural element type"] = "pipe_1"
                config["2"]["material id"] = "2"


                config["3"] = {}
                config["3"]["start point"] = str(list(np.array(value["connecting coords"]) - np.array([0, inlet_pipe["length"], 0])))
                config["3"]["end point"] = str(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
                config["3"]["section type"] = "Pipe section"
                config["3"]["section parameters"] = str([main_chamber["diameter"], main_chamber["wall thickness"], 0, 0, 0, 0])
                config["3"]["structural element type"] = "pipe_1"
                config["3"]["material id"] = "2"

                config["4"] = {}
                config["4"]["start point"] = str(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
                config["4"]["end point"] = str(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"] - outlet_pipe["length"], 0])))
                config["4"]["section type"] = "Pipe section"
                config["4"]["section parameters"] = str([outlet_pipe["diameter"], outlet_pipe["wall thickness"], 0, 0, 0, 0])
                config["4"]["structural element type"] = "pipe_1"
                config["4"]["material id"] = "2"

                config["5"] = {}
                config["5"]["start point"] = str(list(np.array(value["connecting coords"]) + np.array([outlet_pipe["distance"], -inlet_pipe["length"], 0])))
                config["5"]["end point"] = str(list(np.array(value["connecting coords"]) + np.array([main_chamber["length"] - inlet_pipe["distance"], -inlet_pipe["length"], 0])))
                config["5"]["section type"] = "Pipe section"
                config["5"]["section parameters"] = str([main_chamber["diameter"], main_chamber["wall thickness"], 0, 0, 0, 0])
                config["5"]["structural element type"] = "pipe_1"
                config["5"]["material id"] = "2"
            

            project_path = Path(self.file._project_path)
            path = project_path / "psd_construction_info.dat"
            with open(path, 'w') as config_file:
                config.write(config_file)   