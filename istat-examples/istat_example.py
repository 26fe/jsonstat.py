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

# python 2.7.11 raise the following error
#    UnicodeEncodeError: 'ascii' codec can't encode character u'\x96' in position 17: ordinal not in range(128)
# to prevent it the following three lines are added:
# See: http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')

# jsonstat
import istat

if __name__ == "__main__":
    # cache_dir where to store downloaded data file
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "istat-tests", "fixtures", "istat_cached"))
    istat.cache_dir(cache_dir)

    # print all istat area
    for area in istat.areas():
        print(area)

    # print istat dataset contained into area 'Prices'
    area_name = 'Prices'
    print("--- list dataset in area {}".format(area_name))
    area = istat.area(area_name)
    for istat_dataset in area.datasets():
        print(istat_dataset)

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
