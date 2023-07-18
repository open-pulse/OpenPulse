from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class StaticAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Analysis/Structural/static_analysis_inputs.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self._define_qt_variables()

        self.complete = False
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _define_qt_variables(self):
        #
        self.lineEdit_acceleration_x_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_x_axis')
        self.lineEdit_acceleration_y_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_y_axis')
        self.lineEdit_acceleration_z_axis = self.findChild(QLineEdit, 'lineEdit_acceleration_z_axis')

        self.pushButton_run_analysis = self.findChild(QPushButton, 'pushButton_run_analysis')
        self.pushButton_run_analysis.clicked.connect(self.confirm)

        self.radioButton_acceleration_x_axis = self.findChild(QRadioButton, 'radioButton_acceleration_x_axis')
        self.radioButton_acceleration_y_axis = self.findChild(QRadioButton, 'radioButton_acceleration_y_axis')
        self.radioButton_acceleration_z_axis = self.findChild(QRadioButton, 'radioButton_acceleration_z_axis')

    def check_values(self):
        #
        self.gravity = None
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0
        #
        if self.radioButton_acceleration_x_axis.isChecked():
            lineEdit = self.lineEdit_acceleration_x_axis
            self.acceleration_x = self.check_inputs(lineEdit, "x-axis acceleration", only_positive=False)
            if self.stop:
                lineEdit.setFocus()
                return True
        #
        if self.radioButton_acceleration_y_axis.isChecked():
            lineEdit = self.lineEdit_acceleration_y_axis
            self.acceleration_y = self.check_inputs(lineEdit, "y-axis acceleration", only_positive=False)
            if self.stop:
                lineEdit.setFocus()
                return True
        #
        if self.radioButton_acceleration_z_axis.isChecked():
            lineEdit = self.lineEdit_acceleration_z_axis
            self.acceleration_z = self.check_inputs(lineEdit, "z-axis acceleration", only_positive=False)
            if self.stop:
                lineEdit.setFocus()
                return True
        #
        self.gravity = np.array([self.acceleration_x, self.acceleration_y, self.acceleration_z, 0, 0, 0])

    def confirm(self):
        #
        window_title = "WARNING"
        title = "Under development functionality"
        message = "Dear user, the 'Static Analysis' functionality is currently under implementation stage."
        text_info = [title, message, window_title]
        #
        PrintMessageInput(text_info)

        if self.check_values():
            return
        
        if self.gravity is not None:
            print(f"gravity setup: {self.gravity}")
            # self.project.set_gravity_setup(self.gravity)
            self.complete = True
            self.close()

    
    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=True):
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