from pulse import app

import os
import configparser
import numpy as np
from pathlib import Path

class PulsationAttenuatorDevice:
    def __init__(self, project):

        self.project = project
        self.file = project.file

        self._initialize()

    def _initialize(self):
        self.pulsation_attenuator_device = dict()

    def add_pulsation_attenuator_device(self, tag, attenuator_data):

        aux = self.pulsation_attenuator_device.copy()
        for key, data in aux.items():
            if data == attenuator_data:
                self.pulsation_attenuator_device.pop(key)
                tag = key
                break

        self.pulsation_attenuator_device[tag] = attenuator_data

        self.modify_attenuator_filter_in_file(tag, attenuator_data)

    def remove_attenuator_filter(self, tag):

        if tag in self.pulsation_attenuator_device.keys():
            self.pulsation_attenuator_device.pop(tag)

        self.modify_attenuator_filter_in_file(tag, None)

    def modify_attenuator_filter_in_file(self, tag, attenuator_data):
    
        project_path = Path(self.file._project_path)
        path = project_path / "pulsation_attenuator_device.dat"

        config = configparser.ConfigParser()
        config.read(path)

        if attenuator_data is None:
            if str(tag) in config.sections():
                config.remove_section(str(tag))
        else:
            config[str(tag)] = attenuator_data

        if list(config.sections()):
            with open(path, 'w') as config_file:
                config.write(config_file)
        else:
            os.remove(path)