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

# jsonstat
import jsonstat

fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "www.ec.europa.eu_eurostat")
base_uri = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'


def test_one_dimension():
    uri = base_uri + 'nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'

    filename = "eurostat-name_gpd_c-geo_IT.json"
    json_string = jsonstat.download(uri, os.path.join(fixture_dir, filename))

    # extract collection
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    # extract dataset contained into collection
    ds = collection.dataset('nama_gdp_c')
    """:type: jsonstat.JsonStatDataset"""
    assert 69 == len(ds)

    time = ds.dimension('time')
    assert 69 == len(time)

    # show some values
    data = ds.data(geo="IT", time="2011")
    assert 26000 == data.value


def test_two_dimension():
    uri = base_uri + 'nama_gdp_c?precision=1&geo=FR&geo=IT&unit=EUR_HAB&indic_na=B1GM'

    filename = "eurostat-name_gpd_c-geo_IT_FR.json"
    json_string = jsonstat.download(uri, os.path.join(fixture_dir, filename))

    # extract collection
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    # extract dataset contained into collection
    ds = collection.dataset('nama_gdp_c')
    assert 138 == len(ds)

    time = ds.dimension('time')
    assert 69 == len(time)

    # show some values
    data = ds.data(geo="IT", time="2011")
    assert 26000 == data.value

    data = ds.data(geo="FR", time="2011")
    assert 30700 == data.value
