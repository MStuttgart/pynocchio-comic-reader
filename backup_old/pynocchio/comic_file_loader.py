import logging

from PySide6 import QtCore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ComicLoader(QtCore.QObject):

    progress = QtCore.Signal()
    done = QtCore.Signal()

    initial_page = 0

    def __init__(self):
        super().__init__()
        self.data = []

    def load(self, filename):
        raise NotImplementedError("Must subclass me")
