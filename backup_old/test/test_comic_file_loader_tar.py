

import builtins
import os
import random
from unittest import TestCase, mock

from pynocchio.comic_file_loader_tar import TarFile  # noqa: F401
from pynocchio.comic_file_loader_tar import ComicTarLoader, is_tarfile
from pynocchio.exception import NoDataFindException
from pynocchio.utility import IMAGE_FILE_FORMATS, get_file_extension


class TestComicTarLoader(TestCase):
    """ This class load Tar compact files.
    """

    class MockTarFile:
        """Support class to mock TarFile"""

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
        self.loader = ComicTarLoader()
        self.comic_name = 'no_existing_comic.cbt'

        self.files = [
            'text_file_01.txt',
        ]

        # Create TarFilemock object
        self.mock_tar_file = TestComicTarLoader.MockTarFile(self.comic_name)

        for idx, ext in enumerate(IMAGE_FILE_FORMATS):
            self.files.append('%d-image-file%s' % (idx, ext))

        random.shuffle(self.files)

    def test_is_tarfile(self):
        """Test is_tarfile function
        """

        with mock.patch('tarfile.is_tarfile') as mock_tar:
            mock_tar.return_value = True
            self.assertTrue(is_tarfile, True)

        with mock.patch('tarfile.is_tarfile') as mock_tar:
            mock_tar.return_value = False
            self.assertTrue(is_tarfile, False)

    @mock.patch('pynocchio.comic_file_loader_tar.TarFile')
    def test_load_supported_file_format(self, mock_tarfile):

        mock_open_fn = mock.mock_open(read_data='')

        for f in self.files:
            self.mock_tar_file.write(f)

        mock_tarfile.return_value = self.mock_tar_file
        mock_tarfile.return_value.open = mock_open_fn

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

            # The files list must be same amount of pages
            self.assertEqual(len(self.loader.data), len(self.files))

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

    @mock.patch('pynocchio.comic_file_loader_tar.TarFile')
    def test_load_not_supported_file_format(self, mock_tarfile):

        mock_open_fn = mock.mock_open(read_data='')

        mock_tarfile.return_value = self.mock_tar_file
        mock_tarfile.return_value.open = mock_open_fn

        with mock.patch.object(builtins, 'open', mock_open_fn):

            # The data list is empty
            self.assertListEqual(self.loader.data, [])

            # No image to load, then loader raise a exception
            with self.assertRaises(NoDataFindException):
                self.loader.load(self.comic_name)
