import vtk
from molde.poly_data import VerticesData
from molde.utils import set_polydata_property, set_polydata_colors
from molde.actors import GhostActor

from pulse import app

class PointsActor(GhostActor):
    def __init__(self, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.points = app().project.get_geometry_points()
        self.hidden_nodes = kwargs.get('hidden_nodes', set())
        self.show_deformed = show_deformed
        self.build()
    
    def build(self):
        visible_nodes = {i:e for i,e in self.points.items() if (i not in self.hidden_nodes)}
        self._key_index = {j:i for i,j in enumerate(visible_nodes.keys())}

        if self.show_deformed:
            coords = [n.deformed_coordinates for n in visible_nodes.values()]
        else:
            coords = [n.coordinates for n in visible_nodes.values()]

        data = VerticesData(coords)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        set_polydata_colors(data, (255, 180, 50))

        self.SetMapper(mapper)
        self.GetProperty().SetPointSize(15)
        self.GetProperty().RenderPointsAsSpheresOn()
        self.make_ghost()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        set_polydata_colors(data, (255, 180, 50))

    def set_color(self, color, nodes=None):
        data = self.GetMapper().GetInput()
        if (nodes is None):
            set_polydata_colors(data, color)
            self.GetMapper().SetScalarModeToUseCellData()
            self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
            self.GetMapper().ScalarVisibilityOn()
            return

        colors: vtk.vtkCharArray = data.GetCellData().GetArray("colors")
        for i in nodes:
            index = self._key_index.get(i)
            if index is not None:
                colors.SetTuple(index, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

