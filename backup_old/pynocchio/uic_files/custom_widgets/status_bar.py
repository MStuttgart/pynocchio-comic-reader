

from PySide6 import QtCore, QtWidgets


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)

        self.page_number = None
        self.page_resolution = None
        self.comic_path = None
        self.progress_bar = None
        self.slider = None

    def add_page_number_label(self):
        if self.page_number is None:
            self.remove_progress_bar()
            self.page_number = QtWidgets.QLabel(self)
            self.page_number.setMinimumWidth(120)
            self.addWidget(self.page_number, 0)

        self.page_number.show()

    def add_page_resolution_label(self):
        if self.page_resolution is None:
            self.remove_progress_bar()
            self.page_resolution = QtWidgets.QLabel(self)
            self.page_resolution.setMinimumWidth(140)
            self.addWidget(self.page_resolution, 1)

        self.page_resolution.show()

    def add_comic_path_label(self):
        if self.comic_path is None:
            self.remove_progress_bar()
            self.comic_path = QtWidgets.QLabel(self)
            self.addWidget(self.comic_path, 2)

        self.comic_path.show()

    def add_progress_bar(self, maximum_value=100):

        self.remove_labels()
        self.remove_slider()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setMaximum(maximum_value)
        self.progress_bar.setMaximumWidth(self.width())
        self.addWidget(self.progress_bar, 3)
        self.progress_bar.show()

    def add_slider(self):

        if self.slider is None:
            self.remove_progress_bar()
            self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
            self.slider.setFixedWidth(200)
            self.slider.setValue(50)
            self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.addWidget(self.slider, 3)

    def remove_slider(self):

        if self.slider is not None:
            self.removeWidget(self.slider)
            self.slider = None

    def remove_progress_bar(self):

        if self.progress_bar:
            self.removeWidget(self.progress_bar)
            self.progress_bar = None

    def remove_labels(self):

        if self.page_number:
            self.removeWidget(self.page_number)
            self.page_number = None

        if self.page_resolution:
            self.removeWidget(self.page_resolution)
            self.page_resolution = None

        if self.comic_path:
            self.removeWidget(self.comic_path)
            self.comic_path = None

    def set_comic_page(self, current_page, total_pages):
        if not self.page_number:
            self.add_page_number_label()

        self.page_number.setText(
            self.tr('Page: ') + str(current_page) + '/' + str(total_pages))

    def set_page_resolution(self, width, height, orig_w=None, orig_h=None):
        if not self.page_resolution:
            self.add_page_resolution_label()

        text = self.tr('Resolution: ') + str(width) + ' × ' + str(height)
        if (orig_w and orig_h and orig_w != width and orig_h != height):
            text += ' (' + str(orig_w) + ' × ' + str(orig_h) + ')'
        text += ' px'
        self.page_resolution.setText(text)

    def set_comic_path(self, path):
        if not self.comic_path:
            self.add_comic_path_label()

        self.comic_path.setText(self.tr('Title: ') + path[:50])

    @QtCore.Slot(int)
    def set_progressbar_value(self, n):
        if self.progress_bar is None:
            self.add_progress_bar()
        self.progress_bar.setValue(n)

    @QtCore.Slot()
    def close_progress_bar(self):
        self.remove_progress_bar()
        self.add_page_number_label()
        self.add_page_resolution_label()
        self.add_comic_path_label()
