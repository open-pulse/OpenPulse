import vtk
from vtkat.poly_data import LinesData


class ElementLinesActor(vtk.vtkActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.build()

    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        lines = []
        for element in visible_elements.values():
            x0, y0, z0 = element.first_node.coordinates
            x1, y1, z1 = element.last_node.coordinates
            lines.append((x0, y0, z0, x1, y1, z1))

        data = LinesData(lines)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)

        self.SetMapper(mapper)
        self.GetProperty().SetLineWidth(3)
        self.GetProperty().LightingOff()
        self.GetProperty().SetColor(0,0,0)
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

    def set_color(self, color, elements=None, entities=None):
        pass