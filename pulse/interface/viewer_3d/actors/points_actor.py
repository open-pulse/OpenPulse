from vtkmodules.vtkCommonCore import vtkUnsignedIntArray
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper
from vtkmodules.vtkCommonCore import vtkCharArray
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPolyData

from molde.utils import set_polydata_colors
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

        points = vtkPoints()
        data = vtkPolyData()
        node_index = vtkUnsignedIntArray()
        node_index.SetName("node_index")
        data.Allocate(len(visible_nodes))

        for i, node in enumerate(visible_nodes.values()):
            xyz = node.deformed_coordinates if self.show_deformed else node.coordinates
            points.InsertNextPoint(xyz)
            data.InsertNextCell(VTK_VERTEX, 1, [i])
            node_index.InsertNextTuple1(node.external_index)

        data.SetPoints(points)
        data.GetCellData().AddArray(node_index)

        mapper = vtkPolyDataMapper()
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

        colors: vtkCharArray = data.GetCellData().GetArray("colors")
        for i in nodes:
            index = self._key_index.get(i)
            if index is not None:
                colors.SetTuple(index, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

