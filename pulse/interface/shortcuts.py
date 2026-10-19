from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QLineEdit,
    QMenu,
    QPlainTextEdit,
    QTextEdit,
)

from pulse import app

# --- How to add a shortcut -------------------------------------------------
# Add an entry to the SHORTCUTS dict below. Each key is a Qt key sequence; each
# value is a (target, description) tuple, where target is addressed as a dotted
# path from the main window:
#
#   QAction    -> the QShortcut triggers it
#       "Ctrl+S": ("action_save_project", "Save the project")
#       "Ctrl+1": ("view_toolbar.action_front_view", "Front view")
#
#   callable   -> the QShortcut calls it (method/attribute of the main window)
#       "F5": ("update_plots", "Refresh the plots")
#
# register_global_shortcuts() wires everything at startup and the "?" dialog
# lists the keymap automatically.
#
# Shortcuts are NOT attached to the QActions: the ones defined in
# main_window.ui (and in view_toolbar.py) are cleared during the registration,
# so this registry is the single source of truth for application-wide keys.
# Adding a new shortcut only in the .ui file will silently do nothing.
# ---------------------------------------------------------------------------

TEXT_INPUT_WIDGETS = (QLineEdit, QTextEdit, QPlainTextEdit, QAbstractSpinBox)


def is_typing_input(widget) -> bool:
    """
    True when the focused widget actually accepts keyboard text input.

    Non-editable QComboBoxes (selection-only) and read-only widgets should not
    count as text input: they never consume letters/arrows for typing, so we
    should not disable shortcuts while the user is simply picking an option
    (e.g. analysis type / physical domain).
    """
    if isinstance(widget, QComboBox):
        return widget.isEditable()
    return isinstance(widget, TEXT_INPUT_WIDGETS)


# Single source of truth for the application keymap.
# Each entry maps a key sequence to a (target, description) tuple:

SHORTCUTS = {
    # project
    "Ctrl+N": ("action_new_project", "New project"),
    "Ctrl+O": ("action_open_project", "Open a project"),
    "Ctrl+I": ("action_import_geometry", "Import the geometry"),
    "Ctrl+E": ("action_export_geometry", "Export the geometry"),
    "Ctrl+S": ("action_save_project", "Save the project"),
    "Ctrl+Shift+S": ("action_save_project_as", "Save the project as"),
    "Ctrl+W": ("action_home_exit", "Home exit app"),
    "Ctrl+Shift+Q": ("action_exit", "Exit the application"),
    "Ctrl+P": ("action_capture_image", "Capture the image"),
    "Ctrl+C": ("action_copy_screenshot_to_clipboard_callback", "Copy screenshot to clipboard"),

    # model
    "Ctrl+Shift+G": ("input_ui.mesh_setup", "Set up the mesh"),
    "Ctrl+R": ("analysis_toolbar.run_analysis_action", "Run the analysis"),
    "Ctrl+D": ("analysis_toolbar.reset_solution_action", "Reset the solution"),
    "F5": ("update_plots", "Refresh the plots"),
    "Alt+P": ("action_toggle_section_plane_callback", "Toggle the section plane"),

    # workspaces
    "Q": ("use_geometry_workspace", "Geometry editor workspace"),
    "W": ("use_model_setup_workspace", "Model setup workspace"),
    "E": ("use_results_workspace", "Results workspace"),

    # rendering
    "Ctrl+Alt+W": ("action_toggle_wireframe_callback", "Toggle wireframe rendering"),
    "Ctrl+Alt+S": ("action_set_surface_rendering_callback", "Show solid surface rendering"),
    "R": ("action_zoom", "Reset the camera"),
    "T": ("action_show_transparent", "Toggle transparency"),
    "L": ("action_show_lines", "Toggle lines visibility"),

    # render tools
    "Ctrl+Shift+1": ("view_toolbar.action_selection_tool", "Selection tool"),
    "Ctrl+Shift+2": ("view_toolbar.action_grab_tool", "Grab tool"),
    "Ctrl+Shift+3": ("view_toolbar.action_rotation_tool", "Rotation tool"),
    "Ctrl+Shift+4": ("view_toolbar.action_zoom_tool", "Zoom tool"),

    # views
    "Ctrl+1": ("view_toolbar.action_front_view", "Front view"),
    "Ctrl+2": ("view_toolbar.action_back_view", "Back view"),
    "Ctrl+3": ("view_toolbar.action_left_view", "Left view"),
    "Ctrl+4": ("view_toolbar.action_right_view", "Right view"),
    "Ctrl+5": ("view_toolbar.action_top_view", "Top view"),
    "Ctrl+6": ("view_toolbar.action_bottom_view", "Bottom view"),
    "Ctrl+7": ("view_toolbar.action_isometric_view", "Isometric view"),

    # other
    "?": ("action_show_shortcuts_help_callback", "Show this shortcut list"),
}


def _shortcut_key_sequence(keys: str) -> QKeySequence:
    """
    Maps a registry key to the QKeySequence actually used by the QShortcut.

    Qt cannot match a literal "?" sequence against the real key event produced
    by pressing Shift+/ (the sequence object stays empty/ambiguous), so the
    registry keeps displaying "?" while the QShortcut listens for "Shift+/".
    """
    if keys == "?":
        return QKeySequence("Shift+/")
    return QKeySequence(keys)


def register_global_shortcuts(main_window):
    """
    Registers every entry of the SHORTCUTS registry as a standalone
    application-wide QShortcut, wired to a target.

    Targets that are QActions get their key sequence removed (the QShortcut
    takes its place), so Qt does not see the same sequence twice.

    The QActions themselves are never disabled, so their toolbar/menu icons
    stay enabled and visible the whole time. Only the QShortcut objects are
    toggled while the focus is in a widget that truly accepts text input, so
    keystrokes are not stolen while the user types (non-editable QComboBoxes
    are not treated as text input).

    Because the key sequences are not attached to the QActions anymore, Qt
    will no longer draw the shortcut next to a menu entry/toolbar button by
    itself. Use the SHORTCUTS registry (shown by the "?" help) to discover
    and/or display the hints in the UI as needed.
    """
    all_shortcuts = []

    for keys, (target, description) in SHORTCUTS.items():
        resolved = _resolve_target(main_window, target)
        key_sequence = _shortcut_key_sequence(keys)

        if isinstance(resolved, QAction):
            resolved.setShortcut(QKeySequence())
            shortcut = QShortcut(key_sequence, main_window)
            shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
            shortcut.activated.connect(resolved.trigger)
            all_shortcuts.append(shortcut)

        elif callable(resolved):
            shortcut = QShortcut(key_sequence, main_window)
            shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
            shortcut.activated.connect(resolved)
            all_shortcuts.append(shortcut)

        else:
            raise TypeError(f"Invalid shortcut target '{target}': {resolved!r}")

    main_window._global_shortcuts = all_shortcuts

    def update_shortcuts_enabled(old_widget, new_widget):
        typing = is_typing_input(new_widget)
        for shortcut in all_shortcuts:
            shortcut.setEnabled(not typing)

    app().focusChanged.connect(update_shortcuts_enabled)

    _label_menu_shortcuts(main_window)


def _resolve_target(main_window, dotted_path: str):
    obj = main_window
    for attribute in dotted_path.split("."):
        obj = getattr(obj, attribute)
    return obj


def _label_menu_shortcuts(main_window):
    """
    Appends each shortcut's key sequence to the text of the actions that are
    shown inside a QMenu (e.g. Project > Save, Open…). Using a tab separator
    makes Qt right-align the key in menu items, so users see "Save  Ctrl+S"
    even though the shortcut itself is held by a separate QShortcut (not by the
    action). Toolbar/button-only actions are left untouched.
    """
    menus = main_window.findChildren(QMenu)
    menu_actions = set()
    for menu in menus:
        menu_actions.update(menu.actions())

    keys_by_action = {}
    for keys, (target, description) in SHORTCUTS.items():
        action = _resolve_target(main_window, target)
        if action in menu_actions:
            keys_by_action.setdefault(action, []).append(keys)

    for action, keys in keys_by_action.items():
        base_text = action.text().split("\t")[0]
        action.setText(f"{base_text}\t{'  '.join(keys)}")


def is_focus_on_text_input() -> bool:
    return is_typing_input(app().focusWidget())
