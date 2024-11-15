from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QFrame, QLineEdit, QPushButton, QRadioButton, QSlider, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from molde.colors import Color

from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput


# TODO - update this class for new renders

class RendererUserPreferencesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/render/renderer_user_preferences.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window
        self.config = app().config
        self.project = app().project
        self.user_preferences = app().config.user_preferences

        self.renderer_background_color_1 = None
        self.renderer_background_color_2 = None
        self.renderer_font_color = None
        self.nodes_points_color = None
        self.lines_color = None
        self.tubes_color = None
        self.renderer_font_size = None
        self.interface_font_size = None

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
        self.lineEdit_renderer_font_size: QLineEdit
        self.lineEdit_interface_font_size: QLineEdit

        # QPushButton
        self.pushButton_renderer_background_color_1 : QPushButton
        self.pushButton_renderer_background_color_2 : QPushButton
        self.pushButton_renderer_font_color : QPushButton
        self.pushButton_nodes_points_color : QPushButton
        self.pushButton_lines_color : QPushButton
        self.pushButton_tubes_color : QPushButton
        self.pushButton_reset_to_default : QPushButton
        self.pushButton_update_settings : QPushButton

    def _create_connections(self):
        self.pushButton_renderer_background_color_1.clicked.connect(self.update_renderer_background_color_1)
        self.pushButton_renderer_background_color_2.clicked.connect(self.update_renderer_background_color_2)
        self.pushButton_renderer_font_color.clicked.connect(self.update_renderer_font_color)
        self.pushButton_nodes_points_color.clicked.connect(self.update_nodes_points_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_tubes_color.clicked.connect(self.update_tubes_color)
        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.lineEdit_renderer_font_size.textChanged.connect(self.update_renderer_font_size)
        self.lineEdit_interface_font_size.textChanged.connect(self.update_interface_font_size)

    def update_renderer_background_color_1(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_1 = tuple(read.color)
            str_color = str(renderer_background_color_1)[1:-1]
            self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_background_color_1 = Color(*renderer_background_color_1)

    def update_line_edit_renderer_background_color_1(self):
        str_color = str(self.user_preferences.renderer_background_color_1.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_renderer_background_color_2(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_2 = tuple(read.color)
            str_color = str(renderer_background_color_2)[1:-1]
            self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_background_color_2 = Color(*renderer_background_color_2)

    def update_line_edit_renderer_background_color_2(self):
        str_color = str(self.user_preferences.renderer_background_color_2.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            renderer_font_color = tuple(read.color)
            str_color = str(renderer_font_color)[1:-1]
            self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_font_color = Color(*renderer_font_color)

    def update_line_edit_renderer_font_color(self):
        str_color = str(self.user_preferences.renderer_font_color.to_rgb())[1:-1]
        self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_nodes_points_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            nodes_points_color = tuple(read.color)
            str_color = str(nodes_points_color)[1:-1]
            self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.nodes_points_color = Color(*nodes_points_color)
        
    def update_line_edit_nodes_points_color(self):
        str_color = str(self.user_preferences.nodes_points_color.to_rgb())[1:-1]
        self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            lines_color = tuple(read.color)
            str_color = str(lines_color)[1:-1]
            self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.lines_color = Color(*lines_color)
    
    def update_line_edit_lines_color(self):
        str_color = str(self.user_preferences.lines_color.to_rgb())[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_tubes_color(self):
        read = PickColorInput(title="Pick the surfaces color")
        if read.complete:
            tubes_color = tuple(read.color)
            str_color = str(tubes_color)[1:-1]
            self.lineEdit_tubes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
           
            self.tubes_color = Color(*tubes_color)

    def update_line_edit_tubes_color(self):
        str_color = str(self.user_preferences.tubes_color.to_rgb())[1:-1]
        self.lineEdit_tubes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_size(self):
        try:
            self.renderer_font_size = int(self.lineEdit_interface_font_size.text())
            self.user_preferences.renderer_font_size = self.renderer_font_size
        except:
            pass
    
    def update_line_edit_renderer_font_size(self):
        renderer_font_size = str(self.user_preferences.renderer_font_size)
        self.lineEdit_renderer_font_size.setText(renderer_font_size)
        
    def update_interface_font_size(self):
        try:
            self.interface_font_size = int(self.lineEdit_interface_font_size.text())
            self.user_preferences.interface_font_size = self.interface_font_size
        except:
            pass
    
    def update_line_edit_interface_font_size(self):
        interface_font_size = str(self.user_preferences.interface_font_size)
        self.lineEdit_interface_font_size.setText(interface_font_size)

    def confirm_and_update_user_preferences(self):
        if self.renderer_background_color_1 is not None:
            self.user_preferences.renderer_background_color_1 = self.renderer_background_color_1

        if self.renderer_background_color_2 is not None:
            self.user_preferences.renderer_background_color_2 = self.renderer_background_color_2

        if self.renderer_font_color is not None:
            self.user_preferences.renderer_font_color = self.renderer_font_color
        
        if self.nodes_points_color is not None:
            self.user_preferences.nodes_points_color = self.nodes_points_color

        if self.lines_color is not None:
            self.user_preferences.lines_color = self.lines_color

        if self.tubes_color is not None:
            self.user_preferences.tubes_color = self.tubes_color

        if self.renderer_font_size is not None:
            self.user_preferences.renderer_font_size = self.renderer_font_size

        if self.interface_font_size is not None:
            self.user_preferences.interface_font_size = self.interface_font_size

        self.main_window.update_plots()
        self.update_open_pulse_logo_state()
        self.update_reference_scale_state()
        self.accept()        

    def reset_to_default(self):
        if self.main_window.user_preferences["interface theme"] == "dark":
            self.user_preferences.set_dark_theme()
        else:
            self.user_preferences.set_light_theme()
        
        self.user_preferences.reset_font_size()
        self.reset_logo_state()
        self.reset_reference_scale_state()
        self.load_user_preferences()

    def reset_logo_state(self):
        self.user_preferences.reset_open_pulse_logo()
        self.checkBox_OpenPulse_logo.setChecked(1)

    def reset_reference_scale_state(self):
        self.user_preferences.reset_reference_scale_bar()
        self.checkBox_reference_scale.setChecked(1)
    
    def update_open_pulse_logo_state(self):
        if self.checkBox_OpenPulse_logo.isChecked():
            self.user_preferences.show_open_pulse_logo = True
            self.main_window.results_widget.enable_open_pulse_logo()
            self.main_window.geometry_widget.enable_open_pulse_logo()
            self.main_window.mesh_widget.enable_open_pulse_logo()
        else:
            self.user_preferences.show_open_pulse_logo = False
            self.main_window.results_widget.disable_open_pulse_logo()
            self.main_window.geometry_widget.disable_open_pulse_logo()
            self.main_window.mesh_widget.disable_open_pulse_logo()

    def update_show_open_pulse_logo_checkbox(self):
        if self.user_preferences.show_open_pulse_logo:
            self.checkBox_OpenPulse_logo.setChecked(1)
        else:
            self.checkBox_OpenPulse_logo.setChecked(0)

    def update_reference_scale_state(self):
        if self.checkBox_reference_scale.isChecked():
            self.user_preferences.show_reference_scale_bar = True
            self.main_window.results_widget.enable_scale_bar()
            self.main_window.mesh_widget.enable_scale_bar()
        else:
            self.user_preferences.show_reference_scale_bar = False
            self.main_window.results_widget.disable_scale_bar()
            self.main_window.mesh_widget.disable_scale_bar()

    def update_show_reference_scalebar_checkbox(self):
        if self.user_preferences.show_reference_scale_bar:
            self.checkBox_reference_scale.setChecked(1)
        else:
            self.checkBox_reference_scale.setChecked(0)

    def load_user_preferences(self):
        self.update_line_edit_renderer_background_color_1()
        self.update_line_edit_renderer_background_color_2()
        self.update_line_edit_renderer_font_color()
        self.update_line_edit_nodes_points_color()
        self.update_line_edit_lines_color()
        self.update_line_edit_tubes_color()
        self.update_line_edit_renderer_font_size()
        self.update_line_edit_interface_font_size()
        self.update_show_open_pulse_logo_checkbox()
        self.update_show_reference_scalebar_checkbox()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()