import sys
sys.path.append('..\..')
from open_pulse.mesh.fem_mesh import FemMesh

path = 'LINHA_1.iges'
mesh = FemMesh(path, 1, 20)

print('VERTICES')
for index, (x, y, z) in mesh.vertices.items():
    print('{:20e} {:20e} {:20e}'.format(x/1000, y/1000, z/1000)) 

print('EDGES')
for index, (s, e) in mesh.edges.items():
    print('{:5}. {:5}.'.format(s, e)) 
