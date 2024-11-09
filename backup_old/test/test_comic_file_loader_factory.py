
from unittest import TestCase, mock

from pynocchio.comic_file_loader_factory import ComicLoaderFactory
from pynocchio.comic_file_loader_image import ComicImageLoader
from pynocchio.comic_file_loader_rar import ComicRarLoader
from pynocchio.comic_file_loader_tar import ComicTarLoader
from pynocchio.comic_file_loader_zip import ComicZipLoader
from pynocchio.exception import InvalidTypeFileException
from pynocchio.utility import IMAGE_FILE_FORMATS


class TestComicLoaderFactory(TestCase):

    def test_create_loader_invalid_type(self):
        with self.assertRaises(InvalidTypeFileException):
            ComicLoaderFactory.create_loader("test.sh")

    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_zipfile",
        lambda filename: True
    )
    def test_create_loader_zip(self):
        loader = ComicLoaderFactory.create_loader("test.zip")
        self.assertTrue(isinstance(loader, ComicZipLoader))

    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_rarfile",
        lambda filename: True
    )
    def test_create_loader_rar(self):
        loader = ComicLoaderFactory.create_loader("test.rar")
        self.assertTrue(isinstance(loader, ComicRarLoader))

    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_rarfile",
        lambda filename: False
    )
    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_tarfile",
        lambda filename: True
    )
    def test_create_loader_tar(self):
        loader = ComicLoaderFactory.create_loader("test.tar")
        self.assertTrue(isinstance(loader, ComicTarLoader))

    def test_create_loader_images(self):
        for image_format in IMAGE_FILE_FORMATS:
            with self.subTest(image_format=image_format):
                loader = ComicLoaderFactory.create_loader("test"+image_format)
                self.assertTrue(isinstance(loader, ComicImageLoader))

    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_rarfile",
        lambda filename: False
    )
    @mock.patch(
        "pynocchio.comic_file_loader_factory.is_tarfile",
        lambda filename: False
    )
    def test_create_loader_archive_type_but_not_archive(self):
        for archive_format in [".cbt", ".cbr", "cbz"]:
            with self.subTest(archive_format=archive_format):
                with self.assertRaises(InvalidTypeFileException):
                    loader = ComicLoaderFactory.create_loader(
                        "test"+archive_format
                    )
                    assert loader
