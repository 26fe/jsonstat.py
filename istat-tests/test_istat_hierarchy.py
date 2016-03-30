# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

# jsonstat/istat
import jsonstat
import istat


class TestIstat(unittest.TestCase):

    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")
        self.downloader = jsonstat.Downloader(self.fixture_dir)
        self.i_en = istat.IstatRoot(self.downloader, lang=1)

    def test_istat_root(self):
        i_it = istat.IstatRoot(self.downloader, lang=0)
        self.assertEquals(i_it.cache_dir(), self.fixture_dir)

    def test_istat_italian(self):
        i_it = istat.IstatRoot(self.downloader, lang=0)
        n = i_it.area(26).desc()
        self.assertEqual("Lavoro", n)

        d = i_it.area(26).dataset('DCCV_INATTIVMENS').did()
        self.assertEqual(u'Inattivi - dati mensili', d)

        dname = i_it.area(26).dataset('DCCV_INATTIVMENS').dimension(0).did()
        self.assertEqual("Territorio", dname)

    def test_istat_english(self):
        n = self.i_en.area(26).desc()
        self.assertEqual("Labour", n)

        d = self.i_en.area(26).dataset('DCCV_INATTIVMENS').did()
        self.assertEqual(u'Inactive population - monthly data', d)

        dim = self.i_en.area(26).dataset('DCCV_INATTIVMENS').dimension(0)
        self.assertEqual('Territory', dim.did())
        
        dname = self.i_en.area(26).dataset('DCCV_INATTIVMENS').dimension(0).did()
        self.assertEqual("Territory", dname)

    def test_areas(self):
        istat_area = self.i_en.area(3)
        self.assertEqual("CEN", istat_area.cod())

    def test_dataset(self):
        istat_area_name = 'Prices'
        istat_dataset_name = 'DCSP_IPAB'

        istat_dataset = self.i_en.dataset(istat_area_name, istat_dataset_name)
        istat_dimension = istat_dataset.dimension(0)
        self.assertEqual("Territory", istat_dimension.did())

        collection = istat_dataset.getvalues("1,18,0,0,0")
        self.assertEqual(1, len(collection))

        dataset = collection.dataset(0)
        self.assertEqual('IDMISURA1*IDTYPPURCH*IDTIME', dataset.did())

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
        self.assertEqual('IDMISURA1*IDTYPPURCH*IDTIME', dataset.did())
        self.assertEquals(207, len(dataset))

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
        self.assertEqual('IDMISURA1*IDTYPPURCH*IDTIME', dataset.did())
        self.assertEquals(207, len(dataset))

if __name__ == '__main__':
    unittest.main()
