from PyQt5.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import configparser
import numpy as np

from data.user_input.model.setup.general.material_input_new import MaterialInputs
from pulse.preprocessing.material import Material
from pulse.lib.default_libraries import default_material_library
from data.user_input.model.setup.pickColorInput import PickColorInput
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.call_double_confirmation_input import CallDoubleConfirmationInput

window_title = "ERROR"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class SetMaterialInput(QDialog):
    def __init__(   self, project, opv, cache_selected_lines=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # uic.loadUi(Path('data/user_input/ui_files/Model/Setup/Structural/material_input.ui'), self)
        uic.loadUi(Path('data/user_input/ui_files/Model/Setup/general/set_material_input.ui'), self)

        self.project = project
        self.opv = opv
        self.cache_selected_lines = cache_selected_lines

        self.opv.setInputObject(self)
        self.lines_ids = self.opv.getListPickedLines()
        
        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        # self._create_connections()
        self.exec()

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set material")

    def _reset_variables(self):
        self.clicked_item = None
        self.material = None
        self.flagAll = False
        self.flagSelectedLines = False

        self.adding = False
        self.editing = False
        self.list_names = []
        self.list_ids = []
        self.list_colors = []
        self.temp_material_name = ""
        self.temp_material_id = ""
        self.temp_material_color = ""
        self.dict_inputs = {}

        self.main_window = self.opv.parent
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.material_path = self.project.get_material_list_path()
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_attribution_type = self.findChild(QComboBox, 'comboBox_attribution_type')
        self.comboBox_material_id = self.findChild(QComboBox, 'comboBox_material_id')

        # QFrame
        self.frame_main_widget = self.findChild(QFrame, 'frame_main_widget')

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.frame_main_widget.setLayout(self.grid_layout)
        self._add_material_input_widget()

        # QLineEdit
        self.lineEdit_selected_id = self.findChild(QLineEdit, 'lineEdit_selected_id')
        self.lineEdit_selected_material_name = self.findChild(QLineEdit, 'lineEdit_selected_material_name')

        # QPushButton
        self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')
        
        # # QRadioButton
        # self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        
        # QTableWidget
        self.tableWidget_material_data = self.findChild(QTabWidget, 'tableWidget_material_data')
        
        # # QTreeWidget
        # self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')

    def _add_material_input_widget(self):
        self.material_widget = MaterialInputs(self.main_window)
        self.grid_layout.addWidget(self.material_widget)

    def _create_connections(self):
        #
        self.comboBox_material_id.currentIndexChanged.connect(self.get_comboBox_index)
        self.comboBox_attribution_type.currentIndexChanged.connect(self.get_comboBox_index)
        #
        self.pushButton_attribute_material.clicked.connect(self.confirm_material_attribution)
        #
        self.tableWidget_material_data.cellClicked.connect(self.on_cell_clicked)

    def on_cell_clicked(self, row, col):
        print(row, col)

    def _loading_info_at_start(self):
        if self.cache_selected_lines != []:
            self.lines_ids = self.cache_selected_lines

        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)

        else:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)
            self.radioButton_all.setChecked(True) 


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_material_attribution()
        elif event.key() == Qt.Key_Delete:
            self.confirm_material_removal()
        elif event.key() == Qt.Key_Escape:
            self.close()


    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)


    def update(self):
        self.lines_ids = self.opv.getListPickedLines()
        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_id.setEnabled(True)
        else:
            self.lineEdit_selected_id.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_id.setEnabled(False)


    def confirm_material_attribution(self):

        if self.clicked_item is None:
            self.title = "NO MATERIAL SELECTION"
            self.message = "Select a material in the list before \nconfirming the material attribution."
            PrintMessageInput([self.title, self.message, window_title])
            return
        
        try:

            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            density = float(self.clicked_item.text(2))
            young = float(self.clicked_item.text(3))*(10**(9))
            poisson = float(self.clicked_item.text(4))
            thermal_expansion_coefficient = float(self.clicked_item.text(5))
            color = self.clicked_item.text(6)
            
            new_material = Material(name, 
                                    density,
                                    poisson_ratio = poisson, 
                                    young_modulus = young, 
                                    identifier = identifier, 
                                    thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                    color = color)
            self.material = new_material
            
            if self.flagSelectedLines:

                lineEdit = self.lineEdit_selected_id.text()
                self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 
                               
                self.project.set_material_by_lines(self.lines_typed, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_typed, self.material.getNormalizedColorRGB())
            else:
                self.project.set_material_to_all_lines(self.material)       
                print("[Set Material] - {} defined in all entities".format(self.material.name))
                # self.opv.changeColorEntities(entities, self.material.getNormalizedColorRGB())
            self.close()

        except Exception as error_log:
            self.title = "ERROR WITH THE MATERIAL LIST DATA"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            return


    def update_material_id_selector(self):

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_material_id.setFont(font)
        self.comboBox_material_id.setStyleSheet("color: rgb(0, 0, 255);")

        N = 100
        self.available_indexes = list(np.arange(1,N+1))
        for _id in self.list_ids:
            if _id in self.available_indexes:
                self.available_indexes.remove(_id)

        self.comboBox_material_id.clear()
        for material_id in self.available_indexes:
            text = f"         {material_id}"
            self.comboBox_material_id.addItem(text)

        self.get_comboBox_index()


    def get_comboBox_index(self):
        index = self.comboBox_material_id.currentIndex()
        self.material_id = self.available_indexes[index] 


    def check_add_material(self):

        self.editing = False
        self.adding = True

        parameters = {  "name" : self.lineEdit_name,
                        "identifier" : self.material_id,
                        "density" : self.lineEdit_density,
                        "young_modulus" : self.lineEdit_youngModulus,
                        "poisson" : self.lineEdit_poisson,
                        "thermal expansion coefficient" : self.lineEdit_thermal_expansion_coefficient,
                        "color" : self.lineEdit_color  }

        if self.check_add_edit(parameters):
            PrintMessageInput([self.title, self.message, window_title])  


    def check_edit_material(self):

        if self.lineEdit_selected_material_name.text() == "":
            title = "None material selected"
            message = "Select a material in the material list to be edited."
            PrintMessageInput([title, message, window_title])
            return
        
        # if self.selected_material_to_edit():
        #     return

        if self.editing:

            parameters = {  "name" : self.lineEdit_name_edit,
                            "identifier" : self.lineEdit_id_edit.text(),
                            "density" : self.lineEdit_density_edit,
                            "young_modulus" : self.lineEdit_youngModulus_edit,
                            "poisson" : self.lineEdit_poisson_edit,
                            "thermal expansion coefficient" : self.lineEdit_thermal_expansion_coefficient_edit,
                            "color" : self.lineEdit_color_edit  }

            if self.check_add_edit(parameters):
                PrintMessageInput([self.title, self.message, window_title])      


    def check_color_input(self, lineEdit_color):
        
        self.title = "INVALID MATERIAL COLOR ATTRIBUTION"
        message_empty = "An empty entry was detected at the 'Color [r,g,b]' input field. \nYou should to select a color to proceed."
        message_invalid = "Insert a valid material Color in 'r, g, b' format. \nThe r, g and b values must be inside [0, 255] interval."
        color_string = lineEdit_color.text()

        if color_string == "":
            self.message = message_empty
            return True
        else:
            color = color_string
            
            try:

                colorRGB = getColorRGB(color)
                message_color = " The RGB color {} was already used.\n Please, input a different color.".format(colorRGB)
                if len(colorRGB) != 3:
                    self.message = message_invalid
                    return True

                if self.editing:
                    if getColorRGB(self.temp_material_color) != colorRGB:
                        if colorRGB in self.list_colors:
                            self.message = message_color
                            return True 
                elif self.adding:
                    if colorRGB in self.list_colors:
                        self.message = message_color
                        return True

                self.dict_inputs["color"] = color

            except Exception as error_log:
                self.message = message_invalid + "\n\n" + str(error_log)
                return True

    def on_click_item(self, item):
        self.clicked_item = item
        if self.currentTab_ == 0:       
            self.tabWidget_material.setCurrentIndex(1)
        self.selected_material_to_edit()
        self.selected_material_to_remove()

        self.pushButton_pickColor_edit.setDisabled(False)
        self.pushButton_confirm_material_edition.setDisabled(False)
        self.pushButton_confirm_material_removal.setDisabled(False)
        self.lineEdit_selected_material_name.setText(item.text(0))


    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.confirm_material_attribution()
    

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelectedLines = self.radioButton_selected_lines.isChecked()
        if self.flagSelectedLines:
            self.lineEdit_selected_id.setEnabled(True)
            if self.lines_ids != []:
                self.write_ids(self.lines_ids)
            else:
                self.lineEdit_selected_id.setText("")
        elif self.flagAll:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)