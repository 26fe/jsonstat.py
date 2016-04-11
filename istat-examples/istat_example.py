# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

"""
Example how to use istat classes for downloading a dataset from istat
"""
# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

# TODO: remove following hack
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')

# jsonstat
JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
try:
    import istat
    import jsonstat
except ImportError:
    sys.path.append(JSONSTAT_HOME)
    import istat
    import jsonstat

if __name__ == "__main__":
    # cache_dir where to store downloaded data file
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "istat-tests", "fixtures", "istat_cached"))

    # print all istat area
    downloader = jsonstat.Downloader(cache_dir)
    i = istat.IstatRoot(downloader, lang=1)
    for area in i.areas():
        print(area)

    # print istat dataset contained into area 'Prices'
    area_name = 'Prices'
    print("--- list dataset in area {}".format(area_name))
    area = i.area(area_name)
    for istat_dataset in area.datasets():
        # TODO: this not works print(istat_dataset)
        try:
            print(u"{}({}):{}".format(istat_dataset.cod, istat_dataset.nrdim(), istat_dataset.name))
        except istat.IstatException as e:
            # ignore exception
            # TODO: better diagnostic?
            print(e)

    # print some info about istat dataset 'DCSP_IPAB'
    dataset_name = 'DCSP_IPAB'
    print("--- list dimensions for dataset {}".format(dataset_name))
    istat_dataset = area.dataset(dataset_name)
    istat_dataset.info_dimensions()

    # get istat dataset with specific dimension
    collection = istat_dataset.getvalues("1,18,0,0,0")
    print(collection)

    # print some info about jsonstat dataset
    jds = collection.dataset('IDMISURA1*IDTYPPURCH*IDTIME')
    print(jds)
