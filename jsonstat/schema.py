# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os
import json


class JsonStatSchema:
    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), "jsonschema_jsonstat.json")
        jsonschema_jsonstat = open(filename).read()

        self.__all = json.loads(jsonschema_jsonstat)

        self.__dimension = self.__all.copy()
        self.__dimension["$ref"] = "#/definitions/dimension"

        self.__dataset = self.__all.copy()
        self.__dataset["$ref"] = "#/definitions/dataset"

        self.__collection = self.__all.copy()
        self.__collection["$ref"] = "#/definitions/collection"

    @property
    def dimension(self):
        return self.__dimension

    @property
    def dataset(self):
        return self.__dataset

    @property
    def collection(self):
        return self.__collection

    @property
    def all(self):
        return self.__all
