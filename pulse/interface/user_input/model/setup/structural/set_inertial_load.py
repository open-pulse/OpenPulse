from PySide6.QtWidgets import QDialog, QCheckBox, QLineEdit, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class SetInertialLoad(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/inertial_load_input.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor
        
        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._load_inertia_load_setup()
        self.exec()

    def _initialize(self):
        self.complete = False
        self.global_damping = [0, 0, 0, 0]
        # self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)
        self.gravity_vector = self.model.gravity_vector

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_stiffening_effect: QCheckBox

        # QLineEdit
        self.lineEdit_acceleration_x_axis: QLineEdit
        self.lineEdit_acceleration_y_axis: QLineEdit
        self.lineEdit_acceleration_z_axis: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton

    def _create_connections(self):
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)

    def _config_widgets(self):
        pass

    def check_gravity_values(self):

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0

        lineEdit = self.lineEdit_acceleration_x_axis
        self.acceleration_x = self.check_inputs(lineEdit, "x-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True

        lineEdit = self.lineEdit_acceleration_y_axis
        self.acceleration_y = self.check_inputs(lineEdit, "y-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True

        lineEdit = self.lineEdit_acceleration_z_axis
        self.acceleration_z = self.check_inputs(lineEdit, "z-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True

        self.gravity = np.array([self.acceleration_x, self.acceleration_y, self.acceleration_z, 0, 0, 0], dtype=float)

        # if np.sum(np.abs(self.gravity)) == 0:
        #     #
        #     title = "Invalid input fields"
        #     message = "Dear user, you should to enter a valid gravity setup to proceed. The null "
        #     message += "gravity vector does not provide an effective static loading."
        #     #
        #     text_info = [title, message, window_title_2]
        #     PrintMessageInput(text_info)
        #     #
        #     return True

        return False
        
    def check_inputs(self, lineEdit, label, only_positive = False, zero_included = True, _float = True):

        message = ""
        self.stop = False
        
        if lineEdit.text() != "":
            try:

                if _float:
                    value = float(lineEdit.text())
                else:
                    value = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if value < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if value <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as error_log:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(error_log)

        else:

            if zero_included:
                return float(0)
            else: 
                message = f"Insert some value at the {label} input field."

        title = "Invalid input to the analysis setup"
        if message != "":
            PrintMessageInput([window_title_1, title, message])                   
            self.stop = True
            return None

        return value

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

        if np.sum(self.gravity_vector) != 0:
            gravity = self.gravity_vector
            self.lineEdit_acceleration_x_axis.setText(str(gravity[0]))
            self.lineEdit_acceleration_y_axis.setText(str(gravity[1]))
            self.lineEdit_acceleration_z_axis.setText(str(gravity[2]))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()