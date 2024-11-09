import logging

from PyQt5 import QtCore, QtGui

from .bookmark import Bookmark, TemporaryBookmark
from .bookmark_database_manager import BookmarkManager
from .comic import Comic
from .comic_file_loader_factory import ComicLoaderFactory
from .comic_page_handler import ComicPageHandlerDoublePage
from .comic_page_handler_factory import ComicPageHandlerFactory
from .comic_path_filter import ComicPathFilter
from .exception import NoDataFindException
from .settings_manager import SettingsManager
from .utility import get_base_name, get_dir_name, is_dir, is_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MainWindowModel(QtCore.QObject):
    _ORIGINAL_FIT = "action_original_fit"
    _VERTICAL_FIT = "action_vertical_fit"
    _HORIZONTAL_FIT = "action_horizontal_fit"
    _BEST_FIT = "action_best_fit"
    _PAGE_FIT = "action_page_fit"

    load_progress = QtCore.pyqtSignal(int)
    load_done = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.comic = None
        self.comic_page_handler = None
        self.settings_manager = SettingsManager()
        self.rotate_angle = 0
        self.scroll_area_size = None
        self.scroll_bar_size = None
        self.fit_type = self.load_view_adjust(MainWindowModel._ORIGINAL_FIT)
        self.resize_always = True
        self.current_directory = self.load_current_directory()

        ext_list = ["*.cbr", "*.cbz", "*.rar", "*.zip", "*.tar", "*.cbt"]

        self.comic_file_filter = ComicPathFilter(ext_list)

    def save_recent_files(self, recent_files_list):
        self.settings_manager.save_recent_files(recent_files_list)

    def load_recent_files(self):
        return self.settings_manager.load_recent_files()

    def load_view_adjust(self, default_object_name):
        return self.settings_manager.load_view_adjust(default_object_name)

    def load_current_directory(self):
        return self.settings_manager.load_current_directory()

    def load(self, filename, initial_page=None):
        logger.info("Loading %s at %i", filename, 0 if initial_page is None else initial_page)

        loader = ComicLoaderFactory.create_loader(filename)
        loader.progress.connect(self.load_progressbar_value)

        try:
            loader.load(filename)
        except NoDataFindException as exc:
            from pynocchio.comic import Page

            logger.exception("Error in load comic! %s", exc)
            q_file = QtCore.QFile(":/icons/not_cover.png")
            q_file.open(QtCore.QIODevice.ReadOnly)
            loader.data.append(Page(q_file.readAll(), "exit_red_1.png", 0))

        page = initial_page if initial_page is not None else loader.initial_page

        # Memorize last page on comic
        if self.comic:
            if not self.is_first_page() and not self.is_last_page():
                self.add_bookmark(table=TemporaryBookmark)
            else:
                self.remove_bookmark(table=TemporaryBookmark)

        self.comic = Comic(get_base_name(filename), get_dir_name(filename))

        self.comic.pages = loader.data
        self.comic_page_handler = ComicPageHandlerFactory.create_handler(False, self.comic, index=page)
        self.current_directory = get_dir_name(filename)

        if is_dir(filename) or type(loader).__name__ == "ComicImageLoader":
            self.comic_file_filter.parse(filename, isdir=True)
        elif is_file(filename):
            self.comic_file_filter.parse(self.current_directory)

    def save_current_page_image(self, file_name):
        self.get_current_page().save(file_name)

    def next_page(self):
        return self.comic_page_handler.go_next_page()

    def previous_page(self):
        return self.comic_page_handler.go_previous_page()

    def first_page(self):
        self.comic_page_handler.go_first_page()

    def last_page(self):
        self.comic_page_handler.go_last_page()

    def previous_comic(self):
        return self.comic_file_filter.get_previous_comic(self.comic.name)

    def next_comic(self):
        return self.comic_file_filter.get_next_comic(self.comic.name)

    def rotate_left(self):
        self.rotate_angle = (self.rotate_angle - 90) % 360

    def rotate_right(self):
        self.rotate_angle = (self.rotate_angle + 90) % 360

    def get_comic_name(self):
        return self.comic.name

    def get_comic_path(self):
        return self.comic.path

    def get_comic_title(self):
        return self.comic.name

    def get_current_page(self):
        try:
            pix_map = self.comic_page_handler.get_current_page_image()
        except AttributeError:
            return None
        else:
            pix_map = self._rotate_page(pix_map)
            pix_map = self._resize_page(pix_map)
            return pix_map

    def get_current_page_title(self):
        return self.comic_page_handler.get_current_page().title

    def set_current_page_index(self, idx):
        self.comic_page_handler.current_page_index = idx

    def get_current_page_index(self):
        return self.comic_page_handler.current_page_index

    def get_current_page_number(self):
        return self.comic_page_handler.get_current_page().number

    def get_number_of_pages(self):
        return len(self.comic.pages)

    def is_first_page(self):
        return self.comic_page_handler.current_page_index == 0

    def is_last_page(self):
        return self.comic_page_handler.current_page_index + 1 == len(self.comic.pages)

    def is_first_comic(self):
        return self.comic_file_filter.is_first_comic(self.comic.name)

    def is_last_comic(self):
        return self.comic_file_filter.is_last_comic(self.comic.name)

    def _rotate_page(self, pix_map):
        if self.rotate_angle != 0:
            trans = QtGui.QTransform().rotate(self.rotate_angle)
            pix_map = QtGui.QPixmap(pix_map.transformed(trans))
        return pix_map

    def _resize_page(self, pix_map):

        width = pix_map.width()
        height = pix_map.height()

        h = self.scroll_area_size.height()
        w = self.scroll_area_size.width()

        if self.fit_type == MainWindowModel._VERTICAL_FIT:

            try:

                f = h / height

                if int(f * width) > w:
                    h -= self.scroll_bar_size
                    f = h / height
                    if int(f * width) < w:
                        f = w / width
                        h = int(f * height)

                if self.resize_always or h < height:
                    pix_map = pix_map.scaledToHeight(int(h), QtCore.Qt.SmoothTransformation)

            except ZeroDivisionError as exec:
                logging.info(exec)

        elif self.fit_type == MainWindowModel._HORIZONTAL_FIT:

            try:

                f = w / width

                if int(f * height) > h:
                    w -= self.scroll_bar_size
                    f = w / width
                    if int(f * height) < h:
                        f = h / height
                        w = int(f * width)

                if self.resize_always or w < width:
                    pix_map = pix_map.scaledToWidth(int(w), QtCore.Qt.SmoothTransformation)

            except ZeroDivisionError as exec:
                logging.info(exec)

        elif self.fit_type == MainWindowModel._BEST_FIT:
            w *= 0.8

            if self.resize_always or w < width:
                pix_map = pix_map.scaledToWidth(int(w), QtCore.Qt.SmoothTransformation)

        elif self.fit_type == MainWindowModel._PAGE_FIT and (self.resize_always or w < width or h < height):
            pix_map = pix_map.scaled(int(w), int(h), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        pix_map.original_width = width
        pix_map.original_height = height

        return pix_map

    def original_fit(self):
        self.fit_type = MainWindowModel._ORIGINAL_FIT

    def vertical_fit(self):
        self.fit_type = MainWindowModel._VERTICAL_FIT

    def horizontal_fit(self):
        self.fit_type = MainWindowModel._HORIZONTAL_FIT

    def best_fit(self):
        self.fit_type = MainWindowModel._BEST_FIT

    def page_fit(self):
        self.fit_type = MainWindowModel._PAGE_FIT

    def double_page_mode(self, checked):
        index = self.comic_page_handler.current_page_index
        self.comic_page_handler = ComicPageHandlerFactory.create_handler(checked, self.comic, index=index)

    def manga_page_mode(self, checked):
        if isinstance(self.comic_page_handler, ComicPageHandlerDoublePage):
            self.comic_page_handler.inverse = checked

    @QtCore.pyqtSlot(int)
    def load_progressbar_value(self, percent):
        self.load_progress.emit(percent)

    @QtCore.pyqtSlot()
    def load_progressbar_done(self):
        self.load_done.emit()

    def save_settings(self):
        self.settings_manager.save_toggles(self.parent.ui)
        self.settings_manager.save_window(self.parent)
        self.settings_manager.save_view_adjust(self.fit_type)
        self.settings_manager.save_current_directory(self.current_directory)

    @staticmethod
    def get_bookmark_list(qty):
        return BookmarkManager.get_bookmarks(qty)

    def is_bookmark(self):
        return BookmarkManager.is_bookmark(self.comic.path)

    @staticmethod
    def get_bookmark_from_path(path, table=Bookmark):
        return BookmarkManager.get_bookmark_by_path(path, table=table)

    def add_bookmark(self, table=Bookmark):

        if self.comic:
            BookmarkManager.add_bookmark(
                self.comic.name,
                self.comic.path,
                self.comic_page_handler.get_current_page().number,
                data=self.comic_page_handler.get_current_page().data,
                table=table,
            )

    def remove_bookmark(self, path=False, table=Bookmark):
        path = self.comic.path if not path else path
        BookmarkManager.remove_bookmark(path, table=table)

    def load_window(self, size, position):
        return (
            self.settings_manager.load_window_size(size),
            self.settings_manager.load_window_position(position),
            self.settings_manager.load_window_state(),
        )

    def load_toggles(self):
        return self.settings_manager.load_toggles()
