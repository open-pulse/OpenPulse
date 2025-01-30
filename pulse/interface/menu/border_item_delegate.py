from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
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

    def paint(self, painter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)

        if pen is not None:
            width = max(pen.width(), 1)
            # ...and remove the extra room we added in sizeHint...
            option.rect.adjust(width, width, -width, -width)      

        super(BorderItemDelegate, self).paint(painter, option, index)

        if pen is not None:
            painter.save() # Saves previous status
            
            # Align rect 
            painter.setClipRect(rect, Qt.ReplaceClip);          
            pen.setWidth(2 * width)

            # Paint the borders
            painter.setPen(pen)
            painter.drawRect(rect)     
            
            painter.restore() # Recovers previous status