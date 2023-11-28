import h5py
import os
from pulse.utils import *

class SaveData:

    def __init__(self, project, *args, **kwargs):

        self.project = project
        self._project_path = project.file._project_path 

        self.file_name = kwargs.get("file_name", "results_data.hdf5")
        self.folder_name = "solution_data"

        self.update_values(project)
        self.store_data()
    
    def update_values(self, project):

        self.solution_structural = project.solution_structural
        self.solution_acoustic = project.solution_acoustic
        self.analysis_ID = project.analysis_ID
        self.frequencies = project.frequencies
        self.natural_frequencies_acoustic = project.natural_frequencies_acoustic
        self.natural_frequencies_structural = project.natural_frequencies_structural
        self.analysis_type_label = project.analysis_type_label
        self.analysis_method_label = project.analysis_method_label
        
    def store_data(self):
        """ This method stores relevant output data obtained with model solution

        """

        folder_path = get_new_path(self._project_path, self.folder_name)
        file_path = get_new_path(folder_path, self.file_name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
      
        if os.path.exists(folder_path):
            f = h5py.File(file_path, "w")
            f.close()

        f = h5py.File(file_path, 'w')

        if self.solution_structural is not None:
            f.create_dataset('/results/solution_structural', data=self.solution_structural, dtype=complex)
        
        if self.solution_acoustic is not None:
            f.create_dataset('/results/solution_acoustic', data=self.solution_acoustic, dtype=complex)
        
        if self.analysis_ID is not None:
            f.create_dataset('/analysis_info/analysis_ID', data=self.analysis_ID, dtype=int)
        
        if self.analysis_type_label is not None:
            f.create_dataset('/analysis_info/analysis_type_label', data=self.analysis_type_label)
        
        if self.analysis_method_label is not None:
            f.create_dataset('/analysis_info/analysis_method_label', data=self.analysis_method_label)
        
        if self.analysis_ID in [2, 4]:
            if self.natural_frequencies_structural is not None:
                f.create_dataset('/analysis_info/natural_frequencies_structural', data=self.natural_frequencies_structural, dtype=float)
            if self.natural_frequencies_acoustic is not None:
                f.create_dataset('/analysis_info/natural_frequencies_acoustic', data=self.natural_frequencies_acoustic, dtype=float)
        else:
            if self.frequencies is not None:
                f.create_dataset('/analysis_info/frequencies', data=self.frequencies, dtype=float)

        f.close()

        return