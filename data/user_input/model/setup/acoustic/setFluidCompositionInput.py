from PyQt5.QtWidgets import QTreeWidgetItem, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox, QSpinBox, QPushButton, QWidget, QFileDialog, QComboBox, QTreeWidget
import os
from os.path import basename
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput
from pulse.utils import get_new_path
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
import numpy as np

from PyQt5 import uic

window_title_1 = "ERROR"

class SetFluidCompositionInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/model/setup/acoustic/setFluidCompositionInput.ui', self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        icons_path = 'data\\icons\\'
        self.icon_pulse = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon_pulse)

        self.icon_animate = QIcon(icons_path + 'play_pause.png')

        self.project = project
        self.opv = opv
        self.opv.setInputObject(self)

        self.save_path = ""
        self.export_file_path = ""
        self.userPath = os.path.expanduser('~')

        self.selected_fluid = ""
        self.str_composition_value = ""
        self.composition_value = 0
        self.remaining_composition = 1
        self.list_fluids = []
        self.fluid_to_composition = {}

        self.label_selected_fluid = self.findChild(QLabel, 'label_selected_fluid')
        self.lineEdit_composition = self.findChild(QLineEdit, 'lineEdit_composition')
        self.label_remaining_composition = self.findChild(QLabel, 'label_remaining_composition')

        # self.lineEdit_FileName = self.findChild(QLineEdit, 'lineEdit_FileName')
        # self.checkBox_export = self.findChild(QCheckBox, 'checkBox_export')
        # self.checkBox_export.clicked.connect(self.update_export_tabs)
        # self.checkBox_export.setVisible(False)
        # self.label_export_path = self.findChild(QLabel, 'label_export_path')
        
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')

        self.pushButton_reset_fluid = self.findChild(QPushButton, 'pushButton_reset_fluid')
        self.pushButton_reset_fluid.clicked.connect(self.reset_fluid)
        # self.pushButton_confirm.setIcon(self.icon_confirm)
        # self.pushButton_confirm.clicked.connect(self.process_animation)

        # self.pushButton_clean = self.findChild(QPushButton, 'pushButton_clean')
        # self.pushButton_clean.setVisible(False)
        # self.pushButton_clean.clicked.connect(self.reset_input_field)

        self.pushButton_add_gas = self.findChild(QPushButton, 'pushButton_add_gas')
        self.pushButton_add_gas.clicked.connect(self.add_selected_gas)
    
        self.pushButton_remove_gas = self.findChild(QPushButton, 'pushButton_remove_gas')
        self.pushButton_remove_gas.clicked.connect(self.remove_selected_gas)

        # self.comboBox_file_format = self.findChild(QComboBox, 'comboBox_file_format')

        # self.tabWidget_animation = self.findChild(QTabWidget, 'tabWidget_animation')
        # self.tab_main = self.tabWidget_animation.findChild(QWidget, 'tab_main')
        # self.tab_export = self.tabWidget_animation.findChild(QWidget, 'tab_export')

        self.treeWidget_reference_gases = self.findChild(QTreeWidget, 'treeWidget_reference_gases')
        self.treeWidget_reference_gases.itemClicked.connect(self.on_click_item_reference_gases)
        self.treeWidget_new_gas = self.findChild(QTreeWidget, 'treeWidget_new_gas')
        self.treeWidget_new_gas.itemClicked.connect(self.on_click_item_new_gas)
        self.treeWidget_new_gas.setColumnWidth(0, 160)

        self.treeWidget_new_gas.itemDoubleClicked.connect(self.on_double_click_item_new_gas)

        # self.update_export_tabs()
        self.default_library_gases()
        self.load_default_gases_info()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_pressed()
        elif event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.remove_selected_gas()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def add_selected_gas(self):
        if self.label_selected_fluid.text() != "":
            if self.check_composition_input():
                return
            self.load_new_gas_composition_info()
            self.update_remainig_composition()  
        else:
            title = "None 'Fluid' selected"
            message = "Dear user, it is necessary to select a fluid in the list to proceed"
            PrintMessageInput([title, message, window_title_1])   
    
    def update_remainig_composition(self):
        self.remaining_composition = 1
        for [_, composition_value] in self.fluid_to_composition.values():
            self.remaining_composition -= composition_value
        if self.remaining_composition != 1:
            _remain = round(self.remaining_composition*100, 3)
            self.label_remaining_composition.setText(str(_remain))
        else:
            self.label_remaining_composition.setText("")

    def remove_selected_gas(self):
        if self.label_selected_fluid.text() != "":
            _fluid = self.label_selected_fluid.text()
            if _fluid in self.fluid_to_composition.keys():
                self.fluid_to_composition.pop(_fluid)
                self.load_new_gas_composition_info()
                self.update_remainig_composition() 

    def reset_fluid(self):
            title = f"Resetting of the current 'Fluid Composition'"
            message = "Do you really want to reset the current Fluid Composition?\n\n"
            
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Continue')

            if read._stop:
                return

            self.fluid_to_composition.clear()
            self.load_new_gas_composition_info()
            self.update_remainig_composition()

    def load_default_gases_info(self):
        self.treeWidget_reference_gases.clear()
        self.treeWidget_reference_gases.setGeometry(38, 28, 160, 400)
        self.treeWidget_reference_gases.headerItem().setText(0, "Fluid")
        for gas in self.list_gases:
            new = QTreeWidgetItem([gas])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_reference_gases.addTopLevelItem(new)
        
    def load_new_gas_composition_info(self):
        # if self.selected_fluid != "":
        self.treeWidget_new_gas.clear()
        self.treeWidget_new_gas.setGeometry(404, 28, 360, 400)
        self.treeWidget_new_gas.headerItem().setText(0, "Fluid")
        self.treeWidget_new_gas.headerItem().setText(1, "Composition [%]")
        for fluid, [str_composition, _] in self.fluid_to_composition.items():
            new = QTreeWidgetItem([fluid, str_composition])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_new_gas.addTopLevelItem(new)
        self.label_selected_fluid.setText("")
        self.lineEdit_composition.setText("")

    def check_composition_input(self):
        self.str_composition_value = self.lineEdit_composition.text()
        
        title = "Invalid input value to the fluid Composition"
        message = ""
        value = None
        try:
            value = float(self.str_composition_value)
        except Exception as log_error:
            message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
            message += "\nPlease, check the typed value to proceed with the fluid setup.\n\n"
            message += str(log_error)
        
        if value is not None:             
            if value>100 or value<0:
                message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
                message += "The value must be a positive value less or equals to 100."
                message += "\nPlease, check the typed value to proceed with the fluid setup."
        
        if round(value/100, 5) > self.remaining_composition:
            _remain = round(self.remaining_composition*100, 3)
            message = "Dear user, you have typed an invalid entry at the Fluid Composition input. "
            message += f"The value must be a positive value less or equals to {_remain}%."
            message += "\nPlease, check the typed value to proceed with the fluid setup."

        if message == "":
            
            self.composition_value = value/100
            self.fluid_to_composition[self.selected_fluid] = [self.str_composition_value, self.composition_value]
            if self.composition_value == 0:
                if self.selected_fluid in self.fluid_to_composition.keys():
                    self.fluid_to_composition.pop(self.selected_fluid)       
            return False
        else:
            PrintMessageInput([title, message, window_title_1])
            return True

    def on_click_item_reference_gases(self, item):
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(self.selected_fluid)
    
    def on_double_click_item_new_gas(self, item):
        return
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(item.text(0))
        self.lineEdit_composition.setText(item.text(1))

    def on_click_item_new_gas(self, item):
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(item.text(0))
        self.lineEdit_composition.setText(item.text(1))
        
    def confirm_pressed(self):
        pass

    def default_library_gases(self):
        self.list_gases = [ "argon",
                            "benzene", "butane",
                            "carbon dioxide", "carbon monoxide",
                            "helium", "heptane", "hydrogen", "hydrogen sulfide",
                            "isopropane", "isobutane", "isopentene",
                            "methane",
                            "nitrogen",
                            "oxygen",
                            "propane"]

    # def reset_input_field(self):
    #     self.lineEdit_FileName.setText("")

    # def frames_value_changed(self):
    #     self.opv.opvAnalysisRenderer._numberFramesHasChanged(True)
    #     self.frames = self.spinBox_frames.value()
        
    # def cycles_value_changed(self):
    #     self.cycles = self.spinBox_cycles.value()

    # def update_export_tabs(self):
    #     if self.checkBox_export.isChecked():
    #         self.tabWidget_animation.addTab(self.tab_export, "Export animation")
    #     else:
    #         self.tabWidget_animation.removeTab(1)

    # def choose_path_export_animation(self):
    #     self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
    #     self.save_name = basename(self.save_path)
    #     self.label_export_path.setText(str(self.save_path))

    # def get_file_format(self):
    #     index = self.comboBox_file_format.currentIndex()
    #     _formats = [".avi", ".mp4", ".ogv", ".mpeg"]
    #     return _formats[index]

    # def export_animation_to_file(self):
    #     if self.lineEdit_FileName.text() != "":
    #         file_format = self.get_file_format()
    #         filename = self.lineEdit_FileName.text() + file_format
    #         if os.path.exists(self.save_path):
    #             self.export_file_path = get_new_path(self.save_path, filename)
    #             self.opv.opvAnalysisRenderer.start_export_animation_to_file(self.export_file_path, self.frames)
    #             self.process_animation()
    #         else:
    #             title = "Invalid folder path"
    #             message = "Inform a valid folder path before trying export the animation.\n\n"
    #             message += f"{self.label_export_path.text()}"
    #             PrintMessageInput([title, message, "ERROR"])
    #             self.label_export_path.setText("<Folder path>")
    #     else:
    #         title = "Empty file name"
    #         message = "Inform a file name before trying export the animation."
    #         PrintMessageInput([title, message, "ERROR"])
    #         self.lineEdit_FileName.setFocus()
