#
# stdlib
#
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
    def __init__(self, dir="."):
        self.__dir = dir

    def download(self, url, filename):

        filename = os.path.join(self.__dir, filename)

        if not self.__is_cached(filename):
            html = urllib2.urlopen(url).read()
            self.__write_page_from_cache(filename, html)
        html = self.__read_cached_page(filename)
        return html

    #
    # check if pathname exists
    #
    def __is_cached(self, pathname):
        return os.path.exists(pathname)

    #
    # write content to pathname
    #
    def __write_page_from_cache(self, pathname, content):
        f = open(pathname, 'w')
        f.write(content)
        f.close()

    #
    # read content from pathname
    #
    def __read_cached_page(self, pathname):
        f = open(pathname, 'r')
        content = f.read()
        f.close()
        return content


#
# download a url in pathname
#
def download(url, pathname):
    return Downloader(os.path.dirname(pathname)).download(url, os.path.basename(pathname))
