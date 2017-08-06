# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os

# external modules
import pytest

# jsonstat/istat
import jsonstat
import istat

fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")
downloader = jsonstat.Downloader(fixture_dir)
i_en = istat.IstatRoot(downloader, lang=1)


def test_istat_root():
    i_it = istat.IstatRoot(downloader, lang=0)
    assert i_it.cache_dir() == fixture_dir


def test_istat_italian():
    i_it = istat.IstatRoot(downloader, lang=0)
    n = i_it.area(26).desc
    assert "Lavoro" == n

    d = i_it.area(26).dataset('DCCV_INATTIVMENS').name
    assert u'Inattivi - dati mensili' == d

    dname = i_it.area(26).dataset('DCCV_INATTIVMENS').dimension(0).name
    assert "Territorio" == dname


def test_istat_english():
    n = i_en.area(26).desc
    assert "Labour" == n

    d = i_en.area(26).dataset('DCCV_INATTIVMENS').name
    assert u'Inactive population - monthly data' == d

    dim = i_en.area(26).dataset('DCCV_INATTIVMENS').dimension(0)
    assert 'Territory' == dim.name

    dname = i_en.area(26).dataset('DCCV_INATTIVMENS').dimension(0).name
    assert "Territory" == dname


#
# IstatArea
#
def test_areas():
    lst = i_en.areas()
    """:type: istat.IstatAreaList"""
    assert isinstance(lst, istat.IstatAreaList)

    html = lst._repr_html_()
    assert len(html) > 0


def test_area():
    istat_area = i_en.area(3)
    """:type: istat.IstatArea"""
    assert "CEN" == istat_area.cod

    html = istat_area._repr_html_()
    assert len(html) > 0


#
# IstatDataset
#

def test_area_datasets():
    istat_area_name = 'Prices'
    istat_dataset_name = 'DCSP_IPAB'

    istat_area = i_en.area(istat_area_name)
    """:type: istat.IstatArea"""

    lst = istat_area.datasets()
    """:type:istat.IstatDatasetList"""
    html = lst._repr_html_()
    assert len(html) > 0

    istat_dataset = istat_area.dataset(istat_dataset_name)
    """:type: istat.IstatDataset"""
    s = istat_dataset.__str__()
    assert len(s) > 0

    html = istat_dataset._repr_html_()
    assert len(html) > 0


def test_dataset():
    istat_area_name = 'Prices'
    istat_dataset_name = 'DCSP_IPAB'

    istat_dataset = i_en.dataset(istat_area_name, istat_dataset_name)
    istat_dimension = istat_dataset.dimension(0)
    assert "Territory" == istat_dimension.name

    collection = istat_dataset.getvalues("1,18,0,0,0")
    assert 1 == len(collection)

    dataset = collection.dataset(0)
    assert 'IDMISURA1*IDTYPPURCH*IDTIME' == dataset.name

    # same istat dataset with explicit dimension
    spec = {
        "Territory": 1,
        "Index type": 18,
        # "Measure": 0,
        # "Purchases of dwelling": 0,
        # "Time and frequency": 0
    }
    collection = istat_dataset.getvalues(spec)
    dataset = collection.dataset(0)
    assert 'IDMISURA1*IDTYPPURCH*IDTIME' == dataset.name
    assert 207 == len(dataset)

    # same istat dataset with explicit dimension
    spec = {
        "Territory": 'Italy',
        "Index type": 18,
        # "Measure": 0,
        # "Purchases of dwelling": 0,
        # "Time and frequency": 0
    }
    collection = istat_dataset.getvalues(spec)
    dataset = collection.dataset(0)
    assert 'IDMISURA1*IDTYPPURCH*IDTIME' == dataset.name
    assert 207 == len(dataset)
