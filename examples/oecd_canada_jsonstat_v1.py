# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# download from internet a jsonstat file version 1.0
# print some info about downloaded file

# stdlib
from __future__ import print_function
import os

# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
import sys
# TODO: remove following hack
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')

# jsonstat
JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
try:
    import jsonstat
except ImportError:
    sys.path.append(JSONSTAT_HOME)
    import jsonstat


def test(uri, cache_dir, json_filename):
    pathname = os.path.join(cache_dir, json_filename)
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

    print("\n*** value oecd(area:IT,year:2012): {}".format(oecd.data(area='IT', year='2012')))

    print("\ngenerate all vec")
    oecd.generate_all_vec(area='CA')

    df = oecd.to_data_frame('year', content='id', blocked_dims={'area':'CA'})
    print(df)

    table = oecd.to_table()

if __name__ == "__main__":
    uri = 'http://json-stat.org/samples/oecd-canada.json'
    json_filename = "oecd-canada.json"

    # cache_dir where to store downloaded data file
    JSONSTAT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tests", "fixtures", "json-stat.org"))
    test(uri, cache_dir, json_filename)