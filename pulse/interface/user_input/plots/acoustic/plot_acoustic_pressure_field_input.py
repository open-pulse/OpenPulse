from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from pulse.interface.user_input.project.print_message import PrintMessageInput

class PlotAcousticPressureFieldInput(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = f"{main_window.ui_dir}/plot/results/acoustic/plot_acoustic_pressure_field_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies_vector()

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _reset_variables(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None
        self.scaling_key = {0 : "absolute",
                            1 : "real_part"}

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_color_scaling = self.findChild(QComboBox, 'comboBox_color_scaling')
        # QFrame
        self.frame_plot_button = self.findChild(QFrame, 'frame_plot_button')
        self.frame_plot_button.setVisible(False)
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

    def update_plot(self):
        self.complete = False
        if self.lineEdit_selected_frequency.text() != "":
            if self.check_selected_frequency():
                self.complete = True

    def check_selected_frequency(self):
        if self.lineEdit_selected_frequency.text() == "":
            window_title = "Warning"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list "
            message += "before trying to plot the acoustic pressure field."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            self.frequency = self.frequency_to_index[frequency_selected]
            if self.comboBox_color_scaling.currentIndex() == 0:
                absolute = True
            else:
                absolute = False
            self.opv.plot_pressure_field(self.frequency, absolute=absolute)

    def load_frequencies_vector(self):
        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()