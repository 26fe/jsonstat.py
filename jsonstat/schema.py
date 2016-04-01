# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import os
import json


class JsonStatSchema:
    def __init__(self):
        # definitions = {
        #     "definitions": {
        #
        #         # version was introduced in version 2.0.
        #         "version": {"type": "string", "pattern": "^[0-9]+\.[0-9]+$"},
        #
        #         # parse date like 2012-12-27T12:25:09Z
        #         "updated": {"type": "string", "format": "date-time"},
        #
        #         # parse href field
        #         "href": {"type": "string", "format": "uri"},
        #
        #         "category_index": {
        #             "anyOf": [
        #                 {"type": "array"},
        #                 {"type": "object", "properties": {"additionalProperties": {"type": "number"}}}
        #             ]
        #         },
        #
        #         "category_unit": {
        #             "type": "object",
        #             "properties": {
        #                 "additionalProperties": {
        #                     "type": "object",
        #                     "properties": {"label": {"type": "string"},
        #                                    "decimals": {"type": "number"},
        #                                    "type": {"type": "string"},
        #                                    "base": {"type": "string"},
        #                                    "multiplier": {"type": "number"},
        #                                    "position": {"type": "string"}},
        #                     "additionalProperties": False
        #                 }
        #             }
        #         },
        #
        #         "category": {
        #             "type": "object",
        #             "properties": {
        #                 "index": {"$ref": "#/definitions/category_index"},
        #                 "label": {"type": "object"},
        #                 "note": {"type": "array"},
        #                 "unit": {"$ref": "#/definitions/category_index"},
        #                 "child": {"type": "object", "properties": {"additionalProperties": {"type": "array"}}},
        #                 "coordinates": {"type": "object",
        #                                 "properties": {"additionalProperties": {"type": "array"}}}
        #             },
        #             "additionalProperties": False
        #         },
        #
        #         "dimension": {
        #             "type": "object",
        #             "properties": {
        #                 "version": {"$ref": "#/definitions/version"},
        #                 "href": {"$ref": "#/definitions/href"},
        #                 "class": {"type": "string", "enum": ["dimension"]},
        #                 "label": {"type": "string"},
        #                 "note": {"type": "array"},
        #                 "category": {"$ref": "#/definitions/category"}
        #             },
        #             "additionalProperties": False
        #         },
        #
        #         "dataset_role": {
        #             "type": "object",
        #             "properties": {
        #                 "time": {"type": "array", "items": {"type": "string"}},
        #                 "geo": {"type": "array", "items": {"type": "string"}},
        #                 "metric": {"type": "array", "items": {"type": "string"}}
        #             },
        #             "additionalProperties": False
        #         },
        #
        #         "dataset_value": {
        #             "anyOf": [
        #                 {"type": "array", "items": {"anyOf": [
        #                     {"type": "number"},
        #                     {"type": "null"},
        #                     {"type": "string"}
        #                 ]}},
        #                 {"type": "object",
        #                  "properties": {"additionalProperties": {"type": "number"}}}]
        #         },
        #
        #         "dataset_link": {
        #             "type": "object",
        #             "properties": {
        #                 "additionalProperties": {
        #                     "type": "array",
        #                     "items": {"type": "object",
        #                               "properties": {"href": {"$ref": "#/definitions/href"},
        #                                              "type": {"type": "string"}},
        #                               "additionalProperties": False
        #                               }
        #                 }
        #             }
        #         },
        #
        #         "dataset": {
        #             "type": "object",
        #             "properties": {
        #                 "version": {"$ref": "#/definitions/version"},
        #                 "class": {"type": "string", "enum": ["dataset"]},
        #                 "href": {"$ref": "#/definitions/href"},
        #                 "label": {"type": "string"},
        #                 "note": {"type": "array"},
        #                 "source": {"type": "string"},
        #                 "updated": {"$ref": "#/definitions/updated"},
        #                 "id": {"type": "array", "items": {"type": "string"}},
        #                 "size": {"type": "array", "items": {"type": "number"}},
        #                 "role": {"$ref": "#/definitions/dataset_role"},
        #                 "dimension": {"type": "object",
        #                               "properties": {"additionalProperties": {"$ref": "#/definitions/dimension"}}},
        #                 "value": {"$ref": "#/definitions/dataset_value"},
        #                 "status": {"anyOf": [{"type": "string"},
        #                                      {"type": "array"},
        #                                      {"type": "object"}]},
        #                 "link": {"$ref": "#/definitions/dataset_link"},
        #                 "extension": {"type": "object"},
        #             },
        #             "additionalProperties": False
        #         },
        #
        #         "collection": {
        #             "type": "object",
        #             "properties": {
        #                 "version": {"$ref": "#/definitions/version"},
        #                 "class": {"type": "string", "enum": ["collection"]},
        #                 "href": {"$ref": "#/definitions/href"},
        #                 "label": {"type": "string"},
        #                 "updated": {"$ref": "#/definitions/updated"},
        #                 "link": {"type": "object",
        #                          "properties": {
        #                              "item": {
        #                                  "type": "array",
        #                                  "items": {"$ref": "#/definitions/dimension_or_dataset_or_collection"}}}
        #                          }
        #             }
        #         },
        #
        #         "dimension_or_dataset_or_collection": {
        #             "anyOf": [
        #                 {"$ref": "#/definitions/dimension"},
        #                 {"$ref": "#/definitions/dataset"},
        #                 {"$ref": "#/definitions/collection"}
        #             ]
        #         }
        #
        #     }
        # }

        filename = os.path.join(os.path.dirname(__file__), "jsonschema_jsonstat.json")
        definitions_string = open(filename).read()

        definitions = json.loads(definitions_string)
        self.__dimension = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "$ref": "#/definitions/dimension"
        }

        self.__dimension.update(definitions)

        self.__dataset = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "$ref": "#/definitions/dataset"
        }
        self.__dataset.update(definitions)

        self.__collection = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "$ref": "#/definitions/collection"
        }
        self.__collection.update(definitions)

        self.__all = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "jsonstat format",
            "description": "jsonstat format",
            "id": "http://json-stat.org/schema/v2.0/jsonstat.json",
            "$ref": "#/definitions/dimension_or_dataset_or_collection"
        }
        self.__all.update(definitions)

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
