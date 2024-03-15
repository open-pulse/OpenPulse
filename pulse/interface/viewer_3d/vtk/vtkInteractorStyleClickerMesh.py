import vtk 
import PyQt5

from time import time

def constrain(number, floor, ceil):
    if number < floor:
        return floor
    elif number > ceil:
        return ceil
    else:
        return number

class vtkInteractorStyleClickerMesh(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, renderer):
        self.__renderer = renderer
        self.__selectionColor = (255, 0, 0, 255)
        self.__pixelData = vtk.vtkUnsignedCharArray()  
        self.__selectedActors = set()
        self.__selectedActorsProperties = dict()
        self.__callOnSelection = (None, None, None)
        self.__leftButtonClicked = False 
        self.__altKeyClicked = False

        self.createObservers()

    def releaseButtons(self):
        if self.__leftButtonClicked:
            self.leftButtonReleaseEvent(None, None)
        self.EndRotate()

    def getSelectedActors(self):
        return list(self.__selectedActors)

    def callOnSelection(self, function, args=list(), kwargs=dict()):
        self.__callOnSelection = (function, args, kwargs)

    # 
    def createObservers(self):
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.leftButtonReleaseEvent)
        self.AddObserver('RightButtonPressEvent', self.rightButtonPressEvent)
        self.AddObserver('RightButtonReleaseEvent', self.rightButtonReleaseEvent)
        self.AddObserver('MouseMoveEvent', self.mouseMoveEvent)        
        self.AddObserver('KeyPressEvent', self.KeyPressEvent)
        self.AddObserver('KeyReleaseEvent', self.KeyReleaseEvent)
    
    def leftButtonPressEvent(self, obj, event):
        self.clickPosition = self.GetInteractor().GetEventPosition()
        self.__leftButtonClicked = True
        self.createSelectionBox()
    
    def leftButtonReleaseEvent(self, obj, event):
        self.__leftButtonClicked = False
        self.clearSelectionBox()
        self.pickActors()

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
    def pickActors(self):
        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        if renderer is None:
            return 

        self.lowlight(self.getSelectedActors())

        x1, y1 = self.clickPosition
        x2, y2 = self.mousePosition

        tolerance = 5 
        tooSmall = (abs(x1-x2) < tolerance) or (abs(y1-y2) < tolerance)
        pickedActors = set()

        if tooSmall:
            picker = vtk.vtkPropPicker()
            picker.Pick(x2, y2, 0, renderer)
            actor = picker.GetActor()
            if actor:
                pickedActors.add(actor)
        else:
            picker = vtk.vtkAreaPicker()
            picker.AreaPick(x1, y1, x2, y2, renderer)
            actors = set(picker.GetProp3Ds())
            pickedActors.update(actors)

        controlPressed = self.GetInteractor().GetControlKey()
        shiftPressed = self.GetInteractor().GetShiftKey()
        altPressed = self.__altKeyClicked

        if self.checkPoints(pickedActors) or self.checkElements(pickedActors):
            self.pickActors()
            return

        if controlPressed or shiftPressed:
            self.__selectedActors |= pickedActors      
        elif altPressed:
            self.__selectedActors -= pickedActors  
        else:
            self.__selectedActors = pickedActors

        self.highlight(self.getSelectedActors())       

        function, args, kwargs = self.__callOnSelection
        if function is not None:
            actors = self.getSelectedActors()
            function(actors, *args, **kwargs)

        self.__renderer.updateInfoText()
        self.__renderer.update()

    def highlight(self, actors):
        for actor in actors:
            try:
                self.__renderer.pointsActors[actor] #if
            except:
                try:
                    self.__renderer.elementsActors[actor]
                except:
                    continue
            if actor in self.__selectedActorsProperties:
                continue
            current_property = vtk.vtkProperty()
            current_property.DeepCopy(actor.GetProperty())
            self.__selectedActorsProperties[actor] = current_property
            actor.GetProperty().SetColor(255,0,0)
        self.GetInteractor().GetRenderWindow().Render()

    def lowlight(self, actors):
        for actor in actors:
            try:
                self.__renderer.pointsActors[actor]
                if actor is None:
                    continue
                last_property = self.__selectedActorsProperties[actor]
                actor.GetProperty().DeepCopy(last_property)
                self.__selectedActorsProperties.pop(actor)
            except:
                pass

            try:
                self.__renderer.elementsActors[actor]
                if actor is None:
                    continue
                last_property = self.__selectedActorsProperties[actor]
                actor.GetProperty().DeepCopy(last_property)
                self.__selectedActorsProperties.pop(actor)
            except:
                pass
            
    def clear(self):
        self.lowlight(self.getSelectedActors())
        self.__selectedActors = set()

    def getListPickedActorsPoints(self):
        listActorsIDs = []
        for actor in self.getSelectedActors():
            try:
                if self.__renderer.pointsActors[actor] == -1:
                    continue
                listActorsIDs.append(self.__renderer.pointsActors[actor])
            except Exception:
                continue
        return listActorsIDs

    def getListPickedActorsElements(self):
        listActorsIDs = []
        for actor in self.getSelectedActors():
            try:
                if self.__renderer.elementsActors[actor] == -1:
                    continue
                listActorsIDs.append(self.__renderer.elementsActors[actor])
            except Exception:
                continue
        return listActorsIDs

    def checkPoints(self, pickedActors):
        find = False
        for actor in pickedActors:
            try:
                if self.__renderer.linePointsActors[actor] == -1:
                    continue
                self.__renderer.plotPoints(self.__renderer.linePointsActors[actor])
                find = True
            except Exception:
                continue
        return find

    def checkElements(self, pickedActors):
        find = False
        for actor in pickedActors:
            try:
                if self.__renderer.lineElementsActors[actor] == -1:
                    continue
                self.__renderer.plotElements(self.__renderer.lineElementsActors[actor])
                find = True
            except Exception:
                continue
        return find