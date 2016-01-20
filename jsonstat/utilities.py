# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
import os.path

# packages
import requests


class Downloader:
    """
    Helper class to download json stat files.
    It has a very simple cache mechanism
    """
    def __init__(self, cache_dir="."):
        """
        initialize downloader
        :param cache_dir: directory where to store downloaded files
        """
        self.__dir = cache_dir

    def download(self, url, filename):
        """
        Download url from internet. Store the downloaded content into <cache_dir>/file.
        If <cache_dir>/file exists, it returns content from disk
        :param url: page to be donwloaded
        :param filename: filename where to store the content of url
        :return: the content of url
        """

        filename = os.path.join(self.__dir, filename)

        if not self.__is_cached(filename):
            html = requests.get(url).text
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
        f = open(pathname, 'wb')
        f.write(content)
        f.close()

    def __read_cached_page(self, pathname):
        """
        read content from pathname
        :param pathname:
        :return:
        """
        f = open(pathname, 'rb')
        content = f.read()
        f.close()
        return content


def download(url, pathname):
    """
    download a url in pathname
    :param url:
    :param pathname:
    :return: the content of url
    """
    return Downloader(os.path.dirname(pathname)).download(url, os.path.basename(pathname))
