import vtk
import numpy as np
from pulse.uix.vtk.vtkActorBase import vtkActorBase

class ActorAnalysis(vtkActorBase):
    def __init__(self, project, connect, coord_def, color_table, stress):
        super().__init__()

        self.project = project
        self.connect = connect
        self.coord_def = coord_def
        self.colorTable = color_table
        self.stress = stress
        self.elements = self.project.get_elements()

        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()
        self.radiusArray = vtk.vtkDoubleArray()

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)
        self._colorFilter.SetName("Colors")

        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        indice = self.coord_def[:,0]
        x = self.coord_def[:,1]
        y = self.coord_def[:,2]
        z = self.coord_def[:,3]

        for i in range(len(indice)):
            id_ = int(indice[i])
            self._nodes.InsertPoint(id_, x[i], y[i], z[i])

        for i in range(len(self.elements)):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, self.connect[i,1])
            line.GetPointIds().SetId(1, self.connect[i,2])
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def filter(self):
        indice = self.coord_def[:,0]
        if self.stress:
            for key, _ in self.elements.items():
                self._colorFilter.InsertTypedTuple(key-1, self.colorTable.get_color_by_id(key-1))
            self._object.GetCellData().SetScalars(self._colorFilter)
        else:
            for i in range(len(indice)):
                id_ = int(indice[i])
                self._colorFilter.InsertTypedTuple(id_, self.colorTable.get_color_by_id(i))
            self._object.GetPointData().AddArray(self._colorFilter)

        self.radiusArray.SetName("TubeRadius")
        self.radiusArray.SetNumberOfTuples(len(indice))
        radius = self.project.mesh.get_radius()
        for i in range(len(indice)):
            id_ = int(indice[i])
            self.radiusArray.SetTuple1(id_, radius[id_])

        self._object.GetPointData().AddArray(self.radiusArray)
        self._object.GetPointData().SetActiveScalars("TubeRadius")
        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.02)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.SetCapping(True)
        self._tubeFilter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
        self._tubeFilter.Update()
        

    def map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())
        self._mapper.ScalarVisibilityOn()
        self._mapper.SelectColorArray("Colors")
        if self.stress:
            self._mapper.SetScalarModeToUseCellFieldData()
        else:
            self._mapper.SetScalarModeToUsePointFieldData()

    def actor(self):
        self._actor.SetMapper(self._mapper)