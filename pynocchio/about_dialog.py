from PyQt5 import QtCore, QtWidgets

from .uic_files import about_dialog_ui


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.ui = about_dialog_ui.Ui_AboutDialog()
        self.ui.setupUi(self)

        self.ui.about_text_browser.setSource(QtCore.QUrl("qrc:///others/others/about.html"))
