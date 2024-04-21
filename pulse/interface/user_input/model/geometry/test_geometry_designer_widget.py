from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QStackedWidget, QTabWidget
from PyQt5 import uic

from copy import deepcopy

from opps.model import Pipeline

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler


class GeometryDesignerWidget(QWidget):
    def __init__(self, render_widget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/test_geometry_designer_widget.ui"
        uic.loadUi(ui_path, self)

        self.render_widget = render_widget
        self.geometry_handler = GeometryHandler()

        self.project = app().project
        self.pipeline = self.project.pipeline
        self.file = self.project.file

        # This dict is passed as argument for the current
        # creation function, either if it is a pipe, a bend,
        # an i-beam, a square beam, etc.
        # If the argument is useless to the current function,
        # like a diameter in a square beam, the argument
        # will be ignored, and no errors will be raised. 
        self.structure_kwargs = dict()
        self.add_structure_function = self.pipeline.add_bent_pipe
        self.attach_selection_function = self.pipeline.connect_bent_pipes

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self.setContentsMargins(2,2,2,2)

    def _define_qt_variables(self):
        self.x_line_edit: QLineEdit
        self.y_line_edit: QLineEdit
        self.z_line_edit: QLineEdit

        self.unity_combobox: QComboBox
        self.structure_combobox: QComboBox

        self.set_section_button: QPushButton
        self.set_material_button: QPushButton
        self.set_fluid_button: QPushButton

        self.add_button: QPushButton
        self.attach_button: QPushButton
        self.delete_button: QPushButton
    
    def _create_layout(self):
        pass

    def _create_connections(self):
        self.render_widget.selection_changed.connect(self.selection_callback)

        self.unity_combobox.currentIndexChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentIndexChanged.connect(self.structure_type_changed_callback)
        
        self.set_section_button.clicked.connect(self.section_callback)
        self.set_material_button.clicked.connect(self.material_callback)
        self.set_fluid_button.clicked.connect(self.fluid_callback)

        self.x_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)
        self.y_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)
        self.z_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)        

    def selection_callback(self):
        pass

    def unity_changed_callback(self):
        pass

    def structure_type_changed_callback(self):
        pass

    def section_callback(self):
        pass 

    def material_callback(self):
        pass

    def fluid_callback(self):
        pass

    def sizes_coordinates_changed_callback(self):
        if not callable(self.add_structure_function):
            return

        try:
            deltas = self._get_deltas()
        except ValueError:
            return

        radius = self._get_radius()
        self.structure_kwargs["curvature_radius"] = radius

        self.pipeline.dismiss()
        kwargs = deepcopy(self.structure_kwargs)
        self.add_structure_function(deltas, **kwargs)
        self.render_widget.update_plot()

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.render_widget.update_plot()
        self._reset_deltas()

    def attach_selection_callback(self):
        self.pipeline.dismiss()
        if callable(self.attach_selection_function):
            kwargs = deepcopy(self.structure_kwargs)
            self.attach_selection_function(**kwargs)
        self.pipeline.commit()
        self.render_widget.update_plot()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot()
        self._reset_deltas()

    def _get_deltas(self):
        dx = float(self.x_line_edit.text() or 0)
        dy = float(self.y_line_edit.text() or 0)
        dz = float(self.z_line_edit.text() or 0)
        return dx, dy, dz

    def _get_radius(self):
        return 0.3
    
    def _reset_deltas(self):
        pass
