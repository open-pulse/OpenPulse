from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QFrame, QLineEdit, QPushButton, QRadioButton, QSlider, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput


class RendererUserPreferencesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "project/render/renderer_user_preferences.ui", self)

        self.main_window = app().main_window
        self.config = app().config
        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._load_logo_state()
        self._load_reference_scale_state()
        self._load_color_state()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _initialize(self):
        self.cache_setup = [self.opv.background_color,
                            self.opv.font_color,
                            self.opv.opvRenderer.nodes_color,
                            self.opv.opvRenderer.lines_color,
                            self.opv.opvRenderer.surfaces_color,
                            self.opv.opvRenderer.elements_transparency]

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_OpenPulse_logo : QCheckBox
        self.checkBox_reference_scale : QCheckBox
        # QComboBox
        self.comboBox_background_theme : QComboBox
        # QFrame
        self.frame_background_color : QFrame
        # QSlider
        self.slider_transparency : QSlider
        # QLineEdit
        self.lineEdit_background_color : QLineEdit
        self.lineEdit_font_color : QLineEdit
        self.lineEdit_nodes_color : QLineEdit
        self.lineEdit_lines_color : QLineEdit
        self.lineEdit_surfaces_color : QLineEdit
        self.lineEdit_elements_transparency : QLineEdit
        # QPushButton
        self.pushButton_background_color : QPushButton
        self.pushButton_font_color : QPushButton
        self.pushButton_nodes_color : QPushButton
        self.pushButton_lines_color : QPushButton
        self.pushButton_surfaces_color : QPushButton
        self.pushButton_reset_to_default : QPushButton
        self.pushButton_update_settings : QPushButton
        # QTabWidget
        self.tabWidget_main : QTabWidget

    def _create_connections(self):
        self.comboBox_background_theme.currentIndexChanged.connect(self.update_background_color_controls_visibility)
        self.pushButton_background_color.clicked.connect(self.update_background_color)
        self.pushButton_font_color.clicked.connect(self.update_font_color)
        self.pushButton_nodes_color.clicked.connect(self.update_nodes_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_surfaces_color.clicked.connect(self.update_surfaces_color)
        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.slider_transparency.valueChanged.connect(self.update_transparency_value)
        self.update_slider_transparency()

    def update_background_color_controls_visibility(self):
        index = self.comboBox_background_theme.currentIndex()
        if index == 2:
            _bool = False
        else:
            _bool = True
            self.lineEdit_background_color.setStyleSheet("")
        self.pushButton_background_color.setDisabled(_bool)

    def _load_reference_scale_state(self):
        self.checkBox_reference_scale.setChecked(self.opv.show_reference_scale)

    def _load_color_state(self):

        self.background_color = self.opv.background_color
        self.font_color = self.opv.font_color
        self.nodes_color = self.opv.opvRenderer.nodes_color
        self.lines_color = self.opv.opvRenderer.lines_color
        self.surfaces_color = self.opv.opvRenderer.surfaces_color
        self.elements_transparency = self.opv.opvRenderer.elements_transparency

        if self.background_color in ["light", "dark"]:
            if self.background_color == "light":
                self.comboBox_background_theme.setCurrentIndex(0)
            elif self.background_color == "dark":
                self.comboBox_background_theme.setCurrentIndex(1)
            self.pushButton_background_color.setDisabled(True)
            self.lineEdit_background_color.setDisabled(True)
        else:
            self.comboBox_background_theme.setCurrentIndex(2)
            self.pushButton_background_color.setDisabled(False)
            self.lineEdit_background_color.setDisabled(False)
            str_color = str(self.background_color)[1:-1]
            self.lineEdit_background_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.font_color)[1:-1]
        self.lineEdit_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.nodes_color)[1:-1]
        self.lineEdit_nodes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.lines_color)[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.surfaces_color)[1:-1]
        self.lineEdit_surfaces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def _load_logo_state(self):
        self.checkBox_OpenPulse_logo.setChecked(self.opv.add_OpenPulse_logo)

    def update_background_color_state(self):
        index = self.comboBox_background_theme.currentIndex()
        if index == 0:
            self.background_color = "light"
        elif index == 1:
            self.background_color = "dark"
        elif index == 2:
            if self.background_color in ["light", "dark"]:
                if self.update_background_color():
                    return

        self.opv.background_color = self.background_color
        self.opv.opvRenderer.set_background_color(self.background_color)
        self.opv.opvAnalysisRenderer.set_background_color(self.background_color)
        self.opv.opvGeometryRenderer.set_background_color(self.background_color)

    def update_font_color_state(self):
        self.opv.font_color = self.font_color
        self.opv.opvRenderer.change_font_color(self.font_color)
        self.opv.opvAnalysisRenderer.change_font_color(self.font_color)
    
    def update_reference_scale_state(self):
        self.opv.show_reference_scale = self.checkBox_reference_scale.isChecked()
        self.opv.opvRenderer._createScaleBar()
        self.opv.opvAnalysisRenderer._createScaleBar()
            
    def update_logo_state(self):     
        self.opv.add_OpenPulse_logo = self.checkBox_OpenPulse_logo.isChecked()
        self.opv.opvRenderer.add_logos(OpenPulse=self.opv.add_OpenPulse_logo)
        self.opv.opvAnalysisRenderer.add_logos(OpenPulse=self.opv.add_OpenPulse_logo)

    def update_transparency_value(self):
        self.elements_transparency = (self.slider_transparency.value()/100)
        self.lineEdit_elements_transparency.setText(str(self.elements_transparency))

    def update_slider_transparency(self):
        value = self.opv.opvRenderer.elements_transparency
        self.slider_transparency.setValue(int(100*value))
        self.lineEdit_elements_transparency.setText(str(value))

    def update_background_color(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            self.background_color = tuple(read.color)
            str_color = str(self.background_color)[1:-1]
            self.lineEdit_background_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
            return False
        return True

    def update_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            self.font_color = tuple(read.color)
            str_color = str(self.font_color)[1:-1]
            self.lineEdit_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return

    def update_nodes_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            self.nodes_color = tuple(read.color)
            str_color = str(self.nodes_color)[1:-1]
            self.lineEdit_nodes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return 
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            self.lines_color = tuple(read.color)
            str_color = str(self.lines_color)[1:-1]
            self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return

    def update_surfaces_color(self):
        read = PickColorInput(title="Pick the surfaces color")
        if read.complete:
            self.surfaces_color = tuple(read.color)
            str_color = str(self.surfaces_color)[1:-1]
            self.lineEdit_surfaces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return        

    def update_nodes_lines_elements_settings(self):
        self.opv.opvRenderer.changeNodesColor(self.nodes_color)
        self.opv.opvRenderer.changeLinesColor(self.lines_color)
        self.opv.opvRenderer.changeSurfacesColor(self.surfaces_color)
        self.opv.opvRenderer.changeElementsTransparency(self.elements_transparency)

    def confirm_and_update_user_preferences(self):

        self.update_logo_state()
        self.update_background_color_state()
        self.update_font_color_state()
        self.update_reference_scale_state()
        self.update_nodes_lines_elements_settings()
        self.update_transparency_value()

        preferences = { 'interface theme' : self.main_window.interface_theme,
                        'background color' : str(self.opv.background_color),
                        'font color' : str(self.opv.font_color),
                        'nodes color' : str(self.opv.opvRenderer.nodes_color),
                        'lines color' : str(self.opv.opvRenderer.lines_color),
                        'surfaces color' : str(self.opv.opvRenderer.surfaces_color),
                        'transparency' : str(self.opv.opvRenderer.elements_transparency),
                        'openpulse logo' : str(int(self.opv.add_OpenPulse_logo)),
                        'Reference scale' : str(int(self.opv.show_reference_scale)) }
        
        self.config.write_user_preferences_in_file(preferences)
        
        self.update_renders()
        self._initialize()
        # self.close()

    def update_renders(self):

        final_setup = [ self.opv.background_color,
                        self.opv.font_color,
                        self.opv.opvRenderer.nodes_color,
                        self.opv.opvRenderer.lines_color,
                        self.opv.opvRenderer.surfaces_color,
                        self.opv.opvRenderer.elements_transparency ]

        if final_setup != self.cache_setup:
            self.opv.updateRendererMesh()
            self.main_window.update_plot_mesh()

    def reset_to_default(self):
        self.reset_logo_state()
        self.reset_background_color_state()
        self.reset_font_color_state()
        self.reset_reference_scale_state()
        self.reset_nodes_lines_elements_settings()
        self.reset_transparency_value()

        preferences = { 'interface theme' : self.main_window.interface_theme,
                        'background color' : str(self.opv.background_color),
                        'font color' : str(self.opv.font_color),
                        'nodes color' : str(self.opv.opvRenderer.nodes_color),
                        'lines color' : str(self.opv.opvRenderer.lines_color),
                        'surfaces color' : str(self.opv.opvRenderer.surfaces_color),
                        'transparency' : str(self.opv.opvRenderer.elements_transparency),
                        'openpulse logo' : str(int(self.opv.add_OpenPulse_logo)),
                        'Reference scale' : str(int(self.opv.show_reference_scale)) }
        
        self.config.write_user_preferences_in_file(preferences)
        
        self.update_renders()
        self._initialize()

    def reset_logo_state(self):
        self.checkBox_OpenPulse_logo.setChecked(True)
        self.update_logo_state()

    def reset_background_color_state(self):
        if self.main_window.interface_theme == "light":
            self.comboBox_background_theme.setCurrentIndex(0)
        else:
            self.comboBox_background_theme.setCurrentIndex(1)
        self.update_background_color_state()

    def reset_font_color_state(self):
        if self.main_window.interface_theme == "light":
            self.font_color = (0,0,0)
        else:
            self.font_color = (255,255,255)
        self.update_font_color_state()

    def reset_reference_scale_state(self):
        self.checkBox_reference_scale.setChecked(True)
        self.update_reference_scale_state()

    def reset_nodes_lines_elements_settings(self):

        self.nodes_color = (255,255,63)
        self.lines_color = (255,255,255)
        self.surfaces_color = (255,255,255)
        self.elements_transparency = 0.8

        str_color = str(self.font_color)[1:-1]
        self.lineEdit_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.nodes_color)[1:-1]
        self.lineEdit_nodes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.lines_color)[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.surfaces_color)[1:-1]
        self.lineEdit_surfaces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        self.update_nodes_lines_elements_settings()

    def reset_transparency_value(self):
        self.slider_transparency.setValue(80)
        self.update_transparency_value()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()