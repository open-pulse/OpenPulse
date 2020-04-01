import vtk
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMenu, QAction


colors = vtk.vtkNamedColors()

class MouseInteractorPoint(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = parent
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)

        self.listSelectedPoints = []
        self.lastSelectedPointProperty = []
        self.lastSelectedActors = []
        self.position_1 = None
        self.position_2 = None

    def rightButtonReleaseEvent(self, obj, event):
        if (not self.parent.in_points):
            return
        if self.position_1 is None:
            return

        self.position_2 = self.GetInteractor().GetEventPosition()

        #if you already have picked any actor, restore before state
        for i in range(len(self.lastSelectedPointProperty)):
            self.lastSelectedActors[i].GetMapper().ScalarVisibilityOn()
            self.lastSelectedActors[i].GetProperty().DeepCopy(self.lastSelectedPointProperty[i])

        self.lastSelectedActors.clear()
        self.lastSelectedPointProperty.clear()
        self.listSelectedPoints.clear()


        picker = vtk.vtkAreaPicker()
        picker.AreaPick(self.position_1[0], self.position_1[1], self.position_2[0], self.position_2[1], self.GetDefaultRenderer())
        pickedActors = picker.GetProp3Ds()
        for actor in pickedActors:
            current_actor_property = vtk.vtkProperty()
            current_actor_property.DeepCopy(actor.GetProperty())
            self.lastSelectedPointProperty.append(current_actor_property)

            actor.GetMapper().ScalarVisibilityOff()
            actor.GetProperty().SetColor(colors.GetColor3d('Red'))
            actor.GetProperty().SetDiffuse(1.0)
            actor.GetProperty().SetSpecular(0.0)
            self.lastSelectedActors.append(actor)
            self.listSelectedPoints.append(self.parent.actors_points[actor])
        self.parent.update()


    def rightButtonPressEvent(self, obj, event):
        if (not self.parent.in_points):
            return
        self.position_1 = self.GetInteractor().GetEventPosition()

    def leftButtonPressEvent(self, obj, event):
        if (not self.parent.in_points):
            self.OnLeftButtonDown()
            return

        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        actor = picker.GetActor()

        if actor:
            for i in range(len(self.lastSelectedPointProperty)):
                self.lastSelectedActors[i].GetMapper().ScalarVisibilityOn()
                self.lastSelectedActors[i].GetProperty().DeepCopy(self.lastSelectedPointProperty[i])

            self.lastSelectedActors.clear()
            self.lastSelectedPointProperty.clear()
            self.listSelectedPoints.clear()

            current_actor_property = vtk.vtkProperty()
            current_actor_property.DeepCopy(actor.GetProperty())
            self.lastSelectedPointProperty.append(current_actor_property)

            actor.GetMapper().ScalarVisibilityOff()
            actor.GetProperty().SetColor(colors.GetColor3d('Red'))
            actor.GetProperty().SetDiffuse(1.0)
            actor.GetProperty().SetSpecular(0.0)
            self.lastSelectedActors.append(actor)
            self.listSelectedPoints.append(self.parent.actors_points[actor])
            self.parent.update()

        self.OnLeftButtonDown()

    def getListPickedActors(self):
        return self.listSelectedPoints