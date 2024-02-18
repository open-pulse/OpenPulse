from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotAcousticModeShape(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = f"{main_window.ui_dir}/plots/results/acoustic/acoustic_mode_shape.ui"
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_natural_frequencies()
       
    def _initialize(self):
        self.mode_index = None

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
        # QLineEdit
        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        self._config_treeWidget()

    def _create_connections(self):
        self.comboBox_color_scaling.currentIndexChanged.connect(self.update_plot)
        self.pushButton_plot.clicked.connect(self.update_plot)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.update_plot)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def update_plot(self):
        self.complete = False
        if self.lineEdit_natural_frequency.text() != "":
            if self.check_selected_frequency():
                self.complete = True

    def get_dict_modes_frequencies(self):
        self.natural_frequencies = self.project.natural_frequencies_acoustic
        modes = np.arange(1,len(self.natural_frequencies)+1,1)
        self.dict_modes_frequencies = dict(zip(modes, self.natural_frequencies))

    def check_selected_frequency(self):
        message = ""
        if self.lineEdit_natural_frequency.text() == "":
            window_title = "Warning"
            title = "Additional action required to plot the results"
            message = "You should select a natural frequency from the available "
            message += "list before trying to plot the acoustic mode shape."
            PrintMessageInput([window_title, title, message], auto_close=True)
        else:
            self.project.analysis_type_label = "Acoustic Modal Analysis"
            frequency = self.selected_natural_frequency
            self.mode_index = self.natural_frequencies.index(frequency)
            if self.comboBox_color_scaling.currentIndex() == 0:
                absolute = True
            else:
                absolute = False
            self.opv.plot_pressure_field(self.mode_index, absolute=absolute)

    def load_natural_frequencies(self):
        self.get_dict_modes_frequencies()

        self.treeWidget_frequencies.clear()
        for mode, natural_frequency in self.dict_modes_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.update_plot()

    def on_doubleclick_item(self, item):
        natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(natural_frequency))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()