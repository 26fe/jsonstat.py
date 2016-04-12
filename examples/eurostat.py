# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
import os

# jsonstat
import jsonstat


def test(uri, filename):
    print("downloading data from '{}'".format(uri))

    # extract collection
    collection = jsonstat.from_url(uri, filename)
    print(collection)

    # extract dataset contained into collection
    ds = collection.dataset('nama_gdp_c')
    print(ds)

    # show some values
    v = ds.data(geo="IT", time="2011")
    print("IT gdp in 2011 was {}".format(v))


if __name__ == "__main__":
    # cache_dir directory where store json data downloaded from internet
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tests", "fixtures", "www.ec.europa.eu_eurostat"))
    jsonstat.cache_dir(cache_dir)

    base = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'
    uri = base + 'nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c-geo_IT.json"
    test(uri, filename)

    print("*" * 60)

    uri = base + 'nama_gdp_c?precision=1&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c.json"
    test(uri, filename)
