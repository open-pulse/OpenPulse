from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkPropCollection

from pulse.model.elements.element_attributes import ElementAttributes

from pulse import app

class ElementAxesActor(vtkAxesActor):
    def __init__(self) -> None:
        super().__init__()

        self.build()

    def build(self):
        self.AxisLabelsOff()
        self.SetShaftTypeToCylinder()
        self._make_ghost()

    @property
    def undeformed_section_rotations(self):
        return app().project.model.preprocessor.undeformed_section_rotations

    def position_from_element(self, element_attributes: ElementAttributes):

        length = element_attributes.length
        coords = element_attributes.center_coordinates
        rx, ry, rz = self.undeformed_section_rotations[element_attributes.index, :]

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
