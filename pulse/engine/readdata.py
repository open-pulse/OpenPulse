import h5py
import os
 
class ReadData:

    def __init__( self, **kwargs ):

        self.file_name = kwargs.get("file_name", "results_data.hdf5")
        self.folder_name = kwargs.get("folder_name", "output_data")

    def read_data( self ):
        """ This method read output data obtained with model solution

        """
        data = []
        var_name = []
        flag = True
        file_exists = True

        path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]
        os.chdir(path)

        if os.path.exists(self.folder_name):

            os.chdir(self.folder_name)

        else:
            
            print("\nWARNING: There's no folder '" + self.folder_name + "' in path: " + path + ".")
            print("Please, it's necessary to save the results first before to try opening it.")
            file_exists = False

        if os.path.exists(self.file_name) and file_exists:
                
            f = h5py.File(self.file_name, 'r')
            groups = list(f.keys())

            for gp in groups:

                gp_item = f.get(gp).items()

                for j in range(len(gp_item)):
                    
                    gp_data = list(f.get(gp).items())
                    vars()[gp_data[j][0]] = gp_data[j][1].value
                    data.append(vars()[gp_data[j][0]])
                    var_name.append([gp_data[j][0]])

            f.close()

        else:

            if file_exists:

                print("WARNING: The file '" + self.file_name + "' does not exists or cannot be found." )
                flag = False
         
        return var_name, data, flag