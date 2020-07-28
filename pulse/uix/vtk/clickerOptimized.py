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

class vtkInteractorStyleClicker(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, renderer):
        self.__renderer = renderer # OPV vtkRendererBase
        self.__main_renderer = None # vtkRenderer
        self.__secondary_renderer = None #vtkRenderer

        self.__pixelData = vtk.vtkUnsignedCharArray()  
        self.__selection_source = vtk.vtkAppendPolyData()
        self.__selection_mapper = vtk.vtkPolyDataMapper()
        self.__selection_actor = vtk.vtkActor()

        self.__selectedActors = set()
        self.__selectedActorsProperties = dict()
        self.__selectionColor = (255, 0, 0, 255)
        
        self.clickPosition = (0,0)
        self.mousePosition = (0,0)
        self.__leftButtonClicked = False 
        self.__altKeyClicked = False

        self.createObservers()

    def testando(self):
        ra = vtk.vtkRenderer()
        for i in range(0, 10):
            for j in range(0, 10):    
                actor = vtk.vtkActor()
                source = vtk.vtkConeSource()
                mapper = vtk.vtkPolyDataMapper()

                mapper.SetInputConnection(source.GetOutputPort())
                source.SetCenter(i, j, 0)   
                actor.SetMapper(mapper)
                ra.AddActor(actor)
        self.setSecondaryRenderer(ra)

    #
    def getSelectedActors(self):
        return list(self.__selectedActors)

    def setSecondaryRenderer(self, renderer):   
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.AddRenderer(renderer)

        self.__secondary_renderer = renderer
        self.__secondary_renderer.DrawOff()

    def removeSecondaryRenderer(self):
        self.secondary_renderer = None

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
        self.EndRotate()

    #
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
            self.testando()
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
        self.__main_renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        if self.__main_renderer is None:
            print('falta main')
            return 
        if self.__secondary_renderer is None:
            print('falta secondary')
            return 

        if (self.__main_renderer is None) or (self.__secondary_renderer is None):
            print('falta renderer')
            return 

        x1, y1 = self.clickPosition
        x2, y2 = self.mousePosition

        controlPressed = self.GetInteractor().GetControlKey()
        shiftPressed = self.GetInteractor().GetShiftKey()
        altPressed = self.__altKeyClicked

        pickedActors = self.pickActors(x1, y1, x2, y2, tolerance=5)
        
        if controlPressed or shiftPressed:
            self.__selectedActors |= pickedActors      
        elif altPressed:
            self.__selectedActors -= pickedActors  
        else:
            self.__selectedActors = pickedActors

        cam = self.__main_renderer.GetActiveCamera()
        self.__secondary_renderer.SetActiveCamera(cam)
        self.highlight(self.getSelectedActors())

        self.__renderer.updateInfoText()
        self.__renderer.update()

    # 
    def pickActors(self, x1, y1, x2, y2, tolerance=5):
        tooSmall = (abs(x1-x2) < tolerance) or (abs(y1-y2) < tolerance)
        pickedActors = set()

        if tooSmall:
            picker = vtk.vtkPropPicker()
            picker.Pick(x2, y2, 0, self.__secondary_renderer)
            actor = picker.GetActor()
            if actor:
                pickedActors.add(actor)
        else:
            picker = vtk.vtkAreaPicker()
            picker.AreaPick(x1, y1, x2, y2, self.__secondary_renderer)
            pickedActors = set(picker.GetProp3Ds())
        return pickedActors

    def highlight(self, actors):
        self.__main_renderer.RemoveActor(self.__selection_actor)
        self.__selection_source.RemoveAllInputs()
        if len(actors) > 0:
            for actor in actors:
                input_data = actor.GetMapper().GetInput()
                self.__selection_source.AddInputData(input_data)
            self.__selection_mapper.SetInputConnection(self.__selection_source.GetOutputPort())
            self.__selection_actor.SetMapper(self.__selection_mapper)
            self.__selection_actor.GetProperty().SetColor(255,0,0)
            self.__main_renderer.AddActor(self.__selection_actor)
        self.GetInteractor().GetRenderWindow().Render()

    def clear(self):
        if self.__main_renderer is None:
            return
        self.__main_renderer.RemoveActor(self.__selection_actor)
        self.__selection_source.RemoveAllInputs()
        self.__selectedActors = set()

    def getListPickedActors(self):
        listActorsIDs = []
        return listActorsIDs
        for actor in self.getSelectedActors():
            if self.__renderer.actors[actor] == -1:
                continue
            listActorsIDs.append(self.__renderer.actors[actor])