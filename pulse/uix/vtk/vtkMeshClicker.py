import vtk 
import PyQt5

from math import sqrt
from time import time

def constrain(number, floor, ceil):
    if number < floor:
        return floor
    elif number > ceil:
        return ceil
    else:
        return number

def distance(p0, p1):
    x0,y0,z0 = p0
    x1,y1,z1 = p1
    dx = x0-x1
    dy = y0-y1
    dz = z0-z1 
    return sqrt(dx*dx + dy*dy + dz*dz)

class vtkMeshClicker(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, rendererMesh):
        self.__rendererMesh = rendererMesh

        self.__pixelData = vtk.vtkUnsignedCharArray()  
        self.__selection_source = vtk.vtkAppendPolyData()
        self.__selection_mapper = vtk.vtkPolyDataMapper()
        self.__selection_actor = vtk.vtkActor()

        self.__selectedPoints = set()
        self.__selectedElements = set()
        self.__selectionColor = (255, 0, 0, 255)
        
        self.clickPosition = (0,0)
        self.mousePosition = (0,0)
        self.__leftButtonClicked = False 
        self.__altKeyClicked = False

        self.createObservers()

    #
    def getSelectedActors(self):
        return list(self.__selectedActors)

    # 
    def createObservers(self):
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.leftButtonReleaseEvent)
        self.AddObserver('RightButtonPressEvent', self.rightButtonPressEvent)
        self.AddObserver('RightButtonReleaseEvent', self.rightButtonReleaseEvent)
        self.AddObserver('MouseMoveEvent', self.mouseMoveEvent)        
        self.AddObserver('KeyPressEvent', self.KeyPressEvent)
        self.AddObserver('KeyReleaseEvent', self.KeyReleaseEvent)

    def releaseButtons(self):
        if self.__leftButtonClicked:
            self.leftButtonReleaseEvent(None, None)
        self.__altKeyClicked = False
        self.clear()
        self.EndRotate()

    def leftButtonPressEvent(self, obj, event):
        self.clickPosition = self.GetInteractor().GetEventPosition()
        self.mousePosition = self.clickPosition
        self.__leftButtonClicked = True
        self.createSelectionBox()
    
    def leftButtonReleaseEvent(self, obj, event):
        if not self.__leftButtonClicked:
            return
        self.__leftButtonClicked = False
        self.clearSelectionBox()
        if obj is None and event is None:
            return
        self.selectActors()

    def rightButtonPressEvent(self, obj, event):
        self.StartRotate()
    
    def rightButtonReleaseEvent(self, obj, event):
        self.EndRotate()

    def mouseMoveEvent(self, obj, event):  
        self.OnMouseMove()
        self.mousePosition = self.GetInteractor().GetEventPosition()
        if self.__leftButtonClicked:
            self.updateSelectionBox()

    def KeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if (key == 'Alt_L') or (key == 'Alt_R'):
            self.__altKeyClicked = True
            
    def KeyReleaseEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if (key == 'Alt_L') or (key == 'Alt_R'):
            self.__altKeyClicked = False

    # 
    def createSelectionBox(self):
        size = self.GetInteractor().GetSize()
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.Render()
        renderWindow.GetRGBACharPixelData(0, 0, size[0]-1, size[1]-1, 0, self.__pixelData)

    def updateSelectionBox(self):
        minx = min(self.clickPosition[0], self.mousePosition[0])
        maxx = max(self.clickPosition[0], self.mousePosition[0])
        miny = min(self.clickPosition[1], self.mousePosition[1])
        maxy = max(self.clickPosition[1], self.mousePosition[1])

        size = self.GetInteractor().GetSize()

        minx = constrain(minx, 0, size[0])
        maxx = constrain(maxx, 0, size[0])
        miny = constrain(miny, 0, size[1])
        maxy = constrain(maxy, 0, size[1])

        temp_pixels = vtk.vtkUnsignedCharArray()
        temp_pixels.DeepCopy(self.__pixelData)

        for x in range(minx, maxx, 2):
            for y in range(miny, maxy, 2):
                pixel = y*size[0] + x
                temp_pixels.SetTuple(pixel, self.__selectionColor)
        
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.SetRGBACharPixelData(0, 0, size[0]-1, size[1]-1, temp_pixels, 0)
        renderWindow.Frame()

    def clearSelectionBox(self):
        size = self.GetInteractor().GetSize()
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.Render()
        renderWindow.SetRGBACharPixelData(0, 0, size[0]-1, size[1]-1, self.__pixelData, 0)

    #
    def selectActors(self):
        x0, y0 = self.clickPosition
        x1, y1 = self.mousePosition

        controlPressed = bool(self.GetInteractor().GetControlKey())
        shiftPressed = bool(self.GetInteractor().GetShiftKey())
        altPressed = self.__altKeyClicked

        pickedPoints = self.pickPoints(x0,y0,x1,y1)
        pickedElements = self.pickElements(x0,y0,x1,y1)

        if len(pickedPoints) == 1 and len(pickedElements) == 1:
            pickedElements.clear()

        # add or remove selection with control, shift and alt
        if controlPressed or shiftPressed:
            self.__selectedPoints |= pickedPoints
            self.__selectedElements |= pickedElements      
        elif altPressed:
            self.__selectedPoints -= pickedPoints
            self.__selectedElements -= pickedElements  
        else:
            self.__selectedPoints = pickedPoints
            self.__selectedElements = pickedElements
        
        self.InvokeEvent('SelectionChangedEvent')

    # 
    def pickPoints(self, x0, y0, x1, y1, tolerance=10):
        tooSmall = (abs(x0-x1) < tolerance) or (abs(y0-y1) < tolerance)
        if tooSmall:
            x0, x1 = (x0-tolerance//2), (x1+tolerance//2)
            y0, y1 = (y0-tolerance//2), (y1+tolerance//2)

        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        renderer = self.__rendererMesh._renderer
        picker.AreaPick(x0,y0,x1,y1,renderer)
        extractor.SetFrustum(picker.GetFrustum())

        pickedPoints = set()
        for key, coord in self.__rendererMesh.nodesData.items():
            bounds = [n for xyz in zip(coord,coord) for n in xyz] # xyz -> xxyyzz
            if extractor.OverallBoundsTest(bounds):
                pickedPoints.add(key)
                if tooSmall: # isso é uma gambiarra rápida
                    break             
        return pickedPoints
    
    def pickElements(self, x0, y0, x1, y1, tolerance=10):
        tooSmall = (abs(x0-x1) < tolerance) or (abs(y0-y1) < tolerance)

        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        renderer = self.__rendererMesh._renderer
        picker.AreaPick(x0,y0,x1,y1,renderer)
        extractor.SetFrustum(picker.GetFrustum())

        pickedElements = set()
        for key, bound in self.__rendererMesh.elementsData.items():
            if extractor.OverallBoundsTest(bound):
                pickedElements.add(key)
                if tooSmall: # isso é uma gambiarra rápida
                    break
        return pickedElements

    def clear(self):
        self.__rendererMesh.getRenderer().RemoveActor(self.__selection_actor)
        self.__selection_source.RemoveAllInputs()
        self.__selectedActors = set()
        self.__rendererMesh.updateInfoText()
        
    def getListPickedPoints(self):
        return list(self.__selectedPoints)
    
    def getListPickedElements(self):
        return list(self.__selectedElements)
