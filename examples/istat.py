# -*- coding: utf-8 -*-

# stdlib
from __future__ import print_function
import os
# jsonstat
import jsonstat
import jsonstat.istat

if __name__ == "__main__":
    JSONSTAT_HOME = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = os.path.normpath(os.path.join(JSONSTAT_HOME, "tmp", "istat_cached"))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    i = jsonstat.istat.Istat(cache_dir, 1)
    for a in i.areas():
        print(a.info())

    aname = 'Prices'
    print("--- list dataset in area {}".format(aname))
    a = i.area(aname)

    for ds in a.datasets():
        print(u"{}({}):{}".format(ds.cod(), ds.nrdim(), ds.name()))

    dname = 'DCSP_IPAB'
    print("--- list dimesions for dataset {}".format(dname))
    ds = a.dataset(dname)
    ds.info_dimensions()
    json_data = ds.getvalues("1,18,0,0,0")

    multi = jsonstat.JsonStatCollection()
    multi.from_json(json_data)
    multi.info()
    jds = multi.dataset('IDMISURA1*IDTYPPURCH*IDTIME')
    jds.info()
