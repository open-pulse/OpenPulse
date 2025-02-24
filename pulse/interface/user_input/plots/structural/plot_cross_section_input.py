from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.model.cross_section import get_points_to_plot_section
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotCrossSectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/model/plot_section.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.project = self.project
        self.preprocessor = self.project.model.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        
        self.structural_elements = self.project.model.preprocessor.structural_elements

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection : QComboBox

        # QLabel
        self.label_selected_id : QLabel

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit

        # QPushButton
        self.pushButton_plot_cross_section : QPushButton 

    def _create_connections(self):
        #
        self.comboBox_selection.currentIndexChanged.connect(self.selection_type_update)
        #
        self.pushButton_plot_cross_section.clicked.connect(self.plot_section)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_id = list()
        selected_lines = app().main_window.list_selected_lines()
        selected_elments = app().main_window.list_selected_elements()

        self.comboBox_selection.blockSignals(True)

        if selected_lines:
            self.label_selected_id.setText("Line ID:")
            selected_id = selected_lines
            self.comboBox_selection.setCurrentIndex(0)
        
        elif selected_elments:
            self.label_selected_id.setText("Element ID:")
            selected_id = selected_elments
            self.comboBox_selection.setCurrentIndex(1)

        if len(selected_id) == 1:
            text = ", ".join([str(i) for i in selected_id])
            self.lineEdit_selected_id.setText(text)

        else:
            self.lineEdit_selected_id.setText("")
            self.comboBox_selection.setCurrentIndex(0)

        self.comboBox_selection.blockSignals(False)

    def selection_type_update(self):
        
        index = self.comboBox_selection.currentIndex()

        if index == 0:
            self.label_selected_id.setText("Line ID:")
            app().main_window.plot_lines_with_cross_sections()

        elif index == 1:
            self.label_selected_id.setText("Element ID:")
            app().main_window.plot_mesh()

        self.selection_callback()

    # def _get_dict_key_section(self):
    #     self.labels = [ "Pipe", 
    #                     "Rectangular section", 
    #                     "Circular section", 
    #                     "C-section", 
    #                     "I-section", 
    #                     "T-section", 
    #                     "Generic section"   ]

    def preprocess_selection(self):

        self.message = ""
        index = self.comboBox_selection.currentIndex()

        if index == 0:

            lineEdit = self.lineEdit_selected_id.text()
            stop, self.line_typed = self.before_run.check_selected_ids(lineEdit, "lines", single_id=True)
            if stop:
                return True

            cross_section = self.model.properties._get_property("cross_section", line_id=self.line_typed)
            expansion_joint_data = self.model.properties._get_property("expansion_joint_data", ine_id=self.line_typed)

            if cross_section is None and expansion_joint_data is None:
                self.message = "Please, define a cross-section to the \nselected line before trying to plot the section."
                self.title = "Error: undefined line cross-section"
                self.window_title = window_title_1
                return True

        elif index == 1:

            lineEdit = self.lineEdit_selected_id.text()
            stop, self.element_typed = self.before_run.check_selected_ids(lineEdit, "elements", single_id=True)
            if stop:
                return True

            element = self.structural_elements[self.element_typed]
            if element.cross_section is None:
                self.message = "Please, define a cross-section to the selected \nelement before trying to plot the section."
                self.title = "Error: undefined element cross-section"
                self.window_title = window_title_1          
                return True

            cross_section = element.cross_section

        self.section_type_label = cross_section.section_type_label

        if self.section_type_label != 'Expansion joint':
            self.section_parameters = cross_section.section_parameters
            # if self.section_type_label != "Pipe":
            #     self.section_properties = cross_section.section_properties    
        else:
            self.window_title = window_title_2
            self.title = "Unable to plot cross-section"
            self.message = "The cross-section plot has been deactivated to \n\n"
            self.message += "the 'expansion joint' element type."
            return True
            
        return False

       
    def plot_section(self):
        import matplotlib.pyplot as plt    

        plt.ion()
        plt.close()

        if self.preprocess_selection():
            if self.message != "":
                PrintMessageInput([self.window_title, self.title, self.message])
            return
        
        if self.section_type_label == "Pipe":
            Yp, Zp, Yp_ins, Zp_ins, Yc, Zc = get_points_to_plot_section(self.section_type_label, self.section_parameters)
        else:
            Yp, Zp, Yc, Zc = get_points_to_plot_section(self.section_type_label, self.section_parameters)

        if self.stop:
            self.stop = False
            return

        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(Yc, Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)
        third_plot = plt.scatter(0, 0, marker="+", linewidth=1.5, zorder=4, color=[0,0,1], s=120)

        if self.section_type_label == "Pipe" and Yp_ins is not None:
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
        if self.section_type_label == 'C-section':
            plt.xlim(-(1/2)*_max, (3/2)*_max)
        else:
            plt.xlim(-_max*f, _max*f)

        plt.ylim(-_max*f, _max*f)
        plt.grid()
        plt.show()

    def keyPressEvent(self, event):
        import matplotlib.pyplot as plt    

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_section()
        if event.key() == Qt.Key_Escape:
            plt.close()
            self.close()