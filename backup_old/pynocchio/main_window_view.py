import logging

from PySide6 import QtCore, QtGui, QtWidgets

from .about_dialog import AboutDialog
from .bookmark import TemporaryBookmark
from .bookmark_manager_dialog import BookmarkManagerDialog
from .exception import InvalidTypeFileException, LoadComicsException, NoDataFindException
from .go_to_page_dialog import GoToDialog
from .not_found_dialog import NotFoundDialog
from .thumbnails import ThumbnailsDock
from .uic_files import main_window_view_ui
from .utility import COMPACT_FILE_FORMATS, IMAGE_FILE_FORMATS, file_exist

# try:
# import qdarkgraystyle
# except ImportError:
#     pass


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindowView(QtWidgets.QMainWindow):

    MAX_RECENT_FILES = 5
    MAX_BOOKMARK_FILES = 5

    def __init__(self, model, parent=None):
        super().__init__(parent=parent)
        self.model = model
        model.parent = self

        self.ui = main_window_view_ui.Ui_MainWindowView()
        self.ui.setupUi(self)

        # self.default_stylesheet = QtWidgets.QApplication.instance().styleSheet()

        MainWindowView.MAX_RECENT_FILES = len(self.ui.menu_recent_files.actions())
        MainWindowView.MAX_BOOKMARK_FILES = len(self.ui.menu_recent_bookmarks.actions())

        self.ui.menu_recent_files.menuAction().setVisible(False)

        self.thumbnails_dock = ThumbnailsDock()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.thumbnails_dock)
        self.thumbnails_dock.visibilityChanged.connect(self.on_thumbnails_dock_changed)

        self.ui.qscroll_area_viewer.resized.connect(self.update_current_view_container_size)
        self.update_current_view_container_size()

        self.extra_shortcuts = self._define_extra_shortcuts()
        self.global_shortcuts = self._define_global_shortcuts()
        self.create_connections()
        self.centralize_window()

        self.update_recent_file_actions()

        self.update_settings()

        # self.model.load_progress.connect(self.ui.statusbar.set_progressbar_value)

        self.vertical_animation = QtCore.QPropertyAnimation(self.ui.qscroll_area_viewer.verticalScrollBar())

        self.last_scroll_position = 0

    @QtCore.Slot()
    def on_action_open_file_triggered(self):
        cb_formats = " ".join(["*" + cb for cb in COMPACT_FILE_FORMATS])
        img_formats = " ".join(["*" + img for img in IMAGE_FILE_FORMATS])
        all_files = "%s %s" % (cb_formats, img_formats)

        filename = QtWidgets.QFileDialog().getOpenFileName(
            self,
            self.tr("Open Comic File"),
            self.model.current_directory,
            self.tr(
                "all supported files (%s);; "
                "zip files (*.zip *.cbz);; rar files (*.rar *.cbr);; "
                "tar files (*.tar *.cbt);; image files (%s);; "
                "all files (*)" % (all_files, img_formats)
            ),
        )

        if filename:
            logger.info("Opening file")

            initial_page = self.get_page_from_temporary_bookmarks(filename[0])

            self.open_comics(filename[0], initial_page)

    @QtCore.Slot()
    def on_action_save_image_triggered(self):
        img_formats = " ".join(["*" + img for img in IMAGE_FILE_FORMATS])

        if self.model.comic:

            path = self.model.current_directory + self.model.get_current_page_title()
            file_path = QtWidgets.QFileDialog().getSaveFileName(
                self, self.tr("Save Current Page"), path, self.tr("images (%s)" % (img_formats))
            )

            if file_path:
                logger.info("Saving image")
                self.model.save_current_page_image(file_path[0])

    @QtCore.Slot()
    def on_action_previous_page_triggered(self):
        if self.model.previous_page():
            self.update_viewer_content()
            self.update_navigation_actions()
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            vert_scroll_bar.setValue(self.last_scroll_position)
        elif self.ui.action_page_across_files.isChecked():
            self.on_action_previous_comic_triggered()
            self.on_action_last_page_triggered()

    @QtCore.Slot()
    def on_action_next_page_triggered(self):
        if self.model.next_page():
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            self.last_scroll_position = vert_scroll_bar.sliderPosition()
            self.update_viewer_content()
            self.update_navigation_actions()
        elif self.ui.action_page_across_files.isChecked():
            self.on_action_next_comic_triggered()

    @QtCore.Slot()
    def on_action_first_page_triggered(self):
        self.model.first_page()
        self.update_viewer_content()
        self.update_navigation_actions()

    @QtCore.Slot()
    def on_action_last_page_triggered(self):
        self.model.last_page()
        self.update_viewer_content()
        self.update_navigation_actions()

    @QtCore.Slot()
    def on_action_previous_comic_triggered(self):
        try:
            self.open_comics(self.model.previous_comic())
        except NoDataFindException as exc:
            logger.exception(exc.message)

        self.update_navigation_actions()

    @QtCore.Slot()
    def on_action_next_comic_triggered(self):
        try:
            self.open_comics(self.model.next_comic())
        except NoDataFindException as exc:
            logger.exception(exc.message)

        self.update_navigation_actions()

    @QtCore.Slot()
    def on_action_rotate_left_triggered(self):
        self.model.rotate_left()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_rotate_right_triggered(self):
        self.model.rotate_right()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_go_to_page_triggered(self):
        go_to_dlg = GoToDialog(self.model.comic_page_handler, parent=self)
        go_to_dlg.show()
        ret = go_to_dlg.exec_()

        if ret == QtWidgets.QDialog.Accepted:
            self._go_to_page(go_to_dlg.handler.current_page_index)

    def _go_to_page(self, idx):
        self.model.set_current_page_index(idx)
        self.update_viewer_content()
        self.update_navigation_actions()

    @QtCore.Slot()
    def on_action_add_bookmark_triggered(self):
        self.model.add_bookmark()
        self.update_bookmark_actions()

    @QtCore.Slot()
    def on_action_remove_bookmark_triggered(self):
        self.model.remove_bookmark(self.model.get_comic_path())
        self.update_bookmark_actions()

    @QtCore.Slot()
    def on_action_bookmark_manager_triggered(self):
        bookmark_dialog = BookmarkManagerDialog(self, parent=self)
        bookmark_dialog.show()
        bookmark_dialog.exec_()

    @QtCore.Slot()
    def on_action_preference_dialog_triggered(self):
        pass

    @QtCore.Slot()
    def on_action_original_fit_triggered(self):
        self.model.original_fit()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_vertical_fit_triggered(self):
        self.model.vertical_fit()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_horizontal_fit_triggered(self):
        self.model.horizontal_fit()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_best_fit_triggered(self):
        self.model.best_fit()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_page_fit_triggered(self):
        self.model.page_fit()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_fullscreen_triggered(self):

        if self.isFullScreen():
            self.ui.menubar.show()
            if self.ui.action_show_toolbar.isChecked():
                self.ui.toolbar.show()
            if self.ui.action_show_statusbar.isChecked():
                self.ui.statusbar.show()
            self.showNormal()

            for sc in self.global_shortcuts:
                sc.setEnabled(False)
        else:
            self.ui.menubar.hide()
            self.ui.toolbar.hide()
            self.ui.statusbar.hide()
            self.showFullScreen()
            for sc in self.global_shortcuts:
                sc.setEnabled(True)

    @QtCore.Slot(bool)
    def on_action_double_page_mode_triggered(self, checked):
        self.model.double_page_mode(checked)
        self.update_viewer_content()
        self.ui.action_manga_mode.setEnabled(checked)

    @QtCore.Slot(bool)
    def on_action_manga_mode_triggered(self, checked):
        self.model.manga_page_mode(checked)
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_show_toolbar_triggered(self):
        if self.ui.action_show_toolbar.isChecked():
            self.ui.toolbar.show()
        else:
            self.ui.toolbar.hide()

    @QtCore.Slot()
    def on_action_show_statusbar_triggered(self):
        if self.ui.action_show_statusbar.isChecked():
            self.ui.statusbar.show()
            self.update_status_bar()
        else:
            self.ui.statusbar.hide()

    @QtCore.Slot()
    def on_action_show_thumbnails_triggered(self):
        if self.ui.action_show_thumbnails.isChecked():
            self.thumbnails_dock.show()
        else:
            self.thumbnails_dock.hide()

    @QtCore.Slot()
    def on_action_shrink_only_triggered(self):
        self.model.resize_always = not self.ui.action_shrink_only.isChecked()
        self.update_viewer_content()

    @QtCore.Slot()
    def on_action_about_triggered(self):
        ab_dlg = AboutDialog(self)
        ab_dlg.show()
        ab_dlg.exec_()

    @QtCore.Slot()
    def on_action_about_qt_triggered(self):
        QtWidgets.QMessageBox().aboutQt(self, self.tr("About Qt"))

    @QtCore.Slot()
    def on_action_exit_triggered(self):
        self.close()

    @QtCore.Slot()
    def on_thumbnails_dock_changed(self):
        self.ui.action_show_thumbnails.setChecked(self.thumbnails_dock.isVisible())

    @QtCore.Slot(bool)
    def on_action_dark_style_triggered(self):
        qApp = QtWidgets.QApplication.instance()
        if self.ui.action_dark_style.isChecked():
            try:
                qApp.setStyleSheet(qdarkgraystyle.load_stylesheet())
            except NameError:
                pass
        else:
            qApp.setStyleSheet(self.default_stylesheet)

    def create_connections(self):

        # Define group to action fit items and load fit of settings file
        self.ui.action_group_view = QtGui.QActionGroup(self)

        self.ui.action_group_view.addAction(self.ui.action_original_fit)
        self.ui.action_group_view.addAction(self.ui.action_vertical_fit)
        self.ui.action_group_view.addAction(self.ui.action_horizontal_fit)
        self.ui.action_group_view.addAction(self.ui.action_best_fit)
        self.ui.action_group_view.addAction(self.ui.action_page_fit)

        view_adjust = self.model.load_view_adjust(self.ui.action_group_view.checkedAction().objectName())

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
        self.ui.menu_recent_bookmarks.aboutToShow.connect(self.update_recent_bookmarks_menu)

    def _define_extra_shortcuts(self):

        shortcuts = []

        sequence = {
            "Up": self.on_action_previous_page_triggered,
            "PgUp": self.on_action_previous_page_triggered,
            "Down": self.on_action_next_page_triggered,
            "PgDown": self.on_action_next_page_triggered,
            "Ctrl+Up": self.on_action_first_page_triggered,
            "Home": self.on_action_first_page_triggered,
            "Ctrl+Down": self.on_action_last_page_triggered,
            "End": self.on_action_last_page_triggered,
        }

        for key, value in list(sequence.items()):
            s = QtGui.QShortcut(QtGui.QKeySequence(key), self.ui.qscroll_area_viewer, value)
            s.setEnabled(True)

        return shortcuts

    def _define_global_shortcuts(self):

        shortcuts = []

        sequence = {
            "Esc": self.on_action_fullscreen_triggered,
        }

        for key, value in list(sequence.items()):
            s = QtGui.QShortcut(QtGui.QKeySequence(key), self.ui.qscroll_area_viewer, value)
            s.setEnabled(False)
            shortcuts.append(s)

        return shortcuts

    def get_page_from_temporary_bookmarks(self, path):

        bk = self.model.get_bookmark_from_path(path=path, table=TemporaryBookmark)
        initial_page = None

        if bk:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(self.tr("Continue reading from page %d?" % bk.comic_page))
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText(
                self.tr(
                    "<p>You stopped reading here.</p>"
                    '<p> If you choose <b>"Yes"</b>, reading will '
                    "resume on <b>page %d</b>. </p>"
                    "<p>Otherwise, the first page will be "
                    "loaded.</p>" % bk.comic_page
                )
            )
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            q = QtGui.QPixmap()
            q.loadFromData(bk.page_data)
            q = q.scaledToWidth(int(msg.width() * 0.2), QtCore.Qt.SmoothTransformation)
            msg.setIconPixmap(q)

            option = msg.exec_()

            if option == QtWidgets.QMessageBox.Ok:
                initial_page = bk.comic_page - 1

        return initial_page

    def open_comics(self, filename, initial_page=None):
        if filename:
            logger.info("Opening comic %s", filename)

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
                self.update_navigation_actions()

                self.update_thumbnails()

                # Register view like listener of ComicPageHandler events
                # self.model.comic_page_handler.listener.append(self)

                return True

            except LoadComicsException as excp:
                QtWidgets.QMessageBox().warning(
                    self, "LoadComicsException", self.tr(excp.message), QtWidgets.QMessageBox.Close
                )
            except InvalidTypeFileException as excp:
                QtWidgets.QMessageBox().warning(
                    self, "InvalidTypeFileException", self.tr(excp.message), QtWidgets.QMessageBox.Close
                )

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
        del files[MainWindowView.MAX_RECENT_FILES :]

        # Save recent file list
        self.model.save_recent_files(files)

        # Update text and data of recent file actions
        self.update_recent_file_actions()

    def update_recent_file_actions(self):

        files = self.model.load_recent_files()
        num_recent_files = len(files) if files else 0
        num_recent_files = min(num_recent_files, MainWindowView.MAX_RECENT_FILES)

        self.ui.menu_recent_files.menuAction().setVisible(True if files else False)
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

        bookmark_list = self.model.get_bookmark_list(MainWindowView.MAX_BOOKMARK_FILES)
        self.ui.menu_recent_bookmarks.menuAction().setVisible(True if bookmark_list else False)

    def update_recent_bookmarks_menu(self):

        bk_actions = self.ui.menu_recent_bookmarks.actions()
        bookmark_list = self.model.get_bookmark_list(len(bk_actions))

        num_bookmarks_files = len(bookmark_list) if bookmark_list else 0
        num_bookmarks_files = min(num_bookmarks_files, MainWindowView.MAX_BOOKMARK_FILES)

        for i in range(num_bookmarks_files):
            bk_text = "%s [%d]" % (bookmark_list[i].comic_name, bookmark_list[i].comic_page)
            bk_actions[i].setText(bk_text)
            bk_actions[i].setData(bookmark_list[i].comic_page)
            bk_actions[i].setStatusTip(bookmark_list[i].comic_path)
            bk_actions[i].setVisible(True)

        for j in range(num_bookmarks_files, MainWindowView.MAX_BOOKMARK_FILES):
            bk_actions[j].setVisible(False)

    def update_settings(self):
        settings = self.model.load_toggles()
        self.ui.action_show_toolbar.setChecked(settings["show_toolbar"])
        self.on_action_show_toolbar_triggered()
        self.ui.action_show_statusbar.setChecked(settings["show_statusbar"])
        self.on_action_show_statusbar_triggered()
        self.ui.action_show_thumbnails.setChecked(settings["show_thumbnails"])
        self.on_action_show_thumbnails_triggered()
        self.ui.action_shrink_only.setChecked(settings["shrink_only"])
        self.on_action_shrink_only_triggered()
        self.ui.action_page_across_files.setChecked(settings["page_across_files"])
        self.ui.action_dark_style.setChecked(settings["dark_style"])
        self.on_action_dark_style_triggered()

    def update_thumbnails(self):
        self.thumbnails_dock.clear()
        num = self.model.get_current_page_number() - 1
        self.thumbnails_dock.populate(current=num)

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
        action_list += self.ui.menu_navigation.actions()
        action_list += self.ui.menu_bookmarks.actions()

        for action in action_list:
            action.setEnabled(True)

    def update_navigation_actions(self):

        # is_first_page = self.model.is_first_page()
        # is_last_page = self.model.is_last_page()

        # self.ui.action_previous_page.setEnabled(
        #     not self.model.is_first_comic())
        # self.ui.action_first_page.setEnabled(not self.model.is_first_comic())
        #
        # self.ui.action_next_page.setEnabled(not self.model.is_last_comic())
        # self.ui.action_last_page.setEnabled(not self.model.is_last_comic())

        self.ui.action_previous_comic.setEnabled(not self.model.is_first_comic())

        self.ui.action_next_comic.setEnabled(not self.model.is_last_comic())

    def update_status_bar(self):

        if self.model.comic:
            page_number = self.model.get_current_page_number()
            total_pages = self.model.get_number_of_pages()
            page_width = self.model.get_current_page().width()
            page_height = self.model.get_current_page().height()
            original_width = self.model.get_current_page().original_width
            original_height = self.model.get_current_page().original_height
            page_title = self.model.get_current_page_title()

            if self.ui.statusbar.isVisible():
                self.ui.statusbar.set_comic_page(page_number, total_pages)
                self.ui.statusbar.set_page_resolution(page_width, page_height, original_width, original_height)
                self.ui.statusbar.set_comic_path(page_title)

    def centralize_window(self):
        screen = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x_center = (screen.width() - size.width()) / 2
        y_center = (screen.height() - size.height()) / 2
        self.move(int(x_center), int(y_center))
        size = self.size()
        pos = self.pos()
        size, pos, state = self.model.load_window(size, pos)
        self.resize(size)
        self.move(pos)
        if state:
            self.restoreState(state)

    def update_viewer_content(self):

        content = self.model.get_current_page()

        if content:
            try:
                self.ui.label.setPixmap(content)
                self.thumbnails_dock.highlight(self.model.get_current_page_number() - 1)
                self.ui.qscroll_area_viewer.reset_scroll_position()
                self.update_status_bar()

            except RuntimeError:
                pass

    def update_current_view_container_size(self):

        print("tetetet")

        margins = self.ui.qscroll_area_viewer.size() - self.ui.qscroll_area_viewer.contentsRect().size()

        self.model.scroll_area_size = self.ui.qscroll_area_viewer.size() - 2 * margins
        self.model.scroll_bar_size = self.ui.qscroll_area_viewer.style().pixelMetric(
            QtWidgets.QStyle.PM_ScrollBarExtent
        )
        self.update_viewer_content()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_F:
            self.on_action_fullscreen_triggered()

        elif event.key() == QtCore.Qt.Key_Up:
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            next_pos = vert_scroll_bar.sliderPosition() - self.height() * 0.8

            self.vertical_animation.setDuration(250)
            self.vertical_animation.setStartValue(vert_scroll_bar.sliderPosition())
            self.vertical_animation.setEndValue(next_pos)
            self.vertical_animation.start()

        elif event.key() == QtCore.Qt.Key_Down:
            vert_scroll_bar = self.ui.qscroll_area_viewer.verticalScrollBar()
            next_pos = vert_scroll_bar.sliderPosition() + self.height() * 0.8

            self.vertical_animation.setDuration(250)
            self.vertical_animation.setStartValue(vert_scroll_bar.sliderPosition())
            self.vertical_animation.setEndValue(next_pos)
            self.vertical_animation.start()

        super(MainWindowView, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.on_action_fullscreen_triggered()
        super(MainWindowView, self).mousePressEvent(event)

    def contextMenuEvent(self, event):
        self.ui.menu_context.exec(event.globalPos())
        super(MainWindowView, self).contextMenuEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            self.on_action_next_page_triggered()
        else:
            self.on_action_previous_page_triggered()
        event.accept()

    def closeEvent(self, event):
        self.model.save_settings()

        try:
            if self.model.is_first_page() or self.model.is_last_page():
                self.model.remove_bookmark(table=TemporaryBookmark)
            else:
                self.model.add_bookmark(table=TemporaryBookmark)
        except AttributeError as exc:
            logger.warning(exc)

        super(MainWindowView, self).close()
        event.accept()
