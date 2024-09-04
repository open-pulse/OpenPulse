from vtkmodules.vtkRenderingCore import vtkActor

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.pickers import CellAreaPicker, CellPropertyAreaPicker
from molde.render_widgets import CommonRenderWidget

from pulse.interface.viewer_3d.actors import EditorPointsActor, EditorStagedPointsActor, EditorSelectedPointsActor
from pulse import ICON_DIR, app


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.pipeline = app().project.pipeline

        self.open_pulse_logo = None
        self.pipeline_actor = None
        self.control_points_actor = None
        self.staged_points_actor = None
        self.selected_points_actor = None

        # It is better for an editor to have parallel projection
        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.RemoveAllLights()

        self.set_theme("light")
        self.create_axes()
        self.create_camera_light(0.1, 0.1)

        self._create_connections()
        self.update_plot()
    
    def _create_connections(self):
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        app().main_window.theme_changed.connect(self.set_theme)
        app().main_window.visualization_changed.connect(
            self.visualization_changed_callback
        )

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = self.pipeline.as_vtk()
        self.control_points_actor = EditorPointsActor()
        self.staged_points_actor = EditorStagedPointsActor()
        self.selected_points_actor = EditorSelectedPointsActor()

        # The order matters. It defines wich points will appear first.
        self.add_actors(
            self.pipeline_actor,
            self.control_points_actor,
            self.staged_points_actor,
            self.selected_points_actor,
        )

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)
        self.create_logos(theme)

    def create_logos(self, theme="light"):
        if theme == "light":
            path = ICON_DIR / "logos/OpenPulse_logo_gray.png"
        else:
            path = ICON_DIR / "logos/OpenPulse_logo_white.png"

        if hasattr(self, "open_pulse_logo"):
            self.renderer.RemoveViewProp(self.open_pulse_logo)

        self.open_pulse_logo = self.create_logo(path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def visualization_changed_callback(self):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
        self.control_points_actor.SetVisibility(visualization.points)
        self.staged_points_actor.SetVisibility(visualization.points)
        self.selected_points_actor.SetVisibility(visualization.points)
        self.pipeline_actor.SetVisibility(visualization.tubes)
        opacity = 0.9 if visualization.transparent else 1
        self.pipeline_actor.GetProperty().SetOpacity(opacity)
        self.update()

    def _actor_exists(self):
        actors = [
            self.control_points_actor,
            self.staged_points_actor,
            self.selected_points_actor,
            self.pipeline_actor,
        ]
        return all([actor is not None for actor in actors])

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.control_points_actor)
        self.renderer.RemoveActor(self.staged_points_actor)
        self.renderer.RemoveActor(self.selected_points_actor)

        self.pipeline_actor = None
        self.control_points_actor = None
        self.staged_points_actor = None
        self.selected_points_actor = None

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x, y):
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        join = ctrl_pressed | shift_pressed
        remove = alt_pressed

        if not (join or remove):
            self.pipeline.clear_selection()

        picked_points = self._pick_points(x, y)
        picked_structures = self._pick_structures(x, y)

        # give selection priority to points
        if len(picked_points) == 1 and len(picked_structures) <= 1:
            picked_structures.clear()

        if picked_points:
            self.pipeline.select_points(picked_points, join=join, remove=remove)

        if picked_structures:
            self.pipeline.select_structures(picked_structures, join=join, remove=remove)

        # Only dismiss structure creation if something was actually selected
        something_selected = self.pipeline.selected_points or self.pipeline.selected_structures
        something_staged = self.pipeline.staged_points or self.pipeline.staged_structures
        if something_selected and something_staged:
            self.pipeline.dismiss()

        self.update_selection()

    def _pick_points(self, x, y):
        picked = self._pick_actor(x, y, self.control_points_actor)
        indexes = picked.get(self.control_points_actor, [])
        control_points = [self.pipeline.points[i] for i in indexes]

        return control_points

    def _pick_structures(self, x, y):
        try:
            indexes = self._pick_property(x, y, "cell_identifier", self.pipeline_actor)
            return [self.pipeline.structures[i] for i in indexes]
        except IndexError:
            return list()

    def _pick_actor(self, x, y, actor_to_select):
        actor: vtkActor
        selection_picker = CellAreaPicker()
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == actor_to_select:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

    def _pick_property(self, x, y, property_name, desired_actor):
        selection_picker = CellPropertyAreaPicker(property_name, desired_actor)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == desired_actor:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

    def update_selection(self):
        self.selection_changed.emit()
        self.update_plot(reset_camera=False)
