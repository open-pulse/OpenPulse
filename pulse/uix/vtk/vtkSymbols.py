import vtk
import numpy as np
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.actor.actorDamper import ActorDamper

class vtkSymbols:
    def __init__(self):
        pass

    def arrow(self, start, end):
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
        transform.Scale(0.1, 0.1, 0.1)

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

    def getDamper(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.get_lumped_dampings())
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
            a = ActorArrow(node, xyz=v[i], u_def=u_def)
            a.setNormalizedColor([1,1,0])
            a.setShiftValue(shift)
            a.removeTipLenght()
            a.build()
            arrows.append(a.getActor())

            b = ActorDamper(node, xyz=v[i], u_def=u_def)
            b.setShiftValue(shift)
            b.build()
            arrows.append(b.getActor())
        return arrows

    def getArrowBC(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.getStructuralBondaryCondition())
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
            a = ActorArrow(node, xyz=v[i], u_def=u_def)
            a.removeShaftRadius()
            a.setNormalizedColor([0,1,0])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getArrowForce(self, node, shift=0.01):
        a = self.getReal(node.get_prescribed_loads())
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
            a = ActorArrow(node, xyz=v[i])
            a.setNormalizedColor([1,0,0])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getArrowRotation(self, node, shift=0.01):
        a = self.getReal(node.getStructuralBondaryCondition())
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
            a = ActorArrow(node, xyz=v[i])
            a.removeShaftRadius()
            a.setNormalizedColor([1,0.64,0])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getArrowMomento(self, node, shift=0.01):
        a = self.getReal(node.get_prescribed_loads())
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
            a = ActorArrow(node, xyz=v[i])
            a.setNormalizedColor([0,0,1])
            a.setShiftValue(shift)
            a.build()
            arrows.append(a.getActor())
        return arrows

    def getReal(self, vector):
        new_vector = vector.copy()
        for i in range(len(vector)):
            if type(vector[i]) == complex:
                new_vector[i] = vector[i].real
        return new_vector