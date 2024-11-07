import logging

from PyQt5 import QtCore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SettingsManager:

    def __init__(self):
        self.settings = QtCore.QSettings("Pynocchio", "Pynocchio")

    def save_recent_files(self, recent_files_list):
        logger.info("Saving recent files")

        self.settings.beginWriteArray("recent_file_list")

        for idx, value in enumerate(recent_files_list):
            self.settings.setArrayIndex(idx)
            self.settings.setValue("recent_file", value)

        self.settings.endArray()

    def load_recent_files(self):
        logger.info("Loading recent files")

        recent_files_list = []
        size = self.settings.beginReadArray("recent_file_list")

        for idx in range(size):
            self.settings.setArrayIndex(idx)
            recent_files_list.append(self.settings.value("recent_file"))

        self.settings.endArray()
        return recent_files_list

    def save_view_adjust(self, object_name):
        logger.info("Saving view adjust: %s", object_name)
        self.settings.setValue("view_adjust", object_name)

    def load_view_adjust(self, default_object_name):
        logger.info("Loading view adjust")
        return self.settings.value("view_adjust", default_object_name)

    def save_current_directory(self, current_directory):
        logger.info("Saving current directory %s", current_directory)
        self.settings.setValue("current_directory", current_directory)

    def load_current_directory(self):
        logger.info("Loading current directory")
        return self.settings.value("current_directory", ".")

    def save_window(self, window):
        logger.info("Saving window geometry and state")
        self.settings.setValue("window_size", window.size())
        self.settings.setValue("window_position", window.pos())
        self.settings.setValue("window_state", window.saveState())

    def load_window_size(self, default):
        logger.info("Loading window size")
        return self.settings.value("window_size", default)

    def load_window_position(self, default):
        logger.info("Loading window position")
        return self.settings.value("window_position", default)

    def load_window_state(self):
        logger.info("Loading window state")
        return self.settings.value("window_state")

    def save_toggles(self, ui):
        logger.info("Saving togglable settings")
        self.settings.setValue("show_toolbar", ui.action_show_toolbar.isChecked())
        self.settings.setValue("show_statusbar", ui.action_show_statusbar.isChecked())
        self.settings.setValue("show_thumbnails", ui.action_show_thumbnails.isChecked())
        self.settings.setValue("shrink_only", ui.action_shrink_only.isChecked())
        self.settings.setValue("page_across_files", ui.action_page_across_files.isChecked())
        self.settings.setValue("dark_style", ui.action_dark_style.isChecked())

    def load_toggles(self):
        logger.info("Loading togglable settings")
        return {
            "show_toolbar": self.settings.value("show_toolbar", True, type=bool),
            "show_statusbar": self.settings.value("show_statusbar", True, type=bool),
            "show_thumbnails": self.settings.value("show_thumbnails", True, type=bool),
            "shrink_only": self.settings.value("shrink_only", False, type=bool),
            "page_across_files": self.settings.value("page_across_files", True, type=bool),
            "dark_style": self.settings.value("dark_style", True, type=bool),
        }
