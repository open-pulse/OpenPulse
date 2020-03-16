import vtk
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMenu, QAction


colors = vtk.vtkNamedColors()

class MouseInteractorEntity(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = parent
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)

        self.LastPickedActor = None
        self.currentEntity = -1
        self.LastPickedProperty = vtk.vtkProperty()

    def rightButtonPressEvent(self, obj, event):
        if (self.LastPickedActor == None):
            return
        if (self.parent.actors_entities[self.LastPickedActor] == -1):
            return
        clickPos = self.GetInteractor().GetEventPosition()
        id_ = self.parent.actors_entities[self.LastPickedActor]
        point_ = QPoint(clickPos[0], clickPos[1])
        menu = QMenu()
        menu.addAction('Entity')
        menu.addAction("Set Material")
        menu.exec_(self.parent.mapToGlobal(point_))
        self.OnRightButtonDown()
        self.OnLeftButtonDown()
        return

    def leftButtonPressEvent(self, obj, event):
        if (not self.parent.in_entities):
            return
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        self.NewPickedActor = picker.GetActor()

        if self.NewPickedActor:
            if self.LastPickedActor:
                self.LastPickedActor.GetMapper().ScalarVisibilityOn()
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            print(self.parent.actors_entities[self.NewPickedActor])
            if (self.parent.actors_entities[self.NewPickedActor] == -1):
                return

            self.parent.setContextMenuPolicy(Qt.CustomContextMenu)

            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())

            self.NewPickedActor.GetMapper().ScalarVisibilityOff()
            self.NewPickedActor.GetProperty().SetColor(colors.GetColor3d('Red'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)

            self.LastPickedActor = self.NewPickedActor

            if (self.LastPickedActor == None):
                return
            if (self.parent.actors_entities[self.LastPickedActor] == -1):
                return

            id_ = self.parent.actors_entities[self.LastPickedActor]
            # point_ = QPoint(clickPos[0], clickPos[1])
            # menu = QMenu()
            # menu.addAction('Entity')
            # menu.addAction("Set Material")
            # menu.exec_(self.parent.parent.mapToGlobal(point_))
            

            #self.parent.customContextMenuRequested.connect(lambda i : self.parent.on_context_menu(i, 0, id_))

        self.OnLeftButtonDown()
        return

    def getLastPickedActor(self):
        if (self.LastPickedActor == None):
            return
        if (self.parent.actors_entities[self.LastPickedActor] == -1):
            return

        return(self.parent.actors_entities[self.LastPickedActor])