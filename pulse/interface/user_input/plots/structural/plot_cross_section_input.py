from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import app
from pulse.interface import error_title, warning_title
from pulse.interface.ui_generated.plots.model.plot_section_ui import PlotSection_UI
from pulse.interface.user_input.model.setup.cross_section.cross_section_plotter import (
    CrossSectionPlotter,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_section import CrossSection


class SelectionType(IntEnum):
    LINES = 0
    ELEMENTS = 1


class PlotCrossSectionInput(PlotSection_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._create_connections()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.section_info = None
        self.keep_window_open = True
        self.before_run = app().project.get_pre_solution_model_checks()

    def _create_connections(self):
        #
        self.comboBox_selection.currentIndexChanged.connect(self.selection_type_update)
        #
        self.pushButton_plot_section.clicked.connect(self.plot_section)
        self.pushButton_exit.clicked.connect(self.close)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_lines = app().main_window.list_selected_lines()
        selected_elments = app().main_window.list_selected_elements()
        self.comboBox_selection.blockSignals(True)

        if selected_lines:
            selected_id = selected_lines
            self.comboBox_selection.setCurrentIndex(SelectionType.LINES)
        
        elif selected_elments:
            selected_id = selected_elments
            self.comboBox_selection.setCurrentIndex(SelectionType.ELEMENTS)

        else:
            self.comboBox_selection.blockSignals(False)
            return

        if len(selected_id) != 1:
            self.comboBox_selection.blockSignals(False)
            return

        text = ", ".join([str(i) for i in selected_id])
        self.lineEdit_selected_id.setText(text)
        self.comboBox_selection.blockSignals(False)

    def selection_type_update(self):
        
        if self.comboBox_selection.currentIndex() == SelectionType.LINES:
            app().main_window.plot_lines_with_cross_sections()
        else:
            app().main_window.plot_mesh()

        self.selection_callback()

    def preprocess_selection(self):

        model = app().project.model

        if self.comboBox_selection.currentIndex() == SelectionType.LINES:
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_id = self.before_run.check_selected_ids(lineEdit, "lines", single_id=True)
            if stop:
                return True

            section_type_label = model.properties._get_property("section_type_label", line_id=line_id)
            if self.check_invalid_cross_section_plots(section_type_label):
                return True

            cross_section = model.properties._get_property("cross_section", line_id=line_id)
            if cross_section is None:
                self.hide()
                title = "Undefined cross-section"
                message = "You should define a cross-section to the selected line before trying to plot it."
                PrintMessageInput([error_title, title, message])
                return True

        else:
            lineEdit = self.lineEdit_selected_id.text()
            stop, element_id = self.before_run.check_selected_ids(lineEdit, "elements", single_id=True)
            if stop:
                return True

            element = model.preprocessor.structural_elements[element_id]
            cross_section = element.cross_section

            section_type_label = cross_section.section_type_label
            if self.check_invalid_cross_section_plots(section_type_label):
                return True

            if not isinstance(cross_section, CrossSection):
                self.hide()
                title = "Undefined cross-section"
                message = "You should define a cross-section to the selected element before trying to plot it."
                PrintMessageInput([error_title, title, message])
                return True

        self.section_info = cross_section.section_info

        return False
       
    def check_invalid_cross_section_plots(self, section_type_label: str):
        message = ""
        title = "Non-plottable cross-section"

        if section_type_label == "expansion_joint":
            message = "The expansion joint cross-section cannot be plotted."

        elif section_type_label == "valve":
            message = "The valve cross-section cannot be plotted."

        elif section_type_label == "reducer":
            message = "The reducer cross-section cannot be plotted."

        if message != "":
            self.hide()
            PrintMessageInput([warning_title, title, message])
            return True

    def plot_section(self):

        if self.preprocess_selection():
            return

        self.hide()
        plotter = CrossSectionPlotter()

        points = self.section_info.section_points_to_draw

        plotter.plot_cross_section(points, self.section_info.section_type_label)
        plotter.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_section()

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)