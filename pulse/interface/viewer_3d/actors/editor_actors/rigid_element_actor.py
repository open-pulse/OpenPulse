from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from molde.actors import GhostActor
from pulse.utils.cell_utils import fill_cell_identifier, paint_data
from pulse.editor.structures.rigid_element import RigidElement


class RigidElementActor(GhostActor):
    def __init__(self, rigid: RigidElement):
        super().__init__()
        self.rigid = rigid
        self.create_geometry()
        self.make_ghost()

    def create_geometry(self):
        start = self.rigid.start.coords()
        end = self.rigid.end.coords()

        source = vtkLineSource()
        source.SetPoint1(*start)
        source.SetPoint2(*end)
        source.Update()

        data = source.GetOutput()
        paint_data(data, self.rigid.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
        self.GetProperty().SetLineWidth(6)

    def make_ghost(self):
        self.GetProperty().LightingOff()
        offset = -66000
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)


class RigidElementsActor(GhostActor):
    def __init__(self, pipeline):
        super().__init__()
        self.build(pipeline)

    def build(self, pipeline):
        append_filter = vtkAppendPolyData()
        selection_color = (255, 0, 50)
        has_data = False

        for i, structure in enumerate(pipeline.all_structures()):
            if not isinstance(structure, RigidElement):
                continue

            start = structure.start.coords()
            end = structure.end.coords()

            source = vtkLineSource()
            source.SetPoint1(*start)
            source.SetPoint2(*end)
            source.Update()

            data = source.GetOutput()
            if structure.selected or structure.staged:
                paint_data(data, selection_color)
            else:
                paint_data(data, structure.color.to_rgb())

            fill_cell_identifier(data, i)
            append_filter.AddInputData(data)
            has_data = True

        if has_data:
            append_filter.Update()
            merged = append_filter.GetOutput()
        else:
            merged = vtkPolyData()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(merged)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

        self.GetProperty().SetLineWidth(6)
        self.make_ghost()

    def make_ghost(self):
        self.GetProperty().LightingOff()
        offset = -66000
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)
