from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.utils import error
from pulse.preprocessing.cross_section import CrossSection

class CrossSectionInput(QDialog):
    def __init__(self, project, lines_id, elements_id, external_diameter=0, thickness=0, offset_y=0, offset_z=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/crossSectionInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.structural_elements = self.project.mesh.structural_elements
        self.lines_id = lines_id
        self.elements_id = elements_id

        self.external_diameter = external_diameter
        self.thickness = thickness
        self.offset_y = offset_y
        self.offset_z = offset_z

        self.section = None
        self.complete = False
        self.flagAll = False
        self.flagEntity = False
        self.currentTab = 0

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')

        self.lineEdit_outerDiameter = self.findChild(QLineEdit, 'lineEdit_outerDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')

        self.lineEdit_area = self.findChild(QLineEdit, 'lineEdit_area')
        self.lineEdit_iyy = self.findChild(QLineEdit, 'lineEdit_iyy')
        self.lineEdit_izz = self.findChild(QLineEdit, 'lineEdit_izz')
        self.lineEdit_iyz = self.findChild(QLineEdit, 'lineEdit_iyz')

        self.lineEdit_InsulationDensity = self.findChild(QLineEdit, 'lineEdit_InsulationDensity')
        self.lineEdit_InsulationThickness = self.findChild(QLineEdit, 'lineEdit_InsulationThickness')        

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        
        if self.lines_id != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.write_ids(lines_id)
            self.radioButton_selected_lines.setChecked(True)
        elif self.elements_id != []:
            self.lineEdit_id_labels.setText("Elements IDs:")
            self.write_ids(elements_id)
            self.radioButton_selected_elements.setChecked(True)
        else:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all_lines.setChecked(True)

        self.currentTab = self.tabWidget.currentIndex()

        if self.external_diameter!=0 and self.thickness!=0:
            self.lineEdit_outerDiameter.setText(str(self.external_diameter))
            self.lineEdit_thickness.setText(str(self.thickness))
            self.lineEdit_offset_y.setText(str(self.offset_y))
            self.lineEdit_offset_z.setText(str(self.offset_z))

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        if self.flagAll:
            self.lineEdit_selected_ID.setText("All lines")
     
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def check_input_elements(self):

        try:
            tokens = self.lineEdit_selected_ID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.element_typed = list(map(int, tokens))
            
            if self.lineEdit_selected_ID.text()=="":
                error("Inform a valid Node ID before to confirm the input!", title = "Error Node ID's")
                return True

        except Exception:
            error("Wrong input for Node ID's!", "Error Node ID's")
            return True

        try:
            for element in self.element_typed:
                self.elementID = self.structural_elements[element].index
        except Exception:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.structural_elements))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return True
        return False
    
    def check(self):

        if self.flagElements:
            if self.check_input_elements():
                return

        if self.currentTab == 0 or True:
            #Pipe
            if self.lineEdit_outerDiameter.text() == "":
                error("Insert some value (OUTER DIAMETER)!", title="INPUT CROSS-SECTION ERROR")
                return
            elif self.lineEdit_thickness.text() == "":
                error("Insert some value (THICKENSS)!", title="INPUT CROSS-SECTION ERROR")
                return

            offset_y = 0
            offset_z = 0
            insulation_density = 0
            insulation_thickness = 0

            try:
                outerDiameter = float(self.lineEdit_outerDiameter.text())
            except Exception:
                error("Wrong input for OUTER DIAMETER!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            try:
                thickness = float(self.lineEdit_thickness.text())
            except Exception:
                error("Wrong input for THICKENSS!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return

            if self.lineEdit_offset_y.text() != "":
                try:
                    offset_y = float(self.lineEdit_offset_y.text())
                except Exception:
                    error("Wrong input for OFFSET Y!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                    return

            if self.lineEdit_offset_z.text() != "":
                try:
                    offset_z = float(self.lineEdit_offset_z.text())
                except Exception:
                    error("Wrong input for OFFSET Z!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                    return
           
            if self.lineEdit_InsulationDensity.text() != "":
                try:
                    insulation_density = float(self.lineEdit_InsulationDensity.text())
                except Exception:
                    error("Wrong input for INSULATION DENSITY!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                    return
           
            if self.lineEdit_InsulationThickness.text() != "":
                try:
                    insulation_thickness = float(self.lineEdit_InsulationThickness.text())
                except Exception:
                    error("Wrong input for INSULATION THICKNESS!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                    return
           
            if thickness > (outerDiameter/2):
                error("The THICKNESS must be less or equals to the OUTER RADIUS!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return

            elif thickness == 0.0:
                error("The THICKNESS must be greater than zero!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            elif abs(offset_y) > 0.2*(outerDiameter/2):
                error("The OFFSET_Y must be less than 20{%} of the external radius!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            elif abs(offset_z) > 0.2*(outerDiameter/2):
                error("The OFFSET_Y must be less than 20{%} of the external radius!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            # print(insulation_thickness, insulation_density)
            self.cross_section = CrossSection(outerDiameter, thickness, offset_y, offset_z, insulation_density=insulation_density, insulation_thickness= insulation_thickness)
            self.complete = True
            self.close()
        else:
            pass
