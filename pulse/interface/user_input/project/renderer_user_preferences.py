from PySide6.QtWidgets import QDialog, QCheckBox, QFrame, QLineEdit, QPushButton, QSlider, QSpinBox
from PySide6.QtCore import Qt

from pulse import app, UI_DIR

from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput

from molde import load_ui
from molde.colors import Color

from copy import deepcopy


class RendererUserPreferencesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/render/renderer_user_preferences.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window
        self.config = app().config
        self.user_preferences = app().config.user_preferences
        self.tmp_user_preferences = deepcopy(self.user_preferences)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_user_preferences()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_OpenPulse_logo : QCheckBox
        self.checkBox_reference_scale : QCheckBox
        self.checkBox_compatibility_mode : QCheckBox

        # QFrame
        self.frame_background_color : QFrame

        # QSlider
        self.slider_transparency : QSlider

        # QLineEdit
        self.lineEdit_renderer_background_color_1 : QLineEdit
        self.lineEdit_renderer_background_color_2 : QLineEdit
        self.lineEdit_renderer_font_color : QLineEdit
        self.lineEdit_nodes_points_color : QLineEdit
        self.lineEdit_lines_color : QLineEdit
        self.lineEdit_tubes_color : QLineEdit

        # QSpinBox
        self.spinBox_renderer_font_size: QSpinBox
        self.spinBox_nodes_size: QSpinBox
        self.spinBox_points_size: QSpinBox
        self.spinBox_lines_thickness: QSpinBox

        # QPushButton
        self.pushButton_renderer_background_color_1 : QPushButton
        self.pushButton_renderer_background_color_2 : QPushButton
        self.pushButton_renderer_font_color : QPushButton
        self.pushButton_nodes_points_color : QPushButton
        self.pushButton_lines_color : QPushButton
        self.pushButton_tubes_color : QPushButton
        self.pushButton_reset_to_default : QPushButton
        self.pushButton_update_settings : QPushButton
        self.pushButton_apply_settings: QPushButton

    def _create_connections(self):
        self.pushButton_renderer_background_color_1.clicked.connect(self.update_renderer_background_color_1)
        self.pushButton_renderer_background_color_2.clicked.connect(self.update_renderer_background_color_2)
        self.pushButton_renderer_font_color.clicked.connect(self.update_renderer_font_color)
        self.pushButton_nodes_points_color.clicked.connect(self.update_nodes_points_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_tubes_color.clicked.connect(self.update_tubes_color)
        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.pushButton_apply_settings.clicked.connect(self.apply_user_preferences)
        self.spinBox_renderer_font_size.valueChanged.connect(self.update_renderer_font_size)
        self.spinBox_nodes_size.valueChanged.connect(self.update_nodes_size)
        self.spinBox_points_size.valueChanged.connect(self.update_points_size)
        self.spinBox_lines_thickness.valueChanged.connect(self.update_lines_thickness)
        
    def update_renderer_background_color_1(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_1 = tuple(read.color)
            str_color = str(renderer_background_color_1)[1:-1]
            self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.tmp_user_preferences.renderer_background_color_1 = Color(*renderer_background_color_1)

    def update_line_edit_renderer_background_color_1(self):
        str_color = str(self.tmp_user_preferences.renderer_background_color_1.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_renderer_background_color_2(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_2 = tuple(read.color)
            str_color = str(renderer_background_color_2)[1:-1]
            self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.tmp_user_preferences.renderer_background_color_2 = Color(*renderer_background_color_2)

    def update_line_edit_renderer_background_color_2(self):
        str_color = str(self.tmp_user_preferences.renderer_background_color_2.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            renderer_font_color = tuple(read.color)
            str_color = str(renderer_font_color)[1:-1]
            self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.tmp_user_preferences.renderer_font_color = Color(*renderer_font_color)

    def update_line_edit_renderer_font_color(self):
        str_color = str(self.tmp_user_preferences.renderer_font_color.to_rgb())[1:-1]
        self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_nodes_points_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            nodes_points_color = tuple(read.color)
            str_color = str(nodes_points_color)[1:-1]
            self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.tmp_user_preferences.nodes_points_color = Color(*nodes_points_color)
        
    def update_line_edit_nodes_points_color(self):
        str_color = str(self.tmp_user_preferences.nodes_points_color.to_rgb())[1:-1]
        self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            lines_color = tuple(read.color)
            str_color = str(lines_color)[1:-1]
            self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.tmp_user_preferences.lines_color = Color(*lines_color)
    
    def update_line_edit_lines_color(self):
        str_color = str(self.tmp_user_preferences.lines_color.to_rgb())[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_tubes_color(self):
        read = PickColorInput(title="Pick the surfaces color")
        if read.complete:
            tubes_color = tuple(read.color)
            str_color = str(tubes_color)[1:-1]
            self.lineEdit_tubes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
           
            self.tmp_user_preferences.tubes_color = Color(*tubes_color)

    def update_line_edit_tubes_color(self):
        str_color = str(self.tmp_user_preferences.tubes_color.to_rgb())[1:-1]
        self.lineEdit_tubes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_size(self):
        renderer_font_size = self.spinBox_renderer_font_size.value()
        self.tmp_user_preferences.renderer_font_size = renderer_font_size
    
    def update_spin_box_renderer_font_size(self):
        renderer_font_size = self.tmp_user_preferences.renderer_font_size
        self.spinBox_renderer_font_size.setValue(renderer_font_size)

    def update_nodes_size(self):
        nodes_size = self.spinBox_nodes_size.value()
        self.tmp_user_preferences.nodes_size = nodes_size
    
    def update_spin_box_nodes_size(self):
        nodes_size = self.tmp_user_preferences.nodes_size
        self.spinBox_nodes_size.setValue(nodes_size)

    def update_points_size(self):
        points_size = self.spinBox_points_size.value()
        self.tmp_user_preferences.points_size = points_size
    
    def update_spin_box_points_size(self):
        points_size = self.tmp_user_preferences.points_size
        self.spinBox_points_size.setValue(points_size)
    
    def update_lines_thickness(self):
        lines_thickness = self.spinBox_lines_thickness.value()
        self.tmp_user_preferences.lines_thickness = lines_thickness
    
    def update_spin_box_lines_thickness(self):
        lines_thickness = self.tmp_user_preferences.lines_thickness
        self.spinBox_lines_thickness.setValue(lines_thickness)

    def apply_user_preferences(self):
        app().config.user_preferences = self.tmp_user_preferences
        self.update_settings()

        app().config.update_config_file()

    def confirm_and_update_user_preferences(self):
        self.apply_user_preferences()
        self.accept()
    
    def update_settings(self):
        self.update_open_pulse_logo_state()
        self.update_reference_scale_state()
        self.update_renderers_font_size()
        self.update_compatibility_mode_state()
        self.main_window.update_plots(reset_camera=False)

    def reset_to_default(self):
        if self.tmp_user_preferences.interface_theme == "dark":
            self.tmp_user_preferences.set_dark_theme()
        else:
            self.tmp_user_preferences.set_light_theme()
        
        self.tmp_user_preferences.reset_attributes()
        self.reset_logo_state()
        self.reset_reference_scale_state()
        self.reset_compatibility_mode_state()

        self.apply_user_preferences()
        self.load_user_preferences()

    def reset_logo_state(self):
        self.checkBox_OpenPulse_logo.setChecked(True)

    def reset_reference_scale_state(self):
        self.checkBox_reference_scale.setChecked(True)
    
    def reset_compatibility_mode_state(self):
        self.checkBox_compatibility_mode.setChecked(False)
    
    def update_open_pulse_logo_state(self):
        if self.checkBox_OpenPulse_logo.isChecked():
            self.tmp_user_preferences.show_open_pulse_logo = True
            self.main_window.results_widget.enable_open_pulse_logo()
            self.main_window.geometry_widget.enable_open_pulse_logo()
            self.main_window.mesh_widget.enable_open_pulse_logo()
        else:
            self.tmp_user_preferences.show_open_pulse_logo = False
            self.main_window.results_widget.disable_open_pulse_logo()
            self.main_window.geometry_widget.disable_open_pulse_logo()
            self.main_window.mesh_widget.disable_open_pulse_logo()

    def update_show_open_pulse_logo_checkbox(self):
        self.checkBox_OpenPulse_logo.setChecked(self.tmp_user_preferences.show_open_pulse_logo)

    def update_reference_scale_state(self):
        if self.checkBox_reference_scale.isChecked():
            self.tmp_user_preferences.show_reference_scale_bar = True
            self.main_window.results_widget.enable_scale_bar()
            self.main_window.mesh_widget.enable_scale_bar()
        else:
            self.tmp_user_preferences.show_reference_scale_bar = False
            self.main_window.results_widget.disable_scale_bar()
            self.main_window.mesh_widget.disable_scale_bar()

    def update_show_reference_scalebar_checkbox(self):
        self.checkBox_reference_scale.setChecked(self.tmp_user_preferences.show_reference_scale_bar)
        
    def update_compatibility_mode_state(self):
        self.tmp_user_preferences.compatibility_mode = self.checkBox_compatibility_mode.isChecked()

    def update_compatibility_mode_checkbox(self):
        self.checkBox_compatibility_mode.setChecked(self.tmp_user_preferences.compatibility_mode)

    def update_renderers_font_size(self):
        self.main_window.geometry_widget.update_renderer_font_size()
        self.main_window.results_widget.update_renderer_font_size()
        self.main_window.mesh_widget.update_renderer_font_size()

    def load_user_preferences(self):
        self.update_line_edit_renderer_background_color_1()
        self.update_line_edit_renderer_background_color_2()
        self.update_line_edit_renderer_font_color()
        self.update_line_edit_nodes_points_color()
        self.update_line_edit_lines_color()
        self.update_line_edit_tubes_color()
        self.update_spin_box_renderer_font_size()
        self.update_spin_box_nodes_size()
        self.update_spin_box_points_size()
        self.update_spin_box_lines_thickness()
        self.update_show_open_pulse_logo_checkbox()
        self.update_show_reference_scalebar_checkbox()
        self.update_compatibility_mode_checkbox()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()