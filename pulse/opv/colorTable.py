import vtk

class ColorTable(vtk.vtkLookupTable):
    def __init__(self, **kwargs):
        super().__init__()
        