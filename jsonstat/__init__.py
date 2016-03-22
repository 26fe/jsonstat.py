# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

"""
jsonstat module contains classes and utility functions to parse `jsonstat data format <https://json-stat.org/>`_.
"""
from jsonstat.version import __version__

from jsonstat.exceptions import JsonStatException
from jsonstat.exceptions import JsonStatMalformedJson

from jsonstat.dimension import JsonStatDimension
from jsonstat.dataset import JsonStatDataSet
from jsonstat.collection import JsonStatCollection

from jsonstat.downloader import Downloader
from jsonstat.parse_functions import *

import os
__fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures"))
