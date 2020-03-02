import vtk
import numpy as np
import random
from pulse.opv.colorTable import ColorTable

class Lines:
    def __init__(self, **kwargs):

        '''
        Pipeline start with assembly() funcion
        Pipeline # Source -> Filter -> Map -> Actor
        '''
        self.tag = kwargs.get("tag", -1)
        self.initial = kwargs.get("initial", False)

        self.nodesList = kwargs.get("nodes", [])
        self.edgesList = kwargs.get("edges", [])
        self.colorsList = kwargs.get("colors", [])

        #Configs
        self.show_lines = kwargs.get("showLines", False)

        #Source
        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()

        #Filter
        self._colorTable = ColorTable()
        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        #Map
        self._mapper = vtk.vtkPolyDataMapper()

        #Actor
        self._line_actor = vtk.vtkActor()

    def assembly(self):
        self._source()
        self._filter()
        self._map()
        self._actor()

    def _source(self):
        for node in self.nodesList:
            self._nodes.InsertPoint(int(node[0]), node[1], node[2], node[3])

        for edge in self.edgesList:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, edge[1])
            line.GetPointIds().SetId(1, edge[2])
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)


    def _filter(self):
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        if self._colorTable.is_empty():
            for _ in range(self._nodes.GetNumberOfPoints()):
                self._colorFilter.InsertNextTypedTuple(color)
        else:
            for id_, _ in self.structure.nodes.items():
                self._colorFilter.InsertTypedTuple(id_, self._colorTable.get_color_by_id(id_))

        self._object.GetPointData().SetScalars(self._colorFilter)
        
        if not self.show_lines:
            self._tubeFilter.SetInputData(self._object)
            if self.initial:
                self._tubeFilter.SetRadius(0.01)
            else:
                self._tubeFilter.SetRadius(0.05)
            self._tubeFilter.SetNumberOfSides(50)
            self._tubeFilter.Update()


    def _map(self):
        if self.show_lines:
            self._mapper.SetInputData(self._object)
        else:
            self._mapper.SetInputData(self._tubeFilter.GetOutput())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)

    def get_actor(self):
        return self._line_actor

    def get_table(self):
        return self._colorTable