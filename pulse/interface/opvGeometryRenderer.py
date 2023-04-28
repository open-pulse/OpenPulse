import vtk
import numpy as np 
from time import time
from dataclasses import dataclass
from collections import defaultdict

from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.colorTable import ColorTable

from pulse.interface.tubeActor import TubeActor
from pulse.interface.nodesActor import NodesActor
from pulse.interface.linesActor import LinesActor
from pulse.interface.rawLinesActor import RawLinesActor
from pulse.interface.rawNodesActor import RawNodesActor
from pulse.interface.acousticSymbolsActor import AcousticNodesSymbolsActor, AcousticElementsSymbolsActor
from pulse.interface.structuralSymbolsActor import StructuralNodesSymbolsActor, StructuralElementsSymbolsActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor

class opvGeometryRenderer(vtkRendererBase):
    '''
    A renderer to handle plot and selection of geometry files.
    It should be completelly independent from any element or nodes generated
    to use with the actual solver.
    '''

    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project 
        self.opv = opv

        self.opvRawLines = None
        self.opvRawNodes = None
        self.opvSelectionLinesActor = None
        self.opvSelectionNodesActor = None

        # Selection stuff
        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.lineToElements = dict()
        self._style.AddObserver('SelectionChangedEvent', self.highlight)

    def plot(self):
        self.opvRawNodes = RawNodesActor()
        # MODIFIQUE A LINHA ABAIXO:
        # Substitua por algo como
        # pontos = self.project.blabla.pontos
        # self.opvRawNodes.set_data(pontos)
        self.opvRawNodes.load_file("C:\\Users\\User\\Documents\\OpenPulse\\examples\\iges_files\\old_geometries\\tube_2.iges")
        self.opvRawNodes.build()
        
        self.opvRawLines = RawLinesActor()
        # MODIFIQUE A LINHA ABAIXO:
        # Substitua por algo como
        # linhas = self.project.blabla.linhas
        # self.opvRawLines.set_data(linhas)
        self.opvRawLines.load_file("C:\\Users\\User\\Documents\\OpenPulse\\examples\\iges_files\\old_geometries\\tube_2.iges")
        self.opvRawLines.build()
        self._renderer.AddActor(self.opvRawLines.getActor())

        self.save_nodes_bounds()
        self.save_elements_bounds()

        self._renderer.AddActor(self.opvRawNodes.getActor())
        self._renderer.ResetCameraClippingRange()

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()

    def update(self):
        renWin = self._renderer.GetRenderWindow()
        if renWin:
            renWin.Render()

    def updateInfoText(self):
        pass

    def save_nodes_bounds(self):
        self.nodesBounds.clear()

        if self.opvRawNodes is None:
            return

        for i, x, y, z in self.opvRawNodes._nodes:
            self.nodesBounds[i] = (x,x, y,y, z,z)

    def save_elements_bounds(self):
        self.elementsBounds.clear()
        self.lineToElements.clear()
        
        if self.opvRawLines is None:
            return
        
        line_to_elements = defaultdict(list)
        
        t = 0
        for i, (tag, first_node, second_node) in enumerate(self.opvRawLines._segments):
            x0 = min(first_node[0], second_node[0]) - t
            y0 = min(first_node[1], second_node[1]) - t
            z0 = min(first_node[2], second_node[2]) - t
            x1 = max(first_node[0], second_node[0]) + t
            y1 = max(first_node[1], second_node[1]) + t
            z1 = max(first_node[2], second_node[2]) + t
            bounds = (x0,x1,y0,y1,z0,z1)
            self.elementsBounds[i] = bounds
            line_to_elements[tag].append(i)
        
        self.lineToElements = dict(line_to_elements)

    def highlight(self, obj, event):
        self.highlight_nodes(obj, event)
        self.highlight_lines(obj, event)
        self.update()

    def highlight_nodes(self, obj, event):
        selected_nodes = obj.getListPickedPoints()
        selected_nodes_coords = [node for node in self.opvRawNodes._nodes if node[0] in selected_nodes]
        
        if self.opvSelectionNodesActor is not None:
            self._renderer.RemoveActor(self.opvSelectionNodesActor.getActor())
        
        if selected_nodes:
            self.opvSelectionNodesActor = RawNodesActor()
            self.opvSelectionNodesActor.set_data(selected_nodes_coords)
            self.opvSelectionNodesActor.build()

            self.opvSelectionNodesActor.getActor().GetProperty().SetPointSize(10)
            self.opvSelectionNodesActor.getActor().GetProperty().SetColor((1, 0, 0))
            self._renderer.AddActor(self.opvSelectionNodesActor.getActor())

    def highlight_lines(self, obj, event):
        selected_segments = obj.getListPickedLines()
        selected_segments_coords = [segment for segment in self.opvRawLines._segments if segment[0] in selected_segments]
        
        if self.opvSelectionLinesActor is not None:
            self._renderer.RemoveActor(self.opvSelectionLinesActor.getActor())
        

        if selected_segments:
            self.opvSelectionLinesActor = RawLinesActor()
            self.opvSelectionLinesActor.set_data(selected_segments_coords)
            self.opvSelectionLinesActor.build()

            self.opvSelectionLinesActor.getActor().GetProperty().SetLineWidth(5)
            self.opvSelectionLinesActor.getActor().GetProperty().SetColor((1, 0, 0))
            self._renderer.AddActor(self.opvSelectionLinesActor.getActor())