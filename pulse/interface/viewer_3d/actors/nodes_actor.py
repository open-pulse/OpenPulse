import vtk
from vtkat.poly_data import VerticesData
from vtkat.utils import set_polydata_property, set_polydata_colors
from vtkat.actors import GhostActor

class NodesActor(GhostActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()
        self.project = project
        self.nodes = project.get_nodes()
        self.hidden_nodes = kwargs.get('hidden_nodes', set())
        self.build()
    
    def build(self):
        visible_nodes = {i:e for i,e in self.nodes.items() if (i not in self.hidden_nodes)}
        self._key_index = {j:i for i,j in enumerate(visible_nodes)}
        coords = [n.coordinates for n in visible_nodes.values()]
        data = VerticesData(coords)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        set_polydata_colors(data, (255, 180, 50))

        self.SetMapper(mapper)
        self.GetProperty().SetPointSize(10)
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
            # the index of the nodes is the same index of
            # the cells, so we don't need any conversion
            colors.SetTuple3(i, *color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

