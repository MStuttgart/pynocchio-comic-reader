import logging

import rarfile

from .comic import Page
from .comic_file_loader import ComicLoader
from .exception import NoDataFindException
from .utility import IMAGE_FILE_FORMATS, get_file_extension

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_rarfile(filename):
    """Verify if file is rar file

    Args:
        filename: name of file

    Returns: True if file is a rar file otherwise, False

    """
    return rarfile.is_rarfile(filename)


class ComicRarLoader(ComicLoader):

    def __init__(self):
        super().__init__()

    def load(self, filename):
        """Load rar file and create Page objects with them.

        Args:
            filename: name of rar file
        """

        with rarfile.RarFile(filename, "r") as rar:

            name_list = rar.namelist()
            name_list.sort()
            aux = 100.0 / max(1, len(name_list))
            page = 1
            self.data = []

            for idx, name in enumerate(name_list):

                if get_file_extension(name).lower() in IMAGE_FILE_FORMATS:
                    try:
                        self.data.append(Page(rar.read(name), name, page))
                        page += 1
                    except rarfile.BadRarFile as exc:
                        logger.exception("Error reading %s file. %s", name, exc)

                self.progress.emit(idx * aux)
            logger.info("Successfully loaded %s", filename)

        if not self.data:
            error_text = "File not loaded!"
            logger.exception(error_text)
            raise NoDataFindException(error_text)
