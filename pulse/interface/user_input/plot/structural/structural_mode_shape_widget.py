from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np
import configparser

from data.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class PlotStructuralModeShapeInput(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = f"{main_window.ui_dir}/plot/results/structural/structural_mode_shape_widget.ui"
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)

        self.project = main_window.getProject()
        

        self.reset()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        # self.load_natural_frequencies()

    def reset(self):
        self.mode_index = None
        
        self.scaling_key = {0 : "absolute",
                            1 : "real_ux",
                            2 : "real_uy",
                            3 : "real_uz"}

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_color_scaling = self.findChild(QComboBox, 'comboBox_color_scaling')
        # QFrame
        self.frame_plot_button = self.findChild(QFrame, 'frame_plot_button')
        self.frame_plot_button.setVisible(False)
        # QLineEdit
        self.lineEdit_natural_frequency = self.findChild(QLineEdit, 'lineEdit_natural_frequency')
        self.lineEdit_natural_frequency.setDisabled(True)
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        #
        widths = [60, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        self.comboBox_color_scaling.currentIndexChanged.connect(self.plot_update)
        self.pushButton_plot.clicked.connect(self.plot_update)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def plot_update(self):
        self.complete = False
        if self.lineEdit_natural_frequency.text() != "":
            if self.check_selected_frequency():
                self.complete = True

    def get_dict_modes_frequencies(self):
        self.natural_frequencies = self.project.natural_frequencies_structural
        modes = np.arange(1, len(self.natural_frequencies)+1, 1)
        self.dict_modes_frequencies = dict(zip(modes, self.natural_frequencies))

    def check_selected_frequency(self):
        message = ""
        if self.lineEdit_natural_frequency.text() == "":
            title = "Additional action required to plot the results"
            message = "You should select a natural frequency from the available\n\n"
            message += "list before trying to plot the structural mode shape."
            self.text_data = [title, message, window_title_2]
        else:
            self.project.analysis_type_label = "Structural Modal Analysis"
            frequency = self.selected_natural_frequency
            self.mode_index = self.natural_frequencies.index(frequency)
            current_scaling = self.scaling_key[self.comboBox_color_scaling.currentIndex()]
            self.opv.plot_displacement_field(self.mode_index, current_scaling)

        if message != "":
            PrintMessageInput(self.text_data)
            return True
        else:
            return False

    def load_natural_frequencies(self):
        self.get_dict_modes_frequencies()

        self.treeWidget_frequencies.clear()
        for mode, natural_frequency in self.dict_modes_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)
        
        # data = np.zeros((len(self.dict_modes_frequencies),2))
        # data[:,0] = np.array(list(self.dict_modes_frequencies.keys()))
        # data[:,1] = np.array(list(self.dict_modes_frequencies.values()))
        # header = "Mode || Natural frequency [Hz]"
        # np.savetxt("natural_frequencies_reference.dat", data, delimiter=";", header=header)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.plot_update()

    def on_doubleclick_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.plot_update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_update()
        elif event.key() == Qt.Key_Escape:
            self.close()