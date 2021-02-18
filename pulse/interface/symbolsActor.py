import vtk

from pulse.interface.vtkActorBase import vtkActorBase

def loadSymbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

class SymbolsActor(vtkActorBase):
    ARROW_BC_SYMBOL = loadSymbol('pulse/interface/symbols/arrowBC.obj')

    def __init__(self, nodes, project):
        super().__init__()

        self.nodes = nodes
        self.project = project

        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
    
    def source(self):
        for node in self.nodes.values():
            symbols = [
                *self.getArrowBC(node),
                *self.getArrowRotation(node),
            ]

            for symbol in symbols:
                if symbol is not None:
                    self._source.AddInputData(symbol)
    
    def filter(self):
        pass 

    def map(self):
        self._source.Update()
        self._mapper.SetInputData(self._source.GetOutput())
    
    def actor(self):
        self._actor.SetMapper(self._mapper)

    def getArrowBC(self, node):
        mask = [(i != None) for i in node.getStructuralBondaryCondition()[:3]]
        pos = node.coordinates
        return self.orientSourceToAxis(self.ARROW_BC_SYMBOL, mask, pos, size=0.2, distance=0.3)
    
    def getArrowRotation(self, node):
        return []
    
    def orientSourceToAxis(self, source, mask, pos=(0,0,0), size=1, distance=1):
        transformPD = vtk.vtkTransformPolyDataFilter()
        transform = vtk.vtkTransform()
        axes = []

        transformPD.SetTransform(transform)
        transformPD.SetInputData(source)
        transform.Translate(pos)
        transform.Scale(size, size, size)

        if mask[0]:
            transform.Push()
            transform.Translate(distance, 0, 0)
            transform.RotateZ(-90)
            transformPD.Update()
            
            x = vtk.vtkPolyData()
            x.ShallowCopy(transformPD.GetOutput())
            axes.append(x)

            transform.Pop()

        if mask[1]:
            transform.Push()
            transform.Translate(0, distance, 0)
            # transform.RotateZ(0)
            transformPD.Update()

            y = vtk.vtkPolyData()
            y.ShallowCopy(transformPD.GetOutput())
            axes.append(y)

            transform.Pop()

        if mask[2]:
            transform.Push()
            transform.Translate(0, 0, distance)
            transform.RotateX(90)
            transformPD.Update()

            z = vtk.vtkPolyData()
            z.ShallowCopy(transformPD.GetOutput())
            axes.append(z)

            transform.Pop()

        return axes


