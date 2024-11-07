import os

from PyQt5 import QtGui


class Comic:
    """This is basic class of Pynocchio. Represents a comic object"""

    def __init__(self, name, path):
        """
        Comic class __init__ method

        Args:
            name (str): comic name
            path (str): comic file path
        """
        self.name = name
        self._path = path

        # list of Page: list to store the comic pages objects
        self.pages = []

    @property
    def path(self):
        """Get complete comic path, i.g. comic path concatenated with
                     comic name.

        Returns:
            str: The return value. Represents complete comic path.
        """
        return os.path.join(self._path, self.name)

    @path.setter
    def path(self, value):
        self._path = value


class Page:
    """This is basic class of Pynocchio. Represents a comic page object"""

    def __init__(self, data, title, number):
        """
        Comic Page class __init__ method

        Args:
            data (bin): comic page binary data
            title (str): page title
            number (int): page number
        """
        self.data = data
        self.title = title
        self.number = number
        self._pixmap = None

    @property
    def pixmap(self):

        if not self._pixmap:
            self._pixmap = QtGui.QPixmap()
            self._pixmap.loadFromData(self.data)

        return self._pixmap
