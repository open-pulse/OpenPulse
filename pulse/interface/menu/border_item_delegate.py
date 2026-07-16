from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtCore import Qt, QSize

class BorderItemDelegate(QStyledItemDelegate):
    MULTI_ICON_ROLE = Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def initStyleOption(self, option, index):
        super(BorderItemDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = Qt.AlignmentFlag.AlignRight
        option.decorationPosition = QStyleOptionViewItem.Position.Right
        option.icon = QIcon()  # prevent base paint from drawing the icon; drawn manually in paint()

    def sizeHint(self, option, index):        
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        if pen is not None:        
            # Make some room for the border
            # When width is 0, it is a cosmetic pen which
            # will be 1 pixel anyways, so set it to 1
            width = max(pen.width(), 1)            
            size = size + QSize(2 * width, 2 * width)
        return size
    
    def size(self, item):
        separator_size = QSize()
        separator_size.setHeight(2)
        return item.setSizeHint(0, separator_size)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        super().paint(painter, option, index)

        multi_icons: list = index.data(self.MULTI_ICON_ROLE)

        if multi_icons:
            icon_side = max(1, min(16, option.rect.height() - 4))
            icon_size = QSize(icon_side, icon_side)
            spacing = 4
            margin = 8
            x = option.rect.right() - margin
            y = option.rect.top() + (option.rect.height() - icon_size.height()) // 2
            for icon in reversed(multi_icons):
                if icon and not icon.isNull():
                    x -= icon_size.width()
                    pixmap = icon.pixmap(icon_size, QIcon.Mode.Normal, QIcon.State.On)
                    painter.drawPixmap(x, y, pixmap)
                    x -= spacing
            painter.restore()
            return

        original_icon: QIcon = index.data(Qt.ItemDataRole.DecorationRole)
        if original_icon and not original_icon.isNull():
            new_icon_size = QSize(20, 20)
            scaled_pixmap: QPixmap = original_icon.pixmap(new_icon_size, QIcon.Mode.Normal, QIcon.State.On)
            
            x_offset = option.rect.left()
            x_offset += option.rect.width() - 32
            y_offset = option.rect.top() + (option.rect.height() - new_icon_size.height()) // 2

            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)

        painter.restore()
