import numpy as np 
from time import time

from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.colorTable import ColorTable

from pulse.interface.tubeActor import TubeActor
from pulse.interface.nodesActor import NodesActor
from pulse.interface.linesActor import LinesActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor

class opvRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project
        self.opv = opv

        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.entitiesBounds = dict()

        self.opvNodes = None 
        self.opvLines = None
        self.opvTubes = None 
        self.opvDeformedTubes = None

        self._style.AddObserver('SelectionChangedEvent', self.highlight)
        self._style.AddObserver('SelectionChangedEvent', self.updateInfoText)
    
    def plot(self):
        s = time()
        self.reset()
        self.saveNodesBounds()
        self.saveElementsBounds()

        self.opvNodes = NodesActor(self.project.get_nodes(), self.project)
        self.opvLines = LinesActor(self.project.get_elements(), self.project)
        self.opvTubes = TubeActor(self.project.get_elements(), self.project)
        self.opvDeformedTubes = TubeDeformedActor(self.project.get_elements(), self.project)

        self.opvTubes.build()
        self.opvNodes.build()
        self.opvLines.build()
        
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvTubes)
        plt(self.opvNodes)
        plt(self.opvLines)
        plt(self.opvDeformedTubes)
        print('current', time()-s)
    
    def plotDeformed(self):
        try:
            self.opvDeformedTubes.build()
        except Exception as e:
            print(e)

    def showNodes(self, cond=True):
        self.opvNodes.getActor().SetVisibility(cond)

    def showTubes(self, cond=True, transparent=True):
        self.opvTubes.getActor().SetVisibility(cond)
        self.opvTubes.transparent = transparent
    
    def showLines(self, cond=True):
        self.opvLines.getActor().SetVisibility(cond)

    def showDeformedTubes(self, cond=True):
        self.opvDeformedTubes.getActor().SetVisibility(cond)

    # TODO: implement this
    def selectLines(self, cond):
        pass 

    def selectTubes(self, cond):
        pass

    def selectNodes(self, cond):
        pass

    def selectEntities(self, cond):
        pass


    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()
    
    def update(self):
        self.opv.updateDialogs()
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()

    def setPlotRadius(self, plt):
        pass

    # selection 
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
    
    def getListPickedPoints(self):
        return self._style.getListPickedPoints()

    def getListPickedElements(self):
        return self._style.getListPickedElements()

    def getListPickedEntities(self):
        return []
    
    def highlight(self, obj, event):
        visual = [self.opvNodes, self.opvLines, self.opvTubes]
        if any([v is None for v in visual]):
            return

        selectedNodes = self.getListPickedPoints()
        selectedElements = self.getListPickedElements()
        selectedEntities = []
        
        nodesColor = (255, 255, 63)
        linesColor = (10, 10, 10)
        tubesColor = (255, 255, 255)
        selectionColor = (255, 0, 0)

        # clear colors
        self.opvNodes.setColor(nodesColor)
        self.opvLines.setColor(linesColor)
        self.opvTubes.setColor(tubesColor)

        if selectedNodes:
            self.opvNodes.setColor(selectionColor, keys=selectedNodes)

        if selectedElements:
            self.opvLines.setColor(selectionColor, keys=selectedElements)
            self.opvTubes.setColor(selectionColor, keys=selectedElements)

    # info text
    def updateInfoText(self, obj, event):
        text = self.getPointsInfoText()
        self.createInfoText(text)
        self.update()

    def getPointsInfoText(self):
        listSelected = self.getListPickedElements()
        size = len(listSelected)

        if size == 1:
            text = str(listSelected)
        elif size > 1:
            text = f'{size} ELEMENTS IN SELECTION: \n'     
            text += ''.join(str(i)+' ' for i in listSelected[0:10]) + '\n'  
            text += ''.join(str(i)+' ' for i in listSelected[10:20]) + '\n'  
            text += ''.join(str(i)+' ' for i in listSelected[20:30]) + '\n'  
            text += '...' if size>30 else '.'
        else:
            text = ''
        return text
    
    # functions to be removed but currently break the execution
    def getElementsInfoText(self, *args, **kwargs):
        pass
    
    def getEntityInfoText(self, *args, **kwargs):
        pass 

    def getPlotRadius(self, *args, **kwargs):
        return 
    
    def changeColorEntities(self, *args, **kwargs):
        return 