from pulse.interface.user_input.common.editor_input_common import EditorInputCommon
from pulse.interface.user_input.model.setup.structural.expansion_joint_widget import ExpansionJointWidget


class ExpansionJointGeometryInput(EditorInputCommon):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.expansion_joint_widget = ExpansionJointWidget(self)
        self.value = None

        self.set_central_widget(self.expansion_joint_widget)
        self.exec()
    
    def confirm_button_callback(self):
        self.value = self.expansion_joint_widget.get_parameters()
        if self.value is not None:
            self.close()
