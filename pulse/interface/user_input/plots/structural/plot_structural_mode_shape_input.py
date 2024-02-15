from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np
import configparser

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotStructuralModeShapeInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/plots/results/structural/plot_structural_mode_shape.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.natural_frequencies = self.project.natural_frequencies_structural
        self.mode_index = None

        self._define_qt_variables()
        self._create_connections()
        self.load_natural_frequencies()
        self.exec()

    def _define_qt_variables(self):
        self.lineEdit_natural_frequency = self.findChild(QLineEdit, 'lineEdit_natural_frequency')
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        self.radioButton_absolute = self.findChild(QRadioButton, 'radioButton_absolute')
        self.radioButton_real_part_ux = self.findChild(QRadioButton, 'radioButton_real_part_ux')
        self.radioButton_real_part_uy = self.findChild(QRadioButton, 'radioButton_real_part_uy')
        self.radioButton_real_part_uz = self.findChild(QRadioButton, 'radioButton_real_part_uz')
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        #
        self.lineEdit_natural_frequency.setDisabled(True)
        #
        widths = [120, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.confirm_selection)
        self.radioButton_absolute.clicked.connect(self.radioButton_event)
        self.radioButton_real_part_ux.clicked.connect(self.radioButton_event)
        self.radioButton_real_part_uy.clicked.connect(self.radioButton_event)
        self.radioButton_real_part_uz.clicked.connect(self.radioButton_event)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def radioButton_event(self):
        if self.lineEdit_natural_frequency.text() != "":
            self.check_selected_frequency()

    def get_dict_modes_frequencies(self):
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
            scaling_setup = {   "absolute" : self.radioButton_absolute.isChecked(),
                                "real_ux" : self.radioButton_real_part_ux.isChecked(),
                                "real_uy" : self.radioButton_real_part_uy.isChecked(),
                                "real_uz" : self.radioButton_real_part_uz.isChecked()   }
            self.opv.plot_displacement_field(self.mode_index, scaling_setup)

        if message != "":
            PrintMessageInput(self.text_data)
            return True
        else:
            return False

    def confirm_selection(self):
        if self.check_selected_frequency():
            return
        self.complete = True
        # self.close()

    def load_natural_frequencies(self):
        self.get_dict_modes_frequencies()

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

    def on_doubleclick_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.confirm_selection()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()