import vtk
from pulse.uix.vtk.actor.actorArrow import ActorArrow
from pulse.uix.vtk.actor.actorDamper import ActorDamper

class vtkSymbols:
    def __init__(self):
        pass

    def getDamper(self, node, shift=0.01, u_def=[]):
        a = self.getReal(node.get_lumped_dampings())
        v = [1,2,3]
        for i in range(0,3):
            if a[i] is None or a[i] == 0:
                v[i] = 0
            elif a[i] < 0:
                v[i] = -1*v[i]

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
            if a[i] is None:
                v[i] = 0
            elif a[i] < 0:
                v[i] = -1*v[i]

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
            if a[i] is None or a[i] == 0:
                v[i] = 0
            elif a[i] < 0:
                v[i] = -1*v[i]

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
            if a[i] is None or a[i] == 0:
                v[i-3] = 0
            elif a[i] < 0:
                v[i-3] = -1*v[i-3]

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
            if a[i] is None or a[i] == 0:
                v[i-3] = 0
            elif a[i] < 0:
                v[i-3] = -1*v[i-3]

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