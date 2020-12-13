# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

"""
Example of use of JsonStatIstatHelper class
"""
# stdlib
import os
import sys

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
    """retrieve some information about dataset
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
            list_dim(dataset, istat_helper)
    else:
        print("--------------")
        print("cannot retrieve info for area {}".format(area))


def list_area_dataset_dim(istat_helper):
    """
    :type istat_helper: IstatHelper
    :param istat_helper:
    :return:
    """
    json_data = istat_helper.area(show=False)
    for area in json_data:
        list_dataset_dim(istat_helper, area)


if __name__ == "__main__":
    # cache_dir where to store downloaded data file
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "istat-tests", "fixtures", "istat_cached"))
    downloader = jsonstat.Downloader(cache_dir)
    istat = IstatHelper(downloader, lang=1)

    # list_area_dataset_dim(istat_helper)

    istat.help()

    print("*** all areas")
    istat.area()

    # ...
    # {
    #      "Cod": "LAB",
    #      "Desc": "Lavoro",
    #      "Id": 26
    #  }
    # ...

    print("*** show dataset contained into area code 26 (labour)")
    istat.dslist(26)

    # ...
    # {
    #     "Cod": "DCCV_TAXDISOCCUDE",
    #     "Desc": "Tasso di disoccupazione - dati destagionalizzati",
    #     "Id": 14
    # },
    # ...

    print("*** show the dimension of dataset DCCV_TAXDISOCCUDE")
    istat.dim("DCCV_TAXDISOCCUDE")

    # ...
    # {
    # "Territorio"        :[{"Cod":1,"Desc":" Italia"},{"Cod":3,"Desc":" Nord"},{"Cod":62,"Desc":" Centro"},{"Cod":88,"Desc":" Mezzogiorno"},{"Cod":89,"Desc":" Sud"}],
    # "Tipo dato"         :[{"Cod":6,"Desc":" tasso di disoccupazione"}],
    # "Misura"            :[{"Cod":1,"Desc":" valori percentuali"},{"Cod":9,"Desc":" valori assoluti"}],
    # "Sesso"             :[{"Cod":1,"Desc":" maschi"},{"Cod":2,"Desc":" femmine"},{"Cod":3,"Desc":" totale"}],
    # "Classe di et\u00e0":[{"Cod":4,"Desc":" 15-24 anni"},{"Cod":28,"Desc":" 15 anni e pi\u00f9"}],
    # "Edizione"          :[ {"Cod":2330,"Desc":" 30-Set-2011"},
    #                        ...
    #                        {"Cod":3112,"Desc":" 01-Set-2015"},{"Cod":3127,"Desc":" 11-Dic-2015"}
    #                      ],
    # "Tempo e frequenza":[  {"Cod":1764,"Desc":" T4-1992"},{"Cod":1770,"Desc":" T1-1993"},{"Cod":1774,"Desc":" T2-1993"},{"Cod":1779,"Desc":" T3-1993"},{"Cod":1783,"Desc":" T4-1993"},{"Cod":1789,"Desc":" T1-1994"},
    #                        ...
    #                        {"Cod":2192,"Desc":" T2-2015"},{"Cod":2197,"Desc":" T3-2015"}
    #                     ]}
    # ...

    print("*** retrieve jsondata for dataset 'DCCV_TAXDISOCCUDE' using dimension '1,6,9,0,0'")
    istat.datajson('DCCV_TAXDISOCCUDE', "1,6,9,0,0")

    print("*** retrieve data in istat format for dataset 'DCCV_TAXDISOCCUDE' using dimension '1,6,9,0,0'")
    istat.table('DCCV_TAXDISOCCUDE', "1,6,9,0,0")
