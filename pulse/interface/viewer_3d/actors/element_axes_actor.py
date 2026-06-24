from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkPropCollection

from pulse.model.spatial_data import SpatialData
from pulse.model.section_rotations import SectionRotations



class ElementAxesActor(vtkAxesActor):
    def __init__(self) -> None:
        super().__init__()
        self.build()

    def build(self):
        self.AxisLabelsOff()
        self.SetShaftTypeToCylinder()
        self._make_ghost()

    def position_from_element(self, element_spatial_data: SpatialData, section_rotations: SectionRotations):
    
        length = element_spatial_data.length
        coords = element_spatial_data.center_coordinates
        rx, ry, rz = section_rotations.undeformed_rotation_rxyz

        transform = vtkTransform()
        transform.Translate(coords)
        transform.RotateZ(rz)
        transform.RotateX(rx)
        transform.RotateY(ry)
        transform.Scale([length, length, length])

        self.SetUserTransform(transform)
        self.Modified()

    def _make_ghost(self):
        offset = -66000

        actor: vtkActor
        actors = vtkPropCollection()
        self.GetActors(actors)

        for actor in actors:
            # actor.GetProperty().LightingOff()
            mapper = actor.GetMapper()
            mapper.SetResolveCoincidentTopologyToPolygonOffset()
            mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
            mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
            mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)
