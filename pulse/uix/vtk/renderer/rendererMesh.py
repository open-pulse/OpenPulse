from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.vtkSymbols import vtkSymbols

from pulse.interface.tubeActor import TubeActor
from pulse.interface.nodesActor import NodesActor
from pulse.interface.linesActor import LinesActor



from time import time 

import vtk
import numpy as np 

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))
        self.project = project
        self.opv = opv 
        self.symbols = vtkSymbols(self.project)     
        
        self.nodesBounds = dict() # (x,y,z) coordinates
        self.elementsBounds = dict() # bounding coordinates
        self.axes = dict()
        self.elasticLinks = dict()
        self.elementAxe = []
        self.actorNodesList = []

        self.selectionNodesActor = None
        self.selectionNodesActorAcoustic = None
        self.selectionElementsActor = None
        self.selectionTubeActor = None
        self.defaultRadius = None
        
        self._style.AddObserver('SelectionChangedEvent', self.highlight)
    
    def highlight(self, obj, event):
        # selectedNodes = [self.project.get_node(i) for i in self.getListPickedPoints()]
        # selectedElements = [self.project.get_structural_element(i) for i in self.getListPickedElements()]
        selectedNodes = [self.project.preprocessor.nodes[i] for i in self.getListPickedPoints()]
        selectedElements = [self.project.preprocessor.structural_elements[i] for i in self.getListPickedElements()]

        self._renderer.RemoveActor(self.selectionNodesActor)
        self._renderer.RemoveActor(self.selectionNodesActorAcoustic)
        self._renderer.RemoveActor(self.selectionElementsActor)
        self._renderer.RemoveActor(self.selectionTubeActor)
        
        if selectedNodes:
            selectedNodesAcoustic = []
            volume_velocity = self.project.preprocessor.nodes_with_volume_velocity #Vermelha
            acoustic_pressure = self.project.preprocessor.nodes_with_acoustic_pressure #Branca
            specific_impedance = self.project.preprocessor.nodes_with_specific_impedance #Verde
            radiation_impedance = self.project.preprocessor.nodes_with_radiation_impedance #Rosa
            #Remove nodes with volume velocity from nodes[]
            for node in volume_velocity:
                if node in selectedNodes:
                    selectedNodesAcoustic.append(node)
                    selectedNodes.remove(node)
            #Remove nodes with acoustic_pressure from nodes[]
            for node in acoustic_pressure:
                if node in selectedNodes:
                    selectedNodesAcoustic.append(node)
                    selectedNodes.remove(node)
            #Remove nodes with specific_impedance from nodes[]
            for node in specific_impedance:
                if node in selectedNodes:
                    selectedNodesAcoustic.append(node)
                    selectedNodes.remove(node)
            #Remove nodes with specific_impedance from nodes[]
            for node in radiation_impedance:
                if node in selectedNodes:
                    selectedNodesAcoustic.append(node)
                    selectedNodes.remove(node)
            #Shame on you

            source = vtk.vtkCubeSource()
            source.SetXLength(3)
            source.SetYLength(3)
            source.SetZLength(3)
            self.selectionNodesActor = self.createActorNodes(selectedNodes,source)
            self.selectionNodesActor.GetProperty().SetColor(255,0,0)
            self._renderer.AddActor(self.selectionNodesActor)   
            
            source = vtk.vtkSphereSource()
            source.SetRadius(3)
            self.selectionNodesActorAcoustic = self.createActorNodes(selectedNodesAcoustic,source)
            self.selectionNodesActorAcoustic.GetProperty().SetColor(255,0,0)
            self._renderer.AddActor(self.selectionNodesActorAcoustic)    
        
        if selectedElements:
            self.selectionElementsActor = self.createActorElements(selectedElements)
            self.selectionElementsActor.GetProperty().SetLineWidth(5)
            self.selectionElementsActor.GetProperty().SetColor(1,0,0)
            self._renderer.AddActor(self.selectionElementsActor)

            self.selectionTubeActor = self.createActorTubes(selectedElements)
            self.selectionTubeActor.GetProperty().SetColor(1,0,0)
            self.selectionTubeActor.GetProperty().SetOpacity(0.3)
            self._renderer.AddActor(self.selectionTubeActor)        

        self.updateInfoText()
        self.plotElementAxes()
        self.update()
        renWin = self._renderer.GetRenderWindow()
        if renWin:
            renWin.Render()
        
    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()
    
    def getListPickedPoints(self):
        return self._style.getListPickedPoints()

    def getListPickedElements(self):
        return self._style.getListPickedElements()

    def plot(self):
        self.reset()
        self.saveNodesBounds()
        self.saveElementsBounds()
        self.updateAllAxes()
        self.plotNodes()
        self.plotElements()
        self.plotTubes()
    
    def plotTeste(self):
        start_time = time()

        elements = self.project.get_structural_elements().values()
        tube = TubeActor(elements, self.project)
        tube.build()
        tube.getActor().GetProperty().SetOpacity(0.05)
        self._renderer.AddActor(tube.getActor())

        lines = LinesActor(elements, self.project)
        lines.build()
        lines.getActor().GetProperty().SetColor((0.8, 0.2, 1))
        self._renderer.AddActor(lines.getActor())

        nodes = self.project.get_nodes().values()
        nodesActor = NodesActor(nodes, self.project)
        nodesActor.build()
        nodesActor.getActor().GetProperty().SetColor((1, 1, 0.2))
        self._renderer.AddActor(nodesActor.getActor())

        end_time = time()
        print('time to plot', end_time - start_time)
    
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

    def removeActorNodes(self):
        for i in self.actorNodesList:
            self._renderer.RemoveActor(i)
        self.actorNodesList = []

    def plotNodes(self):
        self.removeActorNodes()
        nodes = list(self.project.get_nodes().values())
        volume_velocity = self.project.preprocessor.nodes_with_volume_velocity #Vermelha
        acoustic_pressure = self.project.preprocessor.nodes_with_acoustic_pressure #Branca
        specific_impedance = self.project.preprocessor.nodes_with_specific_impedance #Verde
        radiation_impedance = self.project.preprocessor.nodes_with_radiation_impedance #Rosa
        #Remove nodes with volume velocity from nodes[]
        for node in volume_velocity:
            if node in nodes:
                nodes.remove(node)
        #Remove nodes with acoustic_pressure from nodes[]
        for node in acoustic_pressure:
            if node in nodes:
                nodes.remove(node)
        #Remove nodes with specific_impedance from nodes[]
        for node in specific_impedance:
            if node in nodes:
                nodes.remove(node)
        #Remove nodes with specific_impedance from nodes[]
        for node in radiation_impedance:
            if node in nodes:
                nodes.remove(node)

        source = vtk.vtkCubeSource()
        source.SetXLength(2)
        source.SetYLength(2)
        source.SetZLength(2)
        actor = self.createActorNodes(nodes,source)
        actor.GetProperty().SetColor(1,1,0)
        actor.GetProperty().BackfaceCullingOff()
        actor.GetProperty().ShadingOff()
        self.actorNodesList.append(actor)
        self._renderer.AddActor(actor)

        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(4)
        cube_source.SetYLength(4)
        cube_source.SetZLength(4)

        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(3)
        actor = self.createActorNodes(volume_velocity,sphere_source)
        actor.GetProperty().SetColor(1,0.2,0.2)
        self.actorNodesList.append(actor)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(acoustic_pressure,sphere_source)
        actor.GetProperty().SetColor(1,1,1)
        self.actorNodesList.append(actor)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(specific_impedance,cube_source)
        actor.GetProperty().SetColor(1,0.07,0.57)
        self.actorNodesList.append(actor)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(radiation_impedance,cube_source)
        actor.GetProperty().SetColor(0,1,0)
        self.actorNodesList.append(actor)
        self._renderer.AddActor(actor)

    
    def plotElements(self):
        elements = self.project.get_structural_elements().values()
        actor = self.createActorElements(elements)
        actor.GetProperty().SetLineWidth(2)
        self._renderer.AddActor(actor)
    
    def plotTubes(self):
        elements = self.project.get_structural_elements().values()
        actor = self.createActorTubes(elements)

        actor.GetProperty().SetColor(0.7,0.7,0.8)
        actor.GetProperty().SetOpacity(0.06)

        actor.GetProperty().SetOpacity(0.06)
        actor.GetProperty().VertexVisibilityOn()
        actor.GetProperty().SetLineWidth(2)

        actor.GetProperty().BackfaceCullingOff()
        actor.GetProperty().ShadingOff()
        actor.GetProperty().LightingOff()
        self._renderer.AddActor(actor)

    def plotElementAxes(self):
        listSelected = self.getListPickedElements()
        for i in self.elementAxe:
            self._renderer.RemoveActor(i)
        if len(listSelected) == 1:
            arrows = self.symbols.getElementAxe(self.project.get_structural_element(listSelected[0]))
            self.elementAxe = arrows
            for i in self.elementAxe:
                self._renderer.AddActor(i)

    def createActorNodes(self, nodes, source):
        points = vtk.vtkPoints()
        data = vtk.vtkPolyData()
        cameraDistance = vtk.vtkDistanceToCamera()
        glyph = vtk.vtkGlyph3D()
        actor = vtk.vtkActor()
        mapper = vtk.vtkPolyDataMapper()

        for node in nodes:
            x,y,z = node.x, node.y, node.z
            points.InsertNextPoint(x,y,z)
        
        data.SetPoints(points)
        cameraDistance.SetInputData(data)
        cameraDistance.SetRenderer(self._renderer)
        cameraDistance.SetScreenSize(3)

        glyph.SetInputConnection(cameraDistance.GetOutputPort())
        glyph.SetSourceConnection(source.GetOutputPort())
        glyph.SetColorModeToColorByVector()
        glyph.SetVectorModeToUseNormal()
        glyph.SetInputArrayToProcess(0,0,0,0,'DistanceToCamera')

        mapper.SetInputConnection(glyph.GetOutputPort())  
        actor.SetMapper(mapper)
        return actor 
        
    def createActorElements(self, elements):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        for element in elements:
            points = vtk.vtkPoints()
            edges = vtk.vtkCellArray()
            line = vtk.vtkLine()
            obj = vtk.vtkPolyData()

            points.InsertPoint(0, *element.first_node.coordinates)
            points.InsertPoint(1, *element.last_node.coordinates)
            line.GetPointIds().SetId(0,0)
            line.GetPointIds().SetId(1,1)
            edges.InsertNextCell(line)

            obj.SetPoints(points)
            obj.SetLines(edges)
            source.AddInputData(obj)

        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        return actor
    
    def createActorTubes(self, elements):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        # _first = True

        for element in elements:
            cross_section = element.cross_section
            if cross_section:
                polygon = self.createSectionPolygon(element)    
            else: # not cross section
                if self.defaultRadius is None:
                    self.defaultRadius = element.length/20
                polygon = vtk.vtkRegularPolygonSource()
                polygon.SetRadius(self.defaultRadius)
                polygon.SetNumberOfSides(20)
            
            tube = self.generalSectionTube(element, polygon.GetOutputPort())
            source.AddInputData(tube.GetOutput())

        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        return actor

    def createSectionPolygon(self, element):

        outer_points, inner_points = element.cross_section.get_cross_section_points(element.length)
        number_inner_points = len(inner_points)
        number_outer_points = len(outer_points)

        # definitions
        points = vtk.vtkPoints()
        outerData = vtk.vtkPolyData()    
        innerPolygon = vtk.vtkPolygon()
        innerCell = vtk.vtkCellArray()
        innerData = vtk.vtkPolyData()
        delaunay = vtk.vtkDelaunay2D()
        
        outerPolygon = vtk.vtkPolygon()
        edges = vtk.vtkCellArray()
        data = vtk.vtkPolyData()
        source = vtk.vtkTriangleFilter()

        #TODO: create points - check the axis alignments - older version (0, y, z)
        for y, z in inner_points:
            points.InsertNextPoint(y, z, 0)

        for y, z in outer_points:
            points.InsertNextPoint(y, z, 0)

        # create external polygon
        outerData.SetPoints(points)
        delaunay.SetInputData(outerData)

        if number_inner_points >= 3:
            # remove inner area for holed sections
            for i in range(number_inner_points):
                innerPolygon.GetPointIds().InsertNextId(i)

            innerCell.InsertNextCell(innerPolygon)
            innerData.SetPoints(points)
            innerData.SetPolys(innerCell) 
            delaunay.SetSourceData(innerData)
            delaunay.Update()

            return delaunay

        else:
            
            outerPolygon.GetPointIds().SetNumberOfIds(number_outer_points)
            for i in range(number_outer_points):
                outerPolygon.GetPointIds().SetId(i,i)
            edges.InsertNextCell(outerPolygon)
            
            data.SetPoints(points)
            data.SetPolys(edges)
            source.AddInputData(data)

            return source

    # def createSectionPolygon(self, element):
    #     outer_points, inner_points, number_points = self.project.get_preprocess().get_cross_section_points(element.index)
    #     points = vtk.vtkPoints()
    #     edges = vtk.vtkCellArray()
    #     data = vtk.vtkPolyData()
    #     poly = vtk.vtkPolygon()
    #     source = vtk.vtkTriangleFilter()

    #     for x, y in outer_points:
    #         points.InsertNextPoint(x, y, 0)    
       
    #     n = int(number_points/2)
    #     poly.GetPointIds().SetNumberOfIds(n)

    #     for i in range(n):
    #         poly.GetPointIds().SetId(i,i)
    #     edges.InsertNextCell(poly)
        
    #     data.SetPoints(points)
    #     data.SetPolys(edges)
    #     source.AddInputData(data)

    #     return source

    def generalSectionTube(self, element, section):
        start = element.first_node.coordinates
        size = element.length
 
        u, v, w = element.section_directional_vectors
        
        matrix = vtk.vtkMatrix4x4()
        matrix.Identity()
        for i in range(3):
            matrix.SetElement(i, 0, v[i])
            matrix.SetElement(i, 1, w[i])
            matrix.SetElement(i, 2, u[i])

        data = vtk.vtkTransformPolyDataFilter()
        extrusion = vtk.vtkLinearExtrusionFilter()
        transformation = vtk.vtkTransform()

        extrusion.SetScaleFactor(size)
        extrusion.SetInputConnection(section)
        transformation.Translate(start)
        transformation.Concatenate(matrix)

        data.SetTransform(transformation)
        data.SetInputConnection(extrusion.GetOutputPort())
        data.Update()
        return data

    def update(self):
        self.opv.update()
        # self.opv.updateDialogs()

    def updateInfoText(self):
        pointsText = self.getNodesInfoText()
        elementsText = self.getElementsInfoText()
        text = (pointsText + '\n\n' + elementsText) if pointsText else (elementsText)
        self.createInfoText(text)
    
    def getNodesInfoText(self):
        listSelected = self.getListPickedPoints()
        text = ''
        if len(listSelected) == 1:
            node = self.project.get_node(listSelected[0])
            nodeId = listSelected[0]
            nodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(node.x, node.y, node.z)
            text = f'NODE ID: {nodeId} \n   Position: ({nodePosition}) [m]\n'

            if node in self.project.preprocessor.nodes_with_prescribed_dofs:
                values = node.prescribed_dofs
                labels = np.array(['ux', 'uy', 'uz', 'rx', 'ry', 'rz'])
                unit_labels = ['m', 'rad']
                text += self.structuralNodalInfo(values, labels, 'PRESCRIBED DOFs', unit_labels, node.loaded_table_for_prescribed_dofs)

            if node in self.project.preprocessor.nodes_with_nodal_loads:
                values = node.nodal_loads
                labels = np.array(['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
                unit_labels = ['N', 'N.m']
                text += self.structuralNodalInfo(values, labels, 'NODAL LOADS', unit_labels, node.loaded_table_for_nodal_loads)

            if node in self.project.preprocessor.nodes_connected_to_springs:
                values = node.lumped_stiffness
                labels = np.array(['kx', 'ky', 'kz', 'krx', 'kry', 'krz'])
                unit_labels = ['N/m', 'N.m/rad']
                text += self.structuralNodalInfo(values, labels, 'LUMPED STIFFNESS', unit_labels, node.loaded_table_for_lumped_stiffness)

            if node in self.project.preprocessor.nodes_connected_to_dampers:
                values = node.lumped_dampings
                labels = np.array(['cx', 'cy', 'cz', 'crx', 'cry', 'crz'])
                unit_labels = ['N.s/m', 'N.m.s/rad']
                text += self.structuralNodalInfo(values, labels, 'LUMPED DAMPINGS', unit_labels, node.loaded_table_for_lumped_dampings)

            if node in self.project.preprocessor.nodes_with_masses:
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

            if node.there_are_elastic_nodal_link_damping:
                index = node.external_index
                labels = np.array(['cx', 'cy', 'cz', 'crx', 'cry', 'crz'])
                unit_labels = ['N.s/m', 'N.m.s/rad']
                for key, [_, values] in node.elastic_nodal_link_dampings.items():
                    linked_nodes = [int(node_id) for node_id in key.split('-')]
                    if index in linked_nodes:            
                        text += self.structuralNodalInfo(values, labels, f'DAMPING ELASTIC LINK: [{key}]', unit_labels, node.loaded_table_for_elastic_link_dampings)
 
            if node in self.project.preprocessor.nodes_with_acoustic_pressure:
                value = node.acoustic_pressure
                label = 'P'
                unit_label = '[Pa]'
                text += self.acousticNodalInfo(value, label, 'ACOUSTIC PRESSURE', unit_label)
   
            if node in self.project.preprocessor.nodes_with_volume_velocity:
                value = node.volume_velocity
                label = 'Q'
                unit_label = '[m³/s]'
                text += self.acousticNodalInfo(value, label, 'VOLUME VELOCITY', unit_label)

            if node in self.project.preprocessor.nodes_with_compressor_excitation:
                str_connection = ""
                for _connection in node.dict_index_to_compressor_connection_info.values():
                    str_connection =+ f"{_connection}, "
                connection_type = f'  Connection(s) type(s): {str_connection[:-2]} \n'
                bc_label = 'VOLUME VELOCITY - COMPRESSOR EXCITATION'
                text += self.acousticNodalInfo(value, label, bc_label, unit_label, aditional_info=connection_type)

            if node in self.project.preprocessor.nodes_with_specific_impedance:
                value = node.specific_impedance
                label = 'Zs'
                unit_label = '[kg/m².s]'
                text += self.acousticNodalInfo(value, label, 'SPECIFIC IMPEDANCE', unit_label)

            if node in self.project.preprocessor.nodes_with_radiation_impedance:
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
            text += f'  {label} <--> Table of values \n'
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
            
            if structural_element.cross_section is None: 
                outer_diameter = 'undefined'
                thickness = 'undefined'
                offset_y = 'undefined'
                offset_z = 'undefined'
                insulation_thickness = 'undefined'
                insulation_density = 'undefined'
            else:
                outer_diameter = structural_element.cross_section.outer_diameter
                thickness = structural_element.cross_section.thickness
                offset_y = structural_element.cross_section.offset_y
                offset_z = structural_element.cross_section.offset_z
                insulation_thickness = structural_element.cross_section.insulation_thickness
                insulation_density = structural_element.cross_section.insulation_density
            
            if structural_element.material is None:
                material = 'undefined'
            else:
                material = structural_element.material.name.upper()

            if structural_element.fluid is None:
                fluid = 'undefined'
            else:
                fluid = structural_element.fluid.name.upper()

            if structural_element.element_type is None:
                structural_element_type = 'undefined'
            elif 'beam_1' in structural_element.element_type:

                area = structural_element.cross_section.area
                Iyy = structural_element.cross_section.second_moment_area_y
                Izz = structural_element.cross_section.second_moment_area_z
                Iyz = structural_element.cross_section.second_moment_area_yz
                section_label = structural_element.cross_section.section_label

                if section_label is None:
                    structural_element_type = "{} (-)".format(structural_element.element_type)
                else:
                    structural_element_type = "{} ({})".format(structural_element.element_type, section_label.capitalize())

            else:
                structural_element_type = structural_element.element_type

            firstNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.first_node.x, structural_element.first_node.y, structural_element.first_node.z)
            lastNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.last_node.x, structural_element.last_node.y, structural_element.last_node.z)
            
            rotations = structural_element.section_rotation_xyz_undeformed
            str_rotations = '{:.3f}, {:.3f}, {:.3f}'.format(rotations[0], rotations[1], rotations[2])

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {structural_element.first_node.external_index} -- Coordinates: ({firstNodePosition}) [m]\n'
            text += f'Last Node ID: {structural_element.last_node.external_index} -- Coordinates: ({lastNodePosition}) [m]\n'
            text += f'Rotations xyz: ({str_rotations})[deg]\n\n'
            text += f'Material: {material} \n'
            text += f'Strutural element type: {structural_element_type} \n'
            
            if "PIPE" in structural_element_type:        
                text += f'Diameter: {outer_diameter} [m]\n'
                text += f'Thickness: {thickness} [m]\n'
                if offset_y != 0 or offset_z != 0:
                    text += f'Offset y: {offset_y} [m]\n'
                    text += f'Offset z: {offset_z} [m]\n'
                if insulation_thickness != 0 or insulation_density != 0:
                    text += f'Insulation thickness: {insulation_thickness} [m]\n'
                    text += f'Insulation density: {insulation_density} [kg/m³]\n'

            elif "BEAM" in structural_element_type:
                text += 'Area:  {} [m²]\n'.format(area)
                text += 'Iyy:  {} [m^4]\n'.format(Iyy)
                text += 'Izz:  {} [m^4]\n'.format(Izz)
                text += 'Iyz:  {} [m^4]\n'.format(Iyz)
            
            if structural_element.fluid is not None:
                text += f'\nFluid: {fluid} \n'
            if acoustic_element.element_type is not None:
                text += f'Acoustic element type: {acoustic_element.element_type} \n'
            if acoustic_element.proportional_damping is not None:
                text += f'Proportional damping: {acoustic_element.proportional_damping} \n'             

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


###    
    def updateAllAxes(self):
        for ID, node in self.project.get_nodes().items():
            self.plotAxes(node, ID)
        self.plotElasticLinks()

    def getSize(self):
        return self.project.get_element_size()*0.7

    def transformPoints(self, points_id):
        self._style.clear()
        self.plotElasticLinks()
        for ID in points_id:
            try:
                node = self.project.get_node(ID)
                self.plotAxes(node, ID)
            except Exception as log_error:
                print(str(log_error))

    def plotElasticLinks(self):
        elastic_links_stiffness = self.project.preprocessor.nodes_with_elastic_link_stiffness
        elastic_links_damping = self.project.preprocessor.nodes_with_elastic_link_dampings
        self.removeElasticLinks()
        for key, _ in elastic_links_stiffness.items():
            try:
                self.elasticLinks[key] = []
                k = [int(k) for k in key.split('-')]
                nodeA = self.project.get_node(k[0])
                nodeB = self.project.get_node(k[1])
                self.plotElastic(nodeA, nodeB, key)
                # print(f"Key {key} - Stiff")
            except Exception as log_error:
                print(str(log_error))
                continue
        
        for key, _ in elastic_links_damping.items():
            try:
                self.elasticLinks[key] = []
                k = [int(k) for k in key.split('-')]
                nodeA = self.project.get_node(k[0])
                nodeB = self.project.get_node(k[1])
                self.plotElastic(nodeA, nodeB, key)
                # print(f"Key {key} - Damping")
            except Exception as log_error:
                print(str(log_error))
                continue

    def plotElastic(self, nodeA, nodeB, key):
        i =  self.symbols.getElasticLink(nodeA, nodeB)
        self.elasticLinks[key].append(i)
        self._renderer.AddActor(i)
    
    def plotAxes(self, node, key_id):
        self.removeAxes(key_id)
        self.axes[key_id] = []
        self.plotArrowBC(node, key_id)
        self.plotArrowRotation(node, key_id)
        self.plotArrowForce(node, key_id)
        self.plotArrowMomento(node, key_id)
        self.plotDamper(node, key_id)
        self.plotSpring(node, key_id)
        self.updateInfoText()

    def plotDamper(self, node, key_id):
        for i in self.symbols.getDamper(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)
    
    def plotSpring(self, node, key_id):
        for i in self.symbols.getSpring(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)

    def plotArrowBC(self, node, key_id):
        for i in self.symbols.getArrowBC(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)

    def plotArrowForce(self, node, key_id):
        for i in self.symbols.getArrowForce(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)

    def plotArrowRotation(self, node, key_id):
        for i in self.symbols.getArrowRotation(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)

    def plotArrowMomento(self, node, key_id):
        for i in self.symbols.getArrowMomento(node):
            self.axes[key_id].append(i)
            self._renderer.AddActor(i)

    def removeElasticLinks(self):
        for key, item in self.elasticLinks.items():
            for i in item:
                self._renderer.RemoveActor(i)
        self.elasticLinks = dict()

    def removeAxes(self, key):
        if self.axes.get(key) is not None:
            for actor in self.axes[key]:
                self._renderer.RemoveActor(actor)
            self.axes.pop(key)
