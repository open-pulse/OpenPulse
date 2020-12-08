from PyQt5.QtWidgets import QTabWidget

class MenuInfo(QTabWidget):
    """MenuInfo

    This class is responsible for building a small area below of the item menu
    when some item is clicked. This has been replaced for QDialog windows and currently isn't used.

    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._set_config()

    def _set_config(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self._close_tab)

    def _close_tab(self, index):
        current_widget = self.widget(index)
        self.removeTab(index)
        # print(self.currentIndex)

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
        
