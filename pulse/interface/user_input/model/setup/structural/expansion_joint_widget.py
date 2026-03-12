from PySide6.QtWidgets import QLineEdit

from pulse.interface.ui_generated.model.setup.structural.expansion_joint_widget_ui import ExpansionJointWidget_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.common import CommonUserInputs, get_table_name, update_analysis_setup_in_file



class ExpansionJointWidget(ExpansionJointWidget_UI):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):

        self.complete = False
        self.keep_window_open = True

        self.Kx_table = None
        self.Kyz_table = None
        self.Krx_table = None
        self.Kryz_table = None

        self.Kx_filename = None
        self.Kyz_filename = None
        self.Krx_filename = None
        self.Kryz_filename = None

    def _define_qt_variables(self):
        self._create_lists_of_lineEdits()

    def _create_connections(self):
        #
        self.comboBox_axial_stop_rod.currentIndexChanged.connect(
            self.axial_stop_rod_callback
        )
        #
        self.pushButton_load_table_Kx.clicked.connect(self.load_Kx_table)
        self.pushButton_load_table_Kyz.clicked.connect(
            self.load_Kyz_table
        )
        self.pushButton_load_table_Krx.clicked.connect(
            self.load_Krx_table
        )
        self.pushButton_load_table_Kryz.clicked.connect(
            self.load_Kryz_table
        )

    def _create_lists_of_lineEdits(self):
        self.list_lineEdits = [
            self.lineEdit_effective_diameter,
            self.lineEdit_joint_mass,
            self.lineEdit_axial_locking_criteria,
            self.lineEdit_Kx,
            self.lineEdit_Kyz,
            self.lineEdit_Krx,
            self.lineEdit_Kryz,
            self.lineEdit_Kx_table_path,
            self.lineEdit_Kyz_table_path,
            self.lineEdit_Krx_table_path,
            self.lineEdit_Kryz_table_path,
        ]

    def axial_stop_rod_callback(self):
        if self.comboBox_axial_stop_rod.currentIndex() == 0:
            self.label_axial_lock_criteria.setDisabled(True)
            self.lineEdit_axial_locking_criteria.clear()
            self.lineEdit_axial_locking_criteria.setDisabled(True)
        else:
            self.label_axial_lock_criteria.setDisabled(False)
            self.lineEdit_axial_locking_criteria.setDisabled(False)


    def load_Kx_table(self):
        self.imported_Kx_values, self.Kx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kx_table_path, 
            "Kx", 
            dof_label="axial stiffness",
            )

        if self.imported_Kx_values is None:
            self.line_edit_reset(self.lineEdit_Kx_table_path)

    def load_Kyz_table(self):
        self.imported_Kyz_values, self.Kyz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kyz_table_path, 
            "Kyz", 
            dof_label="transversal stiffness",
            )

        if self.imported_Kyz_values is None:
            self.line_edit_reset(self.lineEdit_Kyz_table_path)

    def load_Krx_table(self):
        self.imported_Krx_values, self.Krx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Krx_table_path, 
            "Krx", 
            dof_label="torsional stiffness",
            )

        if self.imported_Krx_values is None:
            self.line_edit_reset(self.lineEdit_Krx_table_path)

    def load_Kryz_table(self):
        self.imported_Kryz_values, self.Kryz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kryz_table_path, 
            "Kryz", 
            dof_label="angular stiffness"
            )

        if self.Kryz_table_path is None:
            self.line_edit_reset(self.lineEdit_Kryz_table_path)

    def line_edit_reset(self, line_edit: QLineEdit):
        line_edit.clear()
        line_edit.setFocus()

    def check_initial_inputs(self):
        self.joint_parameters = dict()

        stop, value = self.check_input_parameters(self.lineEdit_effective_diameter, 'Effective diameter')
        if stop:
            self.lineEdit_effective_diameter.setFocus()
            return True
        self.joint_parameters["effective_diameter"] = value

        stop, value = self.check_input_parameters(self.lineEdit_joint_mass, 'Joint mass')
        if stop:    
            self.lineEdit_joint_mass.setFocus()
            return True
        self.joint_parameters["joint_mass"] = value

        stop, value = self.check_input_parameters(self.lineEdit_axial_locking_criteria, 'Axial locking criteria')
        if stop:
            self.lineEdit_axial_locking_criteria.setFocus()
            return True

        self.joint_parameters["axial_locking_criteria"] = value
        self.joint_parameters["rods"] = int(self.comboBox_axial_stop_rod.currentIndex())

    def check_constant_values_to_stiffness(self):
        _stiffness = list()

        stop, value = self.check_input_parameters(self.lineEdit_Kx, 'Kx (axial stiffness)')
        if stop:
            self.lineEdit_Kx.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Kyz, 'Kyz (transversal stiffness)')
        if stop:
            self.lineEdit_Kyz.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Krx, 'Krx (torsional stiffness)')
        if stop:
            self.lineEdit_Krx.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Kryz, 'Kryz (angular stiffness)')
        if stop:
            self.lineEdit_Kryz.setFocus()
            return True
        _stiffness.append(value)

        self.joint_parameters["values"] = _stiffness

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):
        title = f"Invalid entry to the '{label}'"
        str_value = lineEdit.text()

        if str_value == "":
            message = f"An empty entry has been detected at the '{label}' input field. " 
            message += "You should to enter a positive value to proceed."
            PrintMessageInput(["Error", title, message])
            return True, None

        try:
            str_value = str_value.replace(",", ".")
            if _float:
                value = float(str_value)
            else:
                value = int(str_value) 

            if value <= 0:
                message = f"You cannot input a non-positive value to the '{label}'."

        except Exception as _log_error:
            message = (
                f"You have typed an invalid value to the '{label}' input field."
                "The input value should be a positive float number.\n\n"
                f"{str(_log_error)}"
            )
            PrintMessageInput(["Error", title, message])
            return True, value

        return False, value

    def get_parameters(self) -> None | dict:
        if self.check_initial_inputs():
            return

        if self.tabWidget_inputs.currentIndex() == 0:
            if self.check_constant_values_to_stiffness():
                return

        return self.joint_parameters
