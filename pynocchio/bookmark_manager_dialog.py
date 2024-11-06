import logging

from PyQt5 import QtCore, QtGui, QtSql, QtWidgets

from .uic_files import bookmark_manager_dialog_ui
from .utility import file_exist, get_dir_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookmarkManagerDialog(QtWidgets.QDialog):

    SCALE_RATIO = 0.25

    def __init__(self, controller, parent=None):
        super(BookmarkManagerDialog, self).__init__(parent=parent)

        self.ui = bookmark_manager_dialog_ui.Ui_Bookmark_Dialog()
        self.ui.setupUi(self)

        self.controller = controller
        path = get_dir_name(controller.model.settings_manager.settings.fileName())

        self.db = QtSql.QSqlDatabase().addDatabase("QSQLITE")
        self.db.setDatabaseName(path + "/bookmark.db")

        if self.db.open():

            self.model = QtSql.QSqlTableModel(self, self.db)
            self.model.setTable("Bookmark")

            self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            self.model.select()
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Name")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Page")

            self.ui.bookmark_table.setModel(self.model)
            self.ui.bookmark_table.hideColumn(0)
            self.ui.bookmark_table.hideColumn(1)
            self.ui.bookmark_table.hideColumn(4)

            self.ui.bookmark_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

            self.ui.bookmark_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

            self.ui.button_remove.clicked.connect(self._remove_table_item)
            self.ui.button_load.clicked.connect(self._get_comic_to_open)

            selection = self.ui.bookmark_table.selectionModel()
            selection.selectionChanged.connect(self.selection_changed)

            self.no_cover_label = self.ui.page_image_label.pixmap().scaledToWidth(
                int(self.width() * self.SCALE_RATIO), QtCore.Qt.SmoothTransformation
            )

            self.ui.page_image_label.setPixmap(self.no_cover_label)
            if self.model.rowCount():
                self.ui.button_load.setEnabled(True)
                self.ui.button_remove.setEnabled(True)
            logger.info("Database load!")

        else:
            logger.error("Unable to create db file!")

    def selection_changed(self, selected):

        model_indexes = selected.indexes()

        if model_indexes:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(model_indexes[4].data())
            pixmap = pixmap.scaledToWidth(int(self.width() * self.SCALE_RATIO), QtCore.Qt.SmoothTransformation)
            self.ui.page_image_label.setPixmap(pixmap)
            self.ui.line_edit_path.setText(model_indexes[1].data())

        else:
            self.ui.page_image_label.setPixmap(self.no_cover_label)
            self.ui.line_edit_path.setText("")

    def _remove_table_item(self):

        option = QtWidgets.QMessageBox().warning(
            self,
            self.tr("Delete bookmarks"),
            self.tr("This action will delete your bookmarks! Proceed?"),
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Ok,
        )

        if option == QtWidgets.QMessageBox.Ok:

            for index in self.ui.bookmark_table.selectedIndexes():
                self.model.removeRow(index.row())

            self.model.submitAll()
            self.ui.page_image_label.setPixmap(self.no_cover_label)

            if not self.model.rowCount():
                self.ui.button_load.setEnabled(False)
                self.ui.button_remove.setEnabled(False)

    def _get_comic_to_open(self):
        selection_model = self.ui.bookmark_table.selectionModel()

        if selection_model.hasSelection():
            path = selection_model.selectedRows(1)[0].data()
            page = selection_model.selectedRows(3)[0].data()

            if file_exist(path):
                self.controller.open_comics(path, page - 1)
                self.close()
            else:
                option = QtWidgets.QMessageBox().warning(
                    self,
                    self.tr("Comic does not exist"),
                    self.tr(
                        "The selected comic does not exist! Would you " "like to remove it from the bookmark list?"
                    ),
                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                    QtWidgets.QMessageBox.Ok,
                )

                if option == QtWidgets.QMessageBox.Ok:
                    for index in self.ui.bookmark_table.selectedIndexes():
                        self.model.removeRow(index.row())

                    self.model.submitAll()
                    self.ui.page_image_label.setPixmap(self.no_cover_label)

                    if not self.model.rowCount():
                        self.ui.button_load.setEnabled(False)
                        self.ui.button_remove.setEnabled(False)

    def close(self):
        self.db.close()
        super(BookmarkManagerDialog, self).close()
