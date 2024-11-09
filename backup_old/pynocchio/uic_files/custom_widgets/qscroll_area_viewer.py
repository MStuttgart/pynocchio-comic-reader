

from PySide6 import QtCore, QtWidgets


class QScrollAreaViewer(QtWidgets.QScrollArea):

    resized = QtCore.Signal()

    def __init__(self, parent=None):
        super(QScrollAreaViewer, self).__init__(parent)
        self.drag_mouse = False
        self.drag_position = {'x': 0, 'y': 0}
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setWidgetResizable(True)

    def reset_scroll_position(self):
        self.verticalScrollBar().setValue(0)

    def change_background_color(self, color):
        style = "QWidget { background-color: %s }" % color.name()
        self.setStyleSheet(style)

    def mousePressEvent(self, *args, **kwargs):
        self.drag_mouse = True
        self.drag_position['x'] = args[0].x()
        self.drag_position['y'] = args[0].y()
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        super(QScrollAreaViewer, self).mousePressEvent(*args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.drag_mouse = False
        self.setCursor(QtCore.Qt.OpenHandCursor)
        super(QScrollAreaViewer, self).mouseReleaseEvent(*args, **kwargs)

    def mouseMoveEvent(self, *args, **kwargs):

        if self.drag_mouse:
            pos = args[0]

            scroll_position = {
                'x': self.horizontalScrollBar().sliderPosition(),
                'y': self.verticalScrollBar().sliderPosition()
            }

            new_x = scroll_position['x'] + self.drag_position['x'] - pos.x()
            new_y = scroll_position['y'] + self.drag_position['y'] - pos.y()

            self.horizontalScrollBar().setSliderPosition(new_x)
            self.verticalScrollBar().setSliderPosition(new_y)

            self.drag_position['x'] = pos.x()
            self.drag_position['y'] = pos.y()

        super(QScrollAreaViewer, self).mouseMoveEvent(*args, **kwargs)

    def resizeEvent(self, event):
        self.resized.emit()
        super(QScrollAreaViewer, self).resizeEvent(event)
