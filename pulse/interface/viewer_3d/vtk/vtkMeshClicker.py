import vtk
from PyQt5 import Qt, QtCore
import numpy as np

from functools import partial
from math import sqrt
from time import time
from pulse.interface.viewer_3d.vtk.vtkInteractorStyleArcballCamera import vtkInteractorStyleArcballCamera

def constrain(number, floor, ceil):
    '''
    Constrains a number between a given interval.

    Parameters
    ----------
    number: int, float  
        number to be constrained.

    float: int, float
        inferior limit.

    ceil: int, float
        superior limit.

    Returns
    -------
    out: int, float
        constrained number.    
    '''

    if number < floor:
        return floor
    elif number > ceil:
        return ceil
    else:
        return number


def distance(p0, p1):
    '''
    Computes the distance between 2 3-dimensional points

    Parameters
    ----------
    p0: iterable of numbers
        sequence of 3 numerical values representing a position.

    p1: iterable of numbers
        sequence of 3 numerical values representing a position.

    Returns
    -------
    out: float 
        distance between these points.

    '''

    x0, y0, z0 = p0
    x1, y1, z1 = p1
    dx = x0-x1
    dy = y0-y1
    dz = z0-z1
    return sqrt(dx*dx + dy*dy + dz*dz)


def getVertsFromBounds(bounds):
    '''
    Get the verices from a sequence of bounds.

    Parameters
    ----------
    bounds: iterable of numbers
        sequence of 6 numerical values representing the min and max bound
        for each of x,y,z coordinates. 

    Returns 
    -------
    verts: list of tuples representing the position of each vertice
    '''

    x0, x1, y0, y1, z0, z1 = bounds
    verts = []
    verts.append((x0, y0, z0))
    verts.append((x0, y0, z1))
    verts.append((x0, y1, z0))
    verts.append((x0, y1, z1))
    verts.append((x1, y0, z0))
    verts.append((x1, y0, z1))
    verts.append((x1, y1, z0))
    return verts
    verts.append((x1, y1, z1))


def distanceBoundsToPoint(point, bounds):
    '''
    Calculate the minimal distance between a point and a set of bounds. 

    Parameters
    ----------
    point: iterable of numbers
        sequence of 3 numerical values representing a position.

    bounds: iterable of numbers
        sequence of 6 numerical values representing the min and max bound
        for each of x,y,z coordinates. 

    Returns
    -------
    minDist: float

    '''

    verts = getVertsFromBounds(bounds)
    minDist = None
    for vertice in verts:
        if (minDist is None) or (distance(vertice, point) < minDist):
            minDist = distance(vertice, point)
    return minDist


class vtkMeshClicker(vtkInteractorStyleArcballCamera):
    '''
    Class that heritage(?) from vtkInteractorStyleTrackballCamera.
    This handles how the user controls the camera, mouse clicks, and stuff like that
    in the renderer.

    Parameters
    ----------
    rendererMesh: rendererMesh class

    '''

    def __init__(self, rendererMesh):
        super().__init__()
        self.__rendererMesh = rendererMesh

        self.__pixelData = vtk.vtkUnsignedCharArray()
        self.__selectedPoints = set()
        self.__selectedElements = set()
        self.__selectedEntities = set()
        self.__selectionColor = (255, 0, 0, 255)

        self.clickPosition = (0, 0)
        self.mousePosition = (0, 0)
        self.__leftButtonClicked = False
        self.__rightButtonClicked = False

        self.createObservers()

    #
    def createObservers(self):
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.leftButtonReleaseEvent)
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

    def createSelectionBox(self):
        size = self.GetInteractor().GetSize()
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.Render()
        renderWindow.GetRGBACharPixelData(
            0, 0, size[0]-1, size[1]-1, 0, self.__pixelData)

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
        renderWindow.SetRGBACharPixelData(
            0, 0, size[0]-1, size[1]-1, temp_pixels, 0)
        renderWindow.Frame()

    def clearSelectionBox(self):
        size = self.GetInteractor().GetSize()
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.Render()
        renderWindow.SetRGBACharPixelData(
            0, 0, size[0]-1, size[1]-1, self.__pixelData, 0)

    #
    def selectActors(self):
        x0, y0 = self.clickPosition
        x1, y1 = self.mousePosition

        modifiers = Qt.QApplication.keyboardModifiers()

        controlPressed = modifiers == QtCore.Qt.ControlModifier
        shiftPressed = modifiers == QtCore.Qt.ShiftModifier
        altPressed = modifiers == QtCore.Qt.AltModifier

        pickedPoints = self.pickPoints(x0, y0, x1, y1)
        pickedElements = self.pickElements(x0, y0, x1, y1)
        pickedEntities = self.pickEntities(pickedElements)

        tolerance = 10  # pixels
        box_selection = (abs(x0-x1) >= tolerance) or (abs(y0-y1) >= tolerance)
        self.selectionPriority(pickedPoints, pickedElements, pickedEntities, box_selection)

        # add or remove selection with control, shift and alt
        if controlPressed:
            self.__selectedPoints ^= pickedPoints
            self.__selectedElements ^= pickedElements      
            self.__selectedEntities ^= pickedEntities
        elif shiftPressed:
            self.__selectedPoints |= pickedPoints
            self.__selectedElements |= pickedElements
            self.__selectedEntities |= pickedEntities
        elif altPressed:
            self.__selectedPoints -= pickedPoints
            self.__selectedElements -= pickedElements
            self.__selectedEntities -= pickedEntities
        else:
            self.__selectedPoints = pickedPoints
            self.__selectedElements = pickedElements
            self.__selectedEntities = pickedEntities

        self.InvokeEvent('SelectionChangedEvent')

    def selectionPriority(self, picked_points, picked_elements, picked_entities, box_selection=False):
        if box_selection:
            return

        # give preference to points selection
        if len(picked_points) == 1 and len(picked_elements) == 1:
            picked_elements.clear()

    #
    def pickPoints(self, x0, y0, x1, y1, tolerance=10):
        tooSmall = (abs(x0-x1) < tolerance) or (abs(y0-y1) < tolerance)
        if tooSmall:
            x0, x1 = (x0-tolerance//2), (x1+tolerance//2)
            y0, y1 = (y0-tolerance//2), (y1+tolerance//2)

        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        renderer = self.__rendererMesh._renderer
        picker.AreaPick(x0, y0, x1, y1, renderer)
        extractor.SetFrustum(picker.GetFrustum())

        nodeBounds = self.__rendererMesh.nodesBounds
        camPos = renderer.GetActiveCamera().GetPosition()
        def distanceFromCamera(key): return distanceBoundsToPoint(
            camPos, nodeBounds[key])
        pickedPoints = {key for key, bound in nodeBounds.items(
        ) if extractor.OverallBoundsTest(bound)}

        # when not box selecting, pick only the closest point
        if tooSmall and pickedPoints:
            closest = min(pickedPoints, key=distanceFromCamera)
            pickedPoints.clear()
            pickedPoints.add(closest)

        return pickedPoints

    def pickElements(self, x0, y0, x1, y1, tolerance=10):
        tooSmall = (abs(x0-x1) < tolerance) or (abs(y0-y1) < tolerance)
        if tooSmall:
            x0, x1 = (x0-tolerance//2), (x1+tolerance//2)
            y0, y1 = (y0-tolerance//2), (y1+tolerance//2)

        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        renderer = self.__rendererMesh._renderer
        picker.AreaPick(x0, y0, x1, y1, renderer)
        extractor.SetFrustum(picker.GetFrustum())

        elementsBounds = self.__rendererMesh.elementsBounds
        camPos = renderer.GetActiveCamera().GetPosition()
        def distanceFromCamera(key): return distanceBoundsToPoint(
            camPos, elementsBounds[key])
        pickedElements = {key for key, bound in elementsBounds.items(
        ) if extractor.OverallBoundsTest(bound)}

        # when not box selecting, pick only the closest element
        if tooSmall and pickedElements:
            closest = min(pickedElements, key=distanceFromCamera)
            pickedElements.clear()
            pickedElements.add(closest)

        return pickedElements

        # ===========================

    def pickEntities(self, pickedElements):
        lines = set()

        for index, line in self.__rendererMesh.lineToElements.items():
            if pickedElements.intersection(line):
                lines.add(index)

        return lines

    def clear(self):
        self.__selectedPoints.clear()
        self.__selectedElements.clear()
        self.__selectedEntities.clear()
        self.InvokeEvent('SelectionChangedEvent')

    def getListPickedPoints(self):
        return list(self.__selectedPoints)

    def getListPickedElements(self):
        return list(self.__selectedElements)

    def getListPickedLines(self):
        return list(self.__selectedEntities)
