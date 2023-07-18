from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import numpy as np
from pathlib import Path

from data.user_input.project.printMessageInput import PrintMessageInput

class StaticAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/Analysis/Structural/static_analysis_inputs.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Static Analysis Setup")

        self._define_qt_variables()

        self.complete = False
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _define_qt_variables(self):
        #
        self.checkBox_self_weight = self.findChild(QCheckBox, 'checkBox_self_weight')
        self.checkBox_self_weight.stateChanged.connect(self.change_input_fields_visibility)
        #
        self.lineEdit_acceleration_x_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_x_axis')
        self.lineEdit_acceleration_y_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_y_axis')
        self.lineEdit_acceleration_z_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_z_axis')
        #
        self.pushButton_run_analysis = self.findChild(QPushButton, 'pushButton_run_analysis')
        self.pushButton_run_analysis.clicked.connect(self.confirm)

    def change_input_fields_visibility(self):
        _bool = not self.checkBox_self_weight.isChecked()
        self.lineEdit_acceleration_x_axis.setDisabled(_bool)
        self.lineEdit_acceleration_y_axis.setDisabled(_bool)
        self.lineEdit_acceleration_z_axis.setDisabled(_bool)

    def check_gravity_values(self):
        #
        self.gravity = None
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
        self.gravity = np.array([self.acceleration_x, self.acceleration_y, self.acceleration_z, 0, 0, 0])
        if np.sum(np.abs(self.gravity)) == 0:
    
            window_title = "WARNING"
            title = "Invalid input fields"
            message = "Dear user, you should to enter a valid gravity setup to proceed. The null gravity vector"
            message += "do not provide an effective static loading."
            text_info = [title, message, window_title]
            PrintMessageInput(text_info)

            return True

    def confirm(self):
        #
        window_title = "WARNING"
        title = "Under development functionality"
        message = "Dear user, the 'Static Analysis' functionality is currently under implementation stage."
        text_info = [title, message, window_title]
        #
        PrintMessageInput(text_info)

        if self.checkBox_self_weight.isChecked():
            if self.check_gravity_values():
                return
        
            if self.gravity is not None:
                print(f"gravity setup: {self.gravity}")
                # self.project.set_gravity_setup(self.gravity)
                self.complete = True
                self.close()
        
        self.complete = True
        self.close()
    
    def check_inputs(self, lineEdit, label, only_positive=False, zero_included=True, _float=True):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        window_title = "ERROR"
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
            PrintMessageInput([title, message, window_title])                   
            self.stop = True
            return None
        return out