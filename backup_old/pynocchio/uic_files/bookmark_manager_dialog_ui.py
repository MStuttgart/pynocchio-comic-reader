

# Form implementation generated from reading ui file './forms/bookmark_manager_dialog.ui'
#
# Created by: PySide6 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

from . import main_window_view_rc


class Ui_Bookmark_Dialog(object):
    def setupUi(self, Bookmark_Dialog):
        Bookmark_Dialog.setObjectName("Bookmark_Dialog")
        Bookmark_Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Bookmark_Dialog.resize(776, 441)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            Bookmark_Dialog.sizePolicy().hasHeightForWidth())
        Bookmark_Dialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/others/pynocchio.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Bookmark_Dialog.setWindowIcon(icon)
        Bookmark_Dialog.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Bookmark_Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bookmark_table = QtWidgets.QTableView(Bookmark_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bookmark_table.sizePolicy().hasHeightForWidth())
        self.bookmark_table.setSizePolicy(sizePolicy)
        self.bookmark_table.setAutoFillBackground(False)
        self.bookmark_table.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bookmark_table.setAutoScroll(True)
        self.bookmark_table.setAutoScrollMargin(9)
        self.bookmark_table.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed |
                                            QtWidgets.QAbstractItemView.EditKeyPressed | QtWidgets.QAbstractItemView.SelectedClicked)
        self.bookmark_table.setTabKeyNavigation(True)
        self.bookmark_table.setProperty("showDropIndicator", False)
        self.bookmark_table.setDragDropOverwriteMode(False)
        self.bookmark_table.setAlternatingRowColors(True)
        self.bookmark_table.setSelectionMode(
            QtWidgets.QAbstractItemView.ContiguousSelection)
        self.bookmark_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.bookmark_table.setShowGrid(True)
        self.bookmark_table.setSortingEnabled(True)
        self.bookmark_table.setWordWrap(True)
        self.bookmark_table.setObjectName("bookmark_table")
        self.horizontalLayout.addWidget(self.bookmark_table)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.page_image_label = QtWidgets.QLabel(Bookmark_Dialog)
        self.page_image_label.setText("")
        self.page_image_label.setPixmap(
            QtGui.QPixmap(":/icons/pynocchio_icon.png"))
        self.page_image_label.setScaledContents(True)
        self.page_image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.page_image_label.setObjectName("page_image_label")
        self.verticalLayout_2.addWidget(self.page_image_label)
        self.page_preview_label = QtWidgets.QLabel(Bookmark_Dialog)
        self.page_preview_label.setEnabled(True)
        font = QtGui.QFont()
        font.setItalic(True)
        self.page_preview_label.setFont(font)
        self.page_preview_label.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.page_preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.page_preview_label.setObjectName("page_preview_label")
        self.verticalLayout_2.addWidget(self.page_preview_label)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.line_edit_path = QtWidgets.QLineEdit(Bookmark_Dialog)
        self.line_edit_path.setReadOnly(True)
        self.line_edit_path.setObjectName("line_edit_path")
        self.verticalLayout_3.addWidget(self.line_edit_path)
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.button_remove = QtWidgets.QPushButton(Bookmark_Dialog)
        self.button_remove.setEnabled(False)
        self.button_remove.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_remove.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/edit-delete.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove.setIcon(icon1)
        self.button_remove.setDefault(False)
        self.button_remove.setObjectName("button_remove")
        self.grid_layout.addWidget(self.button_remove, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacerItem2, 1, 2, 1, 1)
        self.button_cancel = QtWidgets.QPushButton(Bookmark_Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
            ":/icons/elementary3-icon-theme/actions/48/dialog-cancel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cancel.setIcon(icon2)
        self.button_cancel.setObjectName("button_cancel")
        self.grid_layout.addWidget(self.button_cancel, 1, 3, 1, 1)
        self.button_load = QtWidgets.QPushButton(Bookmark_Dialog)
        self.button_load.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/icons/icons/archive-extract.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_load.setIcon(icon3)
        self.button_load.setDefault(True)
        self.button_load.setObjectName("button_load")
        self.grid_layout.addWidget(self.button_load, 1, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.grid_layout)
        self.line_edit_path.raise_()

        self.retranslateUi(Bookmark_Dialog)
        self.button_cancel.clicked.connect(Bookmark_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Bookmark_Dialog)

    def retranslateUi(self, Bookmark_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Bookmark_Dialog.setWindowTitle(_translate(
            "Bookmark_Dialog", "Bookmark manager"))
        self.page_preview_label.setText(
            _translate("Bookmark_Dialog", "Page Preview"))
        self.button_remove.setText(_translate("Bookmark_Dialog", "Remove"))
        self.button_cancel.setText(_translate("Bookmark_Dialog", "Cancel"))
        self.button_load.setText(_translate("Bookmark_Dialog", "Load"))
