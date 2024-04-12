from pulse import app

import os
import configparser
import numpy as np
from pathlib import Path

class PulsationSuppressionDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()

    def _initialize(self):
        self.pulsation_suppression_device = dict()

    def add_pulsation_suppression_device(self, tag, suppression_device_data):

        aux = self.pulsation_suppression_device.copy()
        for key, data in aux.items():
            if data == suppression_device_data:
                self.pulsation_suppression_device.pop(key)
                tag = key
                break

        self.pulsation_suppression_device[tag] = suppression_device_data

        self.modify_suppression_filter_in_file(tag, suppression_device_data)

    def remove_suppression_filter(self, tag):

        if tag in self.pulsation_suppression_device.keys():
            self.pulsation_suppression_device.pop(tag)

        self.modify_suppression_filter_in_file(tag, None)

    def modify_suppression_filter_in_file(self, tag, suppression_device_data):
    
        project_path = Path(self.file._project_path)
        path = project_path / "pulsation_suppression_device.dat"

        config = configparser.ConfigParser()
        config.read(path)

        if suppression_device_data is None:
            if str(tag) in config.sections():
                config.remove_section(str(tag))
        else:
            config[str(tag)] = suppression_device_data

        if list(config.sections()):
            with open(path, 'w') as config_file:
                config.write(config_file)
        else:
            os.remove(path)