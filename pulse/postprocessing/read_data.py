import h5py
import os
from pulse.utils import *
 
class ReadData:

    def __init__( self, project, *args, **kwargs ):

        self.project = project
        self._project_path = project.file._project_path

        self.data = {}
        self.file_name = "results_data.hdf5"
        self.folder_name = "solution_data"

        self.folder_path = get_new_path(self._project_path, self.folder_name)
        self.file_path = get_new_path(self.folder_path, self.file_name)

        self.read_data()

    def read_data( self ):
        """ This method read output data obtained with model solution

        """
        data = []
        var_name = []
        
        if os.path.exists(self.file_path):
                
            f = h5py.File(self.file_path, 'r')
            list_groups = list(f.keys())

            for group in list_groups:

                group_item = f.get(group).items()

                for j in range(len(group_item)):
                    
                    group_data = list(f.get(group).items())
                    vars()[group_data[j][0]] = group_data[j][1][()]
                    data.append(vars()[group_data[j][0]])
                    var_name.append([group_data[j][0]])
                    self.data[group_data[j][0]] = vars()[group_data[j][0]]

            f.close()

            # for i, name in enumerate(var_name):
            #     vars()[name[0]+"_"] = data[i]

            if 'solution_acoustic' in self.data.keys():
                self.project.set_acoustic_solution(self.data['solution_acoustic'])
            if 'solution_structural' in self.data.keys():
                self.project.set_structural_solution(self.data['solution_structural'])
            if 'analysis_ID' in self.data.keys():
                self.project.analysis_ID = self.data['analysis_ID']     
            
            if 'frequencies' in self.data.keys():
                self.project.frequencies = self.data['frequencies']
            if 'natural_frequencies_acoustic' in self.data.keys():
                self.project.natural_frequencies_acoustic = list(self.data['natural_frequencies_acoustic'])
            if 'natural_frequencies_structural' in self.data.keys():
                self.project.natural_frequencies_structural = list(self.data['natural_frequencies_structural'])

            if 'analysis_type_label' in self.data.keys():
                self.project.analysis_type_label = self.data['analysis_type_label']
            if 'analysis_method_label' in self.data.keys():
                self.project.analysis_method_label = self.data['analysis_method_label']
        self.project.remove_solution_data_files()
        return var_name, data