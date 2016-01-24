# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

#  stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os

# jsonstat
from jsonstat.istat.istat_helper import IstatHelper

def list_dim(istat_helper, dataset):
    """
    print some information about dimension
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
    MAIN_DIRECTORY = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(MAIN_DIRECTORY, "tmp", "istat_cached"))
    istat_helper = IstatHelper(cache_dir, lang=1)

    json_data = istat_helper.area(show=False)
    for area in json_data:
        list_dataset_dim(istat_helper, area)

