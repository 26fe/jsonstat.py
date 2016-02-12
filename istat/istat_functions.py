# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# istat
from istat import Istat

__istat__ = None


def cache_dir(dir):
    global __istat__
    if __istat__ is None:
        __istat__ = Istat(dir)


def areas():
    global __istat__
    if __istat__ is None:
        __istat__ = Istat()
    return __istat__.areas()


def area(spec):
    global __istat__
    if __istat__ is None:
        __istat__ = Istat()
    return __istat__.area(spec)


def dataset(spec_area, spec_dataset):
    global __istat__
    if __istat__ is None:
        __istat__ = Istat()
    return __istat__.dataset(spec_area, spec_dataset)
