# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals

# jsonstat


class JsonStatException(Exception):
    # def __init__(self, message, errors):
    #     # Call the base class constructor with the parameters it needs
    #     super(JsonStatException, self).__init__(message)
    #     # Now for your custom code...
    #     self.errors = errors
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class JsonStatMalformedJson(JsonStatException):
    pass