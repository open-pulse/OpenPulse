from pulse import app
from pulse.tools.utils import *

from pulse.editor.single_volume_psd import SingleVolumePSD
from pulse.editor.dual_volume_psd import DualVolumePSD

import os
from configparser import ConfigParser

import numpy as np
from collections import defaultdict

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file
        self.preprocessor = project.preprocessor

        self._initialize()
    
    def _initialize(self):
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

    def build_device(self, device_label, device : (SingleVolumePSD | DualVolumePSD)):

        config = app().main_window.pulse_file.read_pipeline_data_from_file()

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

            start_coords, end_coords, section_data, segment_label = device.segment_data[i]

            if isinstance(section_data, list):

                aux = { 
                        "start coords" : list(np.round(start_coords, 6)),
                        "end coords" : list(np.round(end_coords, 6)),
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
                        "start coords" : list(np.round(start_coords, 6)),
                        "end coords" : list(np.round(end_coords, 6)),
                        "link type" : section_data
                        }
                
                counter += 1
                self.pulsation_suppression_device[device_label][f"Link-{counter}"] = link

        app().main_window.pulse_file.write_pipeline_data_in_file(config)

    def write_psd_length_correction_in_file(self, device_label, device : (SingleVolumePSD | DualVolumePSD)):

        psd_data = app().main_window.pulse_file.read_psd_data_from_file()
        if psd_data is None:
            return

        index = 0
        if device_label in psd_data.keys():    
            for (coords, connection_type) in device.branch_data:
                index += 1
                key = f"element length correction - {index}"
                psd_data[device_label][key] = { "connection coords" : list(np.round(coords, 6)),
                                                "connection type" : connection_type }

        app().main_window.pulse_file.write_psd_data_in_file(psd_data)

    def write_psd_data_in_file(self):
        app().main_window.pulse_file.write_psd_data_in_file(self.pulsation_suppression_device)

    def load_psd_data_from_file(self):

        psd_data = app().main_window.pulse_file.read_psd_data_from_file()
        if psd_data is None:
            return

        self.pulsation_suppression_device.clear()
        self.pulsation_suppression_device = psd_data

        self.link_data = defaultdict(list)

        for psd_label, data in psd_data.items():
            for key, value in data.items():

                if "Link-" in key:
                    link_type = value["link type"]
                    start_coords = value["start coords"]
                    end_coords = value["end coords"]
                    self.link_data[(psd_label, link_type)].append((start_coords, end_coords))

        if self.link_data:
            self.preprocessor.add_psd_link_data_to_nodes(self.link_data)

    def get_device_related_lines(self):

        self.psd_lines = defaultdict(list)

        config = app().main_window.pulse_file.read_pipeline_data_from_file()

        for section in config.sections():
            if "psd label" in config[section].keys():
                psd_label = config[section]["psd label"]
                self.psd_lines[psd_label].append(int(section))

        return self.psd_lines

    def remove_psd_lines_from_pipeline_file(self, device_labels):

        config = app().main_window.pulse_file.read_pipeline_data_from_file()

        if isinstance(device_labels, str):
            device_labels = [device_labels]

        for device_label in device_labels:
            for section in config.sections():
                if "psd label" in config[section].keys():
                    if config[section]["psd label"] == device_label:
                        config.remove_section(section)

        app().main_window.pulse_file.write_pipeline_data_in_file(config)

        if list(config.sections()):
            self.remove_line_gaps_from_file()

    def remove_line_gaps_from_file(self):

        config_no_gap = ConfigParser()
        config = app().main_window.pulse_file.read_pipeline_data_from_file()

        splited_lines = list()
        for section in config.sections():
            if "-" in section:
                splited_lines.append(section)

        tag = 0
        for section in config.sections():

            if section not in splited_lines:
                tag += 1

            if "-" in section:
                suffix = int(section.split("-")[1])
                config_no_gap[f"{tag}-{suffix}"] = config[section]
            else:
                config_no_gap[str(tag)] = config[section]

        app().main_window.pulse_file.write_pipeline_data_in_file(config_no_gap)

    def remove_selected_psd(self, device_label):

        if device_label in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(device_label)

        self.write_psd_data_in_file()
        self.remove_psd_lines_from_pipeline_file(device_label)
        self.remove_psd_related_element_length_correction("_remove_all_")
        self.load_project()
        self.update_length_correction_after_psd_removal()

    def remove_all_psd(self):

        device_labels = list(self.pulsation_suppression_device.keys())
        self.pulsation_suppression_device.clear()

        self.write_psd_data_in_file()
        self.remove_psd_lines_from_pipeline_file(device_labels)
        self.remove_psd_related_element_length_correction("_remove_all_")
        self.load_project()

    def update_length_correction_after_psd_removal(self):

        read_data = app().main_window.pulse_file.read_psd_data_from_file()

        if read_data is None:
            return

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

            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            elements = self.preprocessor.neighboor_elements_of_node(node_id)
            list_elements = [element.index for element in elements]

            if connection_type == "radial":
                _type = 1

            else:
                _type = 0

            section = prefix.format("Selection-1")
            keys = self.preprocessor.group_elements_with_length_correction.keys()

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

        element_ids = list()
        for (property, element_id), data in app().main_window.project.properties.element_properties.items():
            if property == "element length correction":
                if "psd label" in data.keys():
                        if device_label == "_remove_all_":
                            element_ids.append(element_id)
                        elif device_label == data["psd label"]:
                            element_ids.append(element_id)

        app().main_window.project.properties._remove_element_property("element length correction", element_ids) 
        app().main_window.pulse_file.write_model_properties_in_file()

    def load_project(self):
        self.project.initial_load_project_actions()
        self.project.load_project_files()
        app().main_window.input_ui.initial_project_action(True)
        app().main_window.update_plots()

        # app().main_window.use_structural_setup_workspace()

# fmt: on