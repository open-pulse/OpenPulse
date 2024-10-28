from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData


def paint_data(data: vtkPolyData, color: tuple):
    n_cells = data.GetNumberOfCells()
    cell_colors = vtkUnsignedCharArray()
    cell_colors.SetName("colors")
    cell_colors.SetNumberOfComponents(3)
    cell_colors.SetNumberOfTuples(n_cells)
    cell_colors.FillComponent(0, color[0])
    cell_colors.FillComponent(1, color[1])
    cell_colors.FillComponent(2, color[2])
    data.GetCellData().SetScalars(cell_colors)


def fill_cell_identifier(data: vtkPolyData, identifier: int):
    n_cells = data.GetNumberOfCells()
    cell_identifier = vtkUnsignedCharArray()
    cell_identifier.SetName("cell_identifier")
    cell_identifier.SetNumberOfTuples(n_cells)
    cell_identifier.Fill(identifier)
    data.GetCellData().AddArray(cell_identifier)
