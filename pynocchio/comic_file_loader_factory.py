import logging

from .comic_file_loader_dir import ComicDirLoader, is_directory
from .comic_file_loader_image import ComicImageLoader
from .comic_file_loader_rar import ComicRarLoader, is_rarfile
from .comic_file_loader_tar import ComicTarLoader, is_tarfile
from .comic_file_loader_zip import ComicZipLoader, is_zipfile
from .exception import InvalidTypeFileException
from .utility import IMAGE_FILE_FORMATS, SUPPORTED_FILES, get_file_extension

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ComicLoaderFactory:

    @staticmethod
    def create_loader(filename):
        if is_directory(dirname=filename):
            logger.info("Creating dir loader")
            return ComicDirLoader()

        file_extension = get_file_extension(filename=filename)
        if file_extension not in SUPPORTED_FILES:
            message = "File format is not supported: %s" % file_extension
            logger.exception(message)
            raise InvalidTypeFileException(message)

        if file_extension in IMAGE_FILE_FORMATS:
            logger.info("Creating image loader")
            return ComicImageLoader()

        elif is_zipfile(filename=filename):
            logger.info("Creating zip loader")
            return ComicZipLoader()
        elif is_rarfile(filename=filename):
            logger.info("Creating rar loader")
            return ComicRarLoader()
        elif is_tarfile(filename=filename):
            logger.info("Creating tar loader")
            return ComicTarLoader()
        else:
            message = "File is not suported: %s" % file_extension
            logger.exception(message)
            raise InvalidTypeFileException(message)
