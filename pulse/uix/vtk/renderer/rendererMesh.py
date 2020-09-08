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

        self.pointsID = dict()
        self.elementsID = dict()
        self.axes = dict()

        self._rendererPoints = vtk.vtkRenderer()
        self._rendererElements = vtk.vtkRenderer()
        self._rendererPoints.DrawOff()
        self._rendererElements.DrawOff()
    
    def getSelectedPoints(self):
        return self._style.getSelectedPoints()
    
    def getSelectedElements(self):
        return self._style.getSelectedElements()
    
    def getListPickedPoints(self):
        return [self.pointsID[point] for point in self.getSelectedPoints()]

    def getListPickedElements(self):
        return [self.elementsID[element] for element in self.getSelectedElements()]
    
    def plot(self):
        self.reset()
        self.plotPoints()
        self.plotElements()

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._rendererPoints.RemoveAllViewProps()
        self._rendererElements.RemoveAllViewProps()
        self._style.clear()
    
    def update(self):
        self.opv.update()

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

    #     
    def plotPoints(self):
        pointsSource = vtk.vtkAppendPolyData()
        pointsMapper = vtk.vtkPolyDataMapper()
        pointsActor = vtk.vtkActor()

        size = 0.006
        
        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkCubeSource()
            mapper = vtk.vtkPolyDataMapper()
            actor = vtk.vtkActor()

            sphere.SetXLength(size)
            sphere.SetYLength(size)
            sphere.SetZLength(size)
            
            sphere.SetCenter(node.coordinates)

            pointsSource.AddInputConnection(sphere.GetOutputPort())
            mapper.SetInputConnection(sphere.GetOutputPort())
            actor.SetMapper(mapper)

            self.pointsID[actor] = key
            self._rendererPoints.AddActor(actor)
        
        pointsMapper.SetInputConnection(pointsSource.GetOutputPort())
        pointsActor.SetMapper(pointsMapper)
        pointsActor.GetProperty().SetColor(1, 1, 0)
        pointsActor.GetProperty().SetOpacity(0.9)
        pointsActor.GetProperty().SetSpecular(0)
        self._renderer.AddActor(pointsActor)

    
    def plotElements(self):
        elementsSource = vtk.vtkAppendPolyData()
        elementsMapper = vtk.vtkPolyDataMapper()
        elementsActor = vtk.vtkActor()

        for key, element in self.project.get_elements().items():
            cross_section = element.cross_section
            if cross_section and self.plotRadius:
                size = cross_section.external_diameter / 2
            else:
                size = 0.002 

            plot = ActorElement(element, size, key)
            plot.build()
            actor = plot.getActor()
            actor.GetProperty().SetColor(0,255,0)
            
            elementsSource.AddInputData(actor.GetMapper().GetInput())
            self.elementsID[actor] = key
            self._rendererElements.AddActor(actor)

        elementsMapper.SetInputConnection(elementsSource.GetOutputPort())
        elementsActor.SetMapper(elementsMapper)
        elementsActor.GetProperty().SetColor(1, 0, 0.5)
        elementsActor.GetProperty().SetSpecular(0)
        elementsActor.GetProperty().SetOpacity(0.6)
        self._renderer.AddActor(elementsActor)

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