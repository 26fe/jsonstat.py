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

# jsonstat
import jsonstat
import jsonstat.istat as istat

if __name__ == "__main__":
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tmp", "istat_cached"))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # print all istat area
    i = istat.Istat(cache_dir, 1)
    for area in i.areas():
        print(area)

    # print istat dataset contained into area 'Prices'
    area_name = 'Prices'
    print("--- list dataset in area {}".format(area_name))
    area = i.area(area_name)
    for istat_dataset in area.datasets():
        # TODO: this not works print(istat_dataset)
        print(u"{}({}):{}".format(istat_dataset.cod(), istat_dataset.nrdim(), istat_dataset.name()))

    # print some info about istat dataset 'DCSP_IPAB'
    dataset_name = 'DCSP_IPAB'
    print("--- list dimensions for dataset {}".format(dataset_name))
    istat_dataset = area.dataset(dataset_name)
    istat_dataset.info_dimensions()

    # get istat dataset with specific dimension
    json_data = istat_dataset.getvalues("1,18,0,0,0")

    # from istat dataset to jsonstat collection
    collection = jsonstat.JsonStatCollection()
    collection.from_json(json_data)
    collection.info()

    # print some info about jsonstat dataset
    jds = collection.dataset('IDMISURA1*IDTYPPURCH*IDTIME')
    jds.info()
