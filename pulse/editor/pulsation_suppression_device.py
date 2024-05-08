from pulse import app
from pulse.tools.utils import *

from pulse.editor.single_volume_psd import SingleVolumePSD
from pulse.editor.dual_volume_psd import DualVolumePSD

import os
import configparser
import json

import numpy as np
from pathlib import Path
from pprint import pprint
from collections import defaultdict
from itertools import count

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()
    
    def _initialize(self):
        self.psd_entity_data = dict()
        self.pulsation_suppression_device = dict()
        
    def add_pulsation_suppression_device(self, device_label, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                break

        if "volume #2 parameters" in suppression_device_data.keys():
            self.psd_entity_data[device_label] = DualVolumePSD(suppression_device_data)
        else:
            self.psd_entity_data[device_label] = SingleVolumePSD(suppression_device_data)
        
        self.pulsation_suppression_device[device_label] = suppression_device_data
        self.write_psd_data_in_file()

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
        device.process_segment_data()

        counter = 0
        self.psd_link_data = dict()
        
        for i in range(len(device.segment_data)):

            start_point, end_point, section_data = device.segment_data[i]

            if isinstance(section_data, list):

                aux = { 
                        "start point" : list(np.round(start_point, 6)),
                        "end point" : list(np.round(end_point, 6)),
                        "section type" : "Pipe section",
                        "section parameters" : section_data,
                        "structural element type" : "pipe_1",
                        "psd label" : device_label
                        }

                tag = int(shifted_line + i)
                config[str(tag)] = aux

            else:

                link = { 
                        "start point" : list(np.round(start_point, 6)),
                        "end point" : list(np.round(end_point, 6)),
                        "link type" : section_data
                        }

                counter += 1
                self.psd_link_data[(counter, device_label)] = link

        with open(entity_path, 'w') as config_file:
            config.write(config_file)

        self.load_project()

        if self.psd_link_data:
            self.write_psd_link_data_in_file()

    def write_psd_data_in_file(self):
    
        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        with open(path, "w") as file:
            json.dump(self.pulsation_suppression_device, file, indent=2)

        with open(path) as file:
            read_data = json.load(file)

        if read_data == {}:
            os.remove(path)

    def write_psd_link_data_in_file(self):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        if path.exists():

            with open(path) as file:
                psd_info = json.load(file)

            for key, data in self.psd_link_data.items():
                label = key[1]
                psd_info[label][f"Link-{key[0]}"] = data

            with open(path, "w") as file:
                json.dump(psd_info, file, indent=2)

    def load_psd_data_from_file(self):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        self.link_info = defaultdict(list)
        if not os.path.exists(path):
            return

        with open(path) as file:
            read_data = json.load(file)

        for psd_label, data in read_data.items():
            aux = dict()
            for key, value in data.items():

                if "Link-" in key:
                    link_type = value["link type"]
                    start_point = value["start point"]
                    end_point = value["end point"]
                    self.link_info[(psd_label, link_type)].append((start_point, end_point))

                else:
                    aux[key] = value

            self.pulsation_suppression_device[psd_label] = aux

        if self.link_info:
            self.add_psd_link_data_to_nodes()
    
    def add_psd_link_data_to_nodes(self):

        for key, values in  self.link_info.items():
            for (start_coords, end_coords) in values:

                id_1 = self.project.preprocessor.get_node_id_by_coordinates(start_coords)
                id_2 = self.project.preprocessor.get_node_id_by_coordinates(end_coords)
                nodes = (id_1, id_2)

                if key[1] == "acoustic_link":
                    self.project.preprocessor.add_acoustic_link_data(nodes)
                else:
                    self.project.preprocessor.add_structural_link_data(nodes)

    def get_device_related_lines(self):

        config = configparser.ConfigParser()
        config.read(self.file._entity_path)

        self.psd_lines= defaultdict(list)

        for section in config.sections():
            if "psd label" in config[section].keys():
                psd_label = config[section]["psd label"]
                self.psd_lines[psd_label].append(int(section))

        return self.psd_lines

    def remove_psd_lines_from_entity_file(self, device_labels):

        entity_path = self.file._entity_path
        config = configparser.ConfigParser()
        config.read(entity_path)

        if isinstance(device_labels, str):
            device_labels = [device_labels]

        for device_label in device_labels:
            for section in config.sections():
                if "psd label" in config[section].keys():
                    if config[section]["psd label"] == device_label:
                        config.remove_section(section)

        with open(entity_path, 'w') as config_file:
            config.write(config_file)

        if list(config.sections()):
            self.file.remove_entity_gaps_from_file()

    def remove_selected_psd(self, device_label):

        if device_label in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(device_label)

        self.write_psd_data_in_file()
        self.remove_psd_lines_from_entity_file(device_label)
        self.load_project()

    def remove_all_psd(self):

        device_labels = list(self.pulsation_suppression_device.keys())
        self.pulsation_suppression_device.clear()

        self.write_psd_data_in_file()
        self.remove_psd_lines_from_entity_file(device_labels)
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