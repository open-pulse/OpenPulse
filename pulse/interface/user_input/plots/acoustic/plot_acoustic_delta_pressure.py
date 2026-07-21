from enum import IntEnum

import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal

from pulse import app
from pulse.interface.ui_generated.plots.results.acoustic.get_acoustic_delta_pressures_ui import GetAcousticDeltaPressures_UI
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.model.properties.fluid import Fluid


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class PlotAcousticDeltaPressure(GetAcousticDeltaPressures_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._configure_validator()
        self._create_connections()

        app().main_window.set_selection()
        self.selection_callback()

    def _initialize(self):
        self.unit_label = "Pa"
        self.current_line_edit = None
        self.before_run = self.project.get_pre_solution_model_checks()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _configure_validator(self):
        self.lineEdit_cutoff_frequency.setValidator(StrictDoubleValidator(0, 1e8, 6))

    def _create_connections(self):
        #
        self.comboBox_cutoff_frequency_options.currentIndexChanged.connect(self.cutoff_frequency_options_callback)
        #
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        self.pushButton_flip_nodes.clicked.connect(self.flip_nodes)
        #
        self.clickable(self.lineEdit_input_node_id).connect(self.input_line_edit_clicked)
        self.clickable(self.lineEdit_output_node_id).connect(self.output_line_edit_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.output_line_edit_clicked()

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            node_id = selected_nodes[0]
            self.current_line_edit.setText(str(node_id))

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def input_line_edit_clicked(self):
        self.current_line_edit = self.lineEdit_input_node_id
        self.highlight_line_edit()      

    def output_line_edit_clicked(self):
        self.current_line_edit = self.lineEdit_output_node_id
        self.highlight_line_edit()

    def highlight_line_edit(self):
        self.current_line_edit.setStyleSheet("""border-color: rgb(32, 207, 255); border-width: 2px;""")
        if self.current_line_edit == self.lineEdit_input_node_id:
            self.lineEdit_output_node_id.setStyleSheet("")
        elif self.current_line_edit == self.lineEdit_output_node_id:
            self.lineEdit_input_node_id.setStyleSheet("")

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input)

    def call_plotter(self):
        if self.check_inputs():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()

        f_cut = None
        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            f_cut = float(self.lineEdit_cutoff_frequency.text()) 

        self.plotter.set_cutoff_frequency(f_cut)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        input_node_id = self.lineEdit_input_node_id.text()
        stop, self.input_node_id = self.before_run.check_selected_ids(input_node_id, "nodes", single_id=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True

        output_node_id = self.lineEdit_output_node_id.text()
        stop, self.output_node_id = self.before_run.check_selected_ids(output_node_id, "nodes", single_id=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True
        
        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            line_edit = self.lineEdit_cutoff_frequency
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

    def get_response(self):

        P_input = self.project.acoustic_postprocessing.get_acoustic_response_spectrum(self.input_node_id)
        P_output = self.project.acoustic_postprocessing.get_acoustic_response_spectrum(self.output_node_id)

        delta_pressure = P_input - P_output

        if complex(0) in delta_pressure:
            # add a zero shift constant into the delta pressures to avoid zero values in log type plots
            delta_pressure += 1e-12

        return delta_pressure

    def cutoff_frequency_options_callback(self):
        index = self.comboBox_cutoff_frequency_options.currentIndex()
        user_defined = index == CutoffFrequency.USER_DEFINED
        self.lineEdit_cutoff_frequency.setEnabled(user_defined)

        if index == CutoffFrequency.DISABLED:
            self.lineEdit_cutoff_frequency.clear()

        elif index == CutoffFrequency.AUTOMATIC:
            f_cut = self.compute_pipe_cutoff_frequency()
            if isinstance(f_cut, float):
                value = f"{f_cut : .4f}".strip()
                self.lineEdit_cutoff_frequency.setText(value)

    def compute_pipe_cutoff_frequency(self):

        d_in = 0.
        for line_id, data in app().project.model.properties.line_properties.items():
            if not isinstance(data, dict):
                continue

            section_type_label = data.get("section_type_label")
            if section_type_label != "pipe":
                continue

            d_out, t, *_ = data.get("section_parameters")
            if d_out - 2 * t > d_in:
                d_in = d_out - 2 * t

                fluid = data.get("fluid")

        if not isinstance(fluid, Fluid):
            return None
   
        Co = fluid.speed_of_sound

        if d_in == 0:
            return None

        # cut-off frequency of a circular pipe
        f_cut = 1.8412 * Co / (np.pi * d_in)

        return f_cut

    def join_model_data(self):

        self.title = f"Acoustic frequency response - {self.project.analysis_method} method"
        legend_label = f"Delta pressure between nodes {self.input_node_id} and {self.output_node_id}"
        unit_label = "--"
        y_label = "Acoustic pressure ratio"

        self.model_results = dict()

        key = ("nodes", (self.input_node_id, self.output_node_id))

        self.model_results[key] = {
            "x_data": self.model.frequencies,
            "y_data": self.get_response(),
            "x_label": "Frequency [Hz]",
            "y_label": y_label,
            "title": self.title,
            "data_information": legend_label,
            "legend": legend_label,
            "unit": unit_label,
            "color": [0, 0, 1],
            "linestyle": "-",
        }

    def alternate_node_id_input_fields(self):

        if self.current_line_edit == self.lineEdit_input_node_id:
            self.current_line_edit = self.lineEdit_output_node_id
        else:
            self.current_line_edit = self.lineEdit_input_node_id

        self.current_line_edit.setFocus()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()

        elif event.key() in [Qt.Key_Up, Qt.Key_Down]:
            self.alternate_node_id_input_fields()