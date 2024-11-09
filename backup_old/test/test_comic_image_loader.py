
from unittest import TestCase, mock
from unittest.mock import mock_open

from pynocchio.comic_file_loader_image import ComicImageLoader
from pynocchio.exception import NoDataFindException
from pynocchio.utility import IMAGE_FILE_FORMATS


class TestComicImageLoader(TestCase):
    def setUp(self):
        self.comic_image_loader = ComicImageLoader()

    @mock.patch(
        "pynocchio.comic_file_loader_dir.glob.glob1",
        lambda dir, ext: ["image"+ext[1:]]
    )
    @mock.patch(
        "pynocchio.comic_file_loader_dir.open",
        mock_open()
    )
    def test_load_images(self):
        self.comic_image_loader.load("test")
        # Assert comic_image_loader has a page corresponding to each format.
        for idx, image_format in enumerate(IMAGE_FILE_FORMATS):
            with self.subTest(image_format=image_format):
                self.assertEqual(
                    self.comic_image_loader.data[idx].data,
                    ""
                )
                self.assertEqual(
                    self.comic_image_loader.data[idx].title,
                    "image"+image_format
                )
                self.assertEqual(
                    self.comic_image_loader.data[idx].number,
                    idx+1
                )

    @mock.patch(
        "pynocchio.comic_file_loader_dir.glob.glob1",
        lambda dir, ext: []
    )
    def test_load_image_no_files(self):
        with self.assertRaises(NoDataFindException):
            self.comic_image_loader.load("test")
