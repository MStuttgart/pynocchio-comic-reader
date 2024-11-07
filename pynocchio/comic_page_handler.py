from PyQt5 import QtGui


class ComicPageHandler:

    def __init__(self, comic, index=0):
        self.comic = comic
        self._current_page_index = index

    def get_current_page(self):
        return self.comic.pages[self.current_page_index]

    def go_next_page(self):
        raise NotImplementedError("Must subclass me!")

    def go_previous_page(self):
        raise NotImplementedError("Must subclass me!")

    def go_first_page(self):
        self.current_page_index = 0

    def go_last_page(self):
        self.current_page_index = len(self.comic.pages) - 1

    @property
    def current_page_index(self):
        return self._current_page_index

    @current_page_index.setter
    def current_page_index(self, idx):
        if 0 <= idx < len(self.comic.pages):
            self._current_page_index = idx

    def get_current_page_image(self):
        raise NotImplementedError("Must subclass me!")


class ComicPageHandlerSinglePage(ComicPageHandler):

    def go_next_page(self):
        if self.current_page_index < len(self.comic.pages) - 1:
            self.current_page_index += 1
            return True
        else:
            return False

    def go_previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            return True
        else:
            return False

    def get_current_page_image(self):
        return self.get_current_page().pixmap


class ComicPageHandlerDoublePage(ComicPageHandler):

    def __init__(self, comic, inverse=False, index=0):
        super().__init__(comic=comic, index=index)
        self.inverse = inverse

    def go_next_page(self):
        if self.current_page_index < len(self.comic.pages) - 2:
            self.current_page_index += 2
            return True
        else:
            return False

    def go_previous_page(self):
        if self.current_page_index > 1:
            self.current_page_index -= 2
            return True
        else:
            return False

    def get_current_page_image(self):

        pages = []
        page_a = self.get_current_page().pixmap

        try:

            page_b = QtGui.QPixmap()

            direction = -1 if self.get_current_page().number % 2 == 0 else 1

            page_b = self.comic.pages[self.current_page_index + direction].pixmap

        except IndexError:
            width = page_a.width()
            height = page_a.height()
        else:
            height = max(page_a.height(), page_b.height())

            if self.inverse or direction == -1:
                page_b, page_a = page_a, page_b

            width = page_a.width() + page_b.width()

            pages.append([page_a.width(), 0, page_b])

        pages.append([0, 0, page_a])

        double_page = QtGui.QPixmap(width, height)
        painter = QtGui.QPainter(double_page)

        for page in pages:
            painter.drawPixmap(page[0], page[1], page[2])

        return double_page
