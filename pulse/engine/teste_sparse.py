#%%
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix
import time as tm

N_dof = 9264
data = np.arange(N_dof)
I = np.arange(N_dof)
J = np.arange(N_dof)

# J = np.arange(1,N_dof+1,1)

# I = np.concatenate((I,I))
# J = np.concatenate((J,J-1))
# data = np.concatenate((data,data-1))

# ind = np.concatenate((np.arange(1000),np.arange(1200,N_dof,10)))
ind_t = np.arange(N_dof)
ind_r = [0,1,2,3,4,5,7194,7195,7196,7197,7198,7199,9144,9145,9146,9147,9148,9149]
ind_r = [0,1,5,2,4,3]
ind_r = np.sort(ind_r)
# start = tm.time()
# ind = np.delete( ind_t, ind_r )
# end = tm.time()
ind = ind_r
# print(Mslice.todense())
# print('Time to delete "ind" elements from array:', np.round(end-start,6))

M = csr_matrix((data,(I,J)), shape=[N_dof,N_dof+1])
start = tm.time()
Mslice = M[ind,:].tocsc()[:,ind]
end = tm.time()

print(Mslice.todense())
print('Time to drop rows and coluns:', np.round(end-start,6))

