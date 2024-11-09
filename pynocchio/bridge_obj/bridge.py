# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QmlSingleton

QML_IMPORT_NAME = "bridge"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):

    @Slot(str, result=bool)
    def openComic(self, file_path):

        print(file_path)
        return True
