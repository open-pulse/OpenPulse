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
            
            if element.material is None:
                material = 'undefined'
            else:
                material = element.material.name.upper()

            if element.fluid is None:
                fluid = 'undefined'
            else:
                fluid = element.fluid.name.upper()

            firstNodePosition = '{:.3f} {:.3f} {:.3f}'.format(element.first_node.x, element.first_node.y, element.first_node.z)
            lastNodePosition = '{:.3f} {:.3f} {:.3f}'.format(element.last_node.x, element.last_node.y, element.last_node.z)

            text += f'Element ID: {listSelected[0]} \n'
            text += f'First Node ID: {element.first_node.external_index} -- Coordinates: {firstNodePosition} \n'
            text += f'Last Node ID: {element.last_node.external_index} -- Coordinates: {lastNodePosition} \n'
            text += f'Element Type: {element.element_type.upper()} \n'
            text += f'Diameter: {external_diameter} \n'
            text += f'Thickness: {thickness} \n'
            text += f'Offset Y: {offset_y} \n'
            text += f'Offset Z: {offset_z} \n'
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

    def plotMain(self):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkSphereSource()
            radius = 0.02
            sphere.SetRadius(radius)
            sphere.SetCenter(node.coordinates)
            source.AddInputConnection(sphere.GetOutputPort())

        for key, element in self.project.get_elements().items():
            radius = 0.01
            plot = ActorElement(element, radius, key)
            plot.build()
            actor = plot.getActor()
            source.AddInputData(actor.GetMapper().GetInput())
        
        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.6,0,0.4)
        actor.GetProperty().SetDiffuse(1)  
        actor.GetProperty().SetOpacity(0.5)
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
            actor.GetProperty().SetColor(0,255,0)
            self.elementsID[actor] = key
            self._rendererElements.AddActor(actor)





###    
    def getSize(self):
        return 0.5 #self.project.get_element_size()*0.7

    def transformPoints(self, points_id):
        self._style.clear()
        for ID in points_id:
            node = self.project.get_node(ID)
            self.plotAxes(node, ID)
            # try:
            # except Exception as e:
            #     print(e)
    
    def plotAxes(self, node, key_id):
        self.removeAxes(key_id)
        self.axes[key_id] = []
        self.plotForceAxes(node, key_id)
        self.plotBcAxes(node, key_id)
        self.plotRotationAxes(node, key_id)
        self.plotMomentoAxes(node, key_id)
        self.updateInfoText()

    def removeAxes(self, key):
        if self.axes.get(key) is not None:
            for actor in self.axes[key]:
                self._renderer.RemoveActor(actor)
            self.axes.pop(key)

    def transformAxe(self, node, negative_axe):
        transform = vtk.vtkTransform()
        transform.Translate(node.x, node.y, node.z)
        if negative_axe[0] == 1:
            transform.RotateZ(90)
            if negative_axe[1] == 1:
                transform.RotateY(270)
                if negative_axe[2] == 1:
                    transform.RotateY(-90)
                #Z +
            else:
                #Y +
                if negative_axe[2] == 1:
                    transform.RotateY(90)
        else:
            #X +
            if negative_axe[1] == 1:
                transform.RotateX(180)
                transform.RotateY(90)
                if negative_axe[2] == 1:
                    transform.RotateZ(90)
                #Z +
            else:
                #Y +
                if negative_axe[2] == 1:
                    transform.RotateZ(90)
                    transform.RotateX(180)
        return transform

    def getPosAxe(self, negative_axe, have_axe):
        if negative_axe[0] == 1:
            pos_axes = [1,0,2]
            if negative_axe[1] == 1:
                if negative_axe[2] == 1:
                    pos_axes = [1,0,2]
                else:
                    pos_axes = [1,2,0]
            else:
                if negative_axe[2] == 1:
                    pos_axes = [1,2,0]
                else:
                    pos_axes = [1,0,2]
        else:
            pos_axes = [0,1,2]
            if negative_axe[1] == 1:
                if negative_axe[2] == 1:
                    pos_axes = [2,0,1]
                else:
                    pos_axes = [2,1,0]
            else:
                if negative_axe[2] == 1:
                    pos_axes = [1,0,2]
                else:
                    pos_axes = [0,1,2]

        temp = [0,0,0]
        temp[pos_axes[0]] = have_axe[0]
        temp[pos_axes[1]] = have_axe[1]
        temp[pos_axes[2]] = have_axe[2]
        return temp
    
    def getReal(self, vector):
        new_vector = vector.copy()
        for i in range(len(vector)):
            if type(vector[i]) == complex:
                new_vector[i] = vector[i].real
        return new_vector

    def plotBcAxes(self, node, key_id):
        bc = self.getReal(node.getStructuralBondaryCondition())
        have_bc = [0,0,0]
        negative_bc = [0,0,0]
        for i in range(0,3):
            if bc[i] is not None:
                have_bc[i] = 1
            if bc[i] is not None and bc[i] < 0:
                negative_bc[i] = 1

        if have_bc.count(0) == 3:
            return
        
        transform = self.transformAxe(node, negative_bc)
        have_bc = self.getPosAxe(negative_bc, have_bc)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.05*have_bc[0],0.05*have_bc[1],0.05*have_bc[2])
        axe.SetShaftTypeToLine()
        axe.SetNormalizedTipLength(0.8*have_bc[0],0.8*have_bc[1],0.8*have_bc[2])
        axe.SetUserTransform(transform)
        axe.GetXAxisShaftProperty().SetColor(0,1,0)
        axe.GetYAxisShaftProperty().SetColor(0,1,0)
        axe.GetZAxisShaftProperty().SetColor(0,1,0)

        axe.GetXAxisTipProperty().SetColor(0,1,0)
        axe.GetYAxisTipProperty().SetColor(0,1,0)
        axe.GetZAxisTipProperty().SetColor(0,1,0)
        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)

    def plotRotationAxes(self, node, key_id):
        rotation = self.getReal(node.getStructuralBondaryCondition())
        have_rotation = [0,0,0]
        negative_rotation = [0,0,0]
        for i in range(3,6):
            if rotation[i] is not None and rotation[i] != 0:
                have_rotation[i-3] = 1
            if rotation[i] is not None and rotation[i] < 0:
                negative_rotation[i-3] = 1

        if have_rotation.count(0) == 3:
            return
        
        transform = self.transformAxe(node, negative_rotation)
        have_rotation = self.getPosAxe(negative_rotation, have_rotation)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.08*have_rotation[0],0.08*have_rotation[1],0.08*have_rotation[2])
        axe.SetShaftTypeToLine()
        axe.SetNormalizedTipLength(0.5*have_rotation[0],0.5*have_rotation[1],0.5*have_rotation[2])
        axe.SetUserTransform(transform)
        axe.GetXAxisShaftProperty().SetColor(1,0.64,0)
        axe.GetYAxisShaftProperty().SetColor(1,0.64,0)
        axe.GetZAxisShaftProperty().SetColor(1,0.64,0)

        axe.GetXAxisTipProperty().SetColor(1,0.64,0)
        axe.GetYAxisTipProperty().SetColor(1,0.64,0)
        axe.GetZAxisTipProperty().SetColor(1,0.64,0)
        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)

    def plotMomentoAxes(self, node, key_id):
        momento = self.getReal(node.get_prescribed_loads())
        have_momento = [0,0,0]
        negative_momento = [0,0,0]
        for i in range(3,6):
            if momento[i] is not None and momento[i] != 0:
                have_momento[i-3] = 1
            if momento[i] is not None and momento[i] < 0:
                negative_momento[i-3] = 1

        if have_momento.count(0) == 3:
            return

        transform = self.transformAxe(node, negative_momento)
        have_momento = self.getPosAxe(negative_momento, have_momento)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.15*have_momento[0], 0.15*have_momento[1], 0.15*have_momento[2])
        axe.SetShaftTypeToLine()
        axe.SetShaftTypeToCylinder()
        axe.SetCylinderRadius(0.05)
        axe.SetNormalizedTipLength(0.2*have_momento[0], 0.2*have_momento[1], 0.2*have_momento[2])
        axe.SetUserTransform(transform)

        axe.GetXAxisShaftProperty().SetColor(0,0,1)
        axe.GetYAxisShaftProperty().SetColor(0,0,1)
        axe.GetZAxisShaftProperty().SetColor(0,0,1)

        axe.GetXAxisTipProperty().SetColor(0,0,1)
        axe.GetYAxisTipProperty().SetColor(0,0,1)
        axe.GetZAxisTipProperty().SetColor(0,0,1)

        axe2 = vtk.vtkAxesActor()
        axe2.AxisLabelsOff()
        axe2.SetTotalLength(0.18*have_momento[0], 0.18*have_momento[1], 0.18*have_momento[2])
        axe2.SetShaftTypeToLine()
        axe2.SetNormalizedTipLength(0.2*have_momento[0], 0.2*have_momento[1], 0.2*have_momento[2])
        axe2.SetUserTransform(transform)

        axe2.GetXAxisShaftProperty().SetColor(0,0,1)
        axe2.GetYAxisShaftProperty().SetColor(0,0,1)
        axe2.GetZAxisShaftProperty().SetColor(0,0,1)

        axe2.GetXAxisTipProperty().SetColor(0,0,1)
        axe2.GetYAxisTipProperty().SetColor(0,0,1)
        axe2.GetZAxisTipProperty().SetColor(0,0,1)

        self.axes[key_id].append(axe)
        self.axes[key_id].append(axe2)

        self._renderer.AddActor(axe)
        self._renderer.AddActor(axe2)

    def plotForceAxes(self, node, key_id):
        force = self.getReal(node.get_prescribed_loads())
        have_force = [0,0,0]
        negative_force = [0,0,0]
        for i in range(0,3):
            if force[i] is not None and force[i] != 0:
                have_force[i] = 1
            if force[i] is not None and force[i] < 0:
                negative_force[i] = 1

        if have_force.count(0) == 3:
            return

        transform = self.transformAxe(node, negative_force)
        have_force = self.getPosAxe(negative_force, have_force)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.15*have_force[0], 0.15*have_force[1], 0.15*have_force[2])
        axe.SetShaftTypeToLine()
        axe.SetShaftTypeToCylinder()
        axe.SetCylinderRadius(0.05)
        axe.SetNormalizedTipLength(0.2*have_force[0], 0.2*have_force[1], 0.2*have_force[2])
        axe.SetUserTransform(transform)

        axe.GetXAxisShaftProperty().SetColor(1,0,0)
        axe.GetYAxisShaftProperty().SetColor(1,0,0)
        axe.GetZAxisShaftProperty().SetColor(1,0,0)

        axe.GetXAxisTipProperty().SetColor(1,0,0)
        axe.GetYAxisTipProperty().SetColor(1,0,0)
        axe.GetZAxisTipProperty().SetColor(1,0,0)

        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)