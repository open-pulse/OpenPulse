import vtk
import numpy as np 
from time import time
from dataclasses import dataclass

from pulse import app

from pulse.interface.viewer_3d.vtk.vtkRendererBase import vtkRendererBase
from pulse.interface.viewer_3d.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable

from pulse.interface.tubeActor import TubeActor
from pulse.interface.nodesActor import NodesActor
from pulse.interface.viewer_3d.actors.lines_actor import LinesActor
from pulse.interface.viewer_3d.actors.raw_lines_actor import RawLinesActor
from pulse.interface.viewer_3d.actors.acoustic_symbols_actor import AcousticNodesSymbolsActor, AcousticElementsSymbolsActor
from pulse.interface.viewer_3d.actors.structural_symbols_actor import StructuralNodesSymbolsActor, StructuralElementsSymbolsActor
from pulse.interface.viewer_3d.actors.tube_deformed_actor import TubeDeformedActor

from pulse.interface.viewer_3d.renders.model_info_texts import ModelInfoText


@dataclass
class PlotFilter:
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    raw_lines: bool = False

@dataclass
class SelectionFilter:
    nodes: bool    = False
    entities: bool = False
    elements: bool = False


class opvRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.opv = opv
        self.project = project
        self.preprocessor = project.preprocessor

        self.model_info_text = ModelInfoText(self)

        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.lineToElements = dict()

        self.raw_segment_bounds = dict()
        self.raw_segment_to_raw_line = dict()

        self.hidden_nodes    = set()
        self.hidden_elements = set()
        self.hidden_lines = set()

        self._plotFilter = PlotFilter()
        self._selectionFilter = SelectionFilter()
    
        self.opvNodes = None 
        self.opvLines = None
        self.opvTubes = None 
        self.opvSymbols = None
        self.elementAxes = None 
        self.scaleBar = None

        self._style.AddObserver("SelectionChangedEvent", self.highlight)
        self._style.AddObserver("SelectionChangedEvent", self.updateInfoText)
        self._style.AddObserver("SelectionChangedEvent", self.showElementAxes)

        self.updateHud()

    def updateHud(self):
        self._createScaleBar()
        self.add_openpulse_logo()
   
    def getBounds(self):
        if self._plotFilter.tubes:
            return self.opvTubes._actor.GetBounds()
        return ()

    def plot(self):
        self.reset()

        self.opvNodes = NodesActor(self.project)
        self.opvLines = LinesActor(self.project)
        self.opvTubes = TubeActor(self.project, self.opv)

        self.opvAcousticNodesSymbols = AcousticNodesSymbolsActor(self.project)
        self.opvAcousticElementsSymbols = AcousticElementsSymbolsActor(self.project)
        self.opvStructuralNodesSymbols = StructuralNodesSymbolsActor(self.project)
        self.opvStructuralElementsSymbols = StructuralElementsSymbolsActor(self.project)

        self.opvNodes.build()
        self.opvLines.build()
        self.opvTubes.build()
        self.buildSymbols()

        self.saveNodesBounds()
        self.saveElementsBounds()
        self.saveLineToElements()
        self.saveRawLinesData()
        
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvNodes)
        plt(self.opvLines)
        plt(self.opvTubes)
        plt(self.opvAcousticNodesSymbols)
        plt(self.opvAcousticElementsSymbols)
        plt(self.opvStructuralNodesSymbols)
        plt(self.opvStructuralElementsSymbols)

        self.updateColors()
        self.updateHud()
        self._style.set_default_center_of_rotation(self.project.preprocessor.camera_rotation_center)
        self._renderer.ResetCameraClippingRange()

        # update plot filter according to previous configuration
        self.setPlotFilter(self._plotFilter)

    def buildSymbols(self):
        self.opvAcousticNodesSymbols.build()
        self.opvAcousticElementsSymbols.build()
        self.opvStructuralNodesSymbols.build()
        self.opvStructuralElementsSymbols.build()
    
    def hide_selection(self):
        if self.selectionToNodes():
            self.hide_nodes(self.getListPickedPoints())

        if self.selectionToLines():
            lines = self.getListPickedLines()
            if self.opv.change_plot_to_entities_with_cross_section:
                _elements = [element_id for line_id in lines for element_id in self.preprocessor.line_to_elements[line_id]]
                self.hide_elements(_elements)  
            self.hide_lines(lines)

        if self.selectionToElements():
            self.hide_elements(self.getListPickedElements())

        self.clearSelection()
        self.update()

    def unhide_all(self):
        self.unhide_nodes()
        self.unhide_lines()
        self.unhide_elements()
        self.opvTubes.build()
        self.opvLines.build()
        self.opvNodes.build()
        self.clearSelection()
        self.update()

    def hide_nodes(self, nodes, _update_Renderer=False):
        self.hidden_nodes |= set(nodes)
        self.opvNodes.hidden_nodes = self.hidden_nodes
        self.opvNodes.build()
        
        if _update_Renderer:
            self.clearSelection()
            self.update()

    def hide_lines(self, lines, _update_Renderer=False):
        self.hidden_lines |= set(lines)
        for i in lines:
            el = set(self.lineToElements[i])
            self.hidden_elements |= el

        self.opvLines.hidden_elements = self.hidden_elements
        # self.opvTubes.hidden_elements = self.hidden_elements
        self.opvLines.build()
        # self.opvTubes.build()        
        
        if _update_Renderer:
            self.clearSelection()
            self.update()

    def hide_elements(self, elements, _update_Renderer=False):
        self.hidden_elements |= set(elements)
        # self.opvLines.hidden_elements = self.hidden_elements
        self.opvTubes.hidden_elements = self.hidden_elements

        # self.opvLines.build()
        self.opvTubes.build()

        if _update_Renderer:
            self.clearSelection()
            self.update()

    def hide_show_lines(self, _show):
        if _show:
            self.unhide_lines(_update_Renderer=True)
        else:
            picked_lines = self.getListPickedLines()
            picked_elements = self.getListPickedElements()
            if picked_lines:
                self.hide_lines(picked_lines, _update_Renderer=True)
            elif picked_elements:
                _lines = []
                for element_id in picked_elements:
                    line_id = self.preprocessor.elements_to_line[element_id]
                    if line_id not in _lines:
                        _lines.append(line_id)
                self.hide_lines(_lines, _update_Renderer=True)
            else:
                _lines = list(self.preprocessor.dict_tag_to_entity.keys())
                self.hide_lines(_lines, _update_Renderer=True)
            
    def hide_show_elements_and_nodes(self, _show):
        if _show:
            self.unhide_elements(_update_Renderer=True)
            self.unhide_nodes(_update_Renderer=True)
        else:
            picked_elements = self.getListPickedElements()
            picked_lines = self.getListPickedLines()
            if picked_elements:
                self.hide_elements(picked_elements, _update_Renderer=False)
            elif picked_lines:
                picked_elements = [element_id for line_id in picked_lines for element_id in self.preprocessor.line_to_elements[line_id]]
                self.hide_elements(picked_elements, _update_Renderer=False)
            else:
                _elements = list(self.preprocessor.structural_elements.keys())
                self.hide_elements(_elements, _update_Renderer=False)

            picked_nodes = self.getListPickedPoints()
            if picked_nodes:
                self.hide_nodes(picked_nodes, _update_Renderer=True)
            else:
                _nodes = list(self.preprocessor.nodes.keys())
                self.hide_nodes(_nodes, _update_Renderer=True)

    def hide_show_elements(self, _show):
        if _show:
            self.unhide_elements(_update_Renderer=True)
        else:
            picked_elements = self.getListPickedElements()
            picked_lines = self.getListPickedLines()
            if picked_elements:
                self.hide_elements(picked_elements, _update_Renderer=True)
            elif picked_lines:
                picked_elements = [element_id for line_id in picked_lines for element_id in self.preprocessor.line_to_elements[line_id]]
                self.hide_elements(picked_elements, _update_Renderer=True)
            else:
                _elements = list(self.preprocessor.structural_elements.keys())
                self.hide_elements(_elements, _update_Renderer=True)           

    def hide_show_nodes(self, _show):
        if _show:
            self.unhide_nodes(_update_Renderer=True)
        else:
            picked_nodes = self.getListPickedPoints()
            if picked_nodes:
                self.hide_nodes(picked_nodes, _update_Renderer=True)
            else:
                _nodes = list(self.preprocessor.nodes.keys())
                self.hide_nodes(_nodes, _update_Renderer=True)

    def hide_show_acoustic_symbols(self):
        # bitwise xor to toogle bit
        self._plotFilter.acoustic_symbols = not self._plotFilter.acoustic_symbols
        self.setPlotFilter( self._plotFilter )

    def hide_show_structural_symbols(self):
        # bitwise xor to toogle bit
        self._plotFilter.structural_symbols = not self._plotFilter.structural_symbols
        self.setPlotFilter( self._plotFilter )

    def unhide_nodes(self, nodes=None, _update_Renderer=False):
        if not nodes:
            self.hidden_nodes.clear()
        else:
            self.hidden_nodes -= set(nodes)
        if _update_Renderer:
            self.opvNodes.build()
            self.clearSelection()
            self.update()

    def unhide_lines(self, lines=None, _update_Renderer=False):
        if not lines:
            self.hidden_lines.clear()
            self.opvLines.hidden_elements.clear()
        else:
            self.hidden_lines -= set(lines)
        
        if _update_Renderer:
            self.opvLines.build()
            self.clearSelection()
            self.update()

    def unhide_elements(self, elements=None, _update_Renderer=False):
        if not elements:
            self.hidden_elements.clear()
        else:
            self.hidden_elements -= set(elements)
        if _update_Renderer:
            self.opvTubes.build()
            self.clearSelection()
            self.update()

    def setPlotFilter(self, plot_filter: PlotFilter):
        # As nodes, lines and tubes can be individually hidden
        # I am calling the same function instead of hidding the
        # actor itself. This way may avoid some bugs in other places. 

        if (plot_filter.nodes):
            self.unhide_nodes(_update_Renderer=True)
        else:
            _nodes = list(self.preprocessor.nodes.keys())
            self.hide_nodes(_nodes, _update_Renderer=True)

        if (plot_filter.lines):
            self.unhide_lines(_update_Renderer=True)
        else:
            _lines = list(self.preprocessor.dict_tag_to_entity.keys())
            self.hide_lines(_lines, _update_Renderer=True)

        if (plot_filter.tubes):
            self.unhide_elements(_update_Renderer=True)
        else:
            _elements = list(self.preprocessor.structural_elements.keys())
            self.hide_elements(_elements, _update_Renderer=True)           
        
        self.opvTubes.transparent = plot_filter.transparent
        self.buildSymbols()

        self.opvAcousticNodesSymbols.setVisibility(plot_filter.acoustic_symbols)
        self.opvAcousticElementsSymbols.setVisibility(plot_filter.acoustic_symbols)
        self.opvStructuralNodesSymbols.setVisibility(plot_filter.structural_symbols)
        self.opvStructuralElementsSymbols.setVisibility(plot_filter.structural_symbols)

        self._plotFilter = plot_filter
        self.update()

    def setSelectionFilter(self, selection_filter: SelectionFilter):
        self.clearSelection()
        self._selectionFilter = selection_filter
    
    def selectionToNodes(self):
        return self._selectionFilter.nodes
    
    def selectionToElements(self):
        return self._selectionFilter.elements 

    def selectionToLines(self):
        return self._selectionFilter.entities

    def clearSelection(self):
        self._style.clear()

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()
    
    def update(self):
        # TODO: check selection
        self.opv.updateDialogs()
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()

    # selection 
    def saveNodesBounds(self):
        self.nodesBounds.clear()
        for key, node in self.project.get_nodes().items():
            x,y,z = node.coordinates
            self.nodesBounds[key] = (x,x,y,y,z,z)

    def saveElementsBounds(self):
        self.elementsBounds.clear()
        for key, element in self.project.get_structural_elements().items():
            firstNode = element.first_node.coordinates
            lastNode = element.last_node.coordinates

            x0 = min(firstNode[0], lastNode[0])
            y0 = min(firstNode[1], lastNode[1])
            z0 = min(firstNode[2], lastNode[2])
            x1 = max(firstNode[0], lastNode[0])
            y1 = max(firstNode[1], lastNode[1])
            z1 = max(firstNode[2], lastNode[2])

            bounds = (x0,x1,y0,y1,z0,z1)
            self.elementsBounds[key] = bounds

    def saveLineToElements(self):
        # preprocessor = self.project.get_preprocess()
        self.lineToElements = self.preprocessor.line_to_elements
    
    def saveRawLinesData(self):
        pass

    def getListPickedPoints(self):
        if self.selectionToNodes():
            return self._style.getListPickedPoints()
        else:
            return []

    def getListPickedElements(self):
        if self.selectionToElements():
            return self._style.getListPickedElements()
        else:
            return []

    def getListPickedLines(self):
        if self.selectionToLines():
            return self._style.getListPickedLines()
        else:
            return []

    def updateColors(self):
        visual = [self.opvNodes, self.opvLines, self.opvTubes]
        if any([v is None for v in visual]):
            return
        
        self.opvNodes.setColor(self.nodes_color)
        self.opvLines.setColor(self.lines_color)
        self.opvTubes.setColor(self.surfaces_color)


    def call_update_in_QDialogs_if_highlighted(self):
        self.opv.updateDialogs()
        # renWin = self._renderer.GetRenderWindow()
        # if renWin: renWin.Render()    

    def highlight(self, obj, event):
        visual = [self.opvNodes, self.opvLines, self.opvTubes]
        if any([v is None for v in visual]):
            return

        selectedNodes = self.getListPickedPoints()
        selectedElements = self.getListPickedElements()
        selectedLines = self.getListPickedLines()
        
        self.updateColors()  # clear colors
        selectionColor = (255, 0, 0)
        _update = False

        if selectedNodes and self.selectionToNodes():
            self.opvNodes.setColor(selectionColor, keys=selectedNodes)
            _update = True

        if selectedElements and self.selectionToElements():
            self.opvLines.setColor(selectionColor, keys=selectedElements)
            self.opvTubes.setColor(selectionColor, keys=selectedElements)
            _update = True

        if selectedLines and self.selectionToLines():
            elementsFromLines = set()
            for i in selectedLines:
                elements = self.lineToElements[i]
                elementsFromLines = elementsFromLines.union(elements)

            self.opvLines.setColor(selectionColor, keys=elementsFromLines)
            self.opvTubes.setColor(selectionColor, keys=elementsFromLines)
            _update = True

        if _update:
            self.call_update_in_QDialogs_if_highlighted()

    def highlight_lines(self, line_ids, reset_colors=True, color=(255,0,0)):
        if reset_colors:
            self.updateColors()  # clear colors
        selectionColor = color
        elementsFromEntities = set()

        for line_id in line_ids:
            elements = self.lineToElements[line_id]
            elementsFromEntities = elementsFromEntities.union(elements)
        
        self.opvLines.setColor(selectionColor, keys=elementsFromEntities)
        self.opvTubes.setColor(selectionColor, keys=elementsFromEntities)
        self.update()

    def highlight_elements(self, element_ids, reset_colors=True, color=(255,0,0)):
        if reset_colors:
            self.updateColors()  # clear colors
        selectionColor = color

        self.opvLines.setColor(selectionColor, keys=element_ids)
        self.opvTubes.setColor(selectionColor, keys=element_ids)
        self.update()

    def highlight_nodes(self, node_ids, reset_colors=True, color=(255,0,0)):
        if reset_colors:
            self.updateColors()  # clear colors
        selectionColor = color

        self.opvNodes.setColor(selectionColor, keys=node_ids)

    def showElementAxes(self, obj, event):
        self._renderer.RemoveActor(self.elementAxes)
        self.update()

        ids = self.getListPickedElements()

        if not self.selectionToElements():
            return 
        
        if len(ids) != 1:
            return 

        element = self.project.get_structural_elements()[ids[0]]
        xyz = element.element_center_coordinates
        r_xyz = element.section_rotation_xyz_undeformed
        length = element.length
        size = [length, length, length]

        transform = vtk.vtkTransform()
        transform.Translate(xyz)
        transform.RotateZ(r_xyz[2])
        transform.RotateX(r_xyz[0])
        transform.RotateY(r_xyz[1])
        transform.Scale(size)

        self.elementAxes = vtk.vtkAxesActor()
        self.elementAxes.AxisLabelsOff()
        self.elementAxes.SetUserTransform(transform)
        self.elementAxes.SetShaftTypeToCylinder()

        self._renderer.AddActor(self.elementAxes)
        self.update()

    def getPlotRadius(self, *args, **kwargs):
        return 
    
    def changeColorEntities(self, *args, **kwargs):
        return 

    def setPlotRadius(self, *args, **kwargs):
        pass

    def updateInfoText(self, obj, event):
        text = ""
        if self.selectionToNodes() and self.getListPickedPoints():
            text += self.model_info_text.get_nodes_info_text() + "\n"

        if self.selectionToElements() and self.getListPickedElements():
            text += self.model_info_text.get_elements_info_text() + "\n"

        if self.selectionToLines() and self.getListPickedLines():
            text += self.model_info_text.get_entities_info_text()  + "\n"

        self.createInfoText(text)
        self.update()