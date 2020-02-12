import h5py
import os
import numpy as np
 
class ReadData:

    def __init__( self, filename, **kwargs ):
        self.filename = filename
        self.dir_path = kwargs.get("dir_path", None)


    def read_data( self ):
        """ This method read output data obtained with model solution

        """
        if self.dir_path == None:
            self.dir_path = "C:\Petro\OpenPulse\pulse\data_saved"
        os.chdir(self.dir_path)

        f = h5py.File(self.filename, 'r')
        groups = list(f.keys())

        data = []
        var_name = []

        for i, gp in enumerate(groups):

            gp_item = f.get(gp).items()

            for j in range(len(gp_item)):
                
                gp_data = list(f.get(gp).items())
                vars()[gp_data[j][0]] = gp_data[j][1].value
                data.append(vars()[gp_data[j][0]])
                var_name.append([gp_data[j][0]])

        f.close()

        return var_name, data