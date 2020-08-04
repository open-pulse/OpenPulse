from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.utils import error
from pulse.preprocessing.cross_section import CrossSection

class AcousticElementLengthCorrectionInput(QDialog):
    def __init__(self, project, elements_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/acoustic_element_length_correction_input.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.acoustic_elements = project.mesh.acoustic_elements
        self.elements_id = elements_id
        self.type_label = None

        self.currentTab = 0
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')#lineEdit_elementID

        self.radioButton_expansion = self.findChild(QRadioButton, 'radioButton_expansion')
        self.radioButton_side_branch = self.findChild(QRadioButton, 'radioButton_side_branch')
        self.radioButton_loop = self.findChild(QRadioButton, 'radioButton_loop')

        self.radioButton_expansion.toggled.connect(self.radioButtonEvent)
        self.radioButton_side_branch.toggled.connect(self.radioButtonEvent)
        self.radioButton_loop.toggled.connect(self.radioButtonEvent)

        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()

        self.treeWidget_element_length_correction = self.findChild(QTreeWidget, 'treeWidget_element_length_correction')
        self.treeWidget_element_length_correction.setColumnWidth(1, 20)
        self.treeWidget_element_length_correction.setColumnWidth(2, 80)
        self.treeWidget_element_length_correction.itemClicked.connect(self.on_click_item)
        self.treeWidget_element_length_correction.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_element_length_correction = self.findChild(QTabWidget, 'tabWidget_element_length_correction')
        self.tabWidget_element_length_correction.currentChanged.connect(self.tabEvent)

        self.pushButton_upper_remove_confirm = self.findChild(QPushButton, 'pushButton_upper_remove_confirm')
        # self.pushButton_upper_remove_confirm.clicked.connect(self.check)
        self.pushButton_lower_remove_confirm = self.findChild(QPushButton, 'pushButton_lower_remove_confirm')
        # self.pushButton_lower_remove_confirm.clicked.connect(self.check)
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_element_correction_type)

        if self.elements_id != []:
            self.write_ids(elements_id)

        self.currentTab = self.tabWidget_element_length_correction.currentIndex()
        self.load_elements_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()
     
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_elementID.setText(text)

    def tabEvent(self):
        self.currentTab = self.tabWidget_element_length_correction.currentIndex()

    def check_input_elements(self):
        try:
            tokens = self.lineEdit_elementID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.elements_typed = list(map(int, tokens))

            if self.lineEdit_elementID.text()=="":
                error("Inform a valid Element ID before to confirm the input!", title = "ERROR IN ELEMENT ID's")
                return

        except Exception:
            error("Wrong input for Element ID's!", "ERROR IN ELEMENT ID's")
            return

        try:
            for element_id in self.elements_typed:
                self.acoustic_elements[element_id]
        except:
            message = [" The Element ID input values must be\n major than 1 and less than {}.".format(len(self.acoustic_elements))]
            error(message[0], title = " INCORRECT ELEMENT ID INPUT! ")
            return

    def check_element_correction_type(self):
        self.check_input_elements()
        if self.flag_expansion:
            type_id = 0
            self.type_label = "'Expansion'"
   
        elif self.flag_side_branch:
            type_id = 1
            self.type_label = "'Side branch'"

        elif self.flag_loop:
            type_id = 2
            self.type_label = "'Loop'"

        self.project.set_element_length_correction_by_elements(self.elements_typed, type_id)
        self.close()

    def load_elements_info(self):
        
        keys = [0,1,2]
        labels = ['Expansion', 'Side branch', 'Loop']
        dict_correction_types = dict(zip(keys, labels))

        for element in self.project.mesh.element_with_length_correction:
            text = dict_correction_types[element.acoustic_length_correction]
            new = QTreeWidgetItem([str(element.index), text])
            self.treeWidget_element_length_correction.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        self.check_remove_element_length_correction()

    def check_remove_element_length_correction(self):

        self.check_input_elements()
        #TODO under construction
        # key_strings = ["acoustic pressure"]
        # message = "The acoustic pressure attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        # remove_bc_from_file(self.nodes_typed, self.acoustic_bc_info_path, key_strings, message)
        # self.project.mesh.set_acoustic_pressure_bc_by_node(self.nodes_typed, None)
        # self.transform_points(self.nodes_typed)
        # self.close()

    