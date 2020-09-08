from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.utils import error
from pulse.preprocessing.cross_section import CrossSection
import numpy as np

class CrossSectionInput(QDialog):
    def __init__(self, project, lines_id, elements_id, external_diameter=0, thickness=0, offset_y=0, offset_z=0, pipe_to_beam=False, beam_to_pipe=False, *args, **kwargs):
        
        # self.pipe_to_beam = kwargs.get('pipe_to_beam', False)
        # self.beam_to_pipe = kwargs.get('beam_to_pipe', False)

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

        self.pipe_to_beam = pipe_to_beam
        self.beam_to_pipe = beam_to_pipe

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
        self.lineEdit_InsulationDensity = self.findChild(QLineEdit, 'lineEdit_InsulationDensity')
        self.lineEdit_InsulationThickness = self.findChild(QLineEdit, 'lineEdit_InsulationThickness')    

        self.lineEdit_area = self.findChild(QLineEdit, 'lineEdit_area')
        self.lineEdit_Iyy = self.findChild(QLineEdit, 'lineEdit_Iyy')
        self.lineEdit_Izz = self.findChild(QLineEdit, 'lineEdit_Izz')
        self.lineEdit_Iyz = self.findChild(QLineEdit, 'lineEdit_Iyz')
        self.lineEdit_base = self.findChild(QLineEdit, 'lineEdit_base')
        self.lineEdit_height = self.findChild(QLineEdit, 'lineEdit_height')
        self.lineEdit_outer_diameter_beam = self.findChild(QLineEdit, 'lineEdit_outer_diameter_beam')
        self.lineEdit_inner_diameter_beam = self.findChild(QLineEdit, 'lineEdit_inner_diameter_beam')

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)

        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()

        self.tabWidget_beam_info = self.findChild(QTabWidget, 'tabWidget_beam_info')
        self.tabWidget_beam_info.currentChanged.connect(self.tabEvent_beam)
        self.currentTab_beam = self.tabWidget_beam_info.currentIndex()
        
        self.tab_pipe = self.tabWidget_general.findChild(QWidget, "tab_pipe")
        self.tab_beam = self.tabWidget_general.findChild(QWidget, "tab_beam")
        
        self.pushButton_confirm_pipe = self.findChild(QPushButton, 'pushButton_confirm_pipe')
        self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe)

        self.pushButton_confirm_pipe_2 = self.findChild(QPushButton, 'pushButton_confirm_pipe_2')
        self.pushButton_confirm_pipe_2.clicked.connect(self.confirm_pipe)

        self.pushButton_confirm_beam = self.findChild(QPushButton, 'pushButton_confirm_beam')
        self.pushButton_confirm_beam.clicked.connect(self.confirm_beam)

        self.pushButton_confirm_beam_2 = self.findChild(QPushButton, 'pushButton_confirm_beam_2')
        self.pushButton_confirm_beam_2.clicked.connect(self.confirm_beam)

        self.pushButton_confirm_beam_3 = self.findChild(QPushButton, 'pushButton_confirm_beam_3')
        self.pushButton_confirm_beam_3.clicked.connect(self.confirm_beam)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.comboBox_pipe = self.findChild(QComboBox, 'comboBox_pipe')
        # self.comboBox_pipe.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox_pipe.currentIndex()

        self.comboBox_beam = self.findChild(QComboBox, 'comboBox_beam')
        # self.comboBox_beam.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox_beam.currentIndex()
        
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

        if self.external_diameter!=0 and self.thickness!=0:
            self.lineEdit_outerDiameter.setText(str(self.external_diameter))
            self.lineEdit_thickness.setText(str(self.thickness))
            self.lineEdit_offset_y.setText(str(self.offset_y))
            self.lineEdit_offset_z.setText(str(self.offset_z))
               
        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentWidget(self.tab_beam)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentWidget(self.tab_pipe)
            self.tabWidget_general.setTabEnabled(1, False)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.confirm_pipe()
            if self.tabWidget_general.currentIndex() == 1:
                self.confirm_beam()
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

    def tabEvent_cross_section(self):
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()

    def tabEvent_beam(self):
        self.currentTab_beam = self.tabWidget_beam_info.currentIndex()

    # def selectionChange(self, comboBox):
    #     self.index = comboBox.currentIndex()
    #     if self.index == 0:
    #         self.element_type = 'pipe_1'
    #     elif self.index == 1:
    #         self.element_type = 'pipe_2'
    #     elif self.index ==2:
    #         self.element_type = 'beam_1'
    #     # elif self.index == 3:
    #     #     self.element_type = 'shell'

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
    
    def confirm_pipe(self):
        self.index = self.comboBox_pipe.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'
        # print("Element type: ", self.element_type)
        self.check_pipe()

    def confirm_beam(self):
        self.index = self.comboBox_beam.currentIndex()
        if self.index == 0:
            self.element_type = 'beam_1'
        # print("Element type: ", self.element_type)
        self.check_beam()

    def check_pipe(self):

        if self.flagElements:
            if self.check_input_elements():
                return

        if self.currentTab_cross_section == 0:
            if self.lineEdit_outerDiameter.text() == "":
                error("Insert some value (OUTER DIAMETER)!", title="INPUT CROSS-SECTION ERROR")
                return
            elif self.lineEdit_thickness.text() == "":
                error("Insert some value (THICKENSS)!", title="INPUT CROSS-SECTION ERROR")
                return

            offset_y = float(0)
            offset_z = float(0)
            insulation_density = float(0)
            insulation_thickness = float(0)

            try:
                outerDiameter = float(self.lineEdit_outerDiameter.text())
            except Exception:
                error("Wrong input for OUTER DIAMETER!", title="INPUT CROSS-SECTION ERROR")
                return
            try:
                thickness = float(self.lineEdit_thickness.text())
            except Exception:
                error("Wrong input for THICKENSS!", title="INPUT CROSS-SECTION ERROR")
                return

            if self.lineEdit_offset_y.text() != "":
                try:
                    offset_y = float(self.lineEdit_offset_y.text())
                except Exception:
                    error("Wrong input for OFFSET Y!", title="INPUT CROSS-SECTION ERROR")
                    return

            if self.lineEdit_offset_z.text() != "":
                try:
                    offset_z = float(self.lineEdit_offset_z.text())
                except Exception:
                    error("Wrong input for OFFSET Z!", title="INPUT CROSS-SECTION ERROR")
                    return
           
            if self.lineEdit_InsulationDensity.text() != "":
                try:
                    insulation_density = float(self.lineEdit_InsulationDensity.text())
                except Exception:
                    error("Wrong input for INSULATION DENSITY!", title="INPUT CROSS-SECTION ERROR")
                    return
           
            if self.lineEdit_InsulationThickness.text() != "":
                try:
                    insulation_thickness = float(self.lineEdit_InsulationThickness.text())
                except Exception:
                    error("Wrong input for INSULATION THICKNESS!", title="INPUT CROSS-SECTION ERROR")
                    return
           
            if thickness > (outerDiameter/2):
                error("The THICKNESS must be less or equals to the OUTER RADIUS!", title="INPUT CROSS-SECTION ERROR")
                return

            elif thickness == 0.0:
                error("The THICKNESS must be greater than zero!", title="INPUT CROSS-SECTION ERROR")
                return
            
            elif abs(offset_y) > 0.2*(outerDiameter/2):
                error("The OFFSET_Y must be less than 20{%} of the external radius!", title="INPUT CROSS-SECTION ERROR")
                return
            
            elif abs(offset_z) > 0.2*(outerDiameter/2):
                error("The OFFSET_Y must be less than 20{%} of the external radius!", title="INPUT CROSS-SECTION ERROR")
                return
            # print(insulation_thickness, insulation_density)
            self.cross_section = CrossSection(outerDiameter, thickness, offset_y, offset_z, insulation_density=insulation_density, insulation_thickness= insulation_thickness)

        self.complete = True
        self.close()

    def check_beam(self):

        if self.flagElements:
            if self.check_input_elements():
                return
        
        if self.currentTab_cross_section == 1:

            area = float(0)
            Iyy = float(0)
            Izz = float(0)
            Iyz = float(0)

            if self.currentTab_beam == 0:
   
                if self.lineEdit_base.text() != "":
                    try:
                        base = float(self.lineEdit_base.text())
                        if base <= 0:
                            error("Insert a positive value to the BASE!", title="INPUT CROSS-SECTION ERROR")
                            return
                    except Exception:
                        error("Wrong input for BASE!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for BASE!", title="INPUT CROSS-SECTION ERROR")
                    return
                
                if self.lineEdit_height.text() != "":
                    try:
                        height = float(self.lineEdit_height.text())
                        if height <= 0:
                            error("Insert a positive value to the HEIGHT!", title="INPUT CROSS-SECTION ERROR")
                            return     
                    except Exception:
                        error("Wrong input for HEIGHT!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for HEIGHT!", title="INPUT CROSS-SECTION ERROR")
                    return            

                area = base*height
                Iyy = (base**3)*height/12
                Izz = (height**3)*base/12
                self.external_diameter = 2*np.abs(np.sqrt(area/np.pi))

            elif self.currentTab_beam == 1:

                inner_diameter_beam = float(0)

                if self.lineEdit_outer_diameter_beam.text() == "":
                    error("Insert some value for OUTER DIAMETER!", title="INPUT CROSS-SECTION ERROR")
                    return
                else:
                    try:
                        outer_diameter_beam = float(self.lineEdit_outer_diameter_beam.text())
                        if outer_diameter_beam <= 0:
                            error("The OUTER DIAMETER must be greater than ZERO!", title="INPUT CROSS-SECTION ERROR")
                            return                    
                    except Exception:
                        error("Wrong input for OUTER DIAMETER!", title="INPUT CROSS-SECTION ERROR")
                        return

                if self.lineEdit_outer_diameter_beam.text() != "":
                    try:
                        inner_diameter_beam = float(self.lineEdit_inner_diameter_beam.text())
                        if outer_diameter_beam <= inner_diameter_beam:
                            error("The INNER DIAMETER must be less than OUTER DIAMETER!", title="INPUT CROSS-SECTION ERROR")
                            return
                        elif inner_diameter_beam < 0:
                            error("The INNER DIAMETER must be greater than or equals to ZERO!", title="INPUT CROSS-SECTION ERROR")
                            return   
                    except Exception:
                        error("Wrong input for INNER DIAMETER!", title="INPUT CROSS-SECTION ERROR")
                        return

                area = np.pi*((outer_diameter_beam**2)-(inner_diameter_beam**2))/4
                Iyy = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
                Izz = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
                Iyz = 0.
                self.external_diameter = outer_diameter_beam

            elif self.currentTab_beam == 2:

                if self.lineEdit_area.text() != "":
                    try:
                        area = float(self.lineEdit_area.text())
                        if area <= 0:
                            error("Insert a positive value to the AREA!", title="INPUT CROSS-SECTION ERROR")
                            return
                    except Exception:
                        error("Wrong input for AREA!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for AREA!", title="INPUT CROSS-SECTION ERROR")
                    return

                if self.lineEdit_Iyy.text() != "":
                    try:
                        Iyy = float(self.lineEdit_Iyy.text())
                        if Iyy <= 0:
                            error("Insert a positive value to the SECOND MOMENT OF AREA YY!", title="INPUT CROSS-SECTION ERROR")
                            return
                    except Exception:
                        error("Wrong input for Iyy!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for Iyy!", title="INPUT CROSS-SECTION ERROR")
                    return

                if self.lineEdit_Izz.text() != "":
                    try:
                        Izz = float(self.lineEdit_Izz.text())
                    except Exception:
                        error("Wrong input for Izz!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for Izz!", title="INPUT CROSS-SECTION ERROR")
                    return

                if self.lineEdit_Izz.text() != "":
                    try:
                        Izz = float(self.lineEdit_Izz.text())
                        if Izz <= 0:
                            error("Insert a positive value to the SECOND MOMENT OF AREA ZZ!", title="INPUT CROSS-SECTION ERROR")  
                            return 
                    except Exception:
                        error("Wrong input for Izz!", title="INPUT CROSS-SECTION ERROR")
                        return
                else:
                    error("Insert some value for Izz!", title="INPUT CROSS-SECTION ERROR")
                    return

                if self.lineEdit_Iyz.text() == "":
                    try:
                        Iyz = float(self.lineEdit_Iyz.text())
                    except Exception:
                        error("Wrong input for Iyz!", title="INPUT CROSS-SECTION ERROR")
                        return    
                
                self.external_diameter = 2*np.abs(np.sqrt(area/np.pi))

            self.thickness = 0
            self.cross_section = CrossSection(self.external_diameter, self.thickness, 0, 0, area=area, Iyy=Iyy, Izz=Izz, Iyz=Iyz)

        self.complete = True
        self.close()