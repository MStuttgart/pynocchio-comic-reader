# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtCore, QtWidgets

from .main_window_model import MainWindowModel
from .main_window_view import MainWindowView

import qdarkgraystyle

DATADIRS = (
        os.path.abspath('./pynocchio'),
        '/usr/share/pynocchio',
        '/usr/local/share/pynocchio',
        os.path.join(QtCore.QDir.homePath(), '.local/share/pynocchio'),
    )

QLocale = QtCore.QLocale
QLibraryInfo = QtCore.QLibraryInfo
QTranslator = QtCore.QTranslator
QFileInfo = QtCore.QFileInfo
QFile = QtCore.QFile


class Pynocchio(QtWidgets.QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.setOrganizationName('Pynocchio')
        self.setApplicationName('Pynocchio')

        self.setStyle('Fusion')
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        if hasattr(self, 'setApplicationDisplayName'):
            self.setApplicationDisplayName('Pynocchio')

        for path in DATADIRS:
            self.addLibraryPath(path)

        translator = QTranslator(self)
        language = QLocale.system().uiLanguages()[0] + '.qm'

        for path in DATADIRS:
            if translator.load(language, os.path.join(path, 'locale')):
                break
        qt_translator = QTranslator(self)
        qt_translator.load('qt_' + QLocale.system().name(),
                           QLibraryInfo.location(
                               QLibraryInfo.TranslationsPath))
        self.installTranslator(translator)
        self.installTranslator(qt_translator)

        self.model = MainWindowModel()
        self.view = MainWindowView(self.model)

    def run(self):

        self.view.show()

        if len(sys.argv) > 1:
            filename = ''
            for s in sys.argv[1:]:
                filename += s

            filename = filename.replace('\\', ' ')

            if os.path.isfile(filename):
                self.view.open_comics(filename)

        sys.exit(self.exec_())
