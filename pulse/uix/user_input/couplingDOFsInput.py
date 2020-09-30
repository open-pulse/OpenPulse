from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt    
    
class CouplingDOFsInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/dofsCouplingInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.stop = False
        self.complete = False
        
        self.structural_elements = self.project.mesh.structural_elements
        self.nodes = self.project.mesh.nodes

        self.dict_tag_to_entity = self.project.mesh.get_dict_of_entities()
        self.line_id = self.opv.getListPickedEntities()
        self.element_id = self.opv.getListPickedElements()
        self.node_id = self.opv.getListPickedPoints()

        self.lineEdit_selected_element = self.findChild(QLineEdit, 'lineEdit_selected_element')
        self.lineEdit_first_node = self.findChild(QLineEdit, 'lineEdit_first_node')
        self.lineEdit_last_node = self.findChild(QLineEdit, 'lineEdit_last_node')
   
        self.radioButton_first_node = self.findChild(QRadioButton, 'radioButton_first_node')
        self.radioButton_first_node.clicked.connect(self.radioButtonEvent)
        self.flag_first_node = self.radioButton_first_node.isChecked()

        self.radioButton_last_node = self.findChild(QRadioButton, 'radioButton_last_node')
        self.radioButton_last_node.clicked.connect(self.radioButtonEvent)
        self.flag_last_node = self.radioButton_last_node.isChecked()

        self.checkBox_rotation_x = self.findChild(QCheckBox, 'checkBox_rotation_x')
        self.checkBox_rotation_y = self.findChild(QCheckBox, 'checkBox_rotation_y')
        self.checkBox_rotation_z = self.findChild(QCheckBox, 'checkBox_rotation_z')
        self.checkBox_rotation_x.toggled.connect(self.checkBoxEvent)
        self.checkBox_rotation_y.toggled.connect(self.checkBoxEvent)
        self.checkBox_rotation_z.toggled.connect(self.checkBoxEvent)
        self.flag_rotation_x = self.checkBox_rotation_x.isChecked()
        self.flag_rotation_y = self.checkBox_rotation_y.isChecked()
        self.flag_rotation_z = self.checkBox_rotation_z.isChecked()
        self.rotations_mask = [self.flag_rotation_x, self.flag_rotation_y, self.flag_rotation_z]

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')  
        self.pushButton_confirm.clicked.connect(self.check_dofs_coupling)
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset') 
        self.pushButton_reset.clicked.connect(self.check_reset_all)

        self.pushButton_get_nodes = self.findChild(QPushButton, 'pushButton_get_nodes')
        self.pushButton_get_nodes.clicked.connect(self.check_get_nodes)

        self.update()
        self.exec_()
    
    def checkBoxEvent(self):
        self.flag_rotation_x = self.checkBox_rotation_x.isChecked()
        self.flag_rotation_y = self.checkBox_rotation_y.isChecked()
        self.flag_rotation_z = self.checkBox_rotation_z.isChecked()
        self.rotations_mask = [self.flag_rotation_x, self.flag_rotation_y, self.flag_rotation_z]

    def radioButtonEvent(self):
        self.flag_first_node = self.radioButton_first_node.isChecked()
        self.flag_last_node = self.radioButton_last_node.isChecked()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_get_nodes()
        if event.key() == Qt.Key_Escape:
            plt.close()
            self.close()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_element.setText(text)

    def update(self):
        if self.opv.getListPickedElements() == []:
            return
        else:
            self.element_id = self.opv.getListPickedElements()[0]
        self.update_texts(self.element_id)

    def update_texts(self, element_id):
        self.first_node = self.structural_elements[element_id].first_node.external_index
        self.last_node  = self.structural_elements[element_id].last_node.external_index
        self.lineEdit_first_node.setText(str(self.first_node))
        self.lineEdit_last_node.setText(str(self.last_node))
        self.lineEdit_selected_element.setText(str(element_id))

    def check_input_element(self):

        try:
            tokens = self.lineEdit_selected_element.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.element_typed = list(map(int, tokens))

            if len(self.element_typed) > 1:
                message = "Please, select only one element \nto modify dofs coupling."
                title = "Error: multiple elements in selection"
                window_title = "Error message"
                self.info_text = [title, message, window_title]
                return True
            
            if self.lineEdit_selected_element.text() == "":
                message = "Inform a valid Element ID before \nto confirm the input."
                title = "Error: empty Element ID input"
                window_title = "Error message"
                self.info_text = [title, message, window_title]
                return True

        except Exception:
            message = "Wrong input for Element ID."
            title = "Error in Element ID"
            window_title = "Error message"
            self.info_text = [title, message, window_title]
            return True

        try:
            for element in self.element_typed:
                self.element_id = self.structural_elements[element].index
        except Exception:
            message = " The Element ID input values must be\n major than 1 and less than {}.".format(len(self.structural_elements))
            title = "Error: invalid Element ID input"
            window_title = "Error message"
            self.info_text = [title, message, window_title]
            return True
        return False


    def check_get_nodes(self):
        if self.check_input_element():
            PrintMessageInput(self.info_text)
            return True
        self.update_texts(self.element_id)
        return False


    def check_dofs_coupling(self):
        if self.check_get_nodes():
            return
        if self.flag_first_node:
            self.selected_node_id = self.first_node
        elif self.flag_last_node:
            self.selected_node_id = self.last_node
        neighboor_elements = self.project.mesh.neighboor_elements_of_node(self.selected_node_id)
        if len(neighboor_elements)<3:
            message = "The decoupling of rotation dofs can only \nbe applied to the T connections." 
            title = "Incorrect Node ID selection"
            window_title = "Error message"
            PrintMessageInput([title, message, window_title])
            return
        self.complete = True
        self.close()

    def check_reset_all(self):
        N = self.project.mesh.DOFS_ELEMENT
        for element in self.project.mesh.elements_with_decoupled_dofs:
            element.decoupling_matrix = np.ones((N,N), dtype=int)
        self.project.mesh.elements_with_decoupled_dofs = []
        message = "The rotation deccoupling applied \nto all dofs has been reseted." 
        title = "Rotations dofs decoupling"
        window_title = "WARNING"
        PrintMessageInput([title, message, window_title])