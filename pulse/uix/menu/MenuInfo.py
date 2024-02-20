from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
from pulse import UI_DIR

class MenuInfo(QWidget):
    """Menu Info

    This class is responsible for building a small area below of the item menu
    when some item is clicked. This has been replaced for QDialog windows and currently isn't used.

    """
    def __init__(self, main_window, menu_items):
        super().__init__()
        #
        self.main_window = main_window
        self.menu_items = menu_items
        uic.loadUi(UI_DIR / "/project/analysisFilter.ui", self)
        self._define_Qt_variables_and_connections()
        # self._create_radioButtons()
        # self._set_config()

    def _define_Qt_variables_and_connections(self):
        """
        """
        self.radioButton_structural_analysis = self.findChild(QRadioButton, "radioButton_structural_analysis")
        self.radioButton_acoustic_analysis = self.findChild(QRadioButton, "radioButton_acoustic_analysis")
        self.radioButton_coupled_analysis = self.findChild(QRadioButton, "radioButton_coupled_analysis")
        self.radioButton_structural_analysis.toggled.connect(self.menu_items.update_structural_analysis_visibility_items)
        self.radioButton_acoustic_analysis.toggled.connect(self.menu_items.update_acoustic_analysis_visibility_items)
        self.radioButton_coupled_analysis.toggled.connect(self.menu_items.update_coupled_analysis_visibility_items)
        if self.radioButton_structural_analysis.isChecked():
            self.menu_items.update_structural_analysis_visibility_items()

    def _set_config(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self._close_tab)

    def _close_tab(self, index):
        current_widget = self.widget(index)
        self.removeTab(index)

    def _remove_repeated_tabs(self, new_tab):
        for tab in range(self.count()):
            same_index = (tab == new_tab)  
            same_text = (self.tabText(tab) == self.tabText(new_tab))
            if same_text and not same_index: 
                self.removeTab(tab)
    
    # HERITAGE
    def tabInserted(self, index):
        self.setCurrentIndex(index)
        self._remove_repeated_tabs(index)
        
