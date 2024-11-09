

import builtins
import os
import random
from unittest import TestCase, mock

import rarfile  # noqa: F401

from pynocchio.comic_file_loader_rar import ComicRarLoader, is_rarfile
from pynocchio.exception import NoDataFindException
from pynocchio.utility import IMAGE_FILE_FORMATS, get_file_extension


class TestComicRarLoader(TestCase):
    """ This class load Zip compact files.
    """

    class MockRarFile:
        """Support class to mock RarFile class"""

        def __init__(self, filename):
            self.filenames = filename
            self.files = []

        def write(self, filename):
            self.files.append(mock.Mock(filename=filename))

        def __iter__(self):
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return True

        def infolist(self):
            return self.files

        def namelist(self):
            return [f.filename for f in self.files]

        def read(self, filename):
            """Add any data, only to simulate read method"""
            return '\x00\x64'

    def setUp(self):
        self.loader = ComicRarLoader()
        self.comic_name = 'no_existing_comic.rar'

        self.files = [
            'text_file_01.txt',
        ]

        self.mock_rar_file = TestComicRarLoader.MockRarFile(self.comic_name)

        for idx, ext in enumerate(IMAGE_FILE_FORMATS):
            self.files.append('%d-image-file%s' % (idx, ext))

        # Shuffle files to simulate sorted when loaded them
        random.shuffle(self.files)

    def test_is_rarfile(self):
        """Test is_rarfile function
        """
        with mock.patch('rarfile.is_rarfile') as mock_rarfile:
            mock_rarfile.return_value = True
            self.assertTrue(is_rarfile, True)

        with mock.patch('rarfile.is_rarfile') as mock_rarfile:
            mock_rarfile.return_value = False
            self.assertTrue(is_rarfile, False)

    @mock.patch('rarfile.RarFile')
    def test_load_supported_file_format(self, mock_rarfile):
        """Test load method from ComicZipLoader class. Load only image files.
        """

        mock_open_fn = mock.mock_open(read_data='')

        for f in self.files:
            self.mock_rar_file.write(f)

        mock_rarfile.return_value = self.mock_rar_file
        mock_rarfile.return_value.open = mock_open_fn

        with mock.patch.object(builtins, 'open', mock_open_fn):
            # Verify if data is empty
            self.assertListEqual(self.loader.data, [])

            # Call load method
            self.loader.load(self.comic_name)

            # The data list not is empty. All images files were loaded
            self.assertTrue(self.loader.data)

            # The data list must be sorted in alphabetical order
            # then we sort this list to make easy compare
            self.files.sort()

            self.files.remove('text_file_01.txt')

            # Compare loaded file with files in self.files
            for idx, page in enumerate(self.loader.data):
                # Verify with exist data
                self.assertTrue(page.data)

                # Verify page title
                self.assertEqual(page.title, os.path.join(self.files[idx]))

                # Verify if all loaded image is support format file
                self.assertIn(get_file_extension(page.title),
                              IMAGE_FILE_FORMATS)

            # Verify page number
                self.assertEqual(page.number, idx + 1)

    @mock.patch('rarfile.RarFile')
    def test_load_not_supported_file_format(self, mock_rarfile):
        """The load method only load image file.
        """

        mock_open_fn = mock.mock_open(read_data='')

        for f in ['text-file.txt']:
            self.mock_rar_file.write(f)

        mock_rarfile.return_value = self.mock_rar_file
        mock_rarfile.return_value.open = mock_open_fn

        with mock.patch.object(builtins, 'open', mock_open_fn):

            self.assertListEqual(self.loader.data, [])

            with self.assertRaises(NoDataFindException):
                self.loader.load(self.comic_name)
