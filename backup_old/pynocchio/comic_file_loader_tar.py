import logging
import tarfile

from .comic import Page
from .comic_file_loader import ComicLoader
from .exception import NoDataFindException
from .utility import IMAGE_FILE_FORMATS, get_file_extension

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_tarfile(filename):
    """Verify if file is tar file

    Args:
        filename: name of file

    Returns: True if file is a tar file otherwise, False

    """
    return tarfile.is_tarfile(filename)


class TarFile(tarfile.TarFile):
    """Inherit the base class to create read and namelist methods."""

    def read(self, filename):
        """Read compact file

        Args:
            filename: name of compact file

        Returns: binary data of file
        """
        return self.extractfile(filename).read()

    def namelist(self):
        """Get the name of files on .tar file.

        Returns: list of filename

        """
        return self.getnames()


class ComicTarLoader(ComicLoader):

    def __init__(self):
        super().__init__()

    def load(self, filename):
        """Load tar file and create Page objects with them.

        Args:
            filename: name of tar file
        """

        logger.info("Trying to load %s", filename)

        with TarFile(filename, "r") as tar:

            name_list = tar.namelist()
            name_list.sort()
            aux = 100.0 / max(1, len(name_list))
            page = 1
            self.data = []

            for idx, name in enumerate(name_list):
                logger.info("Trying to load %s", name)

                if get_file_extension(name).lower() in IMAGE_FILE_FORMATS:
                    logger.info("Adding page %s", name)
                    try:
                        data = tar.read(name)
                        self.data.append(Page(data, name, page))
                        page += 1
                    except tarfile.ExtractError as exc:
                        logger.exception("Error in extract %s file. %s", name, exc)
                    except tarfile.ReadError as exc:
                        logger.exception("Error in read %s file. %s", name, exc)

                self.progress.emit(idx * aux)

        if not self.data:
            message = "File not loaded"
            logger.exception(message)
            raise NoDataFindException(message)
