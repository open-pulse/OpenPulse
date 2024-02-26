import vtk
from pulse.interface.vtkActorBase import vtkActorBase

class ActorEntityElements(vtkActorBase):
    def __init__(self, elements, tag=-1):
        super().__init__()
        self.elements = elements
        self.tag = tag
        self._object = vtk.vtkAppendPolyData()
        
        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._data = vtk.vtkPolyData()

        self.normalizedColor = [0,1,1]

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        for element in self.elements:
            _nodes = vtk.vtkPoints()
            _edges = vtk.vtkCellArray()
            _data = vtk.vtkPolyData()
            _colorFilter = vtk.vtkUnsignedCharArray()
            _colorFilter.SetNumberOfComponents(3)
            _nodes.InsertPoint(0, element.first_node.x, element.first_node.y, element.first_node.z)
            _nodes.InsertPoint(1, element.last_node.x, element.last_node.y, element.last_node.z)

            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, 0)
            line.GetPointIds().SetId(1, 1)
            _edges.InsertNextCell(line)

            _data.SetPoints(_nodes)
            _data.SetLines(_edges)

            color = [0,0,255]
            for _ in range(_nodes.GetNumberOfPoints()):
                _colorFilter.InsertNextTypedTuple(color)

            _data.GetPointData().SetScalars(_colorFilter)

            _tubeFilter = vtk.vtkTubeFilter()
            _tubeFilter.SetInputData(_data)
            _tubeFilter.SetRadius(0.003)
            _tubeFilter.SetNumberOfSides(36)
            _tubeFilter.Update()

            self._object.AddInputConnection(_tubeFilter.GetOutputPort())
            self._object.Update()

    def filter(self):
        pass

    def map(self):
        self._mapper.SetInputConnection(self._object.GetOutputPort())
        self._mapper.SetColorModeToDirectScalars()
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)