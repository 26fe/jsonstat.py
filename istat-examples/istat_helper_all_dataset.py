# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

"""
download information about all dataset from istat
using JsonStatHelper class
"""

#  stdlib
import os
import sys

# jsonstat
from istat import IstatHelper
import jsonstat


def list_dim(istat_helper, dataset):
    """
    print some information about dimension
    :type istat_helper: IstatHelper
    :param dataset:
    """
    json_data = istat_helper.dim(dataset['Cod'], show=False)
    if json_data is not None:
        msg = "dataset: '{}' '{}' dim: {}".format(dataset['Cod'], dataset['Desc'], len(json_data))
        print(msg)
    else:
        print("cannot retrieve info for dataset: {}".format(dataset))


def list_dataset_dim(istat_helper, area):
    """
    retrieve some information about dataset
    ex di area: {'Desc': 'Censimento popolazione e abitazioni 2011', 'Id': '3', 'Cod': 'CEN'}
    :type istat_helper: IstatHelper
    :param area:
    :return:
    """
    json_data = istat_helper.dslist(area['Id'], show=False)
    if json_data is not None:
        print("-------------------------")
        msg = u"area: {} '{}' nr. dataset {}".format(area['Id'], area['Desc'], len(json_data))
        print(msg)
        for dataset in json_data:
            list_dim(istat_helper, dataset)
    else:
        print("--------------")
        print("cannot retrieve info for area {}".format(area))


if __name__ == "__main__":
    # cache_dir where to store downloaded data file
    # cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "istat-tests", "fixtures", "istat_cached"))
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tmp", "istat_cached"))
    downloader = jsonstat.Downloader(cache_dir)
    istat_helper = IstatHelper(downloader, lang=1)

    json_data = istat_helper.area(show=False)
    for area in json_data:
        list_dataset_dim(istat_helper, area)
