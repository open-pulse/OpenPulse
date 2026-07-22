from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QIconEngine, QPainter, QPixmap, QPixmapCache
from PySide6.QtWidgets import QApplication, QStyleOption

from pulse import ICON_DIR

# Bumped whenever the active icon theme changes so cached pixmaps are dropped.
_icon_generation = 0


def invalidate_themed_icons() -> None:
    """Invalidate every ``ResourceIconEngine`` cache (call on icon theme change).

    Engines lazily clear their cache the next time they are asked for a pixmap,
    so this is a cheap O(1) operation; the actual re-read happens on the next
    repaint of each icon.
    """
    global _icon_generation
    _icon_generation += 1
    QPixmapCache.clear()


class ResourceIconEngine(QIconEngine):
    """Icon engine that follows the active icon theme.

    Unlike a plain ``QIcon(":/icons/...")``, which permanently caches the
    pixmap of the resource that was active when it was created, this engine
    re-reads the currently registered resource whenever the theme changes.
    The same ``QIcon`` therefore follows a ``set_icon_theme`` swap, with no
    need to track icon paths externally nor recreate icons by hand.

    Pixmaps are cached per size and only dropped when
    :func:`invalidate_themed_icons` bumps the global generation, so normal
    repaints/scrolling cost the same as a standard ``QIcon``; only a theme
    switch forces a re-decode. A repaint of the owning widget is still
    required for the new pixmap to be requested.
    """

    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._cache: dict[tuple[int, int, int], QPixmap] = {}
        self._generation = -1

    def _sync_generation(self) -> None:
        if self._generation != _icon_generation:
            self._cache.clear()
            self._generation = _icon_generation

    def _base_pixmap(self, size: QSize) -> QPixmap:
        """Read and scale the Normal-mode pixmap, caching it per size."""
        key = (size.width(), size.height(), QIcon.Mode.Normal.value)
        pixmap = self._cache.get(key)
        if pixmap is None:
            pixmap = QPixmap(self._path)
            if not pixmap.isNull() and pixmap.size() != size:
                pixmap = pixmap.scaled(
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            self._cache[key] = pixmap
        return pixmap

    def pixmap(self, size: QSize, mode, state) -> QPixmap:
        self._sync_generation()

        key = (size.width(), size.height(), mode.value)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        base = self._base_pixmap(size)
        if mode == QIcon.Mode.Normal or base.isNull():
            pixmap = base
        else:
            # Derive Disabled/Active/Selected appearance from the style, just
            # like the default QIcon engine does (e.g. greys out disabled).
            pixmap = QApplication.style().generatedIconPixmap(mode, base, QStyleOption())
            if pixmap.isNull():
                pixmap = base

        self._cache[key] = pixmap
        return pixmap

    def paint(self, painter: QPainter, rect, mode, state) -> None:
        painter.drawPixmap(rect, self.pixmap(rect.size(), mode, state))

    def clone(self) -> QIconEngine:
        return ResourceIconEngine(self._path)


class Icon:
    """
    Class used to instantiate new QIcons.

    It returns a QIcon instance, that manages
    the icon color independently, so we don't
    need to worry about it.

    Args:
    - path (str): a string representing the
    path to the icon in the resource file.

    Usage example:

    icon = Icon(:/folder/bla.png)
    """

    def __new__(cls, path: str = "") -> QIcon:
        return QIcon(ResourceIconEngine(path))


def get_icons_path(filename):
    path = ICON_DIR / filename
    if path.exists():
        return str(path)


def get_formatted_icon(path: Path | str, color: QColor):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


def get_openpulse_icon(color=QColor("#0055DD")):
    icon_path = str(ICON_DIR / "pulse/pulse_icon.png")
    # return get_formatted_icon(icon_path, color)
    return QIcon(icon_path)


def get_warning_icon(color=None):
    if color is None:
        icon_path = str(ICON_DIR / "warnings/warning_2.png")
        return QIcon(icon_path)
    else:
        icon_path = str(ICON_DIR / "warnings/transparent_warning.png")
        return get_formatted_icon(icon_path, color)


def get_error_icon(color=None):
    if color is None:
        icon_path = str(ICON_DIR / "warnings/warning_2.png")
        return QIcon(icon_path)
    else:
        icon_path = str(ICON_DIR / "warnings/transparent_warning.png")
        return get_formatted_icon(icon_path, color)


def change_icon_color(icon: QIcon, size: QSize, color: QColor):
    if icon is None or icon.isNull():
        return None

    pixmap = icon.pixmap(size)
    if pixmap.isNull():
        return None

    painter = QPainter(pixmap)
    if not painter.isActive():
        return None

    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


def change_icon_color_for_widgets(widgets, color: QColor):
    for widget in widgets:
        if not hasattr(widget, "icon") or not callable(widget.icon):
            continue

        if not hasattr(widget, "setIcon") or not callable(widget.setIcon):
            continue

        if hasattr(widget, "should_paint") and not widget.should_paint:
            continue

        icon = widget.icon()
        size = widget.iconSize() if hasattr(widget, "iconSize") else icon.actualSize(QSize(256, 256))
        new_icon = change_icon_color(icon, size, color)
        if new_icon is not None:
            widget.setIcon(new_icon)
