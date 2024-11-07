from PyQt5 import QtWidgets

from .uic_files import preference_dialog_ui


class PreferenceDialog(QtWidgets.QDialog):

    def __init__(self, preference, parent=None):
        super().__init__(parent=parent)

        self.ui = preference_dialog_ui.Ui_config_dialog()
        self.ui.setupUi(self)

        self.preference = preference
        self.ui.line_edit_color.background_color = self.preference.background_color
        self.ui.background_color_button.clicked.connect(self._open_color_dialog)

    def _open_color_dialog(self):
        col_dialog = QtWidgets.QColorDialog(self)
        col = col_dialog.getColor(self.preference.background_color)
        if col.isValid():
            self.preference.background_color = col
            self.ui.line_edit_color.background_color = col

    def close(self):
        self.preference.background_color = self.ui.line_edit_color.background_color
        super(PreferenceDialog, self).close(self)
