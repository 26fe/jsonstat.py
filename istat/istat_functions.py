# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# jsonstat
import jsonstat

# istat
from istat.istat_root import IstatRoot

# global module variable (simulate a singleton)
__istat__ = None


def cache_dir(cache_dir=None, time_to_live=None):
    """Manage the directory ``cached_dir`` where to store downloaded files

    without parameter get the directory
    with a parameter set the directory
    :param time_to_live:
    :param cache_dir:
    """
    global __istat__

    if cache_dir is None:
        if __istat__ is None:
            __istat__ = IstatRoot()
        return __istat__.cache_dir()

    downloader = jsonstat.Downloader(cache_dir, time_to_live)
    __istat__ = IstatRoot(downloader, lang=1)
    return __istat__.cache_dir()


def lang(lg):
    global __istat__
    if __istat__ is None:
        downloader = jsonstat.Downloader(cache_dir="./istat_cached", time_to_live=None)
        __istat__ = IstatRoot(downloader, lang=lg)
    __istat__.lang(lg)
    return lg


def areas():
    """returns a list of IstatArea objects representing all the area used to classify datasets"""
    global __istat__
    if __istat__ is None:
        downloader = jsonstat.Downloader(cache_dir="./istat_cached", time_to_live=None)
        __istat__ = IstatRoot(downloader)
    return __istat__.areas()


def area(spec):
    """returns a IstatArea object conforming to ``spec``.
    :param spec: name of istat area
    """
    global __istat__
    if __istat__ is None:
        downloader = jsonstat.Downloader(cache_dir="./istat_cached", time_to_live=None)
        __istat__ = IstatRoot(downloader)
    return __istat__.area(spec)


def dataset(spec_area, spec_dataset):
    """returns the IstatDataset identified by ``spec_dataset``` (name of the dataset)
    contained into the IstatArea identified by ```spec_area``` (name of the area)
    :param spec_area: name of istat area
    :param spec_dataset: name of istat dataset
    """
    global __istat__
    if __istat__ is None:
        downloader = jsonstat.Downloader(cache_dir="./istat_cached", time_to_live=None)
        __istat__ = IstatRoot(downloader)
    return __istat__.dataset(spec_area, spec_dataset)
