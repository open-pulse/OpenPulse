from PyQt5.QtWidgets import QDialog, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np
from pathlib import Path

from pulse import app, UI_DIR
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class SetInertialLoad(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/model/setup/structural/inertial_load_input.ui")
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        
        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_inertia_load_setup()
        self.exec()

    def _initialize(self):
        self.complete = False
        self.global_damping = [0, 0, 0, 0]
        self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)
        self.gravity_vector = self.project.preprocessor.gravity_vector

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set inertial load")

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_stiffening_effect = self.findChild(QCheckBox, 'checkBox_stiffening_effect')
        self.checkBox_stiffening_effect.stateChanged.connect(self.change_input_fields_visibility)
        # QLineEdit
        self.lineEdit_acceleration_x_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_x_axis')
        self.lineEdit_acceleration_y_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_y_axis')
        self.lineEdit_acceleration_z_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_z_axis')
        # QPushButton
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.confirm)

    def change_input_fields_visibility(self):
        _bool = not self.checkBox_stiffening_effect.isChecked()
        # self.lineEdit_acceleration_x_axis.setDisabled(_bool)
        # self.lineEdit_acceleration_y_axis.setDisabled(_bool)
        # self.lineEdit_acceleration_z_axis.setDisabled(_bool)

    def check_gravity_values(self):
        #
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0
        #
        lineEdit = self.lineEdit_acceleration_x_axis
        self.acceleration_x = self.check_inputs(lineEdit, "x-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True
        #
        lineEdit = self.lineEdit_acceleration_y_axis
        self.acceleration_y = self.check_inputs(lineEdit, "y-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True
        #
        lineEdit = self.lineEdit_acceleration_z_axis
        self.acceleration_z = self.check_inputs(lineEdit, "z-axis acceleration")
        if self.stop:
            lineEdit.setFocus()
            return True
        #
        if self.checkBox_stiffening_effect.isChecked():
            self.gravity = np.array([self.acceleration_x, self.acceleration_y, self.acceleration_z, 0, 0, 0])
        #
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

    def confirm(self):

        if self.check_gravity_values():
            return

        key = self.checkBox_stiffening_effect.isChecked()
        self.project.set_inertia_load_setup(self.gravity, stiffening_effect=key)
        
        self.complete = True
        self.close()
        
    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        if lineEdit.text() != "":
            try:

                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:

            if zero_included:
                return float(0)
            else: 
                message = f"Insert some value at the {label} input field."
        
        if message != "":
            PrintMessageInput([window_title_1, title, message])                   
            self.stop = True
            return None
        return out
    
    def _load_inertia_load_setup(self):

        key_stiffening = self.project.preprocessor.stress_stiffening_enabled
        self.checkBox_stiffening_effect.setChecked(key_stiffening)

        if np.sum(self.gravity_vector) != 0:
            g = self.gravity_vector
            self.lineEdit_acceleration_x_axis.setText(str(g[0]))
            self.lineEdit_acceleration_y_axis.setText(str(g[1]))
            self.lineEdit_acceleration_z_axis.setText(str(g[2]))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()