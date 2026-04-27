import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QCloseEvent

from pulse import app
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.ui_generated.model.setup.structural.inertial_load_input_ui import (
    InertialLoadInput_UI,
)
from pulse.interface.user_input.model.setup.user_input import UserInput
from pulse.model.structural_element import DOF_PER_NODE_STRUCTURAL


error_title = "Error"
warning_title = "Warning"

class SetInertialLoad(UserInput, InertialLoadInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor
        
        self._initialize()
        self._configure_validators()
        self._create_connections()
        self._load_inertia_load_setup()
        self.exec()

    def _initialize(self):
        self.complete = False

    def _configure_validators(self):
        validator = StrictDoubleValidator(-1e8, 1e8, 6)
        self.lineEdit_acceleration_x_axis.setValidator(validator)
        self.lineEdit_acceleration_y_axis.setValidator(validator)
        self.lineEdit_acceleration_z_axis.setValidator(validator)

    def _create_connections(self):
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)

    def check_gravity_values(self):

        self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        line_edits = [
            self.lineEdit_acceleration_x_axis,
            self.lineEdit_acceleration_y_axis,
            self.lineEdit_acceleration_z_axis,
        ]

        line_edits: list[QLineEdit]
        for i, line_edit in enumerate(line_edits):
            if line_edit.text() == "":
                continue

            self.gravity[i] = float(line_edit.text())

        # if self.gravity.any() == 0:
        #     self.hide()
        #     title = "Invalid input detected"
        #     message = "Enter a non-null gravity vector to proceed. The null gravity "
        #     message += "vector does not provide an effective static loading."
        #     PrintMessageInput([warning_title, title, message])
        #     return True

        return False

    def attribute_callback(self):

        if self.check_gravity_values():
            return

        stiffening_effect = self.checkBox_stiffening_effect.isChecked()

        inertia_load = {
            "gravity" : list(self.gravity),
            "stiffening_effect" : stiffening_effect
            }

        self.model.set_gravity_vector(self.gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)
        app().project.file.write_inertia_load_in_file(inertia_load)

        self.complete = True
        self.close()

    def _load_inertia_load_setup(self):

        key_stiffening = self.project.model.preprocessor.stress_stiffening_enabled
        self.checkBox_stiffening_effect.setChecked(key_stiffening)

        gravity = self.model.gravity_vector
        if gravity.any() == 0:
            return

        self.lineEdit_acceleration_x_axis.setText(str(gravity[0]))
        self.lineEdit_acceleration_y_axis.setText(str(gravity[1]))
        self.lineEdit_acceleration_z_axis.setText(str(gravity[2]))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False        