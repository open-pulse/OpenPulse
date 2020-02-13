#%%
from pulse.mesh import Mesh

m = Mesh("C:\\Petro\\OpenPulse\\Examples\\geometry\\tube_1.iges")
m.generate(0.01,0.01)
m.reorder_index_bfs()
coord = m.nodes
connect = m.edges

