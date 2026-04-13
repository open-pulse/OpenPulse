from enum import IntEnum

from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.cross_section.set_cross_section_simplified_ui import SetCrossSectionSimplified_UI
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget


window_title_1 = "Error"
window_title_2 = "Warning"

class TabIndex(IntEnum):
    PIPE = 0
    BEAM = 1
    ACTIVE_SECTIONS = 2


class SetCrossSectionSimplified(SetCrossSectionSimplified_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties
        self.pipeline = app().project.pipeline

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        # while self.keep_window_open:
        #     self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Configure the cross-section")

    def _initialize(self):
        self.selected_column = None
        self.complete = False
        self.keep_window_open = True

    def _define_qt_variables(self):
        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_cross_section.setLayout(self.grid_layout)
        self._add_cross_section_widget()
        # self.frame_main_widget.adjustSize()
        # self.scrollArea_cross_section.adjustSize()

        # QPushButton
        self.pushButton_exit_pipe = self.cross_section_widget.pushButton_exit_pipe
        self.pushButton_exit_beam = self.cross_section_widget.pushButton_exit_beam
        self.pushButton_confirm_beam = self.cross_section_widget.pushButton_confirm_beam
        self.pushButton_confirm_pipe = self.cross_section_widget.pushButton_confirm_pipe

    def _create_connections(self):
        self.pushButton_exit_pipe.clicked.connect(self.close)
        self.pushButton_exit_beam.clicked.connect(self.close)
        self.pushButton_confirm_beam.clicked.connect(self.attribute_callback)
        self.pushButton_confirm_pipe.clicked.connect(self.attribute_callback)

    def _add_cross_section_widget(self):
        self.cross_section_widget = CrossSectionWidget(dialog=self)
        self.grid_layout.addWidget(self.cross_section_widget)

    def attribute_callback(self):
        self.complete = True
        self.close()

    def load_active_sections(self):
        self.cross_section_widget.treeWidget_sections_parameters_by_lines.clear()
        self.cross_section_widget.tabWidget_general.setTabVisible(TabIndex.ACTIVE_SECTIONS, True)
        self.cross_section_widget.treeWidget_sections_parameters_by_lines.hideColumn(1) # hides the 'Element option' column


        active_sections = []
        for structure in self.pipeline.structures:
            cross_section_info = structure.extra_info['cross_section_info']
            section_parameters = cross_section_info['section_parameters']

            if section_parameters not in active_sections:
                active_sections.append(section_parameters)    

                new = QTreeWidgetItem([str(len(active_sections)), '', cross_section_info['section_type_label'], str(section_parameters)])
                
                for i in range(4):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.cross_section_widget.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)

            
        
    # def main_tab_callback(self):
    #     if self.cross_section_widget.tabWidget_general.currentIndex() == TabIndex.ACTIVE_SECTIONS:
    #         self.cross_section_widget.pushButton_edit_section_data.setDisabled(True)
    #         self.cross_section_widget.pushButton_load_section_data.setDisabled(True)
    #         self.cross_section_widget.comboBox_attribution_type.setDisabled(True)
    #         return

        # self.cross_section_widget.comboBox_attribution_type.setDisabled(False)
