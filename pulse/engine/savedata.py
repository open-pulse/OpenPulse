import h5py

class SaveData:
    """


    """

    def __init__(self, 
                    save_results, 
                    data_K, 
                    data_M, 
                    I,
                    J, 
                    dofs_prescribed, 
                    connectivity,
                    nodal_coordinates,
                    eigenVectors,
                    natural_frequencies,
                    U_xyz,
                    frequency_analysis,
                    **kwargs):

        self.save_results = save_results
        self.data_K = data_K
        self.data_M = data_M
        self.I = I
        self.J = J
        self.connectivity = connectivity
        self.nodal_coordinates = nodal_coordinates
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.dofs_not_prescribed = kwargs.get("dofs_not_prescribed", None)
        self.dofs_prescribed = kwargs.get("dofs_prescribed", None)
        self.natural_frequencies = kwargs.get("natural_frequencies", None)
        self.U_xyz = kwargs.get("U_xyz", None)
        self.frequency_analysis = kwargs.get("frequency_analysis", None)
    
    #%% Save obtained results in HDF5 format
        
    def store_data(self,save):
        if self.save_results:
                
            f = h5py.File('output_data.hdf5', 'w')
            f.create_dataset('/input/nodal_coordinates', data = nodal_coordinates, dtype='float64')
            f.create_dataset('/input/connectivity', data = connectivity, dtype='int')
            f.create_dataset('/global_matrices/I', data = I, dtype='int')
            f.create_dataset('/global_matrices/J', data = J, dtype='int')
            f.create_dataset('/global_matrices/coo_K', data = data_K, dtype='float64')
            f.create_dataset('/global_matrices/coo_M', data = data_M, dtype='float64')
            f.create_dataset('/results/eigenVectors', data = eigenVectors, dtype='float64')
            f.create_dataset('/results/natural_frequencies', data = fn, dtype='float64')
            f.close()
        else:
            print('Warning, no data has been stored in hard disk !!!')
        return

    # np.savetxt('M_globalmatrix.txt',M.toarray(),fmt='%.18e')
    # np.savetxt('K_globalmatrix.txt',K.toarray(),fmt='%.18e')

    ## Example how to read files in HDF5 format

    # f = h5py.File('output_data.hdf5', 'r')
    # list(f.keys())
    # K = f['/global_matrices/coo_K']
    # K = f.get('/global_matrices/coo_K').value
    # # f.close()