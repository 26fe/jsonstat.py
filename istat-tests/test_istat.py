# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

# jsonstat
import istat as istat


class TestIstat(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "istat")

    def test_istat_italian(self):
        i = istat.Istat(self.fixture_dir, lang=0)
        n = i.area(26).desc()
        self.assertEqual("Lavoro", n)

        d = i.area(26).dataset('DCCV_INATTIVMENS').name()
        self.assertEqual(u'Inattivi - dati mensili', d)

        dname = i.area(26).dataset('DCCV_INATTIVMENS').dimension(0).name()
        self.assertEqual("Territorio", dname)

    def test_istat_english(self):
        i = istat.Istat(self.fixture_dir, lang=1)
        n = i.area(26).desc()
        self.assertEqual("Labour", n)

        d = i.area(26).dataset('DCCV_INATTIVMENS').name()
        self.assertEqual(u'Inactive population - monthly data', d)

        dim = i.area(26).dataset('DCCV_INATTIVMENS').dimension(0)
        self.assertEqual('Territory', dim.name())
        
        dname = i.area(26).dataset('DCCV_INATTIVMENS').dimension(0).name()
        self.assertEqual("Territory", dname)

    def test_areas(self):
        i = istat.Istat(self.fixture_dir, lang=1)
        istat_area = i.area(3)
        self.assertEqual("CEN", istat_area.cod())

    def test_dataset(self):
        i = istat.Istat(self.fixture_dir, lang=1)
        istat_area_name = 'Prices'
        istat_dataset_name = 'DCSP_IPAB'
        istat_dataset = i.dataset(istat_area_name, istat_dataset_name)
        istat_dimension = istat_dataset.dimension(0)
        self.assertEqual("Territory", istat_dimension.name())

        collection = istat_dataset.getvalues("1,18,0,0,0")
        self.assertEqual(1, len(collection))

        dataset = collection.dataset(0)
        self.assertEqual('IDMISURA1*IDTYPPURCH*IDTIME', dataset.name())

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
        self.assertEqual('IDMISURA1*IDTYPPURCH*IDTIME', dataset.name())


if __name__ == '__main__':
    unittest.main()
