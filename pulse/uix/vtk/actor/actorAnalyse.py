import vtk
import numpy as np
from pulse.uix.vtk.vtkActorBase import vtkActorBase

class ActorAnalyse(vtkActorBase):
    def __init__(self, project, connect, coord_def, color_table):
        super().__init__()

        self.project = project
        self.connect = connect
        self.coord_def = coord_def
        self.colorTable = color_table
        self.elements = self.project.getElements()

        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()
        self.teste = vtk.vtkDoubleArray()

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        indice = self.coord_def[:,0]
        x = self.coord_def[:,1]
        y = self.coord_def[:,2]
        z = self.coord_def[:,3]

        for i in range(len(indice)):
            id_ = int(indice[i])
            self._nodes.InsertPoint(id_, x[i], y[i], z[i])
            # print(id_, x[i], y[i], z[i])


        for i in range(len(self.elements)):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, self.connect[i,1])
            line.GetPointIds().SetId(1, self.connect[i,2])
            self._edges.InsertNextCell(line)
            
        # for element in self.elements.values():
        #     line = vtk.vtkLine()
        #     # line.GetPointIds().SetId(0, element.first_node_id)
        #     # line.GetPointIds().SetId(1, element.last_node_id)
        #     # line.GetPointIds().SetId(0, element.first_node.global_index)
        #     # line.GetPointIds().SetId(1, element.last_node.global_index)
        #     line.GetPointIds().SetId(0, element.first_node.external_index)
        #     line.GetPointIds().SetId(1, element.last_node.external_index)
        #     self._edges.InsertNextCell(line)
            
        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def filter(self):
        indice = self.coord_def[:,0]
        for i in range(len(indice)):
            id_ = int(indice[i])
            self._colorFilter.InsertTypedTuple(id_, self.colorTable.get_color_by_id(i))
        self._object.GetPointData().SetScalars(self._colorFilter)

        self.teste.SetName("TubeRadius")
        self.teste.SetNumberOfTuples(len(indice))
        j = 0.001
        for i in range(500):
            id_ = int(indice[i])
            self.teste.SetTuple1(id_,0.01)

        for i in range(500, len(indice)):
            id_ = int(indice[i])
            self.teste.SetTuple1(id_,0.03)

        self._object.GetPointData().AddArray(self.teste)
        #self._object.GetPointData().SetActiveScalars("TubeRadius")
        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.02)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.SetCapping(True)
        self._tubeFilter.SetVaryRadiusToVaryRadiusByVector()
        self._tubeFilter.Update()
        

    def map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())
        self._mapper.ScalarVisibilityOn()
        #self._mapper.SetScalarModeToUsePointFieldData()

    def actor(self):
        self._actor.SetMapper(self._mapper)