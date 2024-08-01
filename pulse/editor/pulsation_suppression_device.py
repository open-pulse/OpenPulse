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
            device = DualVolumePSD(suppression_device_data)
        else:
            device = SingleVolumePSD(suppression_device_data)

        self.pulsation_suppression_device[device_label] = suppression_device_data

        self.build_device(device_label, device)
        self.write_psd_data_in_file()
        self.write_psd_length_correction_in_file(device_label, device)
        self.load_project()
        self.set_element_length_corrections(device_label, device.branch_data)

    def build_device(self, device_label, device):

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

        device.process_segment_data()

        counter = 0
        for i in range(len(device.segment_data)):

            start_point, end_point, section_data, segment_label = device.segment_data[i]

            if isinstance(section_data, list):

                aux = { 
                        "start point" : list(np.round(start_point, 6)),
                        "end point" : list(np.round(end_point, 6)),
                        "section type" : "Pipe section",
                        "section parameters" : section_data,
                        "structural element type" : "pipe_1",
                        "psd label" : device_label,
                        "psd segment" : segment_label
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
                self.pulsation_suppression_device[device_label][f"Link-{counter}"] = link

        with open(entity_path, 'w') as config_file:
            config.write(config_file)

    def write_psd_length_correction_in_file(self, device_label, device):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        if path.exists():
            with open(path) as file:
                psd_data = json.load(file)

            index = 0
            if device_label in psd_data.keys():    
                for (coords, connection_type) in device.branch_data:
                    index += 1
                    key = f"element length correction - {index}"
                    psd_data[device_label][key] = { "connection coords" : list(np.round(coords, 6)),
                                                    "connection type" : connection_type }

            with open(path, "w") as file:
                json.dump(psd_data, file, indent=2)

    def write_psd_data_in_file(self):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        with open(path, "w") as file:
            json.dump(self.pulsation_suppression_device, file, indent=2)

        with open(path) as file:
            read_data = json.load(file)

            if read_data == {}:
                os.remove(path)

    def load_psd_data_from_file(self):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        self.link_info = defaultdict(list)
        if not os.path.exists(path):
            return

        self.pulsation_suppression_device.clear()
        with open(path) as file:
            read_data = json.load(file)
            self.pulsation_suppression_device = read_data

        self.link_data = defaultdict(list)

        for psd_label, data in read_data.items():
            for key, value in data.items():

                if "Link-" in key:
                    link_type = value["link type"]
                    start_point = value["start point"]
                    end_point = value["end point"]
                    self.link_data[(psd_label, link_type)].append((start_point, end_point))

        if self.link_data:
            self.add_psd_link_data_to_nodes(self.link_data)

    def add_psd_link_data_to_nodes(self, link_data):

        for key, values in  link_data.items():
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
        self.remove_psd_related_element_length_correction("_remove_all_")
        self.load_project()
        self.update_length_correction_after_psd_removal()

    def remove_all_psd(self):

        device_labels = list(self.pulsation_suppression_device.keys())
        self.pulsation_suppression_device.clear()

        self.write_psd_data_in_file()
        self.remove_psd_lines_from_entity_file(device_labels)
        self.remove_psd_related_element_length_correction("_remove_all_")
        self.load_project()

    def update_length_correction_after_psd_removal(self):

        project_path = Path(self.file._project_path)
        path = project_path / "psd_info.json"

        if path.exists():

            with open(path) as file:
                read_data = json.load(file)

            for device_label, psd_data in read_data.items():

                elc_data = list()
                for key, value in psd_data.items():
                    if "element length correction -" in key:
                        elc_coords = value["connection coords"]
                        elc_type = value["connection type"]
                        elc_data.append((elc_coords, elc_type))

                if elc_data:
                    self.set_element_length_corrections(device_label, elc_data)

    def set_element_length_corrections(self, device_label, elc_data):

        prefix = "ACOUSTIC ELEMENT LENGTH CORRECTION || {}"

        for (coords, connection_type) in elc_data:

            node_id = self.project.preprocessor.get_node_id_by_coordinates(coords)
            elements = self.project.preprocessor.neighboor_elements_of_node(node_id)
            list_elements = [element.index for element in elements]

            if connection_type == "radial":
                _type = 1

            else:
                _type = 0

            section = prefix.format("Selection-1")
            keys = self.project.preprocessor.group_elements_with_length_correction.keys()

            if section in keys:
                index = 1
                while section in keys:
                    index += 1
                    section = prefix.format(f"Selection-{index}")

            self.project.set_element_length_correction_by_elements(list_elements, 
                                                                   _type, 
                                                                   section,
                                                                   psd_label = device_label)

    def remove_psd_related_element_length_correction(self, device_label):

        path = self.file._element_info_path
        config = configparser.ConfigParser()

        config.read(path)

        if path.exists():

            for section in config.sections():
                if "psd label" in config[section].keys():
                    if device_label == "_remove_all_":
                        config.remove_section(section=section)

                    elif device_label == config[section]["psd label"]:
                        config.remove_section(section=section)

            if list(config.sections()):
                with open(path, 'w') as config_file:
                    config.write(config_file)

            else:
                if path.exists():
                    os.remove(path)

    def load_project(self):

        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_ui.initial_project_action(True)
        app().main_window.update_plots()

        # app().main_window.use_structural_setup_workspace()
        # app().main_window.plot_entities_with_cross_section()
        # app().main_window.action_front_view_callback()

# fmt: on