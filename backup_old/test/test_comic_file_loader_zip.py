

import builtins
import os
import random
import zipfile  # noqa: F401
from unittest import TestCase, mock

from pynocchio.comic_file_loader_zip import ComicZipLoader, is_zipfile
from pynocchio.exception import NoDataFindException
from pynocchio.utility import IMAGE_FILE_FORMATS, get_file_extension


class TestComicZipLoader(TestCase):
    """ This class load Zip compact files.
    """

    class MockZipFile:
        """ Support class to mock ZipFile class
        """

        def __init__(self, filename):
            self.filename = filename
            self.files = []

        def write(self, filename):
            self.files.append(mock.Mock(filename=filename))

        def __iter__(self):
            return iter(self.files)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return True

        def infolist(self):
            return self.files

        def namelist(self):
            return [f.filename for f in self.files]

        def read(self, filename):
            return '\x00\x64'

    def setUp(self):
        self.loader = ComicZipLoader()

        self.files = [
            'text_file.txt',
        ]

        # Define comic name
        self.comic_name = 'no_existing_comic.cbz'

        # Create ZipFile mock object
        self.mock_zip_file = TestComicZipLoader.MockZipFile(self.comic_name)

        # Insert data in ZipFile mock object and file list
        for idx, ext in enumerate(IMAGE_FILE_FORMATS):
            self.files.append('%d-image-file%s' % (idx, ext))

        # Shuffle list to made more real the test sort of filename
        random.shuffle(self.files)

    def test_is_zipfile(self):
        """Test is_zipfile function
        """
        with mock.patch('zipfile.is_zipfile') as mock_zipfile:
            mock_zipfile.return_value = True
            self.assertTrue(is_zipfile, True)

        with mock.patch('zipfile.is_zipfile') as mock_zipfile:
            mock_zipfile.return_value = False
            self.assertTrue(is_zipfile, False)

    @mock.patch('zipfile.ZipFile')
    def test_load_supported_file_format(self, mock_zipfile):
        """Test load method from ComicZipLoader class. Load only image files.
        """

        mock_open_fn = mock.mock_open(read_data='')

        # Insert data in ZipFile mock object
        for f in self.files:
            self.mock_zip_file.write(f)

        mock_zipfile.return_value = self.mock_zip_file
        mock_zipfile.return_value.open = mock_open_fn

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

            self.files.remove('text_file.txt')

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

    @mock.patch('zipfile.ZipFile')
    def test_load_not_supported_file_format(self, mock_zipfile):
        """Test load method from ComicZipLoader class. The load method only
         load image file.
        """

        mock_open_fn = mock.mock_open(read_data='')

        # Insert data in ZipFile mock object
        for f in ['text-file.txt']:
            self.mock_zip_file.write(f)

        mock_zipfile.return_value = self.mock_zip_file
        mock_zipfile.return_value.open = mock_open_fn

        with mock.patch.object(builtins, 'open', mock_open_fn):

            # Verify if data list is empty. To improve test precision
            self.assertListEqual(self.loader.data, [])

            with self.assertRaises(NoDataFindException):
                self.loader.load(self.comic_name)
