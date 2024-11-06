from PyQt5 import QtCore, QtWidgets

from .comic_page_handler_factory import ComicPageHandlerFactory
from .uic_files import go_to_page_dialog_ui


class GoToDialog(QtWidgets.QDialog):
    def __init__(self, comic_handler, parent=None):
        super().__init__(parent=parent)

        self.ui = go_to_page_dialog_ui.Ui_GoPageDialog()
        self.ui.setupUi(self)

        page_qty = len(comic_handler.comic.pages)
        page_number = comic_handler.get_current_page().number

        self.model_handler = comic_handler
        self.handler = ComicPageHandlerFactory.create_handler(False, comic=comic_handler.comic, index=page_number - 1)

        self.last_page = page_number

        self.ui.total_page_label.setText(self.tr("of %d") % page_qty)

        self.ui.horizontal_slider.setMaximum(page_qty)
        self.ui.spin_box_go_page.setMaximum(page_qty)

        self.ui.spin_box_go_page.setValue(page_number)

    def update(self):

        step_qty = abs(self.ui.horizontal_slider.value() - self.last_page)

        if self.last_page < self.ui.horizontal_slider.value():
            go_action = self.handler.go_next_page
        else:
            go_action = self.handler.go_previous_page

        for go in [go_action] * step_qty:
            go()

        self.last_page = self.ui.spin_box_go_page.value()

        image_page = self.handler.get_current_page_image()
        image_page = image_page.scaledToHeight(int(self.height() * 0.7), QtCore.Qt.SmoothTransformation)
        self.ui.page_label.setPixmap(image_page)

        super(GoToDialog, self).update()

    def show(self):
        self.update()
        super(GoToDialog, self).show()
