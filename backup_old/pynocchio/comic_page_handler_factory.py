from .comic_page_handler import ComicPageHandlerDoublePage, ComicPageHandlerSinglePage


class ComicPageHandlerFactory:
    read_mode = {
        False: ComicPageHandlerSinglePage,
        True: ComicPageHandlerDoublePage,
    }

    @staticmethod
    def create_handler(page_read_mode, comic, index=0):
        return ComicPageHandlerFactory.read_mode[page_read_mode](comic, index=index)
