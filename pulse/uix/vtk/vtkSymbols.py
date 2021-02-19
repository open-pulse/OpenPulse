import vtk
import numpy as np
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.actor.actorSpring import ActorSpring

class vtkSymbols:
    def __init__(self, project):
        self.project = project

    def getElasticLink(self, nodeA, nodeB):
        source = vtk.vtkLineSource()
        source.SetPoint1(nodeA.x, nodeA.y, nodeA.z)
        source.SetPoint2(nodeB.x, nodeB.y, nodeB.z)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0/255,255/255,152/255)
        return actor

    def arrow(self, start, end):
        base_length = self.project.mesh.structure_principal_diagonal/10
        arrowSource = vtk.vtkArrowSource()
        startPoint = start
        endPoint = end
        rng = vtk.vtkMinimalStandardRandomSequence()
        rng.SetSeed(8775070)  # For testing.

        normalizedX = [0] * 3
        normalizedY = [0] * 3
        normalizedZ = [0] * 3

        vtk.vtkMath.Subtract(endPoint, startPoint, normalizedX)
        length = vtk.vtkMath.Norm(normalizedX)
        vtk.vtkMath.Normalize(normalizedX)

        arbitrary = [0] * 3
        for i in range(0, 3):
            rng.Next()
            arbitrary[i] = rng.GetRangeValue(-10, 10)
        vtk.vtkMath.Cross(normalizedX, arbitrary, normalizedZ)
        vtk.vtkMath.Normalize(normalizedZ)

        vtk.vtkMath.Cross(normalizedZ, normalizedX, normalizedY)
        matrix = vtk.vtkMatrix4x4()

        matrix.Identity()
        for i in range(0, 3):
            matrix.SetElement(i, 0, normalizedX[i])
            matrix.SetElement(i, 1, normalizedY[i])
            matrix.SetElement(i, 2, normalizedZ[i])

        transform = vtk.vtkTransform()
        transform.Translate(startPoint)
        transform.Concatenate(matrix)
        #transform.Scale(length, length, length)
        transform.Scale(self.project.get_element_size(), self.project.get_element_size(), self.project.get_element_size())

        transformPD = vtk.vtkTransformPolyDataFilter()
        transformPD.SetTransform(transform)
        transformPD.SetInputConnection(arrowSource.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        mapper.SetInputConnection(arrowSource.GetOutputPort())
        actor.SetUserMatrix(transform.GetMatrix())
        actor.SetMapper(mapper)
        return actor

    def getElementAxe(self, element):
        center, direction = element.get_local_coordinate_system_info()
        arrows = []
        x = self.arrow(center, center+direction[0])
        x.GetProperty().SetColor(1,0,0)
        y = self.arrow(center, center+direction[1])
        y.GetProperty().SetColor(0,1,0)
        z = self.arrow(center, center+direction[2])
        z.GetProperty().SetColor(0,0,1)

        arrows.append(x)
        arrows.append(y)
        arrows.append(z)
        return arrows

    def getSpring(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.get_lumped_stiffness())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/10 < element_length*1.5:
            shift = base_length/10
        else:
            shift = element_length*1.5
        v = [1,2,3]
        for i in range(0,3):
            try:
                if a[i] is None or a[i] == 0:
                    v[i] = 0
                elif a[i] < 0:
                    v[i] = -1*v[i]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)

        if v.count(0) == 3:
            return []

        arrows = []
        for i in range(3):
            if v[i] == 0:
                continue
            b = ActorSpring(node, self.project.get_element_size(), base_length, xyz=v[i], u_def=u_def)
            b.setShiftValue(shift)
            b.setNormalizedColor([1,0,1])
            b.setNormalizedColor([242/255,121/255,0])
            b.build()
            arrows.append(b.getActor())
        return arrows

    def getDamper(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.get_lumped_dampings())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/10 < element_length*1.5:
            shift = base_length/10
        else:
            shift = element_length*1.5
        v = [1,2,3]
        for i in range(0,3):
            try:
                if a[i] is None or a[i] == 0:
                    v[i] = 0
                elif a[i] < 0:
                    v[i] = -1*v[i]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)

        if v.count(0) == 3:
            return []

        arrows = []
        for i in range(3):
            if v[i] == 0:
                continue
            a = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i], u_def=u_def)
            a.setNormalizedColor([242/255,121/255,0])
            a.setNormalizedColor([1,0,1])
            a.setShiftValue(shift)
            a.removeTipLenght()
            a.build()
            arrows.append(a.getActor())

        return arrows

    def getArrowBC(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.getStructuralBondaryCondition())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/20 < element_length/2:
            shift = base_length/20
        else:
            shift = element_length/2
        v = [1,2,3]
        for i in range(0,3):
            try:
                if a[i] is None:
                    v[i] = 0
                elif a[i] < 0:
                    v[i] = -1*v[i]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)
            
        if v.count(0) == 3:
            return []

        arrows = []
        for i in range(3):
            if v[i] == 0:
                continue
            a = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i], u_def=u_def)
            a.removeShaftRadius()
            a.setNormalizedColor([0,1,0])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getArrowForce(self, node, shift=0.01):
        a = self.getReal(node.get_prescribed_loads())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/20 < element_length/2:
            shift = base_length/20
        else:
            shift = element_length/2
        v = [1,2,3]
        for i in range(0,3):
            try:
                if a[i] is None or a[i] == 0:
                    v[i] = 0
                elif a[i] < 0:
                    v[i] = -1*v[i]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)

        if v.count(0) == 3:
            return []

        arrows = []
        for i in range(3):
            if v[i] == 0:
                continue
            a = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i])
            a.setNormalizedColor([1,0,0])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getArrowRotation(self, node, shift=0.01):
        a = self.getReal(node.getStructuralBondaryCondition())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/20 < element_length/2:
            shift = base_length/20
        else:
            shift = element_length/2
        v = [1,2,3]
        for i in range(3,6):
            try:
                if a[i] is None or a[i] == 0:
                    v[i-3] = 0
                elif a[i] < 0:
                    v[i-3] = -1*v[i-3]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)

        if v.count(0) == 3:
            return []

        arrows = []

        for i in range(3):
            if v[i] == 0:
                continue
            
            a = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i])
            a.removeShaftRadius()
            a.setNormalizedColor([0, 1, 1])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())

            b = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i])
            b.removeShaftRadius()
            b.setNormalizedColor([0,1,1])
            b.setShiftValue(6.5*shift)
            b.build()
            arrows.append(b.getActor())

        return arrows

    def getArrowMomento(self, node, shift=0.01):
        a = self.getReal(node.get_prescribed_loads())
        base_length = self.project.mesh.structure_principal_diagonal/10
        element_length = self.project.get_element_size()
        if base_length/20 < element_length/2:
            shift = base_length/20
        else:
            shift = element_length/2
        v = [1,2,3]
        for i in range(3,6):
            try:
                if a[i] is None or a[i] == 0:
                    v[i-3] = 0
                elif a[i] < 0:
                    v[i-3] = -1*v[i-3]
            except Exception as e:
                if isinstance(a[i], np.ndarray):
                    pass
                else:
                    print(e)

        if v.count(0) == 3:
            return []

        arrows = []
        for i in range(3):
            if v[i] == 0:
                continue
            a = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i])
            a.setNormalizedColor([0,0,1])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())

            b = ActorArrow(node, self.project.get_element_size(), base_length, xyz=v[i])
            b.setNormalizedColor([0,0,1])
            b.setShiftValue(6.5*shift)
            b.removeShaftRadius()
            b.build()
            arrows.append(b.getActor())

        return arrows

    def getReal(self, vector):
        new_vector = vector.copy()
        for i in range(len(vector)):
            if type(vector[i]) == complex:
                new_vector[i] = vector[i].real
        return new_vector