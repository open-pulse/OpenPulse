from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkPropCollection


class ElementAxesActor(vtkAxesActor):
    def __init__(self) -> None:
        super().__init__()
        self.build()

    def build(self):
        self.AxisLabelsOff()
        self.SetShaftTypeToCylinder()
        self._make_ghost()

    def position_from_element(self, element):
        xyz = element.center_coordinates
        rx, ry, rz = element.section_rotation_xyz_undeformed
        size = [element.length] * 3

        transform = vtkTransform()
        transform.Translate(xyz)
        transform.RotateZ(rz)
        transform.RotateX(rx)
        transform.RotateY(ry)
        transform.Scale(size)

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
