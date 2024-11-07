import logging

from PyQt5 import QtCore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ComicLoader(QtCore.QObject):

    progress = QtCore.pyqtSignal(int)
    done = QtCore.pyqtSignal()
    initial_page = 0

    def __init__(self):
        super().__init__()
        self.data = []

    def load(self, filename):
        raise NotImplementedError("Must subclass me")
