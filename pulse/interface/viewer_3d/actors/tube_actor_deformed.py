import vtk

from .tube_actor import TubeActor
from vtkat.utils import set_polydata_property


class TubeActorDeformed(TubeActor):
    def __init__(self, project, **kwargs) -> None:
        self.cached = dict()
        super().__init__(project, **kwargs)

    def build(self, use_cache=False):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}

        mapper = vtk.vtkPolyDataMapper()
        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.SetOutputPointsPrecision(0)

        for i, element in visible_elements.items():
            section_coords = element.first_node.deformed_coordinates
            section_rotation_xyz = element.deformed_rotation_xyz

            if (section_coords is None) or (section_rotation_xyz is None):
                section_coords = element.first_node.coordinates
                section_rotation_xyz = element.section_rotation_xyz_undeformed

            source: vtk.vtkPolyData = self.create_element_data(element, use_cache)
            if source is None:
                continue

            transform = vtk.vtkTransform()
            transform.Translate((element.length/2, 0, 0))
            transform.Translate(*section_coords)
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.RotateY(180)
            transform.RotateZ(-90)
            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            transformed_source = transform_filter.GetOutput()
            entity = self.preprocessor.elements_to_line[i]
            set_polydata_property(transformed_source, i, "element_index")
            set_polydata_property(transformed_source, entity, "entity_index")

            append_polydata.AddInputData(transformed_source)
        
        append_polydata.Update()
        data: vtk.vtkPolyData = append_polydata.GetOutput()

        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

        self.clear_colors()

    def create_element_data(self, element, use_cache=False):
        key = (
            round(element.length, 5),
            element.cross_section.section_label,
            tuple(element.cross_section.section_parameters),
        )

        if use_cache and (key in self.cached):
            return self.cached[key]

        source = super().create_element_data(element)
        self.cached[key] = source
        return source
