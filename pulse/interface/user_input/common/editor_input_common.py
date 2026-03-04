from PySide6.QtWidgets import QWidget



from pulse.interface.ui_generated.common.editor_input_common_ui import EditorInputCommon_UI


class EditorInputCommon(EditorInputCommon_UI):
    '''
    A simple window with buttons to confirm and cancel
    that handles any widgets inside it.
    '''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._create_connections()

    def _create_connections(self):
        self.cancel_button.clicked.connect(self.cancel_button_callback)
        self.confirm_button.clicked.connect(self.confirm_button_callback)

    def set_title(self, name: str):
        self.title_label.setText(name)

    def set_central_widget(self, central_widget):
        if not isinstance(central_widget, QWidget):
            return
        
        previous = self.central_widget
        current = central_widget
        self.central_widget = central_widget
        self.layout().replaceWidget(previous, current)
        self.layout().removeWidget(previous)

    def cancel_button_callback(self):
        self.close()

    def confirm_button_callback(self):
        self.close()
