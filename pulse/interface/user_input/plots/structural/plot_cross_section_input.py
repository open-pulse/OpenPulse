from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse.preprocessing.cross_section import CrossSection, get_points_to_plot_section
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt    
    
window_title_1 = "Error"
window_title_2 = "Warning"

class PlotCrossSectionInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('pulse/interface/ui_files/plots/model/plot_section_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.line_id = self.opv.getListPickedLines()
        self.element_id = self.opv.getListPickedElements()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        
        self.structural_elements = self.project.preprocessor.structural_elements
        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity

        self.stop = False

        # self._get_dict_key_section()

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')

        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.pushButton_plot_cross_section = self.findChild(QPushButton, 'pushButton_plot_cross_section')  
        self.pushButton_plot_cross_section.clicked.connect(self.plot_section)

        if self.line_id != []:
            self.lineEdit_id_labels.setText("Line ID:")
            self.write_ids(self.line_id)
            self.radioButton_selected_lines.setChecked(True)

        elif self.element_id != []:
            self.lineEdit_id_labels.setText("Element ID:")
            self.write_ids(self.element_id)
            self.radioButton_selected_elements.setChecked(True)
        else:
            self.lineEdit_id_labels.setText("Line ID:")
            self.lineEdit_selected_ID.setText("")
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_section()
        if event.key() == Qt.Key_Escape:
            plt.close()
            self.close()

    def radioButtonEvent(self):
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        if self.flagEntity:
            self.lineEdit_id_labels.setText("Line ID:")
            self.write_ids(self.line_id)
            if self.opv.change_plot_to_mesh:
                self.opv.changePlotToEntitiesWithCrossSection()

        elif self.flagElements:
            self.lineEdit_id_labels.setText("Element ID:")
            self.write_ids(self.element_id)
            if not self.opv.change_plot_to_mesh:
                self.opv.changePlotToMesh()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):

        self.line_id = self.opv.getListPickedLines()
        self.element_id = self.opv.getListPickedElements()

        if self.line_id != []:
            self.lineEdit_id_labels.setText("Line ID:")
            self.write_ids(self.line_id)
            self.radioButton_selected_lines.setChecked(True)
        elif self.element_id != []:
            self.lineEdit_id_labels.setText("Element ID:")
            self.write_ids(self.element_id)
            self.radioButton_selected_elements.setChecked(True)
        else:
            self.lineEdit_selected_ID.setText("")

    # def _get_dict_key_section(self):
    #     self.labels = [ "Pipe section", 
    #                     "Rectangular section", 
    #                     "Circular section", 
    #                     "C-section", 
    #                     "I-section", 
    #                     "T-section", 
    #                     "Generic section"   ]

    def preprocess_selection(self):

        self.stop = False
        self.message = ""

        if self.flagEntity:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.line_typed = self.before_run.check_input_LineID(lineEdit, single_ID=True)
            if self.stop:
                return True

            if self.line_typed in list(self.project.number_sections_by_line.keys()):
                N = self.project.number_sections_by_line[self.line_typed]
                self.message = f"Dear user, you have selected a line with {N} multiple cross-sections, therefore, the cross-section "
                self.message += "plot by line selection will not work. \n\nIn this case, we strongly recommend selecting an element " 
                self.message += "from the desired line to plot its cross-section."
                self.title = "Line with multiples cross-sections"
                self.window_title = window_title_2
                return True

            entity = self.dict_tag_to_entity[self.line_typed]
            
            if entity.cross_section is None and entity.expansion_joint_parameters is None:
                self.message = "Please, define a cross-section to the \nselected line before trying to plot the section."
                self.title = "Error: undefined line cross-section"
                self.window_title = window_title_1
                return True

            cross_section = entity.cross_section
            
        elif self.flagElements:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.element_typed = self.before_run.check_input_ElementID(lineEdit, single_ID=True)
            if self.stop:
                return True

            element = self.structural_elements[self.element_typed]
            if element.cross_section is None:
                self.message = "Please, define a cross-section to the selected \nelement before trying to plot the section."
                self.title = "Error: undefined element cross-section"
                self.window_title = window_title_1          
                return True

            cross_section = element.cross_section

        self.section_label = cross_section.section_label

        if self.section_label != 'Expansion joint section':
            self.section_parameters = cross_section.section_parameters
            # if self.section_label != "Pipe section":
            #     self.section_properties = cross_section.section_properties    
        else:
            self.window_title = window_title_2
            self.title = "Unable to plot cross-section"
            self.message = "The cross-section plot has been deactivated to \n\n"
            self.message += "the 'expansion joint' element type."
            return True
            
        return False

       
    def plot_section(self):

        plt.close()

        if self.preprocess_selection():
            if not self.stop:
                PrintMessageInput([self.title, self.message, self.window_title])
            return
        
        if self.section_label == "Pipe section":
            Yp, Zp, Yp_ins, Zp_ins, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)
        else:
            Yp, Zp, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)

        if self.stop:
            self.stop = False
            return

        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(Yc, Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)
        third_plot = plt.scatter(0, 0, marker="+", linewidth=1.5, zorder=4, color=[0,0,1], s=120)

        if self.section_label == "Pipe section" and Yp_ins is not None:
            fourth, = plt.fill(Yp_ins, Zp_ins, color=[0.5,1,1], linewidth=2, zorder=5) 
            _max = np.max(np.abs(np.array([Zp_ins, Yp_ins])))*1.2
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            fourth.set_label("Insulation material")
            plt.legend(handles=[second_plot, fourth], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')
        else:
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            plt.legend(handles=[second_plot], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')

        ax.set_title('CROSS-SECTION PLOT', fontsize = 18, fontweight = 'bold')
        ax.set_xlabel('y [m]', fontsize = 16, fontweight = 'bold')
        ax.set_ylabel('z [m]', fontsize = 16, fontweight = 'bold')
        
        f = 1.25
        if self.section_label == 'C-section':
            plt.xlim(-(1/2)*_max, (3/2)*_max)
        else:
            plt.xlim(-_max*f, _max*f)

        plt.ylim(-_max*f, _max*f)
        plt.grid()
        plt.show()