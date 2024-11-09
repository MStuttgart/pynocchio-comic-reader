

from unittest import TestCase

from pynocchio.comic import Comic, Page


class TestComic(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.path = 'comic_dir/comic.zip'
        self.name = 'Comic Test'
        self.obj = Comic('Comic Test', 'comic_dir/comic.zip')

    def test_path(self):
        self.assertEqual(self.path + '/' + self.name, self.obj.path)


class TestPage(TestCase):

    def test__init__(self):
        page = Page(None, 'title', 1)
        self.assertEqual(page.data, None)
        self.assertEqual(page.title, 'title')
        self.assertEqual(page.number, 1)
