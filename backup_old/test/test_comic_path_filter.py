

from unittest import TestCase, mock

from pynocchio.comic_path_filter import ComicPathFilter
from pynocchio.exception import NoDataFindException


class TestComicPathFilter(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.obj = ComicPathFilter(["*.cbr", "*.cbz", "*.rar", "*.zip",
                                    "*.tar", "*.cbt"])

    def test_parse(self):
        with mock.patch('glob.glob1') as mock_glob:
            mock_glob.return_value = ['comic_1.cbr', 'abc.cbr']

            self.obj = ComicPathFilter(['*.cbr'])
            self.obj.parse('.')

            self.assertListEqual(self.obj.file_list,
                                 ['abc.cbr', 'comic_1.cbr'])

            mock_glob.return_value = []

            self.obj = ComicPathFilter(['*.zip'])
            self.obj.parse('.')
            self.assertListEqual(self.obj.file_list, [])

    def test_is_first_comic(self):
        with mock.patch('glob.glob1') as mock_glob:
            mock_glob.return_value = ['comic_3.cbr', 'comic_1.cbr', 'abc.cbr']

            self.obj = ComicPathFilter(['*.cbr'])
            self.obj.parse('.')

            self.assertTrue(self.obj.is_first_comic('abc.cbr'))
            self.assertFalse(self.obj.is_first_comic('comic_3.cbr'))

            self.obj.file_list = []

            with self.assertRaises(NoDataFindException):
                self.obj.is_first_comic('co.cbr')

    def test_is_last_comic(self):
        with mock.patch('glob.glob1') as mock_glob:
            mock_glob.return_value = ['comic_3.cbr', 'comic_1.cbr', 'abc.cbr']

            self.obj = ComicPathFilter(['*.cbr'])
            self.obj.parse('.')

            self.assertFalse(self.obj.is_last_comic('abc.cbr'))
            self.assertTrue(self.obj.is_last_comic('comic_3.cbr'))

            self.obj.file_list = []

            with self.assertRaises(NoDataFindException):
                self.obj.is_last_comic('co.cbr')

    def test_get_previous_comic(self):
        with mock.patch('glob.glob1') as mock_glob:
            mock_glob.return_value = ['comic_3.cbr', 'comic_1.cbr', 'abc.cbr']

            self.obj = ComicPathFilter(['*.cbr'])
            self.obj.parse('pynocchio/comics/')

            previous_comics = self.obj.get_previous_comic('comic_1.cbr')
            self.assertEqual('pynocchio/comics/' + 'abc.cbr', previous_comics)

            with self.assertRaises(NoDataFindException):
                self.obj.get_previous_comic('abc.cbr')

    def test_get_next_comic(self):
        with mock.patch('glob.glob1') as mock_glob:
            mock_glob.return_value = ['comic_3.cbr', 'comic_1.cbr', 'abc.cbr']

            self.obj = ComicPathFilter(['*.cbr'])
            self.obj.parse('pynocchio/comics/')

            next_comics = self.obj.get_next_comic('comic_1.cbr')
            self.assertEqual('pynocchio/comics/' + 'comic_3.cbr', next_comics)

            with self.assertRaises(NoDataFindException):
                self.obj.get_next_comic('comic_3.cbr')
