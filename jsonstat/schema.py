# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os
import json


class JsonStatSchema:
    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), "schemas", "jsonstat.json")
        jsonschema_jsonstat = open(filename).read()
        self.__all = json.loads(jsonschema_jsonstat)

        filename = os.path.join(os.path.dirname(__file__), "schemas", "collection.json")
        jsonschema_jsonstat = open(filename).read()
        self.__collection = json.loads(jsonschema_jsonstat)

        filename = os.path.join(os.path.dirname(__file__), "schemas", "dataset.json")
        jsonschema_jsonstat = open(filename).read()
        self.__dataset = json.loads(jsonschema_jsonstat)

        filename = os.path.join(os.path.dirname(__file__), "schemas", "dimension.json")
        jsonschema_jsonstat = open(filename).read()
        self.__dimension = json.loads(jsonschema_jsonstat)

        # self.__dimension = self.__all.copy()
        # self.__dimension["oneOf"] = [{
        #     "$ref": "#/definitions/dimension",
        #     "additionalProperties": False,
        #     "required": ["version", "class", "category"]
        # }]
        #
        # self.__dataset = self.__all.copy()
        # self.__dataset["oneOf"] = [{
        #     "$ref": "#/definitions/dataset",
        #     "additionalProperties": False,
        #     "required": ["version", "class", "value", "id", "size", "dimension"]
        # }]
        #
        # self.__collection = self.__all.copy()
        # self.__collection["oneOf"] = [{
        #     "$ref": "#/definitions/collection",
        #     "additionalProperties": False,
        #     "required": ["version", "class", "link"]
        # }]

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
