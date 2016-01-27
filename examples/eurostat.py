# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
import os

# jsonstat
import jsonstat

if __name__ == "__main__":
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    out_dir = os.path.join(JSONSTAT_HOME, "tmp", "examples")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    base = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/'
    # series = base + 'nama_gdp_c?precision=1&geo=EU28&unit=EUR_HAB&indic_na=B1GM&time=2011&time=2012'
    series = base + 'nama_gdp_c?precision=1&unit=EUR_HAB&indic_na=B1GM'

    json_string = jsonstat.download(series, os.path.join(out_dir, "eurostat_name_gpd_c.json"))

    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)
    collection.info()

    ds = collection.dataset('nama_gdp_c')
    ds.info()
    ds.info_dimensions()
    ds.value(geo="IT", time="1981")
