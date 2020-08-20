from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
# from pulse.uix.vtk.actor.actorArrow import ActorArrow
# from pulse.uix.vtk.vtkSymbols import vtkSymbols
import vtk

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))
        self.project = project
        self.opv = opv 
        self.plotRadius = False
        
        self.nodesData = dict() # (x,y,z) coordinates
        self.elementsData = dict() # bounding coordinates

        self.selectionNodesActor = None
        self.selectionElementsActor = None

        self._style.AddObserver('SelectionChangedEvent', self.highlight)
    
    def highlight(self, obj, event):
        selectedNodes = [self.project.get_node(i) for i in self.getListPickedPoints()]
        selectedElements = [self.project.get_element(i) for i in self.getListPickedElements()]

        self._renderer.RemoveActor(self.selectionNodesActor)
        self._renderer.RemoveActor(self.selectionElementsActor)
        
        if selectedNodes:
            source = vtk.vtkCubeSource()
            source.SetXLength(2)
            source.SetYLength(2)
            source.SetZLength(2)
            self.selectionNodesActor = self.createActorNodes(selectedNodes,source)
            self.selectionNodesActor.GetProperty().SetColor(255,0,0)
            self._renderer.AddActor(self.selectionNodesActor)    
        
        if selectedElements:
            self.selectionElementsActor = self.createActorElements(selectedElements)
            self.selectionElementsActor.GetProperty().SetColor(1,0,0)
            self.selectionElementsActor.GetProperty().SetOpacity(0.5)
            self._renderer.AddActor(self.selectionElementsActor)        

        self.updateInfoText()
        self.update()
        
    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()
    
    def getListPickedPoints(self):
        return self._style.getListPickedPoints()

    def getListPickedElements(self):
        return self._style.getListPickedElements()
        
    def update(self):
        self.opv.update()
    
    def updateAllAxes(self):
        pass

    def plot(self):
        self.reset()
        self.saveNodesData()
        self.saveElementsData()
        self.plotNodes()
        self.plotElements()

    def plotNodes(self):
        nodes = self.project.get_nodes().values()
        source = vtk.vtkCubeSource()
        source.SetXLength(2)
        source.SetYLength(2)
        source.SetZLength(2)
        actor = self.createActorNodes(nodes,source)
        actor.GetProperty().SetColor(1,1,0)
        self._renderer.AddActor(actor)       
    
    def plotElements(self):
        elements = self.project.get_elements().values()
        actor = self.createActorElements(elements)
        actor.GetProperty().SetColor(0.7,0.7,0.8)
        actor.GetProperty().SetOpacity(0.3)
        self._renderer.AddActor(actor)
    
    def saveNodesData(self):
        self.nodesData.clear()
        for key, node in self.project.get_nodes().items():
            x,y,z = node.coordinates
            self.nodesData[key] = (x,y,z)
    
    def saveElementsData(self):
        self.elementsData.clear()
        for key, element in self.project.get_elements().items():
            cross_section = element.cross_section
            if cross_section:
                size = cross_section.external_diameter / 2
            else:
                size = 0.002
            
            firstNode = element.first_node.coordinates
            lastNode = element.last_node.coordinates

            x0 = min(firstNode[0], lastNode[0])
            y0 = min(firstNode[1], lastNode[1])
            z0 = min(firstNode[2], lastNode[2])
            x1 = max(firstNode[0], lastNode[0])
            y1 = max(firstNode[1], lastNode[1])
            z1 = max(firstNode[2], lastNode[2])

            dx = abs(x0-x1)
            dy = abs(y0-y1)
            dz = abs(z0-z1)

            greatest = max(dx,dy,dz)

            if (dx < size*2) and (dx != greatest):
                x0 -= size
                x1 += size
            if (dy < size*2) and (dy != greatest):
                y0 -= size
                y1 += size
            if (dz < size*2) and (dz != greatest):
                z0 -= size
                z1 += size 

            bounds = (x0,x1,y0,y1,z0,z1)
            self.elementsData[key] = bounds
    
    def createActorNodes(self, nodes, source):
        points = vtk.vtkPoints()
        data = vtk.vtkPolyData()
        cameraDistance = vtk.vtkDistanceToCamera()
        glyph = vtk.vtkGlyph3D()
        actor = vtk.vtkActor()
        mapper = vtk.vtkPolyDataMapper()

        for node in nodes:
            x,y,z = node.coordinates
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

            firstNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(element.first_node.x, element.first_node.y, element.first_node.z)
            lastNodePosition = '{:.3f}, {:.3f}, {:.3f}'.format(element.last_node.x, element.last_node.y, element.last_node.z)

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {element.first_node.external_index} -- Coordinates: ({firstNodePosition}) [m]\n'
            text += f'Last Node ID: {element.last_node.external_index} -- Coordinates: ({lastNodePosition}) [m]\n'
            text += f'Element Type: {element.element_type.upper()} \n'
            text += f'Diameter: {external_diameter} [m]\n'
            text += f'Thickness: {thickness} [m]\n'
            if offset_y != 0 or offset_z != 0:
                text += f'Offset y: {offset_y} [m]\n'
                text += f'Offset z: {offset_z} [m]\n'
            if insulation_thickness != 0 or insulation_density != 0:
                text += f'Insulation thickness: {insulation_thickness} [m]\n'
                text += f'Insulation density: {insulation_density} [kg/m³]\n'
            text += f'Material: {material} \n'
            text += f'Fluid: {fluid} \n'

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