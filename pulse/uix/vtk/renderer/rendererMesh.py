from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.vtkSymbols import vtkSymbols
import vtk

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))
        self.project = project
        self.opv = opv 
        self.symbols = vtkSymbols()
        self.plotRadius = False
        
        self.nodesBounds = dict() # (x,y,z) coordinates
        self.elementsBounds = dict() # bounding coordinates
        self.axes = dict()

        self.selectionNodesActor = None
        self.selectionNodesActorAcoustic = None
        self.selectionElementsActor = None
        self.selectionTubeActor = None

        self._style.AddObserver('SelectionChangedEvent', self.highlight)
    
    def highlight(self, obj, event):
        selectedNodes = [self.project.get_node(i) for i in self.getListPickedPoints()]
        selectedElements = [self.project.get_element(i) for i in self.getListPickedElements()]

        self._renderer.RemoveActor(self.selectionNodesActor)
        self._renderer.RemoveActor(self.selectionNodesActorAcoustic)
        self._renderer.RemoveActor(self.selectionElementsActor)
        self._renderer.RemoveActor(self.selectionTubeActor)
        
        if selectedNodes:
            selectedNodesAcoustic = []
            volume_velocity = self.project.get_mesh().nodes_with_volume_velocity #Vermelha
            acoustic_pressure = self.project.get_mesh().nodes_with_acoustic_pressure #Branca
            specific_impedance = self.project.get_mesh().nodes_with_specific_impedance #Verde
            radiation_impedance = self.project.get_mesh().nodes_with_radiation_impedance #Rosa
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

            source = vtk.vtkCubeSource()
            source.SetXLength(2)
            source.SetYLength(2)
            source.SetZLength(2)
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
    
    # def updateAllAxes(self):
    #     pass

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

    def plotNodes(self):
        nodes = list(self.project.get_nodes().values())
        volume_velocity = self.project.get_mesh().nodes_with_volume_velocity #Vermelha
        acoustic_pressure = self.project.get_mesh().nodes_with_acoustic_pressure #Branca
        specific_impedance = self.project.get_mesh().nodes_with_specific_impedance #Verde
        radiation_impedance = self.project.get_mesh().nodes_with_radiation_impedance #Rosa
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
        self._renderer.AddActor(actor)

        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(4)
        cube_source.SetYLength(4)
        cube_source.SetZLength(4)

        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(3)
        actor = self.createActorNodes(volume_velocity,sphere_source)
        actor.GetProperty().SetColor(1,0.2,0.2)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(acoustic_pressure,sphere_source)
        actor.GetProperty().SetColor(1,1,1)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(specific_impedance,cube_source)
        actor.GetProperty().SetColor(1,0.07,0.57)
        self._renderer.AddActor(actor)

        actor = self.createActorNodes(radiation_impedance,cube_source)
        actor.GetProperty().SetColor(0,1,0)
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
        actor.GetProperty().SetOpacity(0.2)
        self._renderer.AddActor(actor)
    
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
                size = cross_section.external_diameter / 2
            else:
                size = 0.002
            plot = ActorElement(element, size)
            plot.build()
            source.AddInputData(plot.getActor().GetMapper().GetInput())

        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        return actor

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
            element = self.project.get_element(listSelected[0])
            
            if element.cross_section is None: 
                external_diameter = 'undefined'
                thickness = 'undefined'
                offset_y = 'undefined'
                offset_z = 'undefined'
                insulation_thickness = 'undefined'
                insulation_density = 'undefined'
            else:
                external_diameter = element.cross_section.external_diameter
                thickness = element.cross_section.thickness
                offset_y = element.cross_section.offset_y
                offset_z = element.cross_section.offset_z
                insulation_thickness = element.cross_section.insulation_thickness
                insulation_density = element.cross_section.insulation_density
            
            if element.material is None:
                material = 'undefined'
            else:
                material = element.material.name.upper()

            if element.fluid is None:
                fluid = 'undefined'
            else:
                fluid = element.fluid.name.upper()

            if element.element_type is None:
                e_type = 'undefined'
            elif 'BEAM' in element.element_type.upper():

                area = element.cross_section.area
                Iyy = element.cross_section.second_moment_area_y
                Izz = element.cross_section.second_moment_area_z
                Iyz = element.cross_section.second_moment_area_yz
                additional_section_info = element.cross_section.additional_section_info

                if additional_section_info is None:
                    e_type = "{} (-)".format(element.element_type.upper())
                else:
                    e_type = "{} ({})".format(element.element_type.upper(), additional_section_info[0].capitalize())

            else:
                e_type = element.element_type.upper()

            firstNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(element.first_node.x, element.first_node.y, element.first_node.z)
            lastNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(element.last_node.x, element.last_node.y, element.last_node.z)

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {element.first_node.external_index} -- Coordinates: ({firstNodePosition}) [m]\n'
            text += f'Last Node ID: {element.last_node.external_index} -- Coordinates: ({lastNodePosition}) [m]\n\n'
            text += f'Material: {material} \n'
            text += f'Element Type: {e_type} \n'
            
            if "PIPE" in e_type:        
                text += f'Diameter: {external_diameter} [m]\n'
                text += f'Thickness: {thickness} [m]\n'
                if offset_y != 0 or offset_z != 0:
                    text += f'Offset y: {offset_y} [m]\n'
                    text += f'Offset z: {offset_z} [m]\n'
                if insulation_thickness != 0 or insulation_density != 0:
                    text += f'Insulation thickness: {insulation_thickness} [m]\n'
                    text += f'Insulation density: {insulation_density} [kg/m³]\n'

            elif "BEAM" in e_type:
                text += 'Area:  {} [m²]\n'.format(area)
                text += 'Iyy:  {} [m^4]\n'.format(Iyy)
                text += 'Izz:  {} [m^4]\n'.format(Izz)
                text += 'Iyz:  {} [m^4]\n'.format(Iyz)
            
            if element.fluid is not None:
                text += f'\nFluid: {fluid} \n'

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

    def getSize(self):
        return self.project.get_element_size()*0.7

    def transformPoints(self, points_id):
        self._style.clear()
        for ID in points_id:
            try:
                node = self.project.get_node(ID)
                self.plotAxes(node, ID)
            except Exception as e:
                print(e)
    
    def plotAxes(self, node, key_id):
        self.removeAxes(key_id)
        self.axes[key_id] = []
        self.plotArrowBC(node, key_id)
        self.plotArrowRotation(node, key_id)
        self.plotArrowForce(node, key_id)
        self.plotArrowMomento(node, key_id)
        self.plotDamper(node, key_id)
        self.updateInfoText()

    def plotDamper(self, node, key_id):
        for i in self.symbols.getDamper(node):
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

    def removeAxes(self, key):
        if self.axes.get(key) is not None:
            for actor in self.axes[key]:
                self._renderer.RemoveActor(actor)
            self.axes.pop(key)
