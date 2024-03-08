import vtk

colors = vtk.vtkNamedColors()

class vtkInteractorBase(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, renderer=None):
        self.renderer = renderer

        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)
        self.AddObserver("MouseMoveEvent", self.moveEvent)

        self.listSelectedEntities = []
        self.lastSelectedEntitiesProperty = []
        self.lastSelectedActors = []
        self.posA = None
        self.posB = None
        self.boxSelectMode = False

    def allowedPicker(self):
        return self.renderer.getInUse() and self.renderer.getUsePicker()

    def moveEvent(self, obj, event):
        super().OnMouseMove()
        if self.posA is None:
            return
        self.posB = self.GetInteractor().GetEventPosition()
        self.renderer.updateAreaPicker(self.posA, self.posB)

    def rightButtonReleaseEvent(self, obj, event):
        if not self.allowedPicker():
            return
        if self.posA is None:
            return

        self.posB = self.GetInteractor().GetEventPosition()

        #if you already have picked any actor, restore before state
        for i in range(len(self.lastSelectedEntitiesProperty)):
            self.lastSelectedActors[i].GetProperty().DeepCopy(self.lastSelectedEntitiesProperty[i])

        self.lastSelectedActors.clear()
        self.lastSelectedEntitiesProperty.clear()
        self.listSelectedEntities.clear()


        picker = vtk.vtkAreaPicker()
        picker.AreaPick(self.posA[0], self.posA[1], self.posB[0], self.posB[1], self.GetDefaultRenderer())
        pickedActors = picker.GetProp3Ds()
        for actor in pickedActors:
            if self.renderer.actors[actor] == -1:
                continue
            current_actor_property = vtk.vtkProperty()
            current_actor_property.DeepCopy(actor.GetProperty())
            self.lastSelectedEntitiesProperty.append(current_actor_property)

            actor.GetProperty().SetColor(colors.GetColor3d('Red'))
            actor.GetProperty().SetDiffuse(1.0)
            actor.GetProperty().SetSpecular(0.0)
            self.lastSelectedActors.append(actor)
            self.listSelectedEntities.append(self.renderer.actors[actor])
        self.renderer.updateInfoText()
        self.renderer.updateAreaPicker((0,0), (0,0))
        self.posA = None
        self.renderer.update()


    def rightButtonPressEvent(self, obj, event):
        if not self.allowedPicker():
            return
        self.posA = self.GetInteractor().GetEventPosition()
        

    def leftButtonPressEvent(self, obj, event):
        if not self.allowedPicker():
            self.OnLeftButtonDown()
            return
        
        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        actor = picker.GetActor()

        if actor and self.renderer.actors[actor] != -1:
            for i in range(len(self.lastSelectedEntitiesProperty)):
                self.lastSelectedActors[i].GetProperty().DeepCopy(self.lastSelectedEntitiesProperty[i])

            self.lastSelectedActors.clear()
            self.lastSelectedEntitiesProperty.clear()
            self.listSelectedEntities.clear()

            current_actor_property = vtk.vtkProperty()
            current_actor_property.DeepCopy(actor.GetProperty())
            self.lastSelectedEntitiesProperty.append(current_actor_property)

            actor.GetProperty().SetColor(colors.GetColor3d('Red'))
            actor.GetProperty().SetDiffuse(1.0)
            actor.GetProperty().SetSpecular(0.0)
            self.lastSelectedActors.append(actor)
            self.listSelectedEntities.append(self.renderer.actors[actor])
            self.renderer.updateInfoText()
            self.renderer.update()

        self.OnLeftButtonDown()

    def getListPickedActors(self):
        return self.listSelectedEntities

    def clear(self):
        self.lastSelectedActors.clear()
        self.lastSelectedEntitiesProperty.clear()
        self.listSelectedEntities.clear()