

from unittest import TestCase

from pynocchio.comic import Comic, Page
from pynocchio.comic_page_handler import (ComicPageHandler,
                                          ComicPageHandlerDoublePage,
                                          ComicPageHandlerSinglePage)


class TestComicPageHandler(TestCase):

    def setUp(self):
        super(TestComicPageHandler, self).setUp()
        self.comic = Comic('comic_test', 'comic_dir')
        self.page_1 = Page(None, 'page_title_1', 1)
        self.page_2 = Page(None, 'page_title_2', 2)
        self.page_3 = Page(None, 'page_title_3', 3)
        self.obj = ComicPageHandler(self.comic)
        self.comic.pages = [self.page_1, self.page_2, self.page_3]

    def test_get_current_page(self):
        self.comic.pages = []
        self.comic.pages.append(self.page_1)
        self.assertEqual(self.page_1, self.obj.get_current_page())

    def test_go_first_page(self):
        self.obj.current_page_index = 2
        self.obj.go_first_page()
        self.assertEqual(self.obj.current_page_index, 0)

    def test_go_last_page(self):
        self.obj.current_page_index = 0

        self.obj.go_last_page()
        self.assertEqual(self.obj.current_page_index, 2)

    def test_current_page_index(self):
        self.obj.current_page_index = 0

        self.obj.current_page_index = 3
        self.assertEqual(self.obj.current_page_index, 0)

        self.obj.current_page_index = 2
        self.assertEqual(self.obj.current_page_index, 2)


class TestComicPageHandlerSinglePage(TestComicPageHandler):

    def setUp(self):
        super(TestComicPageHandlerSinglePage, self).setUp()
        self.obj = ComicPageHandlerSinglePage(self.comic)

    def test_go_next_page(self):
        self.obj.go_next_page()
        self.assertEqual(1, self.obj.current_page_index)

        self.obj.go_next_page()
        self.assertEqual(2, self.obj.current_page_index)

        self.obj.go_next_page()
        self.assertEqual(2, self.obj.current_page_index)

    def test_go_previous_page(self):
        self.obj.current_page_index = 2

        self.obj.go_previous_page()
        self.assertEqual(1, self.obj.current_page_index)

        self.obj.go_previous_page()
        self.assertEqual(0, self.obj.current_page_index)

        self.obj.go_previous_page()
        self.assertEqual(0, self.obj.current_page_index)


class TestComicPageHandlerDoublePage(TestComicPageHandler):

    def setUp(self):
        super(TestComicPageHandlerDoublePage, self).setUp()
        self.obj = ComicPageHandlerDoublePage(self.comic)

    def test_go_next_page(self):
        self.assertEqual(0, self.obj.current_page_index)

        self.obj.go_next_page()
        self.assertEqual(2, self.obj.current_page_index)

        self.obj.go_next_page()
        self.assertEqual(2, self.obj.current_page_index)

    def test_go_previous_page(self):
        self.obj.current_page_index = 2

        self.obj.go_previous_page()
        self.assertEqual(0, self.obj.current_page_index)

        self.obj.go_previous_page()
        self.assertEqual(0, self.obj.current_page_index)
