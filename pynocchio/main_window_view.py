# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import logging

from .utility import IMAGE_FILE_FORMATS
from .exception import InvalidTypeFileException
from .exception import LoadComicsException
from .exception import NoDataFindException
from .utility import file_exist
from .go_to_page_dialog import GoToDialog
from .bookmark_manager_dialog import BookmarkManagerDialog
from .bookmark import TemporaryBookmark
from .about_dialog import AboutDialog
from .not_found_dialog import NotFoundDialog
from .uic_files import main_window_view_ui

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindowView(QtWidgets.QMainWindow):

    MAX_RECENT_FILES = 5
    MAX_BOOKMARK_FILES = 5

    def __init__(self, model, parent=None):
        super(MainWindowView, self).__init__(parent=parent)
        self.model = model

        self.ui = main_window_view_ui.Ui_MainWindowView()
        self.ui.setupUi(self)

        MainWindowView.MAX_RECENT_FILES = len(
            self.ui.menu_recent_files.actions())

        MainWindowView.MAX_BOOKMARK_FILES = \
            len(self.ui.menu_recent_bookmarks.actions())

        self.ui.menu_recent_files.menuAction().setVisible(False)

        self.global_shortcuts = self._define_global_shortcuts()
        self.create_connections()
        self.centralize_window()

        self.update_recent_file_actions()

        self.model.load_progress.connect(
            self.ui.statusbar.set_progressbar_value)

        self.vertical_animation = QtCore.QPropertyAnimation(
            self.ui.qscroll_area_viewer.verticalScrollBar())

        self.last_scroll_position = 0

    @QtCore.pyqtSlot()
    def on_action_open_file_triggered(self):
        img_formats = ''

        for img in IMAGE_FILE_FORMATS:
            img_formats += ' *' + img

        all_files = '*.zip *.cbz *.rar *.cbr *.tar *.cbt' + img_formats

        filename = QtWidgets.QFileDialog().getOpenFileName(
            self, self.tr('open_comic_file'),
            self.model.current_directory,
            self.tr(
                'all_supported_files (%s);; '
                'zip_files (*.zip *.cbz);; rar_files (*.rar *.cbr);; '
                'tar_files (*.tar *.cbt);; image_files (%s);;'
                'all_files (*)' % (all_files, img_formats)))

        if filename:
            logger.info('Opening file')

            initial_page = self.get_page_from_temporary_bookmarks(filename[0])

            self.open_comics(filename[0], initial_page)

    @QtCore.pyqtSlot()
    def on_action_save_image_triggered(self):

        if self.model.comic:

            path = self.model.current_directory + \
                   self.model.get_current_page_title()
            file_path = QtWidgets.QFileDialog().getSaveFileName(
                self, self.tr('save_current_page'), path,
                self.tr("images (*.png *.xpm *.jpeg *.jpg *.gif)"))

            if file_path:
                logger.info('Saving image')
                self.model.save_current_page_image(file_path[0])

    @QtCore.pyqtSlot()
    def on_action_previous_page_triggered(self):
        if self.model.previous_page():
            self.update_viewer_content()
            self.update_navegation_actions()
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            vert_scroll_bar.setValue(self.last_scroll_position)
        else:
            self.on_action_previous_comic_triggered()
            self.on_action_last_page_triggered()

    @QtCore.pyqtSlot()
    def on_action_next_page_triggered(self):
        if self.model.next_page():
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            self.last_scroll_position = vert_scroll_bar.sliderPosition()
            self.update_viewer_content()
            self.update_navegation_actions()
        else:
            self.on_action_next_comic_triggered()

    @QtCore.pyqtSlot()
    def on_action_first_page_triggered(self):
        self.model.first_page()
        self.update_viewer_content()
        self.update_navegation_actions()

    @QtCore.pyqtSlot()
    def on_action_last_page_triggered(self):
        self.model.last_page()
        self.update_viewer_content()
        self.update_navegation_actions()

    @QtCore.pyqtSlot()
    def on_action_previous_comic_triggered(self):
        try:
            self.open_comics(self.model.previous_comic())
        except NoDataFindException as exc:
            logger.exception(exc.message)

        self.update_navegation_actions()

    @QtCore.pyqtSlot()
    def on_action_next_comic_triggered(self):
        try:
            self.open_comics(self.model.next_comic())
        except NoDataFindException as exc:
            logger.exception(exc.message)

        self.update_navegation_actions()

    @QtCore.pyqtSlot()
    def on_action_rotate_left_triggered(self):
        self.model.rotate_left()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_rotate_right_triggered(self):
        self.model.rotate_right()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_go_to_page_triggered(self):
        go_to_dlg = GoToDialog(self.model.comic_page_handler, parent=self)
        go_to_dlg.show()
        ret = go_to_dlg.exec_()

        if ret == QtWidgets.QDialog.Accepted:
            self.model.set_current_page_index(
                go_to_dlg.handler.current_page_index)
            self.update_viewer_content()
            self.update_navegation_actions()

    @QtCore.pyqtSlot()
    def on_action_add_bookmark_triggered(self):
        self.model.add_bookmark()
        self.update_bookmark_actions()

    @QtCore.pyqtSlot()
    def on_action_remove_bookmark_triggered(self):
        self.model.remove_bookmark(self.model.get_comic_path())
        self.update_bookmark_actions()

    @QtCore.pyqtSlot()
    def on_action_bookmark_manager_triggered(self):
        bookmark_dialog = BookmarkManagerDialog(self, parent=self)
        bookmark_dialog.show()
        bookmark_dialog.exec_()

    @QtCore.pyqtSlot()
    def on_action_preference_dialog_triggered(self):
        pass

    @QtCore.pyqtSlot()
    def on_action_original_fit_triggered(self):
        self.model.original_fit()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_vertical_fit_triggered(self):
        self.model.vertical_fit()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_horizontal_fit_triggered(self):
        self.model.horizontal_fit()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_best_fit_triggered(self):
        self.model.best_fit()
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_fullscreen_triggered(self):

        if self.isFullScreen():
            self.ui.menubar.show()
            self.ui.toolbar.show()
            self.ui.statusbar.show()
            self.showMaximized()

            for sc in self.global_shortcuts:
                sc.setEnabled(False)
        else:
            self.ui.menubar.hide()
            self.ui.toolbar.hide()
            self.ui.statusbar.hide()
            self.showFullScreen()
            for sc in self.global_shortcuts:
                sc.setEnabled(True)

    @QtCore.pyqtSlot(bool)
    def on_action_double_page_mode_triggered(self, checked):
        self.model.double_page_mode(checked)
        self.update_viewer_content()
        self.ui.action_manga_mode.setEnabled(checked)

    @QtCore.pyqtSlot(bool)
    def on_action_manga_mode_triggered(self, checked):
        self.model.manga_page_mode(checked)
        self.update_viewer_content()

    @QtCore.pyqtSlot()
    def on_action_show_toolbar_triggered(self):
        if self.ui.action_show_toolbar.isChecked():
            self.ui.toolbar.show()
        else:
            self.ui.toolbar.hide()

    @QtCore.pyqtSlot()
    def on_action_show_statusbar_triggered(self):
        if self.ui.action_show_statusbar.isChecked():
            self.ui.statusbar.show()
        else:
            self.ui.statusbar.hide()

    @QtCore.pyqtSlot()
    def on_action_about_triggered(self):
        ab_dlg = AboutDialog(self)
        ab_dlg.show()
        ab_dlg.exec_()

    @QtCore.pyqtSlot()
    def on_action_about_qt_triggered(self):
        QtWidgets.QMessageBox().aboutQt(self, self.tr('About Qt'))

    @QtCore.pyqtSlot()
    def on_action_exit_triggered(self):
        super(MainWindowView, self).close()
        self.model.save_settings()

        try:
            if not self.model.is_first_page() and not self.model.is_last_page():  # noqa: 501
                self.model.add_bookmark(table=TemporaryBookmark)
            else:
                self.model.remove_bookmark(table=TemporaryBookmark)
        except AttributeError as exc:
            logger.warning(exc)

    def create_connections(self):

        # Define group to action fit items and load fit of settings file
        self.ui.action_group_view = QtWidgets.QActionGroup(self)

        self.ui.action_group_view.addAction(self.ui.action_original_fit)
        self.ui.action_group_view.addAction(self.ui.action_vertical_fit)
        self.ui.action_group_view.addAction(self.ui.action_horizontal_fit)
        self.ui.action_group_view.addAction(self.ui.action_best_fit)

        view_adjust = self.model.load_view_adjust(
            self.ui.action_group_view.checkedAction().objectName())

        # Define that action fit is checked
        for act in self.ui.action_group_view.actions():
            if act.objectName() == view_adjust:
                act.setChecked(True)
                self.model.fit_type = act.objectName()

        # Connect recent file menu
        for act in self.ui.menu_recent_files.actions():
            act.triggered.connect(self.open_recent_file)

        # Connect recent bookmark menu
        for act in self.ui.menu_recent_bookmarks.actions():
            act.triggered.connect(self.open_recent_bookmark)

        # update recent bookmark menu when mouse hover
        self.ui.menu_recent_bookmarks.aboutToShow.connect(
            self.update_recent_bookmarks_menu)

    def _define_global_shortcuts(self):

        shortcuts = []

        sequence = {
            'Ctrl+Shift+Left': self.on_action_previous_comic_triggered,
            'Ctrl+Left': self.on_action_first_page_triggered,
            'Left': self.on_action_previous_page_triggered,
            'Right': self.on_action_next_page_triggered,
            'Ctrl+Right': self.on_action_last_page_triggered,
            'Ctrl+Shift+Right': self.on_action_next_comic_triggered,
            'Ctrl+R': self.on_action_rotate_left_triggered,
            'Ctrl+Shift+R': self.on_action_rotate_right_triggered,
        }

        for key, value in list(sequence.items()):
            s = QtWidgets.QShortcut(QtGui.QKeySequence(key),
                                    self.ui.qscroll_area_viewer, value)
            s.setEnabled(False)
            shortcuts.append(s)

        return shortcuts

    def get_page_from_temporary_bookmarks(self, path):

        bk = self.model.get_bookmark_from_path(path=path,
                                               table=TemporaryBookmark)
        initial_page = 0

        if bk:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(self.tr(
                'Continue reading from page %d?' % bk.comic_page))
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText(self.tr('<p>You stopped reading here.</p>'
                                '<p> If you choose <b>"Yes"</b>, reading will '
                                'resume on <b>page %d</b>. </p>'
                                '<p>Otherwise, the first page will be '
                                'loaded.</p>'
                                % bk.comic_page))
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            q = QtGui.QPixmap()
            q.loadFromData(bk.page_data)
            q = q.scaledToWidth(msg.width() * 0.2,
                                QtCore.Qt.SmoothTransformation)
            msg.setIconPixmap(q)

            option = msg.exec_()

            if option == QtWidgets.QMessageBox.Ok:
                initial_page = bk.comic_page - 1

        return initial_page

    def open_comics(self, filename, initial_page=0):
        if filename:
            logger.info('Opening comic %s' % filename)

            try:

                # Load comic
                self.model.load(filename, initial_page)

                # Update label and scroll_area_viewer
                self.update_viewer_content()

                # set window title
                self.setWindowTitle(self.model.get_comic_title())

                # Enable window actions
                self.enable_actions()

                # Update status bar data
                self.update_status_bar()

                # Add this comic like recent file
                self.set_current_file(filename)

                # Update status of add and remove bookmark buttons
                self.update_bookmark_actions()

                # Update next page, previous page, next and previous comics
                # actions
                self.update_navegation_actions()

                # Register view like listener of ComicPageHandler events
                # self.model.comic_page_handler.listener.append(self)

                return True

            except LoadComicsException as excp:
                QtWidgets.QMessageBox().warning(self,
                                                self.tr('LoadComicsException'),
                                                self.tr(excp.message),
                                                QtWidgets.QMessageBox.Close)
            except InvalidTypeFileException as excp:
                QtWidgets.QMessageBox().warning(self,
                                                self.tr('InvalidTypeFile'
                                                        'Exception'),
                                                self.tr(excp.message),
                                                QtWidgets.QMessageBox.Close)

        return False

    def open_recent_file(self):
        action = self.sender()
        if action:
            filename = action.data()
            if file_exist(filename):
                initial_page = self.get_page_from_temporary_bookmarks(filename)
                self.open_comics(filename, initial_page=initial_page)
            else:
                files = self.model.load_recent_files()
                files.remove(filename)
                self.model.save_recent_files(files)
                self.update_recent_file_actions()
                not_found_dialog = NotFoundDialog(self)
                not_found_dialog.show()
                not_found_dialog.exec_()

    def set_current_file(self, filename):

        # Load recent files list
        files = self.model.load_recent_files()

        try:
            # Remove the current file from recent file list
            files.remove(filename)
        except ValueError:
            pass

        # Insert it on top of recent file list
        files.insert(0, filename)
        del files[MainWindowView.MAX_RECENT_FILES:]

        # Save recent file list
        self.model.save_recent_files(files)

        # Update text and data of recent file actions
        self.update_recent_file_actions()

    def update_recent_file_actions(self):

        files = self.model.load_recent_files()
        num_recent_files = len(files) if files else 0
        num_recent_files = min(num_recent_files, MainWindowView.MAX_RECENT_FILES)  # noqa: 501

        self.ui.menu_recent_files.menuAction().setVisible(True if files else
                                                          False)
        recent_file_actions = self.ui.menu_recent_files.actions()

        for i in range(num_recent_files):
            text = QtCore.QFileInfo(files[i]).fileName()
            recent_file_actions[i].setText(text)
            recent_file_actions[i].setData(files[i])
            recent_file_actions[i].setVisible(True)
            recent_file_actions[i].setStatusTip(files[i])

        for j in range(num_recent_files, MainWindowView.MAX_RECENT_FILES):
            recent_file_actions[j].setVisible(False)

    def update_bookmark_actions(self):
        is_bookmark = self.model.is_bookmark()
        self.ui.action_remove_bookmark.setVisible(is_bookmark)
        self.ui.action_add_bookmark.setVisible(not is_bookmark)

        bookmark_list = self.model.get_bookmark_list(
            MainWindowView.MAX_BOOKMARK_FILES)
        self.ui.menu_recent_bookmarks.menuAction().setVisible(
            True if bookmark_list else False)

    def update_recent_bookmarks_menu(self):

        bk_actions = self.ui.menu_recent_bookmarks.actions()
        bookmark_list = self.model.get_bookmark_list(len(bk_actions))

        num_bookmarks_files = len(bookmark_list) if bookmark_list else 0
        num_bookmarks_files = min(num_bookmarks_files,
                                  MainWindowView.MAX_BOOKMARK_FILES)

        for i in range(num_bookmarks_files):
            bk_text = '%s [%d]' % (bookmark_list[i].comic_name,
                                   bookmark_list[i].comic_page)
            bk_actions[i].setText(bk_text)
            bk_actions[i].setData(bookmark_list[i].comic_page)
            bk_actions[i].setStatusTip(bookmark_list[i].comic_path)
            bk_actions[i].setVisible(True)

        for j in range(num_bookmarks_files, MainWindowView.MAX_BOOKMARK_FILES):
            bk_actions[j].setVisible(False)

    def open_recent_bookmark(self):
        action = self.sender()
        if action:
            filename = action.statusTip()
            if file_exist(filename):
                self.open_comics(action.statusTip(), action.data() - 1)
            else:
                self.model.remove_bookmark(action.statusTip())
                self.update_bookmark_actions()

    def enable_actions(self):

        action_list = self.ui.menu_file.actions()
        action_list += self.ui.menu_view.actions()
        action_list += self.ui.menu_navegation.actions()
        action_list += self.ui.menu_bookmarks.actions()

        for action in action_list:
            action.setEnabled(True)

    def update_navegation_actions(self):

        # is_first_page = self.model.is_first_page()
        # is_last_page = self.model.is_last_page()

        # self.ui.action_previous_page.setEnabled(
        #     not self.model.is_first_comic())
        # self.ui.action_first_page.setEnabled(not self.model.is_first_comic())
        #
        # self.ui.action_next_page.setEnabled(not self.model.is_last_comic())
        # self.ui.action_last_page.setEnabled(not self.model.is_last_comic())

        self.ui.action_previous_comic.setEnabled(
            not self.model.is_first_comic())

        self.ui.action_next_comic.setEnabled(
            not self.model.is_last_comic())

    def update_status_bar(self):

        if self.model.comic:
            page_number = self.model.get_current_page_number()
            total_pages = self.model.get_number_of_pages()
            page_width = self.model.get_current_page().width()
            page_height = self.model.get_current_page().height()
            page_title = self.model.get_current_page_title()

            if self.ui.statusbar.isVisible():
                self.ui.statusbar.set_comic_page(page_number, total_pages)
                self.ui.statusbar.set_page_resolution(page_width, page_height)
                self.ui.statusbar.set_comic_path(page_title)

    def centralize_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setMinimumSize(screen.size() * 0.8)
        size = self.geometry()
        x_center = (screen.width() - size.width()) / 2
        y_center = (screen.height() - size.height()) / 2
        self.move(x_center, y_center)

    def update_viewer_content(self):
        content = self.model.get_current_page()

        if content:
            self.ui.label.setPixmap(content)
            self.ui.qscroll_area_viewer.reset_scroll_position()
            self.update_status_bar()

    def update_current_view_container_size(self):
        self.model.scroll_area_size = self.ui.qscroll_area_viewer.size()
        self.update_viewer_content()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_F:
            self.on_action_fullscreen_triggered()

        elif event.key() == QtCore.Qt.Key_Up:
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            next_pos = vert_scroll_bar.sliderPosition() - self.height() * 0.8

            self.vertical_animation.setDuration(250)
            self.vertical_animation.setStartValue(
                vert_scroll_bar.sliderPosition())
            self.vertical_animation.setEndValue(next_pos)
            self.vertical_animation.start()

        elif event.key() == QtCore.Qt.Key_Down:
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            next_pos = vert_scroll_bar.sliderPosition() + self.height() * 0.8

            self.vertical_animation.setDuration(250)
            self.vertical_animation.setStartValue(
                vert_scroll_bar.sliderPosition())
            self.vertical_animation.setEndValue(next_pos)
            self.vertical_animation.start()

        super(MainWindowView, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.on_action_fullscreen_triggered()
        super(MainWindowView, self).mousePressEvent(event)

    def resizeEvent(self, event):
        self.update_current_view_container_size()
        super(MainWindowView, self).resizeEvent(event)

    def show(self):
        """
        :doc: Added to set the correct scrool_area_view size in model
        """
        super(MainWindowView, self).show()
        self.update_current_view_container_size()
