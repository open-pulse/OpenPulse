from fem_mesh import FemMesh
from time import time

start = time()
path = 'C:\\Users\\GUILHE~1\\Documents\\fem_mesh\\examples\\PLANE.iges'
f = FemMesh(path, 10, 10)

print(f.edges_matrix, '\n')
print(f.vertices_matrix, '\n')
print(time()-start)