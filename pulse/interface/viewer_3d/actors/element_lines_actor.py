from molde.actors import GhostActor
from molde.poly_data import LinesData
from molde.utils import set_polydata_colors
from vtkmodules.vtkCommonCore import vtkCharArray, vtkIntArray, vtkUnsignedIntArray
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from pulse import app

class ElementLinesActor(GhostActor):
    def __init__(self, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.project = app().project
        self.preprocessor = self.project.preprocessor
        self.elements = self.project.get_structural_elements()
        self.hidden_elements = kwargs.get("hidden_elements", set())
        self.show_deformed = show_deformed
        self.build()

    def build(self):
        visible_elements = {
            i: e for i, e in self.elements.items() if (i not in self.hidden_elements)
        }
        self._key_index = {j: i for i, j in enumerate(visible_elements)}

        lines = []
        entity_index = vtkUnsignedIntArray()
        entity_index.SetName("entity_index")
        element_index = vtkUnsignedIntArray()
        element_index.SetName("element_index")

        for i, element in visible_elements.items():
            if self.show_deformed:
                x0, y0, z0 = element.first_node.deformed_coordinates
                x1, y1, z1 = element.last_node.deformed_coordinates
            else:
                x0, y0, z0 = element.first_node.coordinates
                x1, y1, z1 = element.last_node.coordinates

            lines.append((x0, y0, z0, x1, y1, z1))
            entity = self.preprocessor.mesh.line_from_element[i]
            entity_index.InsertNextTuple1(entity)
            element_index.InsertNextTuple1(i)

        data = LinesData(lines)
        data.GetCellData().AddArray(entity_index)
        data.GetCellData().AddArray(element_index)
        set_polydata_colors(data, (90, 90, 90))

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        mapper.ScalarVisibilityOff()  # Just to force color updates
        mapper.ScalarVisibilityOn()

        self.SetMapper(mapper)
        self.GetProperty().SetLineWidth(6)
        self.make_ghost()

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        set_polydata_colors(data, (90, 90, 90))

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
            element = element_indexes.GetValue(i)
            entity = entity_indexes.GetValue(i)
            if (entity in lines) or (element in elements):
                colors.SetTuple3(i, *color)

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
