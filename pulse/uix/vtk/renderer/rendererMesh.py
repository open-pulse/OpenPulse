from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.vtkSymbols import vtkSymbols

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

        self._style.AddObserver('SelectionChangedEvent', self.highlight)
    
    def highlight(self, obj, event):
        # selectedNodes = [self.project.get_node(i) for i in self.getListPickedPoints()]
        # selectedElements = [self.project.get_structural_element(i) for i in self.getListPickedElements()]
        selectedNodes = [self.project.mesh.nodes[i] for i in self.getListPickedPoints()]
        selectedElements = [self.project.mesh.structural_elements[i] for i in self.getListPickedElements()]

        self._renderer.RemoveActor(self.selectionNodesActor)
        self._renderer.RemoveActor(self.selectionNodesActorAcoustic)
        self._renderer.RemoveActor(self.selectionElementsActor)
        self._renderer.RemoveActor(self.selectionTubeActor)
        
        if selectedNodes:
            selectedNodesAcoustic = []
            volume_velocity = self.project.mesh.nodes_with_volume_velocity #Vermelha
            acoustic_pressure = self.project.mesh.nodes_with_acoustic_pressure #Branca
            specific_impedance = self.project.mesh.nodes_with_specific_impedance #Verde
            radiation_impedance = self.project.mesh.nodes_with_radiation_impedance #Rosa
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
        self.plotNodes()
        self.plotElements()
        self.plotTubes()
    
    def saveNodesBounds(self):
        self.nodesBounds.clear()
        for key, node in self.project.get_nodes().items():
            x,y,z = node.coordinates
            self.nodesBounds[key] = (x,x,y,y,z,z)
    
    def saveElementsBounds(self):
        self.elementsBounds.clear()
        for key, element in self.project.get_elements().items():
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
        volume_velocity = self.project.mesh.nodes_with_volume_velocity #Vermelha
        acoustic_pressure = self.project.mesh.nodes_with_acoustic_pressure #Branca
        specific_impedance = self.project.mesh.nodes_with_specific_impedance #Verde
        radiation_impedance = self.project.mesh.nodes_with_radiation_impedance #Rosa
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
        elements = self.project.get_elements().values()
        actor = self.createActorElements(elements)
        actor.GetProperty().SetLineWidth(2)
        self._renderer.AddActor(actor)
    
    def plotTubes(self):
        elements = self.project.get_elements().values()
        actor = self.createActorTubes(elements)

        actor.GetProperty().SetColor(0.7,0.7,0.8)
        actor.GetProperty().SetOpacity(0.06)

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

        for element in elements:
            cross_section = element.cross_section
            if cross_section:
                label, parameters, *args = cross_section.additional_section_info
                if label == "Pipe section":
                    polygon = vtk.vtkRegularPolygonSource()
                    polygon.SetRadius(cross_section.external_diameter / 2)
                    polygon.SetNumberOfSides(10)
                else:
                    polygon = self.createSectionPolygon(element)
            else: # not cross section
                polygon = vtk.vtkRegularPolygonSource()
                polygon.SetRadius(0.01)
                polygon.SetNumberOfSides(10)
            
            tube = self.generalSectionTube(element, polygon.GetOutputPort())
            source.AddInputData(tube.GetOutput())

        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        return actor

    def createSectionPolygon(self, element):
        Ys, Zs = self.project.get_mesh().get_cross_section_points(element.index)
        points = vtk.vtkPoints()
        edges = vtk.vtkCellArray()
        data = vtk.vtkPolyData()
        poly = vtk.vtkPolygon()
        source = vtk.vtkTriangleFilter()

        for x, y in zip(Ys, Zs):
            points.InsertNextPoint(x, y, 0)    
       
        n = len(Ys)
        poly.GetPointIds().SetNumberOfIds(n)

        for i in range(n):
            poly.GetPointIds().SetId(i,i)
        edges.InsertNextCell(poly)
        
        data.SetPoints(points)
        data.SetPolys(edges)
        source.AddInputData(data)

        return source

    def generalSectionTube(self, element, section):
        start = element.first_node.coordinates
        size = element.length
 
        # _, directional_vectors = element.get_local_coordinate_system_info()
        u, v, w = element.directional_vectors
        
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
        self.opv.updateDialogs()

    def updateInfoText(self):
        pointsText = self.getPointsInfoText()
        elementsText = self.getElementsInfoText()
        text = (pointsText + '\n\n' + elementsText) if pointsText else (elementsText)
        self.createInfoText(text)
    
    def getPointsInfoText(self):
        listSelected = self.getListPickedPoints()
        text = ''
        if len(listSelected) == 1:
            node = self.project.get_node(listSelected[0])
            nodeId = listSelected[0]
            nodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(node.x, node.y, node.z)
            nodeBC = node.getStructuralBondaryCondition()
            text = f'Node Id: {nodeId} \nPosition: ({nodePosition}) [m]\nDisplacement: {nodeBC[:3]} [m]\nRotation: {nodeBC[3:]} [rad]'
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

    def getElementsInfoText(self):
        listSelected = self.getListPickedElements()
        text = ''
        if len(listSelected) == 1:
            structural_element = self.project.get_structural_element(listSelected[0])
            acoustic_element = self.project.get_acoustic_element(listSelected[0])
            
            if structural_element.cross_section is None: 
                external_diameter = 'undefined'
                thickness = 'undefined'
                offset_y = 'undefined'
                offset_z = 'undefined'
                insulation_thickness = 'undefined'
                insulation_density = 'undefined'
            else:
                external_diameter = structural_element.cross_section.external_diameter
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
            elif 'BEAM' in structural_element.element_type.upper():

                area = structural_element.cross_section.area
                Iyy = structural_element.cross_section.second_moment_area_y
                Izz = structural_element.cross_section.second_moment_area_z
                Iyz = structural_element.cross_section.second_moment_area_yz
                additional_section_info = structural_element.cross_section.additional_section_info

                if additional_section_info is None:
                    structural_element_type = "{} (-)".format(structural_element.element_type)
                else:
                    structural_element_type = "{} ({})".format(structural_element.element_type, additional_section_info[0].capitalize())

            else:
                structural_element_type = structural_element.element_type

            firstNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.first_node.x, structural_element.first_node.y, structural_element.first_node.z)
            lastNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(structural_element.last_node.x, structural_element.last_node.y, structural_element.last_node.z)

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {structural_element.first_node.external_index} -- Coordinates: ({firstNodePosition}) [m]\n'
            text += f'Last Node ID: {structural_element.last_node.external_index} -- Coordinates: ({lastNodePosition}) [m]\n\n'
            text += f'Material: {material} \n'
            text += f'Strutural element type: {structural_element_type} \n'
            
            if "PIPE" in structural_element_type:        
                text += f'Diameter: {external_diameter} [m]\n'
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
            if acoustic_element.hysteretic_damping is not None:
                text += f'Hysteretic damping: {acoustic_element.hysteretic_damping} \n'             

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
            except Exception as err:
                print(err)

    def plotElasticLinks(self):
        elastic_links_stiffness = self.project.mesh.dict_nodes_with_elastic_link_stiffness
        elastic_links_damping = self.project.mesh.dict_nodes_with_elastic_link_damping
        self.removeElasticLinks()
        for key, _ in elastic_links_stiffness.items():
            try:
                self.elasticLinks[key] = []
                k = [int(k) for k in key.split('-')]
                nodeA = self.project.get_node(k[0])
                nodeB = self.project.get_node(k[1])
                self.plotElastic(nodeA, nodeB, key)
                # print(f"Key {key} - Stiff")
            except Exception as err:
                print(err)
                continue
        
        for key, _ in elastic_links_damping.items():
            try:
                self.elasticLinks[key] = []
                k = [int(k) for k in key.split('-')]
                nodeA = self.project.get_node(k[0])
                nodeB = self.project.get_node(k[1])
                self.plotElastic(nodeA, nodeB, key)
                # print(f"Key {key} - Damping")
            except Exception as err:
                print(err)
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
