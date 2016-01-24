# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
import os

# jsonstat
import jsonstat

# conf
uri = 'http://json-stat.org/samples/oecd-canada-col.json'
json_filename = "oecd-canada-col.json"

JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
out_dir = os.path.join(JSONSTAT_HOME, "tmp", "examples")
out_dir = os.path.abspath(out_dir)

# main
json_string = jsonstat.download(uri, os.path.join(out_dir, "oecd-canada-col.json"))

collection = jsonstat.JsonStatCollection()
collection.from_string(json_string)

print("*** multiple datasets info")
collection.info()

oecd = collection.dataset(0)
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
