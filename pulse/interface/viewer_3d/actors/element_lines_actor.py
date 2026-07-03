from molde.actors import GhostActor
from molde.colors import PURPLE_7
from molde.poly_data import LinesData
from molde.utils import set_polydata_colors
from vtkmodules.vtkCommonCore import vtkCharArray, vtkIntArray, vtkUnsignedIntArray
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from pulse import app
import numpy as np


class ElementLinesActor(GhostActor):
    def __init__(self, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.show_deformed = show_deformed
        self.hidden_elements = kwargs.get("hidden_elements", set())

        self.rigid_elements = self.model.get_rigid_elements()
        self.deformed_coordinates = app().project.model.preprocessor.deformed_coordinates

        self.build()

    @property
    def user_preferences(self):
        return app().main_window.config.user_preferences

    @property
    def project(self):
        return app().project

    @property
    def model(self):
        return app().project.model

    @property
    def elements_attributes(self):
        return app().project.model.preprocessor.elements_attributes

    def build(self):

        all_elements = np.array(list(self.elements_attributes.keys()), dtype=int)
        visible_elements = all_elements[~np.isin(all_elements, self.hidden_elements)]

        self._key_index = {j: i for i, j in enumerate(visible_elements)}

        lines = list()
        entity_index = vtkUnsignedIntArray()
        entity_index.SetName("entity_index")
        element_index = vtkUnsignedIntArray()
        element_index.SetName("element_index")

        for i, elem_id in enumerate(visible_elements):
            element_attributes = self.elements_attributes.get(elem_id)
            first_node = element_attributes.first_node
            last_node = element_attributes.last_node

            x0, y0, z0 = self.deformed_coordinates[first_node.global_index, 1:] if self.show_deformed else first_node.coordinates
            x1, y1, z1 = self.deformed_coordinates[ last_node.global_index, 1:] if self.show_deformed else last_node.coordinates

            lines.append((x0, y0, z0, x1, y1, z1))
            entity = self.model.mesh.line_from_element.get(elem_id)
            if entity is None:
                print(f"Warning: the element [{i}] is not associated with a line")
                continue

            entity_index.InsertNextTuple1(entity)
            element_index.InsertNextTuple1(elem_id)

        data = LinesData(lines)
        data.GetCellData().AddArray(entity_index)
        data.GetCellData().AddArray(element_index)

        lines_color = self.user_preferences.lines_color.to_rgb()
        set_polydata_colors(data, lines_color)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        mapper.ScalarVisibilityOff()  # Just to force color updates
        mapper.ScalarVisibilityOn()

        self.SetMapper(mapper)
        self.GetProperty().SetLineWidth(6)
        self.make_ghost()

    # def _get_rigid_element_ids(self):
    #     rigid_ids = set()
    #     for structure in self.project.pipeline.structures:
    #         if structure.extra_info.get("structural_element_type") == "rigid_element":
    #             rigid_ids.update(self.mesh.elements_from_line.get(structure.tag))

    #     return rigid_ids

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        lines_color = self.user_preferences.lines_color.to_rgb()
        set_polydata_colors(data, lines_color)

        if not self.rigid_elements:
            return

        self.set_color(PURPLE_7.to_rgb(), elements=self.rigid_elements)

    def set_color(self, color, elements=None, lines=None):
        mapper = self.GetMapper()
        data = mapper.GetInput()

        if (elements is None) and (lines is None):
            set_polydata_colors(data, color)
            mapper.SetScalarModeToUseCellData()
            mapper.ScalarVisibilityOff()  # Just to force color updates
            mapper.ScalarVisibilityOn()
            return

        elements = set(elements) if elements else set()
        lines = set(lines) if lines else set()

        n_cells = data.GetNumberOfCells()
        element_indexes: vtkIntArray = data.GetCellData().GetArray("element_index")
        entity_indexes: vtkIntArray = data.GetCellData().GetArray("entity_index")
        colors: vtkCharArray = data.GetCellData().GetArray("colors")

        for i in range(n_cells):

            try:
                element = element_indexes.GetValue(i)
                entity = entity_indexes.GetValue(i)
               
                if (entity in lines) or (element in elements):
                    colors.SetTuple3(i, *color)

            except Exception as error_log:
                print(str(error_log))

        mapper.SetScalarModeToUseCellData()
        mapper.ScalarVisibilityOff()  # Just to force color updates
        mapper.ScalarVisibilityOn()

    def get_cell_element(self, cell):
        data = self.GetMapper().GetInput()
        element_indexes: vtkIntArray = data.GetCellData().GetArray("element_index")
        return element_indexes.GetValue(cell)

    def get_cell_entity(self, cell):
        data = self.GetMapper().GetInput()
        entity_index: vtkIntArray = data.GetCellData().GetArray("entity_index")
        return entity_index.GetValue(cell)
