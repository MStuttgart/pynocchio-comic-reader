import os

import peewee

from .settings_manager import SettingsManager
from .utility import get_dir_name


# get settings path. In Linux is .config/Pynocchio
def get_settings_path():
    path = get_dir_name(SettingsManager().settings.fileName())
    return os.path.join(path, "bookmark.db")


db = peewee.SqliteDatabase(get_settings_path())


class BookmarkBaseModel(peewee.Model):
    class Meta(object):
        database = db


class Bookmark(BookmarkBaseModel):
    comic_id = peewee.PrimaryKeyField(unique=True, index=True)
    comic_path = peewee.CharField(unique=True)
    comic_name = peewee.CharField(default="")
    comic_page = peewee.IntegerField(default=0)
    page_data = peewee.BlobField(null=True, default=None)


class TemporaryBookmark(Bookmark):
    pass
