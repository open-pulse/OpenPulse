from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt    
    
class PlotCrossSectionInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotSectionInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.stop = False
        
        self.structural_elements = self.project.mesh.structural_elements
        self.dict_tag_to_entity = self.project.mesh.get_dict_of_entities()
        self.line_id = self.opv.getListPickedEntities()
        self.element_id = self.opv.getListPickedElements()
        self._get_dict_key_section()

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
        self.exec_()

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
        elif self.flagElements:
            self.lineEdit_id_labels.setText("Element ID:")
            self.write_ids(self.element_id)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):

        self.line_id = self.opv.getListPickedEntities()
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
            self.lineEdit_id_labels.setText("Selected ID:")
            self.lineEdit_selected_ID.setText("")

    def check_input_element(self):

        try:
            tokens = self.lineEdit_selected_ID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.element_typed = list(map(int, tokens))

            if len(self.element_typed) > 1:
                message = "Please, select only one element \nto plot its cross-section."
                title = "Error: multiple elements in selection"
                self.info_text = [title, message]
                return True
            
            if self.lineEdit_selected_ID.text() == "":
                message = "Inform a valid Element ID before \nto confirm the input."
                title = "Error: empty Element ID input"
                self.info_text = [title, message]
                return True

        except Exception:
            message = "Wrong input for Element ID."
            title = "Error in Element ID"
            self.info_text = [title, message]
            return True

        try:
            for element in self.element_typed:
                self.element = self.structural_elements[element]
        except Exception:
            message = " The Element ID input values must be\n major than 1 and less than {}.".format(len(self.structural_elements))
            title = "Error: invalid Element ID input"
            self.info_text = [title, message]
            return True
        return False

    def check_input_line(self):
        try:
            tokens = self.lineEdit_selected_ID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.line_typed = list(map(int, tokens))

            if len(self.line_typed) > 1:
                message = "Please, select only one line \nto plot its cross-section."
                title = "Error: multiple lines in selection"
                self.info_text = [title, message]
                return True
            
            if self.lineEdit_selected_ID.text()=="":
                message = "Inform a valid Line ID before \nto confirm the input!."
                title = "Error: empty Line ID input"
                self.info_text = [title, message]
                return True
        except Exception:
            message = "Wrong input for Line ID!"
            title = "Error: invalid Line ID input"
            self.info_text = [title, message]
            return True
        try:
            for line in self.line_typed:
                self.line = self.dict_tag_to_entity[line]
        except Exception:
            message = "The Line ID input values must be \nmajor than 1 and less than {}.".format(len(self.dict_tag_to_entity))
            title = "Error: invalid Line ID"
            self.info_text = [title, message]
            return True
        return False

    def _get_dict_key_section(self):
        self.labels = ["Pipe section", "Rectangular section", "Circular section", "C-section", "I-section", "T-section", "Generic section"]
        self.dict_sections = dict(zip(self.labels, np.arange(7)))
        
    def preprocess_selection(self):

        if self.flagEntity:

            if self.check_input_line():
                PrintMessageInput(self.info_text)
                return None

            entity = self.dict_tag_to_entity[self.line_typed[0]]
            if entity.cross_section is None:
                message = "Please, define a cross-section to the \nselected line before trying to plot the section."
                title = "Error: undefined line cross-section"
                self.info_text = [title, message]
                return None
            additional_section_info = entity.cross_section.additional_section_info
    
        elif self.flagElements:

            if self.check_input_element():
                PrintMessageInput(self.info_text)
                return None

            element = self.structural_elements[self.element_typed[0]]
            if element.cross_section is None:
                message = "Please, define a cross-section to the selected \nelement before trying to plot the section."
                title = "Error: undefined element cross-section"
                self.info_text = [title, message]     
                PrintMessageInput(self.info_text)       
                return None

            additional_section_info = element.cross_section.additional_section_info

        self.parameters = additional_section_info[1]
        self.section_type = self.dict_sections[additional_section_info[0]]

        return 0

    def get_points_to_plot_section(self):

        if self.section_type == 0: # Pipe section

            N = 60
            d_out, thickness, offset_y, offset_z, insulation_thickness = self.parameters
            self.insulation_thickness = insulation_thickness
            Yc, Zc = offset_y, offset_z

            d_theta = np.pi/N
            theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)
            d_in = d_out - 2*thickness

            Yp_out = (d_out/2)*np.cos(theta)
            Zp_out = (d_out/2)*np.sin(theta)
            Yp_in = (d_in/2)*np.cos(-theta)
            Zp_in = (d_in/2)*np.sin(-theta)

            Yp_list = [list(Yp_out), list(Yp_in),[0]]
            Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)
            
            Yp = np.array([Yp_right, Yp_left]).flatten() + Yc
            Zp = np.array([Zp_right, Zp_left]).flatten() + Zc
            
            if insulation_thickness != float(0):

                Yp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.cos(theta)
                Zp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.sin(theta)
                Yp_in_ins = (d_out/2)*np.cos(-theta)
                Zp_in_ins = (d_out/2)*np.sin(-theta)

                Yp_list_ins = [list(Yp_out_ins), list(Yp_in_ins), [0]]
                Zp_list_ins = [list(Zp_out_ins), list(Zp_in_ins), [-(d_out/2)]]

                Yp_right_ins = [value for _list in Yp_list_ins for value in _list]
                Zp_right_ins = [value for _list in Zp_list_ins for value in _list]

                Yp_left_ins = -np.flip(Yp_right_ins)
                Zp_left_ins =  np.flip(Zp_right_ins)

                self.Yp_ins = np.array([Yp_right_ins, Yp_left_ins]).flatten() + Yc
                self.Zp_ins = np.array([Zp_right_ins, Zp_left_ins]).flatten() + Zc
                
        if self.section_type == 1: # Rectangular section

            b, h, b_in, h_in, Yc, Zc = self.parameters
            Yp_right = [0, (b/2), (b/2), 0, 0, (b_in/2), (b_in/2), 0, 0]
            Zp_right = [-(h/2), -(h/2), (h/2), (h/2), (h_in/2), (h_in/2), -(h_in/2), -(h_in/2), -(h/2)]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 2: # Circular section
            
            N = 60
            d_out, d_in, Yc, Zc = self.parameters
            
            d_theta = np.pi/N
            theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)

            Yp_out = (d_out/2)*np.cos(theta)
            Zp_out = (d_out/2)*np.sin(theta)
            Yp_in = (d_in/2)*np.cos(-theta)
            Zp_in = (d_in/2)*np.sin(-theta)

            Yp_list = [list(Yp_out), list(Yp_in), [0]]
            Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 3: # Beam: C-section

            h, w1, w2, w3, t1, t2, t3, r, Yc, Zc = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w3, w3, w2+r]) 
            Yp_list.append(list(np.flip(-y_r+w2)))
            Yp_list.append([w2, w2])
            Yp_list.append(list(w2-y_r))
            Yp_list.append([w2+r, w1, w1, 0, 0])

            Zp_list =[]
            Zp_list.append([-(h/2), -(h/2), -(t2/2), -(t2/2)]) 
            Zp_list.append(list(np.flip((-z_r+r)-(t2/2))))
            Zp_list.append([-(h/2)+t3+r, (h/2)-t1-r])
            Zp_list.append(list(z_r+(t2/2)-r))
            Zp_list.append([(h/2)-t1, (h/2)-t1, (h/2), (h/2), -(h/2)])

            Yp = [value for _list in Yp_list for value in _list]
            Zp = [value for _list in Zp_list for value in _list]

        elif self.section_type == 4: # Beam: I-section

            h, w1, w2, w3, t1, t2, t3, r, Yc, Zc = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w3/2, w3/2, (w2/2)+r]) 
            Yp_list.append(list(np.flip(-y_r+(w2/2))))
            Yp_list.append([w2/2, w2/2])
            Yp_list.append(list((w2/2)-y_r))
            Yp_list.append([(w2/2)+r, w1/2, w1/2, 0])

            Zp_list =[]
            Zp_list.append([-(h/2), -(h/2), -((h/2)-t3), -((h/2)-t3)]) 
            Zp_list.append(list(np.flip((-z_r+r)-((h/2)-t3))))
            Zp_list.append([-(h/2)+t3+r, (h/2)-t1-r])
            Zp_list.append(list(z_r+(h/2)-t1-r))
            Zp_list.append([(h/2)-t1, (h/2)-t1, (h/2), (h/2)])

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 5: # Beam: T-section

            h, w1, w2, t1, t2, r, Yc, Zc = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w2/2, w2/2])
            Yp_list.append(list((w2/2)-y_r))
            Yp_list.append([(w2/2)+r, w1/2, w1/2, 0])

            Zp_list =[]
            Zp_list.append([-(t2/2), -(t2/2), (h/2)-t1-r])
            Zp_list.append(list(z_r+(t2/2)-r))
            Zp_list.append([(t2/2), (t2/2), (t2/2)+t1, (t2/2)+t1])

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()
        
        elif self.section_type == 6: # Beam: Generic section

            message = "The GENERIC BEAM SECTION cannot be ploted."
            title = "Error while graphing cross-section"
            info_text = [title, message]

            PrintMessageInput(info_text)

            self.stop = True
            return 0, 0, 0, 0

        return Yp, Zp, Yc, Zc
        
    def get_points_at_radius(self, r, N=20):

            d_theta = (np.pi/2)/N
            theta = np.arange(d_theta, (np.pi/2), d_theta)
            y_r = -r + r*np.cos(theta)
            z_r = r*np.sin(theta)

            return y_r, z_r

    def plot_section(self):

        plt.close()

        if self.preprocess_selection() is None:
            return

        Yp, Zp, Yc, Zc = self.get_points_to_plot_section()

        if self.stop:
            self.stop = False
            return

        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(Yc, Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)

        if self.section_type == 0 and self.insulation_thickness != float(0):
            third_plot, = plt.fill(self.Yp_ins, self.Zp_ins, color=[0.5,1,1], linewidth=2, zorder=4) 
            _max = np.max(np.abs(np.array([self.Zp_ins, self.Yp_ins])))*1.2
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            third_plot.set_label("Insulation material")
            plt.legend(handles=[second_plot, third_plot], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')
        else:
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            plt.legend(handles=[second_plot], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')

        ax.set_title('CROSS-SECTION PLOT', fontsize = 18, fontweight = 'bold')
        ax.set_xlabel('y [m]', fontsize = 16, fontweight = 'bold')
        ax.set_ylabel('z [m]', fontsize = 16, fontweight = 'bold')
        
        f = 1.25
        if self.section_type == 3:
            plt.xlim(-(1/2)*_max, (3/2)*_max)
        else:
            plt.xlim(-_max*f, _max*f)

        plt.ylim(-_max*f, _max*f)
        plt.grid()
        plt.show()