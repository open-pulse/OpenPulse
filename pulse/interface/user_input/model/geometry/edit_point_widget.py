from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget

from pulse import app, UI_DIR

from opps.model import Point


class EditPointWidget(QWidget):
    def __init__(self, geometry_widget):
        super().__init__()

        ui_path = UI_DIR / "model/geometry/edit_point.ui"
        uic.loadUi(ui_path, self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.pipeline = self.project.pipeline
        self.file = self.project.file

        self._define_qt_variables()
        self._create_connections()

    def update(self):
        super().update()

        if not self.pipeline.selected_points:
            return

        *_, last_point = self.pipeline.selected_points
        if not isinstance(last_point, Point):
            return

        self.coord_x.setText(str(round(last_point.x, 8)))
        self.coord_y.setText(str(round(last_point.y, 8)))
        self.coord_z.setText(str(round(last_point.z, 8)))

        enable = last_point in self.pipeline.points
        self.coord_x.setEnabled(enable)
        self.coord_y.setEnabled(enable)
        self.coord_z.setEnabled(enable)

        if enable:
            text = ""
        else:
            text = "Invalid point"

        self.coord_x.setPlaceholderText(text)
        self.coord_y.setPlaceholderText(text)
        self.coord_z.setPlaceholderText(text)

    def _define_qt_variables(self):

        self.coord_x: QLineEdit
        self.coord_y: QLineEdit
        self.coord_z: QLineEdit
        
        self.merge_button: QPushButton
        self.remove_point_button: QPushButton
        self.separete_button: QPushButton
        self.add_flange_button: QPushButton
        self.add_bend_button: QPushButton
        self.add_elbow_button: QPushButton
        self.remove_point_button : QPushButton

    def _create_connections(self):
        self.coord_x.textEdited.connect(self.position_edited_callback)
        self.coord_y.textEdited.connect(self.position_edited_callback)
        self.coord_z.textEdited.connect(self.position_edited_callback)
        self.add_flange_button.clicked.connect(self.add_flange_callback)
        self.add_bend_button.clicked.connect(self.add_bend_callback)
        self.add_elbow_button.clicked.connect(self.add_elbow_callback)
        self.remove_point_button.clicked.connect(self.remove_selection_callback)

    def remove_selection_callback(self):
        self.pipeline.delete_selection()
        app().update()

    def get_position(self):
        dx = self.coord_x.text()
        dy = self.coord_y.text()
        dz = self.coord_z.text()
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
        return dx, dy, dz

    def position_edited_callback(self):
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)
        if not self.pipeline.selected_points:
            return

        *_, last_point = self.pipeline.selected_points
        if not isinstance(last_point, Point):
            return

        try:
            x, y, z = self.get_position()
        except ValueError:
            return

        last_point.set_coords(x, y, z)
        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)

    def add_flange_callback(self):
        return
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)
        editor = self.geometry_widget.editor
        editor.add_flange()
        editor.commit()
        editor.clear_selection()
        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)

    def add_bend_callback(self):
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)
        self.pipeline.add_bend()
        self.pipeline.commit()
        self.pipeline.clear_selection()
        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)

    def add_elbow_callback(self):
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(True)
        self.pipeline.add_elbow()
        self.pipeline.commit()
        self.pipeline.clear_selection()
        app().update()
        app().main_window.geometry_input_wigdet.pushButton_finalize.setDisabled(False)
