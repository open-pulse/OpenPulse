"""Register the compiled Qt icon resources for one theme at a time.
"""

from pulse.interface.data.icons.dark_theme import resources_rc as _dark_rc
from pulse.interface.data.icons.light_theme import resources_rc as _light_rc
from pulse.interface.formatters.icons import invalidate_themed_icons

_THEME_RESOURCES = {
    "dark": _dark_rc,
    "light": _light_rc,
}

DEFAULT_THEME = "dark"

_active_theme: str | None = None


def set_icon_theme(theme: str) -> None:
    """Register the icon resources for ``theme`` and unregister all others."""
    global _active_theme

    if theme not in _THEME_RESOURCES:
        raise ValueError(
            f"Unknown icon theme {theme!r}; expected one of {list(_THEME_RESOURCES)}."
        )

    if theme == _active_theme:
        return

    for resources in _THEME_RESOURCES.values():
        resources.qCleanupResources()

    _THEME_RESOURCES[theme].qInitResources()
    _active_theme = theme
    
    invalidate_themed_icons()


set_icon_theme(DEFAULT_THEME)