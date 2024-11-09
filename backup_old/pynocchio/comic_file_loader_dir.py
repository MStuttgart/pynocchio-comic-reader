import glob
import logging

from .comic import Page
from .comic_file_loader import ComicLoader
from .exception import NoDataFindException
from .utility import IMAGE_FILE_FORMATS, get_file_extension, is_dir, join_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_directory(dirname):
    """Verify if dirname is a directory

    Args:
        dirname: name of directory

    Returns: True if dirname is a directory otherwise, False

    """
    return is_dir(dirname)


class ComicDirLoader(ComicLoader):
    """This class loads a directory."""

    def __init__(self):
        super().__init__()

    def load(self, dirname):
        """Load image files in directory and create Page objects with them.

        Args:
            dirname: name of directory

        Raises:
            NoDataFindException: if no data loaded from directory
        """

        # get files with extension stored in ext
        logger.info("Trying to load directory %s", dirname)

        name_list = []

        for ext in IMAGE_FILE_FORMATS:
            name_list += glob.glob1(dirname, "*" + ext)

        # sort list
        name_list.sort()
        aux = 100.0 / max(1, len(name_list))
        page = 1
        self.data = []

        for idx, name in enumerate(name_list):
            logger.info("Trying to load %s", name)

            if get_file_extension(name).lower() in IMAGE_FILE_FORMATS:
                logger.info("Adding page %s", name)
                try:
                    with open(join_path("", dirname, name), "rb") as img:
                        self.data.append(Page(img.read(), name, page))
                    page += 1
                except OSError as exc:
                    logger.exception("Error in read %s file. %s", name, exc)

            self.progress.emit(idx * aux)

        if not self.data:
            message = "File not loaded"
            logger.exception(message)
            raise NoDataFindException(message)
