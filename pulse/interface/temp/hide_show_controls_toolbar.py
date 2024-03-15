from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtWidgets import QAction, QToolBar, QLabel, QSpinBox, QRadioButton

from pulse.interface.formatters.icons import *


class HideShowControlsToolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        self.load_icons()
        self.create_actions()
        self.configure_layout()
        self.configure_appearance()

    def load_icons(self):
        self.element_and_lines_with_cross_sections_icon = QIcon(get_icons_path('cross_section_representation.png'))
        self.lines_only_icon = QIcon(get_icons_path('lines_only.png'))
        self.elements_and_nodes_icon = QIcon(get_icons_path('elements_and_nodes.png'))
        self.elements_only_icon = QIcon(get_icons_path('elements_only.png'))
        self.nodes_only_icon = QIcon(get_icons_path('nodes_only.png'))

    def configure_appearance(self):
        # self.setContentsMargins(4,4,4,4)
        self.setMovable(True)
        self.setFloatable(True)

    def create_actions(self):

        label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
        radioButton_font = self._getFont(9, bold=True, italic=True, family_type="Arial")  

        self.hide_selection_action = QAction('&Hide \nselection', self)
        self.hide_selection_action.setFont(radioButton_font)
        self.hide_selection_action.setShortcut('H')
        self.hide_selection_action.triggered.connect(self.hide_selection)
        
        self.show_all_action = QAction('&Show \nall', self)
        self.show_all_action.setFont(radioButton_font)
        self.show_all_action.setShortcut('U')
        self.show_all_action.triggered.connect(self.unhide_selection)

        self.acoustic_symbols_action = QAction('&Acoustic \nsymbols', self)
        self.acoustic_symbols_action.setFont(radioButton_font)
        # self.acoustic_symbols_action.setShortcut('')
        self.acoustic_symbols_action.triggered.connect(self.hide_show_acoustic_symbols)

        self.structural_symbols_action = QAction('&Structural \nsymbols', self)
        self.structural_symbols_action.setFont(radioButton_font)
        # self.structural_symbols_action.setShortcut('')
        self.structural_symbols_action.triggered.connect(self.hide_show_structural_symbols)

        self.show_lines_action = QAction(self.lines_only_icon, '&Hide/Show lines', self)
        # self.show_lines_action.setShortcut('')
        self.show_lines_action.setStatusTip('Hide/Show lines')
        self.show_lines_action.triggered.connect(self.hide_show_lines)

        self.show_elements_and_nodes_action = QAction(self.elements_and_nodes_icon, '&Hide/Show elements and nodes', self)
        # self.show_elements_and_nodes_action.setShortcut('')
        self.show_elements_and_nodes_action.setStatusTip('Hide/Show elements and nodes')
        self.show_elements_and_nodes_action.triggered.connect(self.hide_show_elements_and_nodes)

        self.show_elements_action = QAction(self.elements_only_icon, '&Hide/Show elements', self)
        # self.show_elements_action.setShortcut('')
        self.show_elements_action.setStatusTip('Hide/Show elements')
        self.show_elements_action.triggered.connect(self.hide_show_elements)

        self.show_nodes_action = QAction(self.nodes_only_icon, '&Hide/Show nodes', self)
        # self.show_nodes_action.setShortcut('')
        self.show_nodes_action.setStatusTip('Hide/Show nodes')
        self.show_nodes_action.triggered.connect(self.hide_show_nodes)
        
        self.label_hide_show_controls = QLabel(' Hide/Show controls:  ', self)
        self.label_hide_show_controls.setFont(label_font)

        self.radioButton_hide = QRadioButton("Hide ", self)
        self.radioButton_show = QRadioButton("Show ", self)
        self.radioButton_hide.setChecked(True)
        self.radioButton_hide.setFont(radioButton_font)
        self.radioButton_show.setFont(radioButton_font)

    def configure_layout(self):       
        self.addWidget(self.label_hide_show_controls)
        self.addAction(self.hide_selection_action)
        self.addWidget(self.radioButton_hide)
        self.addWidget(self.radioButton_show)

        self.addSeparator()
        self.addAction(self.show_lines_action)
        self.addAction(self.show_elements_and_nodes_action)
        self.addAction(self.show_elements_action)
        self.addAction(self.show_nodes_action)
        self.addAction(self.show_all_action)
        self.addAction(self.acoustic_symbols_action)
        self.addAction(self.structural_symbols_action)

        # widget_hide_selection = self.widgetForAction(self.hide_selection_action)
        widget_show_all = self.widgetForAction(self.show_all_action)
        widget_acoustic_symbols = self.widgetForAction(self.acoustic_symbols_action)
        widget_structural_symbols = self.widgetForAction(self.structural_symbols_action)

        # widget_hide_selection.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_show_all.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_acoustic_symbols.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_structural_symbols.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")

    def update_frames(self):
        self.main_window.opv_widget.opvAnalysisRenderer._numberFramesHasChanged(True)

    def toggle_button_callback(self):
        frames = self.spinBox_frames.value()
        cycles = self.spinBox_cycles.value()
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberFrames(frames)
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberCycles(cycles)
        self.main_window.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()

    def _getFont(self, fontSize, bold=False, italic=False, family_type="Arial"):
        font = QFont()
        font.setFamily(family_type)
        font.setPointSize(fontSize)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(75)  
        return font
    
    def hide_selection(self):
        self.main_window.opv_widget.opvRenderer.hide_selection()

    def unhide_selection(self):
        self.main_window.opv_widget.opvRenderer.unhide_all()

    def hide_show_lines(self):
        self.main_window.opv_widget.opvRenderer.hide_show_lines(self.radioButton_show.isChecked())

    def hide_show_elements_and_nodes(self):
        self.main_window.opv_widget.opvRenderer.hide_show_elements_and_nodes(self.radioButton_show.isChecked())

    def hide_show_elements(self):
        self.main_window.opv_widget.opvRenderer.hide_show_elements(self.radioButton_show.isChecked())
            
    def hide_show_nodes(self):
        self.main_window.opv_widget.opvRenderer.hide_show_nodes(self.radioButton_show.isChecked())

    def hide_show_acoustic_symbols(self):
        self.main_window.opv_widget.opvRenderer.hide_show_acoustic_symbols()

    def hide_show_structural_symbols(self):
        self.main_window.opv_widget.opvRenderer.hide_show_structural_symbols()