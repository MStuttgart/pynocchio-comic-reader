from PySide6 import QtGui, QtWidgets


class ColorLine(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(ColorLine, self).__init__(parent=parent)
        self.background_color = QtGui.QColor()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.fillRect(0, 0, self.width(), self.height(), self.background_color)
        p.end()
        e.accept()

    def reset_background_color(self):
        self.background_color = QtGui.QColor()
