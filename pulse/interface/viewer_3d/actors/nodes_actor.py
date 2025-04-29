from molde.actors import GhostActor
from molde.colors import Color
from molde.utils import set_polydata_colors, set_polydata_property
from vtkmodules.vtkCommonCore import vtkCharArray, vtkPoints, vtkUnsignedIntArray
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper
from pulse import app

from pulse import app

class NodesActor(GhostActor):
    def __init__(self, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.project = app().project
        self.user_preferences = app().main_window.config.user_preferences
        self.nodes = self.project.model.preprocessor.nodes

        self.hidden_nodes = kwargs.get('hidden_nodes', set())
        self.show_deformed = show_deformed

        self.build()

    def build(self):
        visible_nodes = {
            i: e for i, e in self.nodes.items() if (i not in self.hidden_nodes)
        }
        self._key_index = {j: i for i, j in enumerate(visible_nodes.keys())}

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

        self.SetMapper(mapper)

        nodes_size = app().config.user_preferences.nodes_size
        self.GetProperty().SetPointSize(nodes_size)

        if not app().main_window.config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()
        self.make_ghost()
        
        self.clear_colors()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        nodes_color = self.user_preferences.nodes_points_color.to_rgb()
        set_polydata_colors(data, nodes_color)

    def set_color(self, color, nodes=None):
        data = self.GetMapper().GetInput()
        if nodes is None:
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
