from fem_mesh import FemMesh
from time import time

start = time()
path = '..\\..\\examples\\LINHA_1.step'
f = FemMesh(path, 10, 10)

print(f.edges_matrix, '\n')
print(f.vertices_matrix, '\n')
print(time()-start)