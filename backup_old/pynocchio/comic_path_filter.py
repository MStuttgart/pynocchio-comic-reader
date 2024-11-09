import glob

from .exception import NoDataFindException
from .utility import join_path


class ComicPathFilter:

    def __init__(self, extension_list):
        self.file_list = []
        self.current_path = None
        self.extension_list = extension_list
        self.current_index = None

    def parse(self, path, isdir=False):

        self.current_path = path
        self.file_list = []

        if isdir:
            self.file_list = [None]
            return

        for ext in self.extension_list:
            self.file_list.extend(glob.glob1(path, "*" + ext))

        # sort list
        self.file_list.sort()

    def is_first_comic(self, filename):
        try:
            return self.file_list[0] == filename or self.file_list[0] is None
        except IndexError as exc:
            raise NoDataFindException("ComicPathFilter file list is empty!") from exc

    def is_last_comic(self, filename):
        try:
            return self.file_list[-1] == filename or self.file_list[-1] is None
        except IndexError as exc:
            raise NoDataFindException("ComicPathFilter file list is empty!") from exc

    def get_previous_comic(self, filename):

        if not self.is_first_comic(filename) and filename in self.file_list:
            name = self.file_list[self.file_list.index(filename) - 1]
            return join_path(self.current_path, "", name)
        else:
            raise NoDataFindException("ComicPathFilter reach first file!")

    def get_next_comic(self, filename):

        if not self.is_last_comic(filename) and filename in self.file_list:
            name = self.file_list[self.file_list.index(filename) + 1]
            return join_path(self.current_path, "", name)
        else:
            raise NoDataFindException("ComicPathFilter reach last file!")
