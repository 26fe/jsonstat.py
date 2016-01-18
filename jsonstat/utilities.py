# This file is part of jsonstat.py
# stdlib
import os.path
import urllib2


# from urllib2 import Request, urlopen, URLError
# req = Request(someurl)
# try:
#     response = urlopen(req)
# except URLError as e:
#     if hasattr(e, 'reason'):
#         print 'We failed to reach a server.'
#         print 'Reason: ', e.reason
#     elif hasattr(e, 'code'):
#         print 'The server couldn\'t fulfill the request.'
#         print 'Error code: ', e.code
# else:
#     # everything is fine

class Downloader:
    """
    Helper class to download json stat file
    """
    def __init__(self, dir="."):
        self.__dir = dir

    def download(self, url, filename):

        filename = os.path.join(self.__dir, filename)

        if not self.__is_cached(filename):
            html = urllib2.urlopen(url).read()
            self.__write_page_from_cache(filename, html)
        html = self.__read_cached_page(filename)
        return html

    def __is_cached(self, pathname):
        """
        check if pathname exists
        :param pathname:
        :return:
        """
        return os.path.exists(pathname)

    def __write_page_from_cache(self, pathname, content):
        """
        write content to pathname
        :param pathname:
        :param content:
        :return:
        """
        f = open(pathname, 'w')
        f.write(content)
        f.close()

    def __read_cached_page(self, pathname):
        """
        read content from pathname
        :param pathname:
        :return:
        """
        f = open(pathname, 'r')
        content = f.read()
        f.close()
        return content


def download(url, pathname):
    """
    download a url in pathname
    :param url:
    :param pathname:
    :return:
    """
    return Downloader(os.path.dirname(pathname)).download(url, os.path.basename(pathname))
