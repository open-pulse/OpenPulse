from PySide6.QtWidgets import QToolBar, QSizePolicy
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, Signal

from pulse import ICON_DIR
from pulse.interface.viewer_3d.render_tools import (
    RenderTool,
    RotationTool,
    GrabTool,
    ZoomTool,
    SelectionTool
)

from pulse import app


class ViewToolbar(QToolBar):
    render_tool_changed = Signal(RenderTool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._define_qt_variables()
        self._load_icons()
        self._configure_layout()
        self._configure_appearence()
        self._configure_widgets()
        self._connect_actions()

        self.setWindowTitle("View toolbar")

    def _define_qt_variables(self):
        self.action_selection_tool = QAction(self)
        self.action_grab_tool = QAction(self)
        self.action_rotation_tool = QAction(self)
        self.action_zoom_tool = QAction(self)

        self.action_top_view = QAction(self)
        self.action_bottom_view = QAction(self)
        self.action_left_view = QAction(self)
        self.action_right_view = QAction(self)
        self.action_front_view = QAction(self)
        self.action_back_view = QAction(self)
        self.action_isometric_view = QAction(self)

    def _load_icons(self):
        self.selection_tool_icon = QIcon(str(ICON_DIR / "common/selection_icon.png"))
        self.grab_tool_icon = QIcon(str(ICON_DIR / "common/grab_icon.png"))
        self.rotation_tool_icon = QIcon(str(ICON_DIR / "common/rotation_icon.png"))
        self.zoom_tool_icon = QIcon(str(ICON_DIR / "common/zoom_icon.png"))

        self.top_view_icon = QIcon(str(ICON_DIR / "common/top.png"))
        self.bottom_view_icon = QIcon(str(ICON_DIR / "common/bottom.png"))
        self.left_view_icon = QIcon(str(ICON_DIR / "common/left.png"))
        self.right_view_icon = QIcon(str(ICON_DIR / "common/right.png"))
        self.front_view_icon = QIcon(str(ICON_DIR / "common/front.png"))
        self.back_view_icon = QIcon(str(ICON_DIR / "common/back.png"))
        self.isometric_view_icon = QIcon(str(ICON_DIR / "common/isometric.png"))

    def _configure_layout(self):
        self.addAction(self.action_selection_tool)
        self.addAction(self.action_grab_tool)
        self.addAction(self.action_rotation_tool)
        self.addAction(self.action_zoom_tool)
        self.addSeparator()
        self.addAction(self.action_top_view)
        self.addAction(self.action_bottom_view)
        self.addAction(self.action_left_view)
        self.addAction(self.action_right_view)
        self.addAction(self.action_front_view)
        self.addAction(self.action_back_view)
        self.addAction(self.action_isometric_view)

    def _configure_appearence(self):
        self.setMovable(True)
        self.setOrientation(Qt.Horizontal)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setStyleSheet(
            """
            QToolBar {
                border-style: solid;
                border-width: 1px;
                border-color: #888888;
            }
            """
        )

    def _configure_widgets(self):
        self.action_selection_tool.setCheckable(True)
        self.action_grab_tool.setCheckable(True)
        self.action_rotation_tool.setCheckable(True)
        self.action_zoom_tool.setCheckable(True)

        self.action_selection_tool.setChecked(True)

        self.action_selection_tool.setIcon(self.selection_tool_icon)
        self.action_selection_tool.setToolTip("Selection tool")

        self.action_grab_tool.setIcon(self.grab_tool_icon)
        self.action_grab_tool.setToolTip("Grab tool")

        self.action_rotation_tool.setIcon(self.rotation_tool_icon)
        self.action_rotation_tool.setToolTip("Rotation tool")

        self.action_zoom_tool.setIcon(self.zoom_tool_icon)
        self.action_zoom_tool.setToolTip("Zoom tool")

        self.action_top_view.setIcon(self.top_view_icon)
        self.action_top_view.setText("Top View")
        self.action_top_view.setToolTip("Top View")
        self.action_top_view.setShortcut(QKeySequence("Ctrl+Shift+1"))

        self.action_bottom_view.setIcon(self.bottom_view_icon)
        self.action_bottom_view.setText("Bottom View")
        self.action_bottom_view.setToolTip("Bottom View")
        self.action_bottom_view.setShortcut(QKeySequence("Ctrl+Shift+2"))

        self.action_left_view.setIcon(self.left_view_icon)
        self.action_left_view.setText("Left View")
        self.action_left_view.setToolTip("Left View")
        self.action_left_view.setShortcut(QKeySequence("Ctrl+Shift+5"))

        self.action_right_view.setIcon(self.right_view_icon)
        self.action_right_view.setText("Right View")
        self.action_right_view.setToolTip("Right View")
        self.action_right_view.setShortcut(QKeySequence("Ctrl+Shift+6"))

        self.action_front_view.setIcon(self.front_view_icon)
        self.action_front_view.setText("Front View")
        self.action_front_view.setToolTip("Front View")
        self.action_front_view.setShortcut(QKeySequence("Ctrl+Shift+3"))

        self.action_back_view.setIcon(self.back_view_icon)
        self.action_back_view.setText("Back View")
        self.action_back_view.setToolTip("Back View")
        self.action_back_view.setShortcut(QKeySequence("Ctrl+Shift+4"))

        self.action_isometric_view.setIcon(self.isometric_view_icon)
        self.action_isometric_view.setText("Isometric View")
        self.action_isometric_view.setToolTip("Isometric View")
        self.action_isometric_view.setShortcut(QKeySequence("Ctrl+Shift+7"))

    def _connect_actions(self):
        self.action_selection_tool.triggered.connect(self.action_selection_tool_callback)
        self.action_grab_tool.triggered.connect(self.action_grab_tool_callback)
        self.action_rotation_tool.triggered.connect(self.action_rotation_tool_callback)
        self.action_zoom_tool.triggered.connect(self.action_zoom_tool_callback)

        self.action_top_view.triggered.connect(self.action_top_view_callback)
        self.action_bottom_view.triggered.connect(self.action_bottom_view_callback)
        self.action_left_view.triggered.connect(self.action_left_view_callback)
        self.action_right_view.triggered.connect(self.action_right_view_callback)
        self.action_front_view.triggered.connect(self.action_front_view_callback)
        self.action_back_view.triggered.connect(self.action_back_view_callback)
        self.action_isometric_view.triggered.connect(self.action_isometric_view_callback)

    def action_grab_tool_callback(self):
        if self.action_grab_tool.isChecked():
            self.discheck_all_actions_of_view_toolbar_except(self.action_grab_tool)
            self.render_tool_changed.emit(GrabTool)
        else:
            self.action_selection_tool_callback()

    def action_selection_tool_callback(self):
        self.discheck_all_actions_of_view_toolbar_except(self.action_selection_tool)

        if not app().main_window.use_base_render_tool:
            self.render_tool_changed.emit(SelectionTool)
        else:
            self.render_tool_changed.emit(RenderTool)

    def action_rotation_tool_callback(self):
        if self.action_rotation_tool.isChecked():
            self.discheck_all_actions_of_view_toolbar_except(self.action_rotation_tool)
            self.render_tool_changed.emit(RotationTool)
        else:
            self.action_selection_tool_callback()

    def action_zoom_tool_callback(self):
        if self.action_zoom_tool.isChecked():
            self.discheck_all_actions_of_view_toolbar_except(self.action_zoom_tool)
            self.render_tool_changed.emit(ZoomTool)
        else:
            self.action_selection_tool_callback()

    def _current_render_widget(self):
        return app().main_window.render_widgets_stack.currentWidget()

    def action_top_view_callback(self):
        self._current_render_widget().set_top_view()

    def action_bottom_view_callback(self):
        self._current_render_widget().set_bottom_view()

    def action_left_view_callback(self):
        self._current_render_widget().set_left_view()

    def action_right_view_callback(self):
        self._current_render_widget().set_right_view()

    def action_front_view_callback(self):
        self._current_render_widget().set_front_view()

    def action_back_view_callback(self):
        self._current_render_widget().set_back_view()

    def action_isometric_view_callback(self):
        self._current_render_widget().set_isometric_view()

    def discheck_all_actions_of_view_toolbar_except(self, action: QAction):
        for _action in [
            self.action_selection_tool,
            self.action_grab_tool,
            self.action_rotation_tool,
            self.action_zoom_tool,
        ]:
            _action.setChecked(False)

        action.setChecked(True)

    def enable_selection_tool(self):
        self.action_selection_tool.setEnabled(True)
        app().main_window.use_base_render_tool = False

    def disable_selection_tool(self):
        self.action_selection_tool.setEnabled(False)
        app().main_window.use_base_render_tool = True
