# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# istat
from istat.istat_root import IstatRoot

__istat__ = None


def cache_dir(cached_dir='', time_to_live=None):
    """ Manage the directory where to store downloaded file

    without parameter get the directory
    with a parameter set the directory
    """
    global __istat__

    if cached_dir == '':
        if __istat__ is None:
            __istat__ = IstatRoot()
        return __istat__.cache_dir()

    __istat__ = IstatRoot(cached_dir, time_to_live, lang=1)
    return __istat__.cache_dir()


# todo new function to select language istat.lang(lang)

def areas():
    global __istat__
    if __istat__ is None:
        __istat__ = IstatRoot()
    return __istat__.areas()


def areas_as_html():
    global __istat__
    if __istat__ is None:
        __istat__ = IstatRoot()
    return __istat__.areas_as_html()


def area(spec):
    global __istat__
    if __istat__ is None:
        __istat__ = IstatRoot()
    return __istat__.area(spec)


def dataset(spec_area, spec_dataset):
    global __istat__
    if __istat__ is None:
        __istat__ = IstatRoot()
    return __istat__.dataset(spec_area, spec_dataset)
