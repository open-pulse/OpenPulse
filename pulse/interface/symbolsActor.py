import vtk
import numpy as np 
from time import time
from collections import namedtuple
from itertools import chain

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
    NODAL_LOAD_POSITION_SYMBOL = loadSymbol('pulse/interface/symbols/nodalLoadPosition.obj')
    NODAL_LOAD_ROTATION_SYMBOL = loadSymbol('pulse/interface/symbols/nodalLoadRotation.obj')
    DUMPER_SYMBOL = loadSymbol('pulse/interface/symbols/dumper.obj')
    SPRING_SYMBOL = loadSymbol('pulse/interface/symbols/spring.obj')
    VOLUME_VELOCITY_SYMBOL = loadSymbol('pulse/interface/symbols/volumeVelocity.obj')
    ACOUSTIC_PRESSURE_SYMBOL = loadSymbol('pulse/interface/symbols/acousticPressure.obj')
    SPECIFIC_IMPEDANCE_SYMBOL = loadSymbol('pulse/interface/symbols/specificImpedance.obj')
    RADIATION_IMPEDANCE_SYMBOL = loadSymbol('pulse/interface/symbols/radiationImpedance.obj')
    LUMPED_MASS_SYMBOL = loadSymbol('pulse/interface/symbols/lumpedMass.obj')
    COMPRESSOR_SYMBOL = loadSymbol('pulse/interface/symbols/compressor.obj')
    

    def __init__(self, nodes, project, deformed=False):
        super().__init__()
        
        self.project = project
        self.nodes = nodes
        self.deformed = deformed
        self.scaleFactor = 0.3

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()
    
    def source(self):
        self.scaleFactor = self.project.mesh.structure_principal_diagonal / 10
        
        self._createArrays()
        self._loadSources()
        self._createNodalLinks()
        
        for node in self.nodes.values():
            for symbol in self._getAllSymbols(node):
                self._createSymbol(symbol)        

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetScaleFactor(self.scaleFactor)
        
        self._mapper.SourceIndexingOn()
        self._mapper.SetOrientationModeToRotation()
        self._mapper.Update()

    def filter(self):
        pass
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetOpacity(0.9)
        self._actor.GetProperty().BackfaceCullingOff()

    def _createArrays(self):
        self._sources = vtk.vtkIntArray()
        self._positions = vtk.vtkPoints()
        self._rotations = vtk.vtkDoubleArray()
        self._colors = vtk.vtkUnsignedCharArray()

        self._sources.SetName('sources')
        self._rotations.SetName('rotations')
        self._rotations.SetNumberOfComponents(3)
        self._colors.SetNumberOfComponents(3)

        self._data.SetPoints(self._positions)
        self._data.GetPointData().AddArray(self._rotations)
        self._data.GetPointData().AddArray(self._sources)
        self._data.GetPointData().SetScalars(self._colors)

    def _loadSources(self):
        # HERE YOU SET THE INDEXES OF THE SOURCES
        self._mapper.SetSourceData(1, self.PRESCRIBED_POSITION_SYMBOL)
        self._mapper.SetSourceData(2, self.PRESCRIBED_ROTATION_SYMBOL)
        self._mapper.SetSourceData(3, self.NODAL_LOAD_POSITION_SYMBOL)
        self._mapper.SetSourceData(4, self.NODAL_LOAD_ROTATION_SYMBOL)
        self._mapper.SetSourceData(5, self.DUMPER_SYMBOL)
        self._mapper.SetSourceData(6, self.SPRING_SYMBOL)
        self._mapper.SetSourceData(7, self.VOLUME_VELOCITY_SYMBOL)
        self._mapper.SetSourceData(8, self.ACOUSTIC_PRESSURE_SYMBOL)
        self._mapper.SetSourceData(9, self.SPECIFIC_IMPEDANCE_SYMBOL)
        self._mapper.SetSourceData(10, self.RADIATION_IMPEDANCE_SYMBOL)
        self._mapper.SetSourceData(11, self.LUMPED_MASS_SYMBOL)
        self._mapper.SetSourceData(12, self.COMPRESSOR_SYMBOL)
    
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
        symbols.extend(self._getNodalLoadPosition(node))
        symbols.extend(self._getNodalLoadRotation(node))
        symbols.extend(self._getDamper(node))
        symbols.extend(self._getSpring(node))
        symbols.extend(self._getVolumeVelocity(node))
        symbols.extend(self._getAcousticPressure(node))
        symbols.extend(self._getSpecificImpedance(node))
        symbols.extend(self._getRadiationImpedance(node))
        symbols.extend(self._getLumpedMass(node))
        symbols.extend(self._getCompressor(node))
        return symbols
    
    def _createNodalLinks(self):
        # temporary structure to plot elastic links 

        linkedNodes = set()
        linkedSymbols = vtk.vtkAppendPolyData()

        # extract from string values that shoud be avaliable
        # create a set without useless repetitions 
        for node in self.nodes.values():
            stif = tuple(node.elastic_nodal_link_stiffness.keys())
            damp = tuple(node.elastic_nodal_link_damping.keys())
            if stif:
                nodes = sorted(int(i) for i in stif[0].split('-'))
            elif damp:
                nodes = sorted(int(i) for i in damp[0].split('-'))
            else:
                continue 
            linkedNodes.add(tuple(nodes))

        for a, b in linkedNodes:
            # divide the value of the coordinates by the scale factor
            source = vtk.vtkLineSource()
            source.SetPoint1(self.nodes[a].coordinates / self.scaleFactor) 
            source.SetPoint2(self.nodes[b].coordinates / self.scaleFactor)
            source.Update()
            linkedSymbols.AddInputData(source.GetOutput())
        
        linkedSymbols.Update()
        self._mapper.SetSourceData(0, linkedSymbols.GetOutput())
        self._sources.InsertNextTuple1(0)
        self._positions.InsertNextPoint(0,0,0)
        self._rotations.InsertNextTuple3(0,0,0)
        self._colors.InsertNextTuple3(16,222,129)
    
    def _getPrescribedPositionSymbols(self, node):
        offset = 0
        x,y,z = self._getCoords(node)
        sor = 1
        col = (0,255,0)

        symbols = []
        mask = [(i != None) for i in node.getStructuralBondaryCondition()[:3]]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y+offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols

    def _getPrescribedRotationSymbols(self, node):
        offset = 0
        x,y,z = self._getCoords(node)
        sor = 2
        col = (0,200,200)

        symbols = []
        mask = [(i != None) for i in node.getStructuralBondaryCondition()[3:]]
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols

    def _getNodalLoadPosition(self, node):
        offset = 0.01
        x,y,z = self._getCoords(node)
        sor = 3
        col = (255,0,0)

        symbols = []
        mask = node.get_prescribed_loads()[:3]
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y+offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols
    
    def _getNodalLoadRotation(self, node):
        offset = 0.01
        x,y,z = self._getCoords(node)
        sor = 4
        col = (0,0,255)

        symbols = []
        mask = node.get_prescribed_loads()[3:]
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y+offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols
    
    def _getDamper(self, node):
        offset = 0.01
        x,y,z = self._getCoords(node)
        sor = 5
        col = (255,0,100)

        symbols = []
        mask = node.get_lumped_dampings()[:3]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y+offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols
    
    def _getSpring(self, node):
        offset = 0.01
        x,y,z = self._getCoords(node)
        sor = 6
        col = (242,121,0)

        symbols = []
        mask = node.get_lumped_stiffness()[:3]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[1]:
            pos = (x, y+offset, z)
            rot = (0,0,180)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        
        return symbols

    def _getVolumeVelocity(self, node):
        sor = 7
        pos = node.coordinates
        rot = (0,0,0)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_connection_info is None):
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols

    def _getAcousticPressure(self, node):
        sor = 8
        pos = node.coordinates
        rot = (0,0,0)
        col = (150,0,210) #violet
        symbols = []

        if node.acoustic_pressure is not None:
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols

    def _getSpecificImpedance(self, node):
        sor = 9
        pos = node.coordinates
        rot = (0,0,0)
        col = (100,255,100)
        symbols = []

        if node.specific_impedance is not None:
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols
    
    def _getRadiationImpedance(self, node):
        sor = 10
        pos = node.coordinates
        rot = (0,0,0)
        col = (224,0,75)
        symbols = []

        if node.radiation_impedance_type in [0,1,2]:
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols

    def _getLumpedMass(self, node):
        sor = 11
        pos = node.coordinates
        rot = (0,0,0)
        col = (7,156,231)
        symbols = []

        if any(node.lumped_masses):
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols
    
    def _getCompressor(self, node):
        sor = 12
        pos = node.coordinates
        rot = (0,0,0)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_connection_info is not None):
            symbols.append(Symbol(source=sor, position=pos, rotation=rot, color=col))
        return symbols
    
    def _getCoords(self, node):
        if self.deformed:
            return node.deformed_coordinates
        else:
            return node.coordinates
