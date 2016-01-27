# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# download from internet a jsonstat file version 1.0
# print some info about downloaded file

# stdlib
from __future__ import print_function
import os

# jsonstat
import jsonstat

# conf
uri = 'http://json-stat.org/samples/oecd-canada.json'
json_filename = "oecd-canada.json"

JSONSTAT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_dir = os.path.join(JSONSTAT_HOME, "tmp", "examples")

def test(uri, json_filename):
    pathname = os.path.join(out_dir, json_filename)
    json_string = jsonstat.download(uri, pathname)

    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    print("*** multiple datasets info")
    collection.info()

    oecd = collection.dataset('oecd')
    print("\n*** dataset {} info".format(oecd.name()))
    oecd.info()

    for d in oecd.dimensions():
        print("\n*** info for dimensions '{}'".format(d.name()))
        d.info()

    print("\n*** value oecd(area:IT,year:2012): {}".format(oecd.value(area='IT', year='2012')))

    print("\ngenerate all vec")
    oecd.generate_all_vec(area='CA')

    df = oecd.to_data_frame('year', area='CA')
    print(df)

    table = oecd.to_table()

if __name__ == "__main__":
    test(uri, json_filename)