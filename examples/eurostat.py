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
    json_string = jsonstat.download(uri, os.path.join(out_dir, filename))

    # extract collection
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)
    print(collection)

    # extract dataset contained into collection
    ds = collection.dataset('nama_gdp_c')
    print(ds)
    ds.info_dimensions()

    # show some values
    v = ds.value(geo="IT", time="2011")
    print("IT gdp in 2011 was {}".format(v))


if __name__ == "__main__":
    # cache directory where store json data download from internet
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    out_dir = os.path.join(JSONSTAT_HOME, "tmp", "examples")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    base = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'

    uri = base + 'nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c-geo_IT.json"
    test(uri, filename)

    uri = base + 'nama_gdp_c?precision=1&unit=EUR_HAB&indic_na=B1GM'
    filename = "eurostat-name_gpd_c.json"
    test(uri, filename)

