

# Form implementation generated from reading ui file './forms/about_dialog.ui'
#
# Created by: PySide6 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

from . import main_window_view_rc


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AboutDialog.resize(506, 363)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/others/pynocchio.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        AboutDialog.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        AboutDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.about_text_browser = QtWidgets.QTextBrowser(AboutDialog)
        self.about_text_browser.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.about_text_browser.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.about_text_browser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.about_text_browser.setSource(
            QtCore.QUrl("qrc:/others/others/about.html"))
        self.about_text_browser.setSearchPaths([''])
        self.about_text_browser.setOpenExternalLinks(True)
        self.about_text_browser.setObjectName("about_text_browser")
        self.verticalLayout.addWidget(self.about_text_browser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_close = QtWidgets.QPushButton(AboutDialog)
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

        self.retranslateUi(AboutDialog)
        self.button_close.clicked.connect(AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate(
            "AboutDialog", "About Pynocchio"))
        self.about_text_browser.setHtml(_translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.button_close.setText(_translate("AboutDialog", "Close"))
