from pulse import app
from pulse.tools.utils import *

from pulse.editor.single_chamber_psd import SingleChamberPSD
from pulse.editor.dual_chambers_psd import DualChambersPSD

import os
import configparser
import numpy as np
from pathlib import Path
from pprint import pprint
from collections import defaultdict

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

        for i in range(len(device.segment_data)):

            start_point, end_point, section_parameters = device.segment_data[i]

            aux = { 
                    "start point" : list(np.round(start_point, 6)),
                    "end point" : list(np.round(end_point, 6)),
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

                    if key in ["main axis", "connection pipe", "volumes connection"]:
                        aux[key] = section[key]

                    elif key == "volumes spacing":
                        aux[key] = float(section[key])

                    elif key in list_data_keys:
                        aux[key] = get_list_of_values_from_string(section[key], int_values=False)

                if aux:
                    self.pulsation_suppression_device[tag] = aux

    def get_device_related_lines(self):

        config = configparser.ConfigParser()
        config.read(self.file._entity_path)

        self.psd_lines= defaultdict(list)

        for section in config.sections():
            if "psd label" in config[section].keys():
                psd_label = config[section]["psd label"]
                self.psd_lines[psd_label].append(int(section))

        return self.psd_lines

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
        # app().main_window.opv_widget.updatePlots()
        # app().main_window.use_structural_setup_workspace()
        # app().main_window.plot_entities_with_cross_section()
        # app().main_window.action_front_view_callback()

# fmt: on