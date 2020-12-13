# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os

# jsonstat
import jsonstat


def test(uri, filename):
    json_string = jsonstat.download(uri, filename)
    collection = jsonstat.JsonStatCollection()
    collection.from_string(json_string)

    print("*** multiple datasets info")
    print(collection)
    oecd = collection.dataset(0)

    print("\n*** dataset '{}' info".format(oecd.name))
    print(oecd)
    for d in oecd.dimensions():
        print("\n*** info for dimensions '{}'".format(d.did))
        print(d)

    print("\n*** value oecd(area:IT,year:2012): {}".format(oecd.data(area='IT', year='2012')))

    print("\ngenerate all vec")
    oecd.generate_all_vec(area='CA')
    df = oecd.to_data_frame('year', content='id', blocked_dims={'area': 'CA'})
    print(df)


if __name__ == "__main__":
    uri = 'http://json-stat.org/samples/oecd-canada-col.json'
    filename = "oecd-canada-col.json"

    # store downloaded data file in cache_dir
    cache_dir = os.path.join(jsonstat._examples_dir, "www.json-stat.org")
    jsonstat.cache_dir(cache_dir)
    test(uri, filename)
