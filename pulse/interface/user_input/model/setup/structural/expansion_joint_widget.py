from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTreeWidget,
    QComboBox,
)

from pulse import UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui


class ExpansionJointWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        ui_path = UI_DIR / "model/setup/structural/expansion_joint_widget.ui"
        load_ui(ui_path, self)

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
        # QComboBox
        self.comboBox_axial_stop_rod: QComboBox

        # QFrame
        self.selection_frame: QFrame

        # QLabel
        self.label_selected_id: QLabel
        self.label_selection: QLabel
        self.label_axial_lock_criteria: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        #
        self.lineEdit_effective_diameter: QLineEdit
        self.lineEdit_joint_mass: QLineEdit
        self.lineEdit_axial_locking_criteria: QLineEdit
        #
        self.lineEdit_axial_stiffness: QLineEdit
        self.lineEdit_transversal_stiffness: QLineEdit
        self.lineEdit_torsional_stiffness: QLineEdit
        self.lineEdit_angular_stiffness: QLineEdit
        #
        self.lineEdit_path_table_axial_stiffness: QLineEdit
        self.lineEdit_path_table_transversal_stiffness: QLineEdit
        self.lineEdit_path_table_torsional_stiffness: QLineEdit
        self.lineEdit_path_table_angular_stiffness: QLineEdit
        self._create_lists_of_lineEdits()

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_load_table_axial_stiffness: QPushButton
        self.pushButton_load_table_transversal_stiffness: QPushButton
        self.pushButton_load_table_torsional_stiffness: QPushButton
        self.pushButton_load_table_angular_stiffness: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget
        self.tabWidget_inputs: QTabWidget

        # QTreeWidget
        self.treeWidget_expansion_joint_by_lines: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_axial_stop_rod.currentIndexChanged.connect(
            self.axial_stop_rod_callback
        )
        #
        self.pushButton_load_table_axial_stiffness.clicked.connect(self.load_Kx_table)
        self.pushButton_load_table_transversal_stiffness.clicked.connect(
            self.load_Kyz_table
        )
        self.pushButton_load_table_torsional_stiffness.clicked.connect(
            self.load_Krx_table
        )
        self.pushButton_load_table_angular_stiffness.clicked.connect(
            self.load_Kryz_table
        )

    def _create_lists_of_lineEdits(self):
        self.list_lineEdits = [
            self.lineEdit_effective_diameter,
            self.lineEdit_joint_mass,
            self.lineEdit_axial_locking_criteria,
            self.lineEdit_axial_stiffness,
            self.lineEdit_transversal_stiffness,
            self.lineEdit_torsional_stiffness,
            self.lineEdit_angular_stiffness,
            self.lineEdit_path_table_axial_stiffness,
            self.lineEdit_path_table_transversal_stiffness,
            self.lineEdit_path_table_torsional_stiffness,
            self.lineEdit_path_table_angular_stiffness,
        ]

    def axial_stop_rod_callback(self):
        if self.comboBox_axial_stop_rod.currentIndex() == 0:
            self.label_axial_lock_criteria.setDisabled(True)
            self.lineEdit_axial_locking_criteria.setText("")
            self.lineEdit_axial_locking_criteria.setDisabled(True)
        else:
            self.label_axial_lock_criteria.setDisabled(False)
            self.lineEdit_axial_locking_criteria.setDisabled(False)

    def load_Kx_table(self):
        stiffness_label = "Axial stiffness"
        lineEdit = self.lineEdit_path_table_axial_stiffness
        self.Kx_table, self.Kx_filename = self.load_table(lineEdit, stiffness_label)
        if self.Kx_table is None:
            self.lineedit_reset(lineEdit)

    def load_Kyz_table(self):
        stiffness_label = "Transversal stiffness"
        lineEdit = self.lineEdit_path_table_transversal_stiffness
        self.Kyz_table, self.Kyz_filename = self.load_table(lineEdit, stiffness_label)
        if self.Kyz_table is None:
            self.lineedit_reset(lineEdit)

    def load_Krx_table(self):
        stiffness_label = "Torsional stiffness"
        lineEdit = self.lineEdit_path_table_torsional_stiffness
        self.Krx_table, self.Krx_filename = self.load_table(lineEdit, stiffness_label)
        if self.Krx_table is None:
            self.lineedit_reset(lineEdit)

    def load_Kryz_table(self):
        stiffness_label = "Angular stiffness"
        lineEdit = self.lineEdit_path_table_angular_stiffness
        self.Kryz_table, self.Kryz_filename = self.load_table(lineEdit, stiffness_label)
        if self.Kryz_table is None:
            self.lineedit_reset(lineEdit)

    def lineedit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_table(self):
        "implement something here"

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

        stop, value = self.check_input_parameters(self.lineEdit_axial_stiffness, 'Axial stiffness')
        if stop:
            self.lineEdit_axial_stiffness.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_transversal_stiffness, 'Transversal stiffness')
        if stop:
            self.lineEdit_transversal_stiffness.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_torsional_stiffness, 'Torsional stiffness')
        if stop:
            self.lineEdit_torsional_stiffness.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_angular_stiffness, 'Angular stiffness')
        if stop:
            self.lineEdit_angular_stiffness.setFocus()
            return True
        _stiffness.append(value)

        self.joint_parameters["stiffness_values"] = _stiffness

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
