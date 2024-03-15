import vtk
import numpy as np 
from time import time
from dataclasses import dataclass

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

        self.project = project
        self.preprocessor = project.preprocessor
        self.opv = opv

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

        self._style.AddObserver('SelectionChangedEvent', self.highlight)
        self._style.AddObserver('SelectionChangedEvent', self.updateInfoText)
        self._style.AddObserver('SelectionChangedEvent', self.showElementAxes)

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
        # self.opv.updateDialogs()
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
        
        # self.opv.parent.update_toolbar_radioButtons(selectedNodes, selectedElements, selectedLines)
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
        text = ''
        if self.selectionToNodes() and self.getListPickedPoints():
            text += self.getNodesInfoText() + '\n'

        if self.selectionToElements() and self.getListPickedElements():
            text += self.getElementsInfoText() + '\n'
        
        if self.selectionToLines() and self.getListPickedLines():
            text += self.getEntityInfoText()  + '\n'
            
        self.createInfoText(text)
        self.update()

    def getNodesInfoText(self):
        listSelected = self.getListPickedPoints()
        text = ''
        if len(listSelected) == 1:
            node = self.project.get_node(listSelected[0])
            nodeId = listSelected[0]
            nodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(node.x, node.y, node.z)
            text = f'NODE ID: {nodeId} \n   Position: ({nodePosition}) [m]\n'

            if node in self.preprocessor.nodes_with_prescribed_dofs:
                values = node.prescribed_dofs
                labels = np.array(['ux', 'uy', 'uz', 'rx', 'ry', 'rz'])
                unit_labels = ['m', 'rad']
                text += self.structuralNodalInfo(values, labels, 'PRESCRIBED DOFs', unit_labels, node.loaded_table_for_prescribed_dofs)

            if node in self.preprocessor.nodes_with_nodal_loads:
                values = node.nodal_loads
                labels = np.array(['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
                unit_labels = ['N', 'N.m']
                text += self.structuralNodalInfo(values, labels, 'NODAL LOADS', unit_labels, node.loaded_table_for_nodal_loads)

            if node in self.preprocessor.nodes_connected_to_springs:
                values = node.lumped_stiffness
                labels = np.array(['kx', 'ky', 'kz', 'krx', 'kry', 'krz'])
                unit_labels = ['N/m', 'N.m/rad']
                text += self.structuralNodalInfo(values, labels, 'LUMPED STIFFNESS', unit_labels, node.loaded_table_for_lumped_stiffness)

            if node in self.preprocessor.nodes_connected_to_dampers:
                values = node.lumped_dampings
                labels = np.array(['cx', 'cy', 'cz', 'crx', 'cry', 'crz'])
                unit_labels = ['N.s/m', 'N.m.s/rad']
                text += self.structuralNodalInfo(values, labels, 'LUMPED DAMPINGS', unit_labels, node.loaded_table_for_lumped_dampings)

            if node in self.preprocessor.nodes_with_masses:
                values = node.lumped_masses
                labels = np.array(['mx', 'my', 'mz', 'Jx', 'Jy', 'Jz'])
                unit_labels = ['kg', 'N.m²']
                text += self.structuralNodalInfo(values, labels, 'LUMPED MASSES', unit_labels, node.loaded_table_for_lumped_masses)

            if node.there_are_elastic_nodal_link_stiffness:
                index = node.external_index
                labels = np.array(['kx', 'ky', 'kz', 'krx', 'kry', 'krz'])
                unit_labels = ['N/m', 'N.m/rad']
                for key, [_, values] in node.elastic_nodal_link_stiffness.items():
                    linked_nodes = [int(node_id) for node_id in key.split('-')]
                    if index in linked_nodes:            
                        text += self.structuralNodalInfo(values, labels, f'STIFFNESS ELASTIC LINK: [{key}]', unit_labels, node.loaded_table_for_elastic_link_stiffness)

            if node.there_are_elastic_nodal_link_dampings:
                index = node.external_index
                labels = np.array(['cx', 'cy', 'cz', 'crx', 'cry', 'crz'])
                unit_labels = ['N.s/m', 'N.m.s/rad']
                for key, [_, values] in node.elastic_nodal_link_dampings.items():
                    linked_nodes = [int(node_id) for node_id in key.split('-')]
                    if index in linked_nodes:            
                        text += self.structuralNodalInfo(values, labels, f'DAMPING ELASTIC LINK: [{key}]', unit_labels, node.loaded_table_for_elastic_link_dampings)
 
            if node in self.preprocessor.nodes_with_acoustic_pressure:
                value = node.acoustic_pressure
                label = 'P'
                unit_label = '[Pa]'
                text += self.acousticNodalInfo(value, label, 'ACOUSTIC PRESSURE', unit_label)
   
            if node in self.preprocessor.nodes_with_volume_velocity:
                value = node.volume_velocity
                label = 'Q'
                unit_label = '[m³/s]'
                text += self.acousticNodalInfo(value, label, 'VOLUME VELOCITY', unit_label)

            if node in self.preprocessor.nodes_with_compressor_excitation:
                value = node.volume_velocity
                label = 'Q'
                unit_label = '[m³/s]'

                values_connection_info = list(node.dict_index_to_compressor_connection_info.values())         
                if len(values_connection_info) == 1:
                    connection_type = f'  Connection type: {values_connection_info[0]} \n'
                else:
                    if 'discharge' in values_connection_info and 'suction' in values_connection_info:
                        connection_type = f"  Connections types: discharge ({values_connection_info.count('discharge')}x) & "
                        connection_type += f"suction ({values_connection_info.count('suction')}x) \n"
                    elif 'discharge' in values_connection_info:
                        connection_type = f"  Connections types: discharge ({values_connection_info.count('discharge')}x) \n"
                    elif 'suction' in values_connection_info:
                        connection_type = f"  Connections types: suction ({values_connection_info.count('suction')}x) \n"    
                        
                bc_label = 'VOLUME VELOCITY - COMPRESSOR EXCITATION'
                text += self.acousticNodalInfo(value, label, bc_label, unit_label, aditional_info=connection_type)
            
            if node in self.preprocessor.nodes_with_specific_impedance:
                value = node.specific_impedance
                label = 'Zs'
                unit_label = '[kg/m².s]'
                text += self.acousticNodalInfo(value, label, 'SPECIFIC IMPEDANCE', unit_label)

            if node in self.preprocessor.nodes_with_radiation_impedance:
                Z_type = node.radiation_impedance_type
                _dict = {0:'anechoic termination', 1:'unflanged pipe', 2:'flanged pipe'}
                label = 'Type'
                value = _dict[Z_type]
                unit_label = ''
                text += self.acousticNodalInfo(value, label, 'RADIATION IMPEDANCE', unit_label)

        elif len(listSelected) > 1:
            text += f'{len(listSelected)} NODES IN SELECTION: \n'
            for i, ids in enumerate(listSelected):
                if i == 30:
                    text += '...'
                    break
                text += f'{ids} '
                if i ==10 or i==20:
                    text += '\n'
            text += '\n'
        return text

    def structuralNodalInfo(self, values, labels, bc_label, unit_labels, isThereTable):
        mask = [True if value is not None else False for value in values]
        indexes = np.arange(6)
        masked_labels = labels[mask]
        masked_indexes = indexes[mask]
        text = f'\n{bc_label}: \n'

        for index, label  in enumerate(masked_labels):
            if isThereTable:
                value = 'Table'
                unit = ''
            else:
                value = values[masked_indexes[index]]
                if masked_indexes[index] in [0,1,2]:
                    unit = f'[{unit_labels[0]}]'
                else:
                    unit = f'[{unit_labels[1]}]'
            text += f'  {label} = {value} {unit} \n'

        return text

    def acousticNodalInfo(self, value, label, bc_label, unit_label, aditional_info=None):
        text = f'\n{bc_label}: \n'
        if aditional_info is not None:
            text += aditional_info
        if isinstance(value, np.ndarray):
            text += f'  {label} = Table of values \n'
        else:
            unit = f'{unit_label}'
            text += f'  {label} = {value} {unit} \n'

        return text

    def getElementsInfoText(self):
        listSelected = self.getListPickedElements()
        text = ''

        if len(listSelected) == 1:

            structural_element = self.project.get_structural_element(listSelected[0])
            acoustic_element = self.project.get_acoustic_element(listSelected[0])

            firstNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.first_node.x, 
                                                                structural_element.first_node.y, 
                                                                structural_element.first_node.z)
            lastNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.last_node.x, 
                                                                structural_element.last_node.y, 
                                                                structural_element.last_node.z)

            structural_element_type = structural_element.element_type
            acoustic_element_type = acoustic_element.element_type

            material = structural_element.material
            # fluid = structural_element.fluid
            fluid = acoustic_element.fluid
            
            if structural_element_type is None:
                structural_element_type = "undefined"

            if acoustic_element_type is None:
                acoustic_element_type = "undefined"

            if material is None:
                material_name = 'undefined'
            else:
                material_name = material.name

            if fluid is None:
                fluid_name = 'undefined'
            else:
                fluid_name = fluid.name
                fluid_temperature = fluid.temperature
                fluid_pressure = fluid.pressure

            if structural_element.cross_section is None: 
                outer_diameter = 'undefined'
                thickness = 'undefined'
                offset_y = 'undefined'
                offset_z = 'undefined'
                insulation_thickness = 'undefined'
                insulation_density = 'undefined'
            else:
                if structural_element.cross_section is not None:                 
                    if structural_element.element_type == "pipe_1":
                        outer_diameter = structural_element.cross_section.outer_diameter
                        thickness = structural_element.cross_section.thickness
                        offset_y = structural_element.cross_section.offset_y
                        offset_z = structural_element.cross_section.offset_z
                        insulation_thickness = structural_element.cross_section.insulation_thickness
                        insulation_density = structural_element.cross_section.insulation_density
                        structural_element_type = structural_element.element_type
                    
                    elif structural_element.element_type == "beam_1":
                        area = structural_element.cross_section.area
                        Iyy = structural_element.cross_section.second_moment_area_y
                        Izz = structural_element.cross_section.second_moment_area_z
                        Iyz = structural_element.cross_section.second_moment_area_yz
                        section_label = structural_element.cross_section.section_label
                        xaxis_rotation = structural_element.xaxis_beam_rotation

                        structural_element_type = f"{structural_element.element_type} ({section_label.capitalize()})"               

                    elif structural_element_type == "expansion_joint":
                        effective_diameter = structural_element.cross_section.outer_diameter

            # rotations = structural_element.section_rotation_xyz_undeformed
            # str_rotations = '{:.3f}, {:.3f}, {:.3f}'.format(rotations[0], rotations[1], rotations[2])

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {structural_element.first_node.external_index} -- Coordinates: ({firstNodePosition}) [m]\n'
            text += f'Last Node ID: {structural_element.last_node.external_index} -- Coordinates: ({lastNodePosition}) [m]\n\n'
            # text += f'Rotations xyz: ({str_rotations})[deg]\n\n'
            text += f'Material: {material_name} \n'
            text += f'Strutural element type: {structural_element_type} \n\n'
            
            if "pipe_" in structural_element_type:        
                text += f'Diameter: {outer_diameter} [m]\n'
                text += f'Thickness: {thickness} [m]\n'
                if offset_y != 0 or offset_z != 0:
                    text += f'Offset y: {offset_y} [m]\n'
                    text += f'Offset z: {offset_z} [m]\n'
                if insulation_thickness != 0 or insulation_density != 0:
                    text += f'Insulation thickness: {insulation_thickness} [m]\n'
                    text += f'Insulation density: {insulation_density} [kg/m³]\n'

                if acoustic_element.fluid is not None:
                    text += f'\nFluid: {fluid_name} \n'
                    if fluid_temperature is not None:
                        text += f'\nTemperature: {fluid_temperature} [K]'
                    if fluid_pressure is not None:
                        text += f'\nPressure: {fluid_pressure} [Pa] \n' 

                if acoustic_element.element_type is not None:
                    text += f'Acoustic element type: {acoustic_element_type} \n'
                    if acoustic_element.element_type in ["undamped mean flow", "peters", "howe"]:
                        if acoustic_element.vol_flow:
                            text += f'Volume flow rate: {acoustic_element.vol_flow} [m³/s]\n'
                    elif acoustic_element.element_type in ["proportional"]:
                        if acoustic_element.proportional_damping:
                            text += f'Proportional damping: {acoustic_element.proportional_damping}\n'   
         
            elif "beam_1" in structural_element_type:
                text += f'Area:  {area} [m²]\n'
                text += f'Iyy:  {Iyy} [m^4]\n'
                text += f'Izz:  {Izz} [m^4]\n'
                text += f'Iyz:  {Iyz} [m^4]\n'
                text += f'x-axis rotation: {xaxis_rotation} [deg]\n'

            elif structural_element_type == "expansion_joint":
                text += f'Effective diameter: {effective_diameter} [m]\n'
            
        elif len(listSelected) > 1:
            text += f'{len(listSelected)} ELEMENTS IN SELECTION: \n'
            for i, ids in enumerate(listSelected):
                if i == 30:
                    text += '...'
                    break
                text += f'{ids} '
                if i ==10 or i==20:
                    text += '\n'
        return text

    def getEntityInfoText(self):
        line_ids = self.getListPickedLines()
        text = ''
        if len(line_ids) == 0: 
            return

        elif len(line_ids) == 1:

            entity = self.project.get_entity(line_ids[0])
            
            material = entity.material
            fluid = entity.fluid
            structural_element_type = entity.structural_element_type
            acoustic_element_type = entity.acoustic_element_type

            if material is None:
                material_name = 'undefined'    
            else:
                material_name = material.name

            if fluid is None:
                fluid_name = 'undefined'    
            else:
                fluid_name = fluid.name
                fluid_temperature = fluid.temperature
                fluid_pressure = fluid.pressure

            if entity.structural_element_type is None:
                structural_element_type = 'undefined'

            if entity.cross_section is None:
                outer_diameter = 'undefined'
                thickness = 'undefined'
                offset_y = 'undefined'
                offset_z = 'undefined'
                insulation_thickness = 'undefined'
                insulation_density = 'undefined'
  
            if entity.tag in self.project.number_sections_by_line.keys():

                number_cross_sections = self.project.number_sections_by_line[entity.tag]
                text = f'Line ID  {line_ids[0]}\n'
                text += f'Number of cross-sections: {number_cross_sections}\n'
                if entity.tag in self.preprocessor.number_expansion_joints_by_lines.keys():
                    number_expansion_joints = self.preprocessor.number_expansion_joints_by_lines[entity.tag]
                    # text = f'Line ID  {line_ids[0]} ({number_cross_sections} cross-sections & {number_expansion_joints} expansion joints)\n\n'
                    text += f'Number of expansion joints: {number_expansion_joints}\n'
                if entity.tag in self.preprocessor.number_valves_by_lines.keys():
                    number_valves = self.preprocessor.number_valves_by_lines[entity.tag]
                    text += f'Number of valves: {number_valves}\n'
                # else:
                #     text = f'Line ID  {line_ids[0]} ({number_cross_sections} cross-sections)\n\n'              
                text += f'\nMaterial:  {material_name}\n'

                if structural_element_type in ['pipe_1', 'valve']:
                
                    outer_diameter = 'multiples'
                    thickness = 'multiples'
                    offset_y = 'multiples'
                    offset_z = 'multiples'
                    insulation_thickness = 'multiples'
                    insulation_density = 'multiples'

                    text += f'Structural element type:  {structural_element_type}\n'
              
                if entity.fluid is not None:
                    text += f'\nFluid: {fluid_name}' 
                    if fluid_temperature is not None:
                        text += f'\nTemperature: {fluid_temperature} [K]'
                    if fluid_pressure is not None:
                        text += f'\nPressure: {fluid_pressure} [Pa] \n' 

                if entity.acoustic_element_type is not None:
                    text += f'\nAcoustic element type: {acoustic_element_type}'
                if entity.acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                    if entity.vol_flow:
                        text += f'\nVolume flow rate: {entity.vol_flow} [m³/s]'
                elif entity.acoustic_element_type in ["proportional"]:
                    if entity.proportional_damping:
                        text += f'\nProportional damping: {entity.proportional_damping}'        
               
            else:

                text = ''
                text += f'Line ID  {line_ids[0]}\n\n'
                
                if entity.material is not None:
                    text += f'Material:  {entity.material.name}\n'

                if entity.cross_section is not None:
                    if entity.structural_element_type == 'beam_1':

                        area = entity.cross_section.area
                        Iyy = entity.cross_section.second_moment_area_y
                        Izz = entity.cross_section.second_moment_area_z
                        Iyz = entity.cross_section.second_moment_area_yz
                        section_label = entity.getCrossSection().section_label
                        xaxis_rotation = entity.xaxis_beam_rotation

                        text += f'Structural element type:  {structural_element_type} '
                        text += f'({section_label.capitalize()})\n\n'

                        text += f'Area:  {area} [m²]\n'
                        text += f'Iyy:  {Iyy} [m^4]\n'
                        text += f'Izz:  {Izz} [m^4]\n'
                        text += f'Iyz:  {Iyz} [m^4]\n'
                        text += f'x-axis rotation: {xaxis_rotation} [deg]\n'

                    elif entity.structural_element_type in ['pipe_1', 'valve']:

                        text += f'Structural element type:  {structural_element_type}\n\n'
                        
                        outer_diameter = entity.cross_section.outer_diameter
                        thickness = entity.cross_section.thickness
                        offset_y = entity.cross_section.offset_y
                        offset_z = entity.cross_section.offset_z
                        insulation_thickness = entity.cross_section.insulation_thickness
                        insulation_density = entity.cross_section.insulation_density
                                            
                        text += f'Outer diameter:  {outer_diameter} [m]\n'
                        text += f'Thickness:  {thickness} [m]\n'
                        if offset_y != 0 or offset_z != 0:
                            text += f'Offset y: {offset_y} [m]\nOffset z: {offset_z} [m]\n'
                        if insulation_thickness != 0 or insulation_density != 0: 
                            text += f'Insulation thickness: {insulation_thickness} [m]\n'
                            text += f'Insulation density: {int(insulation_density)} [kg/m³]\n'
                                                                           
                        if entity.fluid is not None:
                            text += f'\nFluid: {entity.fluid.name}' 
                            if fluid_temperature is not None:
                                text += f'\nTemperature: {fluid_temperature} [K]'
                            if fluid_pressure is not None:
                                text += f'\nPressure: {fluid_pressure} [Pa] \n' 

                        if entity.acoustic_element_type is not None:
                            text += f'\nAcoustic element type: {entity.acoustic_element_type}'

                        if entity.acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                            if entity.vol_flow:
                                text += f'\nVolume flow rate: {entity.vol_flow} [m³/s]'
                        elif entity.acoustic_element_type in ["proportional"]:
                            if entity.proportional_damping:
                                text += f'\nProportional damping: {entity.proportional_damping}' 
                
                if entity.expansion_joint_parameters is not None:
                    if entity.structural_element_type == 'expansion_joint':
                        effective_diameter = entity.expansion_joint_parameters[0][1]
                        text += f'Structural element type:  {structural_element_type}\n\n'
                        text += f'Effective diameter:  {effective_diameter} [m]\n\n'

        else:

            text = f'{len(line_ids)} lines in selection:\n\n'
            i = 0
            for ids in line_ids:
                if i == 30:
                    text += '...'

                    break
                elif i == 19: 
                    text += f'{ids}\n'
                elif i == 9:
                    text += f'{ids}\n'
                else:
                    text += f'{ids}  '
                i+=1
                
        return text