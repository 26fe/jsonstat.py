# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

"""
This module contains helper class useful exploring the Italian Statistics Institute.
"""
from istat.istat_exception import IstatException
from istat.istat_helper import IstatHelper
from istat.istat_area import IstatArea
from istat.istat_dataset import IstatDataset
from istat.istat_dimension import IstatDimension
from istat.istat_root import IstatRoot

from istat.istat_functions import (cache_dir, lang, areas, areas_as_html, area, dataset)
