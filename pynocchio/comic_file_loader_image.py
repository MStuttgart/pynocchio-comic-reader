import logging

from .comic_file_loader_dir import ComicDirLoader
from .utility import get_base_name, get_dir_name, is_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ComicImageLoader(ComicDirLoader):

    def __init__(self):
        super().__init__()

    def load(self, filename):
        """Load image file and create Page objects with them.

        Args:
            filename: name of compact image file
        """

        if is_dir(filename):
            dir_name = filename
        else:
            dir_name = get_dir_name(filename)

        super().load(dir_name)

        for i, page in enumerate(self.data):
            if page.title == get_base_name(filename):
                self.initial_page = i
