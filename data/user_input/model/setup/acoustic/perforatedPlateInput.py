import os
from os.path import basename
from pulse.processing.solution_acoustic import relative_error
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QDialog, QTreeWidget, QToolButton, QSpinBox, QWidget, QRadioButton, QCheckBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pulse.utils import error
import configparser
import numpy as np
import matplotlib.pyplot as plt

from pulse.postprocessing.plot_acoustic_data import get_acoustic_absortion, get_perforated_plate_impedance
from pulse.preprocessing.perforated_plate import PerforatedPlate
from pulse.utils import info_messages, remove_bc_from_file
from data.user_input.project.printMessageInput import PrintMessageInput
window_title = "ERROR"


class SnaptoCursor(object):
    def __init__(self, ax, x, y, show_cursor):

        self.ax = ax
        self.x = x
        self.y = y
        self.show_cursor = show_cursor

        if show_cursor:
                
            self.vl = self.ax.axvline(x=x[0], color='k', alpha=0.3, label='_nolegend_')  # the vertical line
            self.hl = self.ax.axhline(y=y[0], color='k', alpha=0.3, label='_nolegend_')  # the horizontal line 
            self.marker, = ax.plot(x[0], y[0], markersize=4, marker="s", color=[0,0,0], zorder=3)
            # self.marker.set_label("x: %1.2f // y: %4.2e" % (self.x[0], self.y[0]))
            # plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')

    def mouse_move(self, event):
        if self.show_cursor:   

            if not event.inaxes: return
            x, y = event.xdata, event.ydata
            if x>=np.max(self.x): return

            indx = np.searchsorted(self.x, [x])[0]
            
            x = self.x[indx]
            y = self.y[indx]
            self.vl.set_xdata(x)
            self.hl.set_ydata(y)
            self.marker.set_data([x],[y])
            self.marker.set_label("x: %1.2f // y: %4.2e" % (x, y))
            plt.legend(handles=[self.marker], loc='lower right', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')
    
            self.ax.figure.canvas.draw_idle()

class PerforatedPlateInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/PerforatedPlateInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.userPath = os.path.expanduser('~')
        self.project_folder_path = project.project_folder_path

        self.project = project
        self.preprocessor = project.preprocessor
        self.frequencies = project.frequencies
        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.dict_group_elements = project.preprocessor.group_elements_with_perforated_plate
        self.elements_id = self.opv.getListPickedElements()
        self.type_label = None
        self.dkey = None
        self.elements_info_path = project.file._element_info_path
        self.dict_label = "PERFORATED PLATE || {}"
        self.tol = 1e-6

        
        self.dict_inputs = {}
        self.dict_inputs['dimensionless impedance'] = None

        # Elements selection
        self.currentTab = 0
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')
        self.label_selection = self.findChild(QLabel, 'label_selection')

        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.remove_all_perforated_plate)

        # Tabs
        self.tabWidget_perforated_plate = self.findChild(QTabWidget, 'tabWidget_perforated_plate')
        self.tabWidget_perforated_plate.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_perforated_plate.currentIndex()

        # Setup tab
        self.radioButton_OpenPulse = self.findChild(QRadioButton, 'radioButton_OpenPulse')
        self.radioButton_OpenPulse.toggled.connect(self.radioButtonEvent_setup)
        
        self.radioButton_melling = self.findChild(QRadioButton, 'radioButton_melling')
        self.radioButton_melling.toggled.connect(self.radioButtonEvent_setup)

        self.flag_OpenPulse = self.radioButton_OpenPulse.isChecked()
        self.flag_melling = self.radioButton_melling.isChecked()
        self.dict_inputs['type'] = 0

        self.lineEdit_HoleDiameter = self.findChild(QLineEdit, 'lineEdit_HoleDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_porosity = self.findChild(QLineEdit, 'lineEdit_porosity')
        self.lineEdit_discharge = self.findChild(QLineEdit, 'lineEdit_discharge')

        self.checkBox_nonlinear = self.findChild(QCheckBox, 'checkBox_nonlinear')
        self.checkBox_nonlinear.toggled.connect(self.checkBoxEvent_nonlinear)
        self.flag_nonlinear = self.checkBox_nonlinear.isChecked()
        self.lineEdit_nonlinDischarge = self.findChild(QLineEdit, 'lineEdit_nonlinDischarge')
        self.lineEdit_correction = self.findChild(QLineEdit, 'lineEdit_correction')
        
        self.checkBox_bias = self.findChild(QCheckBox, 'checkBox_bias')
        self.checkBox_bias.toggled.connect(self.checkBoxEvent_bias)
        self.checkBoxEvent_bias()
        self.lineEdit_bias = self.findChild(QLineEdit, 'lineEdit_bias')

        # User defined tab
        self.tabWidget_dimensionless = self.findChild(QTabWidget, "tabWidget_dimensionless")

        self.lineEdit_impedance_real = self.findChild(QLineEdit, 'lineEdit_impedance_real')
        self.lineEdit_impedance_imag = self.findChild(QLineEdit, 'lineEdit_impedance_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')
        self.user_impedance = None
        self.load_path_table = ''

        self.toolButton_load_table = self.findChild(QToolButton, 'toolButton_load_table')
        self.toolButton_load_table.clicked.connect(self.load_table)

        self.lineEdit_skiprows = self.findChild(QSpinBox, 'spinBox')
        
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_perforated_plate_attribution)

        # Preview tab
        self.treeWidget_perforated_plate_plot = self.findChild(QTreeWidget, 'treeWidget_perforated_plate_plot')
        self.treeWidget_perforated_plate_plot.setColumnWidth(0, 80)

        self.pushButton_get_information_plot = self.findChild(QPushButton, 'pushButton_get_information_plot')
        self.pushButton_get_information_plot.clicked.connect(self.get_information_of_group)
        
        self.treeWidget_perforated_plate_plot.itemClicked.connect(self.on_click_item_plot)
        self.treeWidget_perforated_plate_plot.itemDoubleClicked.connect(self.on_doubleclick_item_plot)

        self.label_elementID_plot = self.findChild(QLabel, 'label_elementID_plot')

        self.lineEdit_specify_elementID = self.findChild(QLineEdit, 'lineEdit_specify_elementID')

        self.radioButton_impedance = self.findChild(QRadioButton, 'radioButton_impedance')
        self.radioButton_impedance.toggled.connect(self.radioButtonEvent_preview)

        self.radioButton_absortion = self.findChild(QRadioButton, 'radioButton_absortion')
        self.radioButton_absortion.toggled.connect(self.radioButtonEvent_preview)

        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotReal.toggled.connect(self.radioButtonEvent_preview)

        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        self.radioButton_plotImag.toggled.connect(self.radioButtonEvent_preview)

        self.pushButton_plot_parameter = self.findChild(QPushButton, 'pushButton_plot_parameter')
        self.pushButton_plot_parameter.clicked.connect(self.pushButton_plot)

        self.flag_impedance = self.radioButton_impedance.isChecked()
        self.flag_absortion = self.radioButton_absortion.isChecked()
        self.flag_plotReal = self.radioButton_plotReal.isChecked()
        self.flag_plotImag = self.radioButton_plotImag.isChecked()

        # Remove tab
        self.treeWidget_perforated_plate_remove = self.findChild(QTreeWidget, 'treeWidget_perforated_plate_remove')
        self.treeWidget_perforated_plate_remove.setColumnWidth(0, 80)

        self.pushButton_get_information_remove = self.findChild(QPushButton, 'pushButton_get_information_remove')
        self.pushButton_get_information_remove.clicked.connect(self.get_information_of_group)

        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_remove.clicked.connect(self.remove_perforated_plate_by_group)
        
        self.treeWidget_perforated_plate_remove.itemClicked.connect(self.on_click_item)
        self.treeWidget_perforated_plate_remove.itemDoubleClicked.connect(self.on_doubleclick_item_remove)

        if self.elements_id != []:
            self.write_ids(self.elements_id)

        self.load_elements_info()
        self.exec_()

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_perforated_plate.currentIndex()
        if self.currentTab_ == 0:
            self.write_ids(self.elements_id)
        elif self.currentTab_ in [1,2]: 
            self.lineEdit_elementID.setText("")

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_elementID.setText(text)

    def check_input_elements(self):
        try:
            tokens = self.lineEdit_elementID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.elements_typed = list(map(int, tokens))

            if self.lineEdit_elementID.text()=="":
                title = "ERROR IN ELEMENT ID's"
                message = "Inform a valid Element ID before to confirm the input!"
                self.info_text = [title, message, "ERROR MESSAGE"]
                return True

        except Exception:
            title = "ERROR IN ELEMENT ID's"
            message = "Wrong input for Element ID's!"
            self.info_text = [title, message, "ERROR MESSAGE"]
            return True

        try:
            for element_id in self.elements_typed:
                self.acoustic_elements[element_id]
        except:
            title = "INCORRECT ELEMENT ID INPUT"
            message = " The Element ID input values must be\n greater than 1 and less than {}.".format(len(self.acoustic_elements))
            self.info_text = [title, message, "ERROR MESSAGE"]
            return True
        return False
            
    def checkBoxEvent_nonlinear(self):
        self.flag_nonlinear = self.checkBox_nonlinear.isChecked()
        if self.flag_nonlinear:
            self.lineEdit_nonlinDischarge.setDisabled(False)
            self.lineEdit_correction.setDisabled(False)
        else:
            self.lineEdit_nonlinDischarge.setDisabled(True)
            self.lineEdit_correction.setDisabled(True)

    def checkBoxEvent_bias(self):
        self.flag_bias = self.checkBox_bias.isChecked()
        if self.flag_bias:
            self.lineEdit_bias.setDisabled(False)
        else:
            self.lineEdit_bias.setDisabled(True)
 
    def radioButtonEvent_setup(self):
        self.flag_OpenPulse = self.radioButton_OpenPulse.isChecked()
        self.flag_melling = self.radioButton_melling.isChecked()

        if self.flag_OpenPulse:
            self.checkBox_nonlinear.setDisabled(False)
            self.lineEdit_nonlinDischarge.setDisabled(False)
            self.lineEdit_correction.setDisabled(False)

            self.checkBox_bias.setDisabled(False)
            self.lineEdit_bias.setDisabled(False)
            self.dict_inputs['type'] = 0
        elif self.flag_melling:
            self.checkBox_nonlinear.setDisabled(True)
            self.lineEdit_nonlinDischarge.setDisabled(True)
            self.lineEdit_correction.setDisabled(True)

            self.checkBox_bias.setDisabled(True)
            self.lineEdit_bias.setDisabled(True)
            self.dict_inputs['type'] = 1
        

    def check_input_parameters(self, string, label, not_None = False):
        title = "INPUT ERROR"
        if string != "":
            try:
                value = float(string)
                if value < 0:
                    message = "The {} must be a positive number.".format(label)
                    PrintMessageInput([title, message, "ERROR MESSAGE"])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return True
        elif not_None:
            message = "The {} must be given.".format(label)
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return True
        else:
            self.value = None
        return False

    def check_svalues(self):
        if self.lineEdit_impedance_real.text() != "":
            try:
                z_real = float(self.lineEdit_impedance_real.text())
            except Exception:
                title = "INPUT ERROR"
                message = "Wrong input for real part of dimensionless impedance."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return True
        else:
            z_real = 0

        if self.lineEdit_impedance_imag.text() != "":
            try:
                z_imag = float(self.lineEdit_impedance_imag.text())
            except Exception:
                title = "INPUT ERROR"
                message = "Wrong input for imaginary part of dimensionless impedance."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return True
        else:
            z_imag = 0
        
        if z_real == 0 and z_imag == 0:
            self.dict_inputs['dimensionless impedance'] = None
        else:
            self.dict_inputs['dimensionless impedance'] = z_real + 1j*z_imag

    def load_table(self):
        self.basename = ""
        window_label = 'Choose a table to import the dimensionless impedance'
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.dat; *.csv)')

        if self.path_imported_table == "":
            return

        self.basename = os.path.basename(self.path_imported_table)
        self.lineEdit_load_table_path.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        if "\\" in self.project_folder_path:
            self.load_path_table = "{}\\{}".format(self.project_folder_path, self.basename)
        elif "/" in self.project_folder_path:
            self.load_path_table = "{}/{}".format(self.project_folder_path, self.basename)
        
        try:
            skiprows = int(self.lineEdit_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
        except Exception as e:
            title = "INPUT ERROR"
            message = [str(e) + " It is recommended to skip the header rows."] 
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return
        
        if imported_file.shape[1]<2:
            title = "INPUT ERROR"
            message = "The imported table has insufficient number of columns. The spectrum \ndata must have frequencies, real and imaginary columns."
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return
    
        try:
            self.imported_values = imported_file[:,1] + 1j*imported_file[:,2]
            if imported_file.shape[1]>2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.imported_table = True

                real_values = np.real(self.imported_values)
                imag_values = np.imag(self.imported_values)
                abs_values = np.imag(self.imported_values)
                data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
                header = "dimensionless impedance || Frequency [Hz], real[Pa], imaginary[Pa], absolute[Pa]"
                np.savetxt(self.load_path_table, data, delimiter=",", header=header)

        except Exception as e:
            title = "INPUT ERROR"
            message = str(e)
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return

        self.dict_inputs['dimensionless impedance'] = self.imported_values
        self.basename_specific_impedance = self.basename

    def check_perforated_plate(self):
        self.check_input_elements()

        if self.elements_typed == []:
            return True
        else:
            elements_diameter = []
            elements_lengths = []
            for element_id in self.elements_typed:
                elements_diameter.append(self.acoustic_elements[element_id].cross_section.inner_diameter)
                elements_lengths.append(self.acoustic_elements[element_id].length)

        # Check hole diameter
        if self.check_input_parameters(self.lineEdit_HoleDiameter.text(), 'hole diameter', True):
            return True
        else:
            self.min_diameter = min(elements_diameter)
            if self.value > self.min_diameter:
                title = "Invalid hole diameter value"
                message = "The hole diameter must be less than element inner diameter."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return False
            self.dict_inputs['hole diameter'] = self.value
        
        # Check plate thickness
        if self.check_input_parameters(self.lineEdit_thickness.text(), 'plate thickness', True):
            return True
        else:
            aux = np.append(np.array(elements_lengths) > self.value-self.tol, np.array(elements_lengths) < self.value+self.tol)
            if not all(aux):
                title = "Plate thickness different from element length"
                message = "If possible, use plate thickness equal to the element length for better precision."
                PrintMessageInput([title, message, "WARNING MESSAGE"])
            self.dict_inputs['plate thickness'] = self.value

        # Check area porosity
        if self.check_input_parameters(self.lineEdit_porosity.text(), 'area porosity', True):
            return True
        else:
            if self.value >= 1:
                title = "Invalid area porosity value"
                message = "The area porosity must be less than 1."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return False
            self.dict_inputs['area porosity'] = self.value

        # Check discharge coefficient
        if self.check_input_parameters(self.lineEdit_discharge.text(), 'discharge coefficient'):
            return True
        else:
            if self.value > 1:
                title = "Invalid discharge coefficient value"
                message = "The discharge coefficient must be less than or equal to 1."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return False
            self.dict_inputs['discharge coefficient'] = self.value

        self.dict_inputs['nonlinear effects'] = self.flag_nonlinear

        # Check nonlinear discharge coefficient
        if self.check_input_parameters(self.lineEdit_nonlinDischarge.text(), 'nonlinear discharge coefficient'):
            return True
        else:
            if self.value > 1:
                title = "Invalid nonlinear discharge coefficient value"
                message = "The nonlinear discharge coefficient must be less than or equal to 1."
                PrintMessageInput([title, message, "ERROR MESSAGE"])
                return False
            self.dict_inputs['nonlinear discharge coefficient'] = self.value

        # Check correction factor
        if self.check_input_parameters(self.lineEdit_correction.text(), 'correction factor'):
            return True
        else:
            self.dict_inputs['correction factor'] = self.value

        self.dict_inputs['bias flow effects'] = self.flag_bias

        # Check bias flow
        if self.check_input_parameters(self.lineEdit_bias.text(), 'bias flow coefficient'):
            return True
        else:
            self.dict_inputs['bias flow coefficient'] = self.value

        # Check dimensionless impedance
        if self.tabWidget_dimensionless.currentIndex()==0:
            if self.check_svalues():
                return

        self.perforated_plate = PerforatedPlate(self.dict_inputs['hole diameter'], 
                                                self.dict_inputs['plate thickness'],
                                                self.dict_inputs['area porosity'],
                                                discharge_coefficient = self.dict_inputs['discharge coefficient'],
                                                nonlinear_effect = self.dict_inputs['nonlinear effects'],
                                                nonlinear_discharge_coefficient = self.dict_inputs['nonlinear discharge coefficient'],
                                                correction_factor = self.dict_inputs['correction factor'],
                                                bias_effect = self.dict_inputs['bias flow effects'],
                                                bias_coefficient = self.dict_inputs['bias flow coefficient'],
                                                dimensionless_impedance = self.dict_inputs['dimensionless impedance'],
                                                type = self.dict_inputs['type'])
        if self.load_path_table != '':
            self.perforated_plate.dimensionless_path = self.load_path_table

    def confirm_perforated_plate_attribution(self):
        
        try:
            if self.check_perforated_plate():
                return
            size = len(self.dict_group_elements)
            section = self.dict_label.format("Selection-{}".format(size+1))
            self.replaced = False
            temp_dict = self.dict_group_elements.copy()
            if not temp_dict:
                self.set_perforated_plate_to_elements(section, _print=True)
            else:
                for key, values in temp_dict.items():
                    if list(np.sort(self.elements_typed)) == list(np.sort(values[1])):
                        self.dkey = key
                        self.remove_perforated_plate_by_group()
                        self.set_perforated_plate_to_elements(key)
                    else:
                        count1, count2 = 0, 0
                        for element in self.elements_typed:
                            if element in values[1]:
                                count1 += 1
                        fill_rate1 = count1/len(self.elements_typed)

                        for element in values[1]:
                            if element in self.elements_typed:
                                count2 += 1
                        fill_rate2 = count2/len(values[1])
                        
                        if np.max([fill_rate1, fill_rate2])>0.5 :
                            if not self.replaced:
                                self.set_perforated_plate_to_elements(key)
                                self.replaced = True
                            else:
                                self.dkey = key
                                self.remove_perforated_plate_by_group()
                self.dkey = None  
            self.close()         

        except Exception as err:
            title = "Error with the perforated plate data"
            message = str(err)
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return

    def set_perforated_plate_to_elements(self, section, _print=False): 
        self.project.set_perforated_plate_by_elements(list(np.sort(self.elements_typed)), self.perforated_plate, section)
        if _print:
            if len(self.elements_typed)>20:
                print("[Set Perforated Plate] - defined at {} selected elements".format(len(self.elements_typed)))
            else:
                print("[Set Perforated Plate] - defined at elements {}".format(self.elements_typed))
        self.load_elements_info()

    def remove_function(self, key, reset=False):
        section = key

        if not reset:
            group_label = section.split(" || ")[1]
            message = "The perforated plate attributed to the {} group of elements have been removed.".format(group_label)
        else:
            message = None

        values = self.dict_group_elements[section]
        self.project.preprocessor.set_perforated_plate_by_elements(values[1], None, section, delete_from_dict=True)

        key_strings = ['perforated plate data', 'dimensionless impedance', 'list of elements']
        remove_bc_from_file([section], self.elements_info_path, key_strings, message)
        self.load_elements_info()

    def remove_perforated_plate_by_group(self):
        if self.dkey is None:
            key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in self.lineEdit_elementID.text():
                self.remove_function(key)
            self.lineEdit_elementID.setText("")
        else:
            self.remove_function(self.dkey)
    
    def remove_all_perforated_plate(self):
        temp_dict_groups = self.dict_group_elements.copy()
        keys = temp_dict_groups.keys()
        for key in keys:
            self.remove_function(key, reset=True)
        window_title = "WARNING" 
        title = "INFO MESSAGE"
        message = "The perforated plate has been \nremoved from all elements."
        PrintMessageInput([title, message, window_title])

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item_remove(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        self.remove_perforated_plate_by_group()

    def on_click_item_plot(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        selected_key = self.dict_label.format(self.lineEdit_elementID.text())
        if "Selection-" in selected_key:
            value = self.dict_group_elements[selected_key]
            self.label_elementID_plot.setText(str(value[1]))
            if len(value[1]) == 1:
                self.lineEdit_specify_elementID.setText(str(value[1][0]))
            else:
                self.lineEdit_specify_elementID.setText('')
    
    def on_doubleclick_item_plot(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def radioButtonEvent_preview(self):
        self.flag_impedance = self.radioButton_impedance.isChecked()
        self.flag_absortion = self.radioButton_absortion.isChecked()

        if self.flag_absortion: 
            self.radioButton_plotReal.setDisabled(True)
            self.radioButton_plotImag.setDisabled(True)
        else:
            self.radioButton_plotReal.setDisabled(False)
            self.radioButton_plotImag.setDisabled(False)
            self.flag_plotReal = self.radioButton_plotReal.isChecked()
            self.flag_plotImag = self.radioButton_plotImag.isChecked()        

    def check_select_element(self):        
        selected_key = self.dict_label.format(self.lineEdit_elementID.text())
        if "Selection-" in selected_key:
            value = self.dict_group_elements[selected_key]
            tokens = self.lineEdit_specify_elementID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            specified_element = list(map(int, tokens))
            group_elements = value[1]
            if len(specified_element) > 1:
                title = "ERROR IN ELEMENT SELECTION"
                message = "Please, select only one element in the group to plot the preview."
                self.info_text = [title, message, window_title]
                PrintMessageInput(self.info_text)
                return True
            elif specified_element[0] in group_elements:
                self.plot_select_element = specified_element
                return False
            else:
                title = "ERROR IN ELEMENT SELECTION"
                message = "Please, select an element in the group to plot the preview."
                self.info_text = [title, message, window_title]
                PrintMessageInput(self.info_text)
                return True
        else:
            title = "ERROR IN GROUP SELECTION"
            message = "Please, select a group in the list to plot the preview."
            self.info_text = [title, message, window_title]
            PrintMessageInput(self.info_text)
            return True

    def check_frequencies(self):
        if self.frequencies is None:
            title = "Frequencies definition"
            message = "The frequencies of analysis must be defined to run the preview."
            PrintMessageInput([title, message, "ERROR MESSAGE"])
            return True
        else:
            return False

    def get_response(self):
        self.lineEdit_specify_elementID
        element = self.acoustic_elements[self.plot_select_element[0]]
        if self.flag_absortion: 
            output_data = get_acoustic_absortion(element, self.frequencies)
        elif self.flag_impedance:
            if self.flag_plotReal:
                output_data = get_perforated_plate_impedance(element, self.frequencies, True)
            elif self.flag_plotImag:
                output_data = get_perforated_plate_impedance(element, self.frequencies, False)
        return output_data

    def pushButton_plot(self):
        if self.check_select_element():
            return
        if self.check_frequencies():
            return
        self.plot()

    def plot(self):
        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = self.get_response()

        if self.flag_impedance:
            if self.flag_plotReal:
                ax.set_ylabel(("Normalized Impedance - Real [-]"), fontsize = 14, fontweight = 'bold')
            elif self.flag_plotImag:
                ax.set_ylabel(("Normalized Impedance - Imaginary [-]"), fontsize = 14, fontweight = 'bold')
        elif self.flag_absortion: 
            ax.set_ylabel(("Absortion coefficient [-]"), fontsize = 14, fontweight = 'bold')
            ax.set_ylim(0,1)

        cursor = SnaptoCursor(ax, frequencies, response, True)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Response at element {}".format(self.plot_select_element)
        first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
        _legends = plt.legend(handles=[first_plot], labels=[legend_label], loc='upper right')

        plt.gca().add_artist(_legends)

        ax.set_title(('PERFORATED PLATE'), fontsize = 16, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')

        plt.show()

    def load_elements_info(self):
        self.treeWidget_perforated_plate_plot.clear()
        for section, value in self.dict_group_elements.items():
            text = "d_h: {}m; t_p: {}m; φ: {}".format(value[0].hole_diameter, value[0].thickness, value[0].porosity)
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_perforated_plate_plot.addTopLevelItem(new)  
            
        self.treeWidget_perforated_plate_plot.header().setStyleSheet('font: bold 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_perforated_plate_plot.setStyleSheet('font: bold 16px; font-size: 9pt; font-family: Arial;')

        self.treeWidget_perforated_plate_remove.clear()
        for section, value in self.dict_group_elements.items():
            text = "d_h: {}m; t_p: {}m; φ: {}".format(value[0].hole_diameter, value[0].thickness, value[0].porosity)
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)  
            self.treeWidget_perforated_plate_remove.addTopLevelItem(new)  

        self.treeWidget_perforated_plate_remove.header().setStyleSheet('font: bold 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_perforated_plate_remove.setStyleSheet('font: bold 16px; font-size: 9pt; font-family: Arial;')

    def get_information_of_group(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                value = self.dict_group_elements[selected_key]
                GetInformationOfGroup(value, selected_key)
            else:
                title = "ERROR IN GROUP SELECTION"
                message = "Please, select a group in the list to get the information."
                self.info_text = [title, message, window_title]
                PrintMessageInput(self.info_text)
        except Exception as er:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(er)
            self.info_text = [title, message, window_title]
            PrintMessageInput(self.info_text)

    def update(self):
        self.write_ids(self.opv.getListPickedElements())
        self.elements_id = self.opv.getListPickedElements()

class GetInformationOfGroup(QDialog):
    def __init__(self, value, selected_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Info/getGroupInformationPerforatedPlate.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.perforated_plate = value[0]
        self.elements = value[1]

        self.title_label = self.findChild(QLabel, 'title_label')
        self.title_label.setText("{} information".format(selected_key))

        self.treeWidget_info = self.findChild(QTreeWidget, 'treeWidget_group_info')

        self.Label_dh = self.findChild(QLabel, 'Label_dh')
        self.Label_tp = self.findChild(QLabel, 'Label_tp')
        self.Label_phi = self.findChild(QLabel, 'Label_phi')
        self.Label_sigma = self.findChild(QLabel, 'Label_sigma')
        self.Label_nl_effects = self.findChild(QLabel, 'Label_nl_effects')
        self.Label_nl_sigma = self.findChild(QLabel, 'Label_nl_sigma')
        self.Label_correction = self.findChild(QLabel, 'Label_correction')
        self.Label_bias_effects = self.findChild(QLabel, 'Label_bias_effects')
        self.Label_bias_coefficient = self.findChild(QLabel, 'Label_bias_coefficient')
        self.Label_dimensionless_impedance = self.findChild(QLabel, 'Label_dimensionless_impedance')

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.load_group_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        new = QTreeWidgetItem([str(self.elements)])
        new.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.addTopLevelItem(new)
        
        self.Label_dh.setText(str(self.perforated_plate.hole_diameter))
        self.Label_tp.setText(str(self.perforated_plate.thickness))
        self.Label_phi.setText(str(self.perforated_plate.porosity))
        self.Label_sigma.setText(str(self.perforated_plate.linear_discharge_coefficient))
        if self.perforated_plate.nonlinear_effect:
            self.Label_nl_effects.setText("On")
            self.Label_nl_sigma.setText(str(self.perforated_plate.nonlinear_discharge_coefficient))
            self.Label_correction.setText(str(self.perforated_plate.correction_factor))
        else:
            self.Label_nl_effects.setText("Off")
            self.Label_nl_sigma.setText("___")
            self.Label_correction.setText("___")
            self.Label_nl_sigma.setDisabled(True)
            self.Label_correction.setDisabled(True)
        if self.perforated_plate.bias_effect:
            self.Label_bias_effects.setText("On")
            self.Label_bias_coefficient.setText(str(self.perforated_plate.bias_coefficient))
        else:
            self.Label_bias_effects.setText("Off")
            self.Label_bias_coefficient.setText("___")
            self.Label_bias_coefficient.setDisabled(True)
        if isinstance(self.perforated_plate.dimensionless_impedance, (int, float, complex)):
            self.Label_dimensionless_impedance.setText(str(self.perforated_plate.dimensionless_impedance))
        elif isinstance(self.perforated_plate.dimensionless_impedance, (np.ndarray)):
            self.Label_dimensionless_impedance.setText('Table')
        else:
            self.Label_dimensionless_impedance.setText("___")
            self.Label_dimensionless_impedance.setDisabled(True)
    
    def force_to_close(self):
        self.close()