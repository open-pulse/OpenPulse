from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen, QPainter
from PySide6.QtCore import Qt, QSize, QRect

class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def initStyleOption(self, option, index):
        super(BorderItemDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = Qt.AlignRight
        option.decorationPosition = QStyleOptionViewItem.Right

    def sizeHint(self, option, index):        
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        
        default_size = super().sizeHint(option, index)
        tree = index.model().parent()
        item = tree.itemFromIndex(index)
        if item and item.parent():
            return QSize(default_size.width(), 22)
        
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

    def paint(self, painter: QPainter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)
        
        tree = index.model().parent()
        item = tree.itemFromIndex(index) if hasattr(tree, 'itemFromIndex') else None
        if item and item.parent():
            # remove icon to not duplicate when super() is called
            original_icon  = item.icon(0)
            item.setIcon(0, QIcon())
            super(BorderItemDelegate, self).paint(painter, option, index)
            item.setIcon(0, original_icon)
            
            # draw icon
            icon = index.data(Qt.DecorationRole)
            if icon is not None:
                icon_size = option.decorationSize.width() + 2
                spacing = 5
                icon_rect = QRect(option.rect.right() - icon_size - spacing, option.rect.top() + (option.rect.height() - icon_size)//2, icon_size, icon_size)
                icon.paint(painter, icon_rect)
        else:
            super(BorderItemDelegate, self).paint(painter, option, index)