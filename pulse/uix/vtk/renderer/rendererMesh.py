from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
import vtk

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))
        self.project = project
        self.opv = opv 

        self.pointsID = {}
        self.elementsID = {}

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
        self.plotMain()
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
        text = self.getPointsInfoText() + '\n\n' + self.getElementsInfoText()
        self.createInfoText(text)
    
    def getPointsInfoText(self):
        listSelected = self.getListPickedPoints()
        text = ''
        if len(listSelected) == 1:
            node = self.project.get_node(listSelected[0])
            nodeId = listSelected[0]
            nodePosition = '{:.3f} {:.3f} {:.3f}'.format(node.x, node.y, node.z)
            nodeBC = node.getStructuralBondaryCondition()
            text = f'Node Id: {nodeId} \nPosition: {nodePosition} \nDisplacement: {nodeBC[:3]} \nRotation: {nodeBC[3:]}'
        elif len(listSelected) > 1:
            text = 'SELECTED POINTS: \n'
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
            
            if element.material is None:
                material = 'undefined'
            else:
                material = element.material.name.upper()

            if element.fluid is None:
                fluid = 'undefined'
            else:
                fluid = element.fluid.name.upper()

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {element.first_node.external_index} \n'
            text += f'Last Node ID: {element.last_node.external_index} \n'
            text += f'Element Type: {element.element_type.upper()} \n'
            text += f'Diameter: {external_diameter} \n'
            text += f'Thickness: {thickness} \n'
            text += f'Offset Y: {offset_y} \n'
            text += f'Offset Z: {offset_z} \n'
            text += f'Material: {material} \n'
            text += f'Fluid: {fluid} \n'

        elif len(listSelected) > 1:
            text += 'SELECTED ELEMENTS: \n'
            for i, ids in enumerate(listSelected):
                if i == 30:
                    text += '...'
                    break
                text += f'{ids} '
                if i ==10 or i==20:
                    text += '\n'
                    
        return text

    # 
    def plotMain(self):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(0.02)
            sphere.SetCenter(node.coordinates)
            source.AddInputConnection(sphere.GetOutputPort())

        for key, element in self.project.get_elements().items():
            plot = ActorElement(element, 0.01, key)
            plot.build()
            source.AddInputData(plot.getActor().GetMapper().GetInput())
        
        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.6,0,0.4)
        actor.GetProperty().SetDiffuse(1)
        actor.GetProperty().SetSpecular(0)
        self._renderer.AddActor(actor)
    
    def plotPoints(self):
        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkSphereSource()
            mapper = vtk.vtkPolyDataMapper()
            actor = vtk.vtkActor()
            
            sphere.SetRadius(0.02)
            sphere.SetCenter(node.coordinates)
            mapper.SetInputConnection(sphere.GetOutputPort())
            actor.SetMapper(mapper)

            self.pointsID[actor] = key
            self._rendererPoints.AddActor(actor)
    
    def plotElements(self):
        for key, element in self.project.get_elements().items():
            plot = ActorElement(element, 0.01, key)
            plot.build()
            actor = plot.getActor()
            self.elementsID[actor] = key
            self._rendererElements.AddActor(actor)
