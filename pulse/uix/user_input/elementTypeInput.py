from PyQt5.QtWidgets import  QDialog, QComboBox, QPushButton, QRadioButton, QLineEdit
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class ElementTypeInput(QDialog):
    def __init__(self, project, entities_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/elementTypeInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.dict_entities = project.mesh.get_dict_of_entities()
        self.entities_id = entities_id
        self.index = 0
        self.element_type = 'pipe_1'
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')

        if self.entities_id != []:
            self.write_ids(entities_id)
            self.radioButton_entity.setChecked(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.button_clicked)

        self.exec_()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            # self.index = -1
            self.close()

    def check_element_type_changes(self):
        final_etype = self.element_type
        for tag in self.entities_id:
            initial_etype = self.dict_entities[tag].element_type
            if initial_etype in ['pipe_1', 'pipe_2'] and final_etype in ['beam_1']:
                self.update_cross_section = True
                self.pipe_to_beam = True
                return
            elif initial_etype in ['beam_1'] and final_etype in ['pipe_1', 'pipe_2']:
                self.update_cross_section = True
                self.beam_to_pipe = True
                return
            else:
                self.update_cross_section = False
                self.pipe_to_beam = False
                self.beam_to_pipe = False

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'
        elif self.index ==2:
            self.element_type = 'beam_1'
        # elif self.index == 3:
        #     self.element_type = 'shell'

    def check(self):
        self.close()

    def button_clicked(self):
        self.check()
        self.check_element_type_changes()
        print("The element change has been checked!")