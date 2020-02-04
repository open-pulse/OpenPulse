import h5py

class Storage:
    """


    """

    def __init__(self, **kwargs):
        self.data_name = kwargs.get("data_name", None)


    #%% Save important results using HDF5 format

    save_results = False

    if save_results:
        
    # np.savetxt('M_globalmatrix.txt',M.toarray(),fmt='%.18e')
    # np.savetxt('K_globalmatrix.txt',K.toarray(),fmt='%.18e')

    f = h5py.File('output_data.hdf5', 'w')
    f.create_dataset('/input/nodal_coordinates', data = nodal_coordinates, dtype='float64')
    f.create_dataset('/input/connectivity', data = connectivity, dtype='int')
    f.create_dataset('/global_matrices/I', data = I, dtype='int')
    f.create_dataset('/global_matrices/J', data = J, dtype='int')
    f.create_dataset('/global_matrices/coo_K', data = coo_K, dtype='float64')
    f.create_dataset('/global_matrices/coo_M', data = coo_M, dtype='float64')
    f.create_dataset('/results/eigenVectors', data = eigenVectors, dtype='float64')
    f.create_dataset('/results/natural_frequencies', data = fn, dtype='float64')
    f.close()

    ## Example how to read files in HDF5 format

    # f = h5py.File('output_data.hdf5', 'r')
    # list(f.keys())
    # K = f['/global_matrices/coo_K']
    # # f.close()