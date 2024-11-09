

# Form implementation generated from reading ui file 'forms/not_found_dialog.ui'
#
# Created by: PySide6 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

from . import main_window_view_rc


class Ui_NotFoundDialog(object):
    def setupUi(self, NotFoundDialog):
        NotFoundDialog.setObjectName("NotFoundDialog")
        NotFoundDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NotFoundDialog.resize(506, 363)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            NotFoundDialog.sizePolicy().hasHeightForWidth())
        NotFoundDialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/others/pynocchio.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NotFoundDialog.setWindowIcon(icon)
        NotFoundDialog.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        NotFoundDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(NotFoundDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.not_found_text_label = QtWidgets.QLabel(NotFoundDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.not_found_text_label.sizePolicy().hasHeightForWidth())
        self.not_found_text_label.setSizePolicy(sizePolicy)
        self.not_found_text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.not_found_text_label.setObjectName("not_found_text_label")
        self.verticalLayout.addWidget(self.not_found_text_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_close = QtWidgets.QPushButton(NotFoundDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_close.sizePolicy().hasHeightForWidth())
        self.button_close.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/edit-delete.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon1)
        self.button_close.setDefault(True)
        self.button_close.setFlat(False)
        self.button_close.setObjectName("button_close")
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NotFoundDialog)
        self.button_close.clicked.connect(NotFoundDialog.close)
        QtCore.QMetaObject.connectSlotsByName(NotFoundDialog)

    def retranslateUi(self, NotFoundDialog):
        _translate = QtCore.QCoreApplication.translate
        NotFoundDialog.setWindowTitle(
            _translate("NotFoundDialog", "File not found"))
        self.not_found_text_label.setText(_translate(
            "NotFoundDialog", "The file was not found"))
        self.button_close.setText(_translate("NotFoundDialog", "Close"))
