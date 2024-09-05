from abc import ABC, abstractmethod
from collections import namedtuple

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import vtkGlyph3DMapper

from pulse.interface.viewer_3d.actors.actor_base import ActorBase


def loadSymbol(path):
    reader = vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


SymbolTransform = namedtuple(
    "SymbolTransform", ["source", "position", "rotation", "scale", "color"]
)


class SymbolsActorBase(ActorBase):
    """
    Abstract class that defines how to create a new set of Symbols.

    Note
    ----
    If you want to inherit this class, you need to define at least 2 methods:
        _createConnections()
        _createSequence()
    Check out their definitions to understand how they are meant to be defined
    """

    def __init__(self, project, deformed=False):
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.deformed = deformed
        if self.process_scaleFactor():
            self.scale_factor = 1
        # print(f"scaleFactor: {self.scale_factor}")

        self._connections = self._createConnections()
        # self._sequence = self._createSequence()

        self._data = vtkPolyData()
        self._mapper = vtkGlyph3DMapper()

    @abstractmethod
    def _createConnections(self):
        """
        This method is meant to return a list of pairs of function and symbols.
            [Function] is a set of rules of how and when to display your symbol.
            [Symbol] is a vtkPolyData object of whatever you want to display.

        Example:
        --------
        def _createConnections(self):
            return [(functionA, symbolA), (functionB, symbolB)]

        def _createConnection(self):
            return [(functionTest, loadSymbol("path/to/my/symbol.obj"))]
        """

        return []

    # @abstractmethod
    # def _createSequence(self):
    #     '''
    #     Every function of how to display a symbol will be applied to some sequence
    #     like nodes, elements, or whatever our creative minds come up with. Here you define the
    #     sequence of things you want those functions to map.
    #     '''

    #     return []

    def process_scaleFactor(self):
        if self.project.preprocessor.structure_principal_diagonal is None:
            return True
        else:
            diagonal = self.project.preprocessor.structure_principal_diagonal
            if diagonal <= 0.01:
                self.scale_factor = 0.01
            elif diagonal <= 0.1:
                self.scale_factor = 0.05
            elif diagonal <= 1:
                self.scale_factor = 0.2
            elif diagonal <= 2:
                self.scale_factor = 0.3
            elif diagonal <= 10:
                self.scale_factor = 0.4
            elif diagonal <= 20:
                self.scale_factor = 0.6
            elif diagonal <= 30:
                self.scale_factor = 0.8
            elif diagonal <= 40:
                self.scale_factor = 1
            elif diagonal <= 50:
                self.scale_factor = 1.2
            else:
                self.scale_factor = 2.5

            # print(f"Structure diagonal: {diagonal}")
            # print(f"Symbols scale factor: {self.scale_factor}")

    def source(self):

        self._createArrays()
        # self._loadSources()

        for i, (transforms, symb) in enumerate(self._connections):
            self._mapper.SetSourceData(i, symb)
            for transform in transforms:
                self._createSymbol(i, transform)

        self._populateData()

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetSourceIndexArray("sources")
        self._mapper.SetOrientationArray("rotations")
        self._mapper.SetScaleArray("scales")
        self._mapper.SetScaleFactor(self.scale_factor)

        self._mapper.SourceIndexingOn()
        self._mapper.SetOrientationModeToRotation()
        self._mapper.SetScaleModeToScaleByVectorComponents()
        self._mapper.Update()

    def filter(self):
        pass

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetOpacity(0.9)
        self._actor.GetProperty().BackfaceCullingOff()
        self._actor.SetUseBounds(False)

    def _createArrays(self):
        self._sources = vtkIntArray()
        self._positions = vtkPoints()
        self._rotations = vtkDoubleArray()
        self._scales = vtkDoubleArray()
        self._colors = vtkUnsignedCharArray()

        self._sources.SetName("sources")
        self._rotations.SetName("rotations")
        self._scales.SetName("scales")
        self._rotations.SetNumberOfComponents(3)
        self._scales.SetNumberOfComponents(3)
        self._colors.SetNumberOfComponents(3)

    def _populateData(self):
        self._data.SetPoints(self._positions)
        self._data.GetPointData().AddArray(self._sources)
        self._data.GetPointData().AddArray(self._rotations)
        self._data.GetPointData().AddArray(self._scales)
        self._data.GetPointData().SetScalars(self._colors)

    # def _loadSources(self):
    #     for i, (func, symb) in enumerate(self._connections):
    #         self._mapper.SetSourceData(i, symb)

    def _createSymbol(self, src, symbol):
        self._sources.InsertNextTuple1(src)
        self._positions.InsertNextPoint(symbol.position)
        self._rotations.InsertNextTuple(symbol.rotation)
        self._scales.InsertNextTuple(symbol.scale)
        self._colors.InsertNextTuple(symbol.color)
