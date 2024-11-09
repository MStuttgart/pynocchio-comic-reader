import os

from PySide6 import QtGui

IMAGE_FILE_FORMATS = [f".{str(ext)}" for ext in QtGui.QImageReader.supportedImageFormats()]

COMPACT_FILE_FORMATS = [
    ".cbr",
    ".cbz",
    ".rar",
    ".zip",
    ".tar",
    ".cbt",
]

SUPPORTED_FILES = IMAGE_FILE_FORMATS + COMPACT_FILE_FORMATS


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


def get_dir_name(file_path):
    return os.path.dirname(file_path)


def get_base_name(file_path):
    return os.path.basename(file_path)


def get_parent_path(file_path):
    return os.path.split(os.path.abspath(os.path.dirname(file_path)))[0]


def join_path(root_dir, directory, filename):
    return os.path.join(root_dir, directory, filename)


def path_exist(file_path):
    return os.path.lexists(file_path)


def file_exist(file_path):
    return os.path.exists(file_path)


def is_dir(file_path):
    return os.path.isdir(file_path)


def is_file(filename):
    return os.path.isfile(filename)


def convert_string_to_boolean(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        raise ValueError
