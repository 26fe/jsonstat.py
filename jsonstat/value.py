# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from collections import namedtuple


class JsonStatValue(namedtuple('JsonStatValue', ['idx', 'value', 'status'])):
    """Represents a value (datapoint) contained into JsonStatDataset"""
    pass
