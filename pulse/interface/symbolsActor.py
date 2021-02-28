from collections import namedtuple
import vtk

from pulse.interface.vtkActorBase import vtkActorBase

def loadSymbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

Symbol = namedtuple('Symbol', ['source', 'position', 'rotation', 'color'])

class SymbolsActor(vtkActorBase):
    PRESCRIBED_POSITION_SYMBOL = loadSymbol('pulse/interface/symbols/prescribedPosition.obj')
    PRESCRIBED_ROTATION_SYMBOL = loadSymbol('pulse/interface/symbols/prescribedRotation.obj')
    # NODAL_LOAD_POSITION_SYMBOL = loadSymbol('pulse/interface/symbols/nodalLoadPosition.obj')
    # NODAL_LOAD_ROTATION_SYMBOL = loadSymbol('pulse/interface/symbols/nodalLoadRotation.obj')

    def __init__(self, nodes, project):
        super().__init__()
        
        self.project = project
        self.nodes = nodes

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()
    
    def source(self):
        self._createArrays()
        self._loadSources()
        
        for node in self.nodes.values():
            for symbol in self._getAllSymbols(node):
                self._createSymbol(symbol)        

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetScaleFactor(0.1)
        
        self._mapper.SourceIndexingOn()
        self._mapper.SetOrientationModeToRotation()
        self._mapper.Update()

    def filter(self):
        pass
    
    def actor(self):
        self._actor.SetMapper(self._mapper)

    def _createArrays(self):
        self._sources = vtk.vtkIntArray()
        self._positions = vtk.vtkPoints()
        self._rotations = vtk.vtkDoubleArray()
        self._colors = vtk.vtkUnsignedCharArray()

        self._sources.SetName('sources')
        self._rotations.SetName('rotations')
        self._rotations.SetNumberOfComponents(3)
        self._colors.SetNumberOfComponents(3)
        # self._colors.SetNumberOfTuples(len(self.nodes))

        self._data.SetPoints(self._positions)
        self._data.GetPointData().AddArray(self._rotations)
        self._data.GetPointData().AddArray(self._sources)
        self._data.GetPointData().SetScalars(self._colors)

    def _loadSources(self):
        # HERE YOU SET THE INDEXES OF THE SOURCES
        self._mapper.SetSourceData(0, self.PRESCRIBED_POSITION_SYMBOL)
        self._mapper.SetSourceData(1, self.PRESCRIBED_ROTATION_SYMBOL)
        # self._mapper.SetSourceData(2, self.NODAL_LOAD_POSITION_SYMBOL)
        # self._mapper.SetSourceData(3, self.NODAL_LOAD_ROTATION_SYMBOL)

    
    def _createSymbol(self, symbol):
        self._sources.InsertNextTuple1(symbol.source)
        self._positions.InsertNextPoint(symbol.position)
        self._rotations.InsertNextTuple(symbol.rotation)
        self._colors.InsertNextTuple(symbol.color)

    def _getAllSymbols(self, node):
        # HERE YOU CALL THE FUNCTIONS CREATED
        symbols = []
        symbols.extend(self._getPrescribedPositionSymbols(node))
        symbols.extend(self._getPrescribedRotationSymbols(node))
        symbols.extend(self._getNodalLoadDisplacement(node))
        symbols.extend(self._getNodalLoadRotation(node))
        return symbols
    
    def _getPrescribedPositionSymbols(self, node):
        offset = 0.01
        x,y,z = node.coordinates
        mask = [(i != None) for i in node.getStructuralBondaryCondition()[:3]]

        symbols = []
        if mask[0]:
            s = Symbol(source=0, position=(x-offset, y, z), rotation=(0,0,90), color=(0,255,0))
            symbols.append(s)

        if mask[1]:
            s = Symbol(source=0, position=(x, y+offset, z), rotation=(0,180,0), color=(0,255,0))
            symbols.append(s)

        if mask[2]:
            s = Symbol(source=0, position=(x, y, z-offset), rotation=(-90,0,0), color=(0,255,0))
            symbols.append(s)
        
        return symbols


    def _getPrescribedRotationSymbols(self, node):
        offset = 0
        x,y,z = node.coordinates
        mask = [(i != None) for i in node.getStructuralBondaryCondition()[3:]]

        symbols = []
        if mask[0]:
            s = Symbol(source=1, position=(x-offset, y, z), rotation=(0,0,90), color=(0,200,200))
            symbols.append(s)

        if mask[1]:
            s = Symbol(source=1, position=(x, y+offset, z), rotation=(0,180,0), color=(0,200,200))
            symbols.append(s)

        if mask[2]:
            s = Symbol(source=1, position=(x, y, z-offset), rotation=(-90,0,0), color=(0,200,200))
            symbols.append(s)
        
        return symbols

    def _getNodalLoadDisplacement(self, node):
        offset = 0.01
        x,y,z = node.coordinates
        mask = node.get_prescribed_loads()[:3]

        symbols = []
        if mask[0]:
            s = Symbol(source=0, position=(x-offset, y, z), rotation=(0,0,90), color=(255,0,0))
            symbols.append(s)

        if mask[1]:
            s = Symbol(source=0, position=(x, y+offset, z), rotation=(0,180,0), color=(255,0,0))
            symbols.append(s)

        if mask[2]:
            s = Symbol(source=0, position=(x, y, z-offset), rotation=(-90,0,0), color=(255,0,0))
            symbols.append(s)
        
        return symbols
    
    def _getNodalLoadRotation(self, node):
        mask = node.get_prescribed_loads()[3:]
        return []

