# import numpy as np 

# class BoundaryCondition:
#     def __init__(self, dx=None, dy=None, dz=None, rx=None, ry=None, rz=None):
#         self.displacement = (dx, dy, dz)
#         self.rotation = (rx, ry, rz)

#     @property
#     def dof(self):
#         return np.concatenate((self.displacement, self.rotation))

#     @property
#     def prescribed_dof(self):
#         prescribed = [i for i, value in enumerate(self.dof) if value is not None]
#         return np.array(prescribed)