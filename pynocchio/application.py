# Copyright
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import platform
import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator, QUrl, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from pynocchio.utility import COMPACT_FILE_FORMATS, IMAGE_FILE_FORMATS, file_exist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PynocchioApplication(QGuiApplication):

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()
        self._translator_pynocchio = QTranslator()
        self._translator_qt = QTranslator()

        QQuickStyle.setStyle("Material")

    def set_window_icon(self):
        icon = QIcon(":/data/app-icon.svg")
        self.setWindowIcon(icon)

    def set_up_signals(self):
        self.aboutToQuit.connect(self._on_quit)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _on_quit(self) -> None:
        del self._engine

    def _retranslate(self):
        locale = QLocale(self._engine.uiLanguage())

        self.removeTranslator(self._translator_qt)
        self.removeTranslator(self._translator_pynocchio)

        self._translator_qt.load(locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self._translator_pynocchio.load(f":/i18n/{locale.name()}.qm")

        self.installTranslator(self._translator_qt)
        self.installTranslator(self._translator_pynocchio)

        self.setLayoutDirection(locale.textDirection())

    def set_up_imports(self):
        self._engine.addImportPath(":/qml")

    def set_up_window_event_filter(self):

        if platform.system() == "Windows":
            from pynocchio.framelesswindow.win import WindowsEventFilter

            self._event_filter = WindowsEventFilter(border_width=5)
            self.installNativeEventFilter(self._event_filter)

        elif platform.system() == "Linux":
            from pynocchio.framelesswindow.linux import LinuxEventFilter

            self._event_filter = LinuxEventFilter(border_width=5)
            self.installEventFilter(self._event_filter)

    def start_engine(self):
        self._engine.load(QUrl.fromLocalFile(":/qml/main.qml"))

    def set_up_window_effects(self):
        if sys.platform == "win32":
            hwnd = self.topLevelWindows()[0].winId()
            from pynocchio.framelesswindow.win import WindowsWindowEffect

            self._effects = WindowsWindowEffect()
            self._effects.addShadowEffect(hwnd)
            self._effects.addWindowAnimation(hwnd)

    def verify(self):
        if not self._engine.rootObjects():
            sys.exit(-1)

    def on_action_open_file(self, comic_path):

        if comic_path:
            logger.info("Opening file %s", comic_path)

            # initial_page = self.get_page_from_temporary_bookmarks(filename[0])

            # self.open_comics(filename[0], initial_page)
