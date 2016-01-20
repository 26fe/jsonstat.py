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
        :return: the content of url (str type)
        """

        # note: html must be a str type not byte type
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
        it writes content to pathname
        :param pathname:
        :param content:
        """
        # note:
        # in python 3 file must be open without b (binary) option to write string
        # otherwise the following error will be generated
        # TypeError: a bytes-like object is required, not 'str'
        f = open(pathname, 'w')
        f.write(content)
        f.close()

    def __read_cached_page(self, pathname):
        """
        it reads content from pathname
        :param pathname:
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
    :return: the content of url
    """
    d = Downloader(os.path.dirname(pathname))
    return d.download(url, os.path.basename(pathname))
