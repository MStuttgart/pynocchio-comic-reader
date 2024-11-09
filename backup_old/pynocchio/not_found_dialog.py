from PySide6 import QtWidgets

from .uic_files import not_found_dialog_ui


class NotFoundDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = not_found_dialog_ui.Ui_NotFoundDialog()
        self.ui.setupUi(self)
