from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np
import matplotlib.pyplot as plt  

from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class DecouplingRotationDOFsInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/Model/Setup/Structural/decouplingRotationDOFsInput.ui', self)

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

        self.dict_tag_to_entity = self.project.mesh.dict_tag_to_entity#get_dict_of_entities()
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

        self.lineEdit_decoupled_DOFs = self.findChild(QLineEdit, 'lineEdit_decoupled_DOFs')
        self.lineEdit_element_IDs = self.findChild(QLineEdit, 'lineEdit_element_IDs')
        self.lineEdit_node_IDs = self.findChild(QLineEdit, 'lineEdit_node_IDs')
        self.lineEdit_decoupled_DOFs.setDisabled(True)
        self.lineEdit_element_IDs.setDisabled(True)
        self.lineEdit_node_IDs.setDisabled(True)
        
        self.treeWidget_B2PX_rotation_decoupling = self.findChild(QTreeWidget, 'treeWidget_B2PX_rotation_decoupling')
        self.treeWidget_B2PX_rotation_decoupling.setColumnWidth(0, 120)
        self.treeWidget_B2PX_rotation_decoupling.setColumnWidth(1, 140)
        self.treeWidget_B2PX_rotation_decoupling.setColumnWidth(2, 110)
        self.treeWidget_B2PX_rotation_decoupling.itemClicked.connect(self.on_click_item_group)
        self.treeWidget_B2PX_rotation_decoupling.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_B2PX_rotation_decoupling.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_B2PX_rotation_decoupling.headerItem().setTextAlignment(2, Qt.AlignCenter)
  
        self.tabWidget_B2PX_rotation_decoupling = self.findChild(QTabWidget, 'tabWidget_B2PX_rotation_decoupling')
        self.tabWidget_B2PX_rotation_decoupling.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_B2PX_rotation_decoupling.currentIndex()

        self.pushButton_remove_group = self.findChild(QPushButton, 'pushButton_remove_group')
        self.pushButton_remove_group.clicked.connect(self.remove_group)
        self.pushButton_get_information_group = self.findChild(QPushButton, 'pushButton_get_information_group')
        self.pushButton_get_information_group.clicked.connect(self.get_information)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')  
        self.pushButton_confirm.clicked.connect(self.check_dofs_coupling)
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset') 
        self.pushButton_reset.clicked.connect(self.check_reset_all)

        self.pushButton_get_nodes = self.findChild(QPushButton, 'pushButton_get_nodes')
        self.pushButton_get_nodes.clicked.connect(self.check_get_nodes)
        self.load_decoupling_info()
        self.update()
        self.exec_()
    
    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_B2PX_rotation_decoupling.currentIndex()
        if self.currentTab_ == 1:
            self.clear_texts()
            self.pushButton_remove_group.setDisabled(True)
            self.pushButton_get_information_group.setDisabled(True)   

    def clear_texts(self):
        self.lineEdit_decoupled_DOFs.setText("")
        self.lineEdit_element_IDs.setText("")
        self.lineEdit_node_IDs.setText("")

    def update_texts(self, element_id):
        self.first_node = self.structural_elements[element_id].first_node.external_index
        self.last_node  = self.structural_elements[element_id].last_node.external_index
        self.lineEdit_first_node.setText(str(self.first_node))
        self.lineEdit_last_node.setText(str(self.last_node))
        self.lineEdit_selected_element.setText(str(element_id))

    def on_click_item_group(self, item):
        self.lineEdit_decoupled_DOFs.setText(item.text(0))
        self.lineEdit_element_IDs.setText(item.text(1))
        self.lineEdit_node_IDs.setText(item.text(2))
        self.pushButton_remove_group.setDisabled(False)
        self.pushButton_get_information_group.setDisabled(False)
        
    def checkBoxEvent(self):
        self.flag_rotation_x = self.checkBox_rotation_x.isChecked()
        self.flag_rotation_y = self.checkBox_rotation_y.isChecked()
        self.flag_rotation_z = self.checkBox_rotation_z.isChecked()
        self.rotations_mask = [self.flag_rotation_x, self.flag_rotation_y, self.flag_rotation_z]
        if self.rotations_mask.count(False) == 3:
            title = "INVALID DECOUPLING SETUP"
            message = "There are no rotation DOFs decoupling in the current setup. \nYou should tick at least one rotation DOF before continue."
            PrintMessageInput([title, message, window_title1])
            return  

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
            for elem_ID in self.element_typed:
                self.element = self.structural_elements[elem_ID]
                self.element_id = self.structural_elements[elem_ID].index
        except Exception:
            message = " The Element ID input values must be\n major than 1 and less than {}.".format(len(self.structural_elements))
            title = "Error: invalid Element ID input"
            window_title = "Error message"
            self.info_text = [title, message, window_title]
            return True
        return False

    def remove_group(self):
        key = self.dict_decoupled_DOFs_label_to_bool[self.lineEdit_decoupled_DOFs.text()]
        _, _, section = self.project.mesh.dict_B2PX_rotation_decoupling[key]
        self.project.mesh.dict_elements_with_B2PX_rotation_decoupling.pop(key)
        self.project.mesh.dict_nodes_with_B2PX_rotation_decoupling.pop(key)
        self.project.mesh.dict_B2PX_rotation_decoupling.pop(key)
        self.project.file.modify_B2PX_rotation_decoupling_in_file([], [], [], section, remove=True)
        self.load_decoupling_info()
        self.clear_texts()

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

        if self.rotations_mask.count(False) == 3:
            title = "INVALID DECOUPLING SETUP"
            message = "There are no rotation DOFs decoupling in the current setup. \nYou should tick at least one rotation DOF before continue."
            PrintMessageInput([title, message, window_title1])
            return 
        
        if self.element.element_type in ['beam_1']:
            self.project.set_B2PX_rotation_decoupling(self.element_id, self.selected_node_id, self.rotations_mask)
            self.complete = True
            self.close()
        else:
            title = "INVALID DECOUPLING SETUP"
            message = "The selected element have a {} formulation, you should have a \nBEAM_1 element type in selection to decouple the rotation dofs. \nTry to choose another element or change the element type formulation.".format(self.element.element_type.upper())
            PrintMessageInput([title, message, window_title1])
            return

    def check_reset_all(self):
        self.project.reset_B2PX_totation_decoupling()
        message = "The rotation decoupling applied \nto all dofs has been reseted." 
        title = "Rotations dofs decoupling"
        window_title = "WARNING"
        PrintMessageInput([title, message, window_title])
        self.load_decoupling_info()
        self.clear_texts()
    
    def text_label(self, mask):
        text = ""
        load_labels = np.array(['Rx','Ry','Rz'])
        temp = load_labels[mask]
        if list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_decoupling_info(self):
        self.treeWidget_B2PX_rotation_decoupling.clear()
        self.dict_decoupled_DOFs_label_to_bool = {}
        self.dict_decoupled_DOFs_bool_to_label = {}
        for key, elements in self.project.mesh.dict_elements_with_B2PX_rotation_decoupling.items():
            bool_list = self.project.file._get_list_bool_from_string(key)
            nodes = self.project.mesh.dict_nodes_with_B2PX_rotation_decoupling[key]
            decoupling_dofs_mask = bool_list
            label_decoupled_DOFs = self.text_label(decoupling_dofs_mask)
            
            new = QTreeWidgetItem([label_decoupled_DOFs, str(elements), str(nodes)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            new.setTextAlignment(2, Qt.AlignCenter)
            self.treeWidget_B2PX_rotation_decoupling.addTopLevelItem(new)
            self.dict_decoupled_DOFs_label_to_bool[label_decoupled_DOFs] = key
            self.dict_decoupled_DOFs_bool_to_label[key] = label_decoupled_DOFs

    def get_information(self):
        try:
            if self.lineEdit_decoupled_DOFs.text() != "": 
                decoupled_DOFs_bool = self.dict_decoupled_DOFs_label_to_bool[self.lineEdit_decoupled_DOFs.text()]  
                decoupled_DOFs_labels =  self.dict_decoupled_DOFs_bool_to_label[decoupled_DOFs_bool]     
                read = GetInformationOfGroup(self.project, decoupled_DOFs_bool, decoupled_DOFs_labels)
                if read.lines_removed:
                    self.load_decoupling_info()
                    self.clear_texts()
            else:
                title = "UNSELECTED GROUP"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([title, message, window_title2])
                
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([title, message, window_title1])

class GetInformationOfGroup(QDialog):
    def __init__(self, project, decoupled_DOFs_bool, decoupled_DOFs_labels, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
 
        uic.loadUi('pulse/uix/user_input/ui/Model/Info/getInformationRotationDecouplingInput.ui', self)
        self.flagLines = True
        self.flagElements = False
        self.lineEdit_decoupled_DOFs = self.findChild(QLineEdit, 'lineEdit_decoupled_DOFs')
        self.lineEdit_element_IDs = self.findChild(QLineEdit, 'lineEdit_element_IDs')
        self.lineEdit_node_IDs = self.findChild(QLineEdit, 'lineEdit_node_IDs')
        self.lineEdit_decoupled_DOFs.setDisabled(True)
        self.lineEdit_element_IDs.setDisabled(True)
        self.lineEdit_node_IDs.setDisabled(True)

        # self.lineEdit_id_labels_decoupled_DOFs = self.findChild(QLineEdit, 'lineEdit_id_labels_decoupled_DOFs')
        # self.lineEdit_id_labels_element_IDs = self.findChild(QLineEdit,'lineEdit_id_labels_element_IDs ')
        # self.lineEdit_id_labels_node_IDs = self.findChild(QLineEdit,'lineEdit_id_labels_node_IDs ')

        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_remove.clicked.connect(self.check_remove)
        self.lines_removed = False

        self.decoupled_DOFs_bool = decoupled_DOFs_bool
        self.decoupled_DOFs_labels = decoupled_DOFs_labels
        self.project = project

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.treeWidget_group_info.setColumnWidth(0, 120)
        self.treeWidget_group_info.setColumnWidth(1, 140)
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.update_dict()
        self.load_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()

    def update_dict(self):
        self.list_elements = self.project.mesh.dict_elements_with_B2PX_rotation_decoupling[self.decoupled_DOFs_bool]
        self.list_nodes = self.project.mesh.dict_nodes_with_B2PX_rotation_decoupling[self.decoupled_DOFs_bool]
        
    def on_click_item_(self, item):
        self.lineEdit_decoupled_DOFs.setText(self.decoupled_DOFs_labels)
        self.lineEdit_element_IDs.setText(item.text(0))
        self.lineEdit_node_IDs.setText(item.text(1))

    def check_remove(self):
        if self.lineEdit_decoupled_DOFs.text() != "":
            element = int(self.lineEdit_element_IDs.text())
            node = int(self.lineEdit_node_IDs.text())
            list_bool = self.project.file._get_list_bool_from_string(self.decoupled_DOFs_bool)
            self.project.set_B2PX_rotation_decoupling(element, node, list_bool, remove=True)

        self.update_dict()
        self.load_info()
        self.lineEdit_decoupled_DOFs.setText("")
        self.lineEdit_element_IDs.setText("")
        self.lineEdit_node_IDs.setText("")
        self.lines_removed = True

    def load_info(self):
        self.treeWidget_group_info.clear()
        for index, element in enumerate(self.list_elements):
            node = self.list_nodes[index]
            new = QTreeWidgetItem([str(element), str(node)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)
        
    def force_to_close(self):
        self.close()