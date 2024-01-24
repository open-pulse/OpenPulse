import vtk
from vtkat.poly_data import VerticesData


class NodesActor(vtk.vtkActor):
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

        self.SetMapper(mapper)
        self.GetProperty().SetPointSize(8)
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().LightingOff()
        self.GetProperty().SetColor([i/255 for i in (255, 180, 50)])
        self.appear_in_front(True)

    def appear_in_front(self, cond: bool):
        # this offset is the Z position of the camera buffer.
        # if it is -66000 the object stays in front of everything.
        offset = -66000 if cond else 0
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)

    def set_color(self, color, nodes=None):
        pass
