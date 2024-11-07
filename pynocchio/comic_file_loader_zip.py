import logging
import zipfile

from .comic import Page
from .comic_file_loader import ComicLoader
from .exception import NoDataFindException
from .utility import IMAGE_FILE_FORMATS, get_file_extension

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_zipfile(filename):
    """Verify if file is zip file

    Args:
        filename: name of file

    Returns: True if file is a zip file otherwise, False

    """
    return zipfile.is_zipfile(filename)


class ComicZipLoader(ComicLoader):
    """This class load Zip compact files."""

    def __init__(self):
        super().__init__()

    def load(self, filename):
        """Load zip file and create Page objects with them.

        Args:
            filename: name of compact zip file

        Raises:
            NoDataFindException: if no data loaded from zip file
        """

        logger.info("Trying to load %s", filename)

        with zipfile.ZipFile(filename, "r") as zf:

            name_list = zf.namelist()
            name_list.sort()
            aux = 100.0 / max(1, len(name_list))
            page = 1
            self.data = []

            for idx, name in enumerate(name_list):
                logger.info("Trying to load %s", name)

                if get_file_extension(name).lower() in IMAGE_FILE_FORMATS:
                    logger.info("Adding page %s", name)
                    try:
                        self.data.append(Page(zf.read(name), name, page))
                        page += 1
                    except zipfile.BadZipfile as exc:
                        logger.exception("Error in read %s file. %s", name, exc)

                self.progress.emit(idx * aux)

        if not self.data:
            message = "File not loaded"
            logger.exception(message)
            raise NoDataFindException(message)
