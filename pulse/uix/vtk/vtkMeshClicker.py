import vtk
from PyQt5 import Qt, QtCore
import numpy as np

from functools import partial
from math import sqrt
from time import time


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


class vtkMeshClicker(vtk.vtkInteractorStyleTrackballCamera):
    '''
    Class that heritage(?) from vtkInteractorStyleTrackballCamera.
    This handles how the user controls the camera, mouse clicks, and stuff like that
    in the renderer.

    Parameters
    ----------
    rendererMesh: rendererMesh class

    '''

    def __init__(self, rendererMesh):
        self.__rendererMesh = rendererMesh

        self.__pixelData = vtk.vtkUnsignedCharArray()
        self.__selectedPoints = set()
        self.__selectedElements = set()
        self.__selectedEntities = set()
        self.__selectionColor = (255, 0, 0, 255)

        self.clickPosition = (0, 0)
        self.mousePosition = (0, 0)
        self.center_of_rotation = None
        self.__leftButtonClicked = False
        self.__rightButtonClicked = False
        self.__rotating = False
        self.picker = vtk.vtkPropPicker()

        self.make_rotation_sphere()
        self.createObservers()

    #
    def createObservers(self):
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.leftButtonReleaseEvent)
        self.AddObserver('RightButtonPressEvent', self.rightButtonPressEvent)
        self.AddObserver('RightButtonReleaseEvent', self.rightButtonReleaseEvent)
        self.AddObserver('MouseMoveEvent', self.mouseMoveEvent)
        self.AddObserver('KeyPressEvent', self.KeyPressEvent)
        self.AddObserver('KeyReleaseEvent', self.KeyReleaseEvent)
        self.AddObserver('MouseWheelForwardEvent', self.MouseWheelForward)
        self.AddObserver('MouseWheelBackwardEvent', self.MouseWheelBackward)

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
        self.clickPosition = self.GetInteractor().GetEventPosition()
        self.mousePosition = self.clickPosition
        self.__rightButtonClicked = True
        renderer = self.__rendererMesh._renderer

        picker = vtk.vtkPropPicker()
        picker.Pick(self.clickPosition[0], self.clickPosition[1], 0, renderer)
        pos = picker.GetPickPosition()

        if pos != (0, 0, 0):
            self.center_of_rotation = pos

        else:
            self.center_of_rotation = self.__rendererMesh.project.preprocessor.camera_rotation_center
            # x0, x1, y0, y1, z0, z1 = renderer.ComputeVisiblePropBounds()
            # self.center_of_rotation = [ (x0+x1)/2,
            #                             (y0+y1)/2,
            #                             (z0+z1)/2 ]

        self.sphere_rotation_actor.SetPosition(self.center_of_rotation)
        renderer.AddActor(self.sphere_rotation_actor)

        self.__rotating = True

    def rightButtonReleaseEvent(self, obj, event):
        renderer = self.__rendererMesh._renderer
        renderer.RemoveActor(self.sphere_rotation_actor)
        self.GetInteractor().Render()

        self.__rightButtonClicked = False
        self.__rotating = False
        self.EndDolly()

    def mouseMoveEvent(self, obj, event):
        self.OnMouseMove()
        self.mousePosition = self.GetInteractor().GetEventPosition()

        if self.__rotating:
            self.rotate()

        if self.__leftButtonClicked:
            self.updateSelectionBox()

        if self.__rightButtonClicked and self.center_of_rotation is not None:
            renderer = self.__rendererMesh._renderer
            camera = renderer.GetActiveCamera()

    def KeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if (key == 'Alt_L') or (key == 'Alt_R'):
            self.__altKeyClicked = True

    def KeyReleaseEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if (key == 'Alt_L') or (key == 'Alt_R'):
            self.__altKeyClicked = False

    def make_rotation_sphere(self):
        colors = vtk.vtkNamedColors()
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetRadius(0.01)
        sphereSource.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(sphereSource.GetOutput())

        self.sphere_rotation_actor = vtk.vtkActor()
        self.sphere_rotation_actor.SetMapper(mapper)
        self.sphere_rotation_actor.GetProperty().SetColor(colors.GetColor3d("red"))

    def rotate(self):

        renderer = self.__rendererMesh._renderer

        if renderer is None:
            return

        rwi = self.GetInteractor()
        dx = rwi.GetEventPosition()[0] - rwi.GetLastEventPosition()[0]
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]

        size = renderer.GetRenderWindow().GetSize()
        delta_elevation = -20.0 / size[1]
        delta_azimuth = -20.0 / size[0]

        motion_factor = 10

        rxf = dx * delta_azimuth * motion_factor
        ryf = dy * delta_elevation * motion_factor

        camera = renderer.GetActiveCamera()

        self.rotate_cam(rxf, ryf)

        camera.OrthogonalizeViewUp()

        renderer.ResetCameraClippingRange()

        if rwi.GetLightFollowCamera():
            renderer.UpdateLightsGeometryToFollowCamera()

        rwi.Render()

    def rotate_cam(self, anglex, angley):

        renderer = self.__rendererMesh._renderer
        camera = renderer.GetActiveCamera()

        transform_camera = vtk.vtkTransform()
        transform_camera.Identity()

        axis = [
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 0),
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 1),
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 2),
        ]

        saved_view_up = camera.GetViewUp()
        transform_camera.RotateWXYZ(angley, axis)
        new_view_up = transform_camera.TransformPoint(camera.GetViewUp())
        camera.SetViewUp(new_view_up)
        transform_camera.Identity()

        cor = self.center_of_rotation

        transform_camera.Translate(+cor[0], +cor[1], +cor[2])
        transform_camera.RotateWXYZ(anglex, camera.GetViewUp())
        transform_camera.RotateWXYZ(angley, axis)
        transform_camera.Translate(-cor[0], -cor[1], -cor[2])

        new_camera_position = transform_camera.TransformPoint(
            camera.GetPosition())
        camera.SetPosition(new_camera_position)

        new_focal_point = transform_camera.TransformPoint(
            camera.GetFocalPoint())
        camera.SetFocalPoint(new_focal_point)

        camera.SetViewUp(saved_view_up)

        camera.Modified()

    def MouseWheelForward(self, obj, event):

        int_pos = self.GetInteractor().GetEventPosition()

        self.FindPokedRenderer(int_pos[0], int_pos[1])

        if self.GetCurrentRenderer() is None:
            return
        
        motion_factor = 10
        mouse_motion_factor = 1

        factor = motion_factor * 0.2 * mouse_motion_factor

        self.dolly(1.1 ** factor)

        self.ReleaseFocus()
        

    def MouseWheelBackward(self, obj, event):
        int_pos = self.GetInteractor().GetEventPosition()

        self.FindPokedRenderer(int_pos[0], int_pos[1])

        if self.GetCurrentRenderer() is None:
             return
        
        motion_factor = 10
        mouse_motion_factor = 1

        factor = motion_factor * -0.2 * mouse_motion_factor

        self.dolly(1.1 ** factor)
        
        self.ReleaseFocus()


    def dolly(self, factor):
        renderer = self.__rendererMesh._renderer
        camera = renderer.GetActiveCamera()
        cursor = self.GetInteractor().GetEventPosition()

        if factor <= 0:
            return

        cam_up = np.array(camera.GetViewUp())
        cam_in =  np.array(camera.GetDirectionOfProjection())
        cam_side = np.cross(cam_in, cam_up)

        displacements = self._get_dolly_displacements(
            factor,
            cursor,
            camera,
            renderer,
        )

        camera_position =  np.array(camera.GetPosition())
        focal_point = np.array(camera.GetFocalPoint())
        rotated_displacements = cam_side * displacements[0] + cam_up * displacements[1]
        camera.SetPosition(camera_position + rotated_displacements)
        camera.SetFocalPoint(focal_point + rotated_displacements)
        
        if camera.GetParallelProjection():
            camera.SetParallelScale(camera.GetParallelScale() / factor)
        else:
            camera.Dolly(factor)
            if self.GetAutoAdjustCameraClippingRange():
                renderer.ResetCameraClippingRange()

        if self.GetInteractor().GetLightFollowCamera():
            renderer.UpdateLightsGeometryToFollowCamera()

        self.GetInteractor().Render()

    def _get_dolly_displacements(self, factor, cursor, camera, renderer):
        cursor = np.array(cursor)
        view_center = np.array(renderer.GetSize()) / 2
        cursor_to_center = cursor - view_center

        if camera.GetParallelProjection():
            view_height = 2 * camera.GetParallelScale()
        else:
            correction = camera.GetDistance()
            view_height = 2 * correction * np.tan(0.5 * camera.GetViewAngle() / 57.296)
        
        scale = view_height / renderer.GetSize()[1]
        return cursor_to_center * scale * (1 - 1/factor)

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

        # give preference to points selection
        if len(pickedPoints) == 1 and len(pickedElements) == 1:
            pickedElements.clear()

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
        entities = set()

        for index, line in self.__rendererMesh.lineToElements.items():
            if pickedElements.intersection(line):
                entities.add(index)

        return entities

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
