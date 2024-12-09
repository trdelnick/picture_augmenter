from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class ColorDelegate(QStyledItemDelegate):
    def __init__(self, selected_inodes: set, parent=None):
        super().__init__(parent)
        self.selected_inodes = selected_inodes
        self.base_color = QColor(100, 200, 0, 100)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):

        path: str = index.model().filePath(index)
        if path.endswith("/"):
            path = path[:-1]

        if path in self.selected_inodes:
            painter.fillRect(option.rect, QBrush(self.base_color))
            super().paint(painter, option, index)
            return

        painter.fillRect(option.rect, QBrush(Qt.NoBrush))
        super().paint(painter, option, index)