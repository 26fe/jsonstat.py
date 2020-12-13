# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2021 gf <gf@26fe.com>
# See LICENSE file

# stdlib
import sys
import re

# external modules
import pytest

# jsonstat
import jsonstat


@pytest.fixture(scope='module')
def json_str_only_index():
    return '''
        {
            "label" : "2003-2014",
            "category" : {
                "index" : {
                    "2003" : 0,
                    "2004" : 1,
                    "2005" : 2,
                    "2006" : 3,
                    "2007" : 4,
                    "2008" : 5,
                    "2009" : 6,
                    "2010" : 7,
                    "2011" : 8,
                    "2012" : 9,
                    "2013" : 10,
                    "2014" : 11
                }
            }
        }
        '''


@pytest.fixture(scope='module')
def json_str_hole_in_index():
    return '''
        {
            "label" : "2003-2014",
            "category" : {
                "index" : {
                    "2003" : 0,
                    "2004" : 1,
                    "2005" : 2,
                    "2006" : 3,
                    "2011" : 8,
                    "2012" : 9,
                    "2013" : 10,
                    "2014" : 11
                }
            }
        }
        '''


@pytest.fixture(scope='module')
def json_str_size_one():
    return '''
            {
                "label" : "country",
                "category" : {"label" : { "CA" : "Canada" }}
            }
        '''


@pytest.fixture(scope='module')
def json_str_label_and_index():
    return '''
            {
                "label" : "OECD countries, EU15 and total",
                "category" : {
                    "index" : { "AU" : 0, "AT" : 1, "BE" : 2, "IT": 3 },
                    "label" : { "AU" : "Australia", "AT" : "Austria", "BE" : "Belgium", "CA" : "Canada", "IT":"Italy" }
                }
            }
        '''  #


# building and parsing
#

def test_getters():
    dim = jsonstat.JsonStatDimension("test_dim", 10, 0, 'role')
    assert dim.did == "test_dim"
    assert len(dim) == 10
    assert dim.pos == 0
    assert dim.role == "role"


def test_exception_not_valid():
    dim = jsonstat.JsonStatDimension("year", 10, 0, None)
    with pytest.raises(jsonstat.JsonStatException):
        dim._idx2pos('2013')


def test_exception_size(json_str_only_index):
    dim = jsonstat.JsonStatDimension("year", 10, 0, None)

    with pytest.raises(jsonstat.JsonStatException):
        dim.from_string(json_str_only_index)


def test_exception_hole_in_category_index(json_str_hole_in_index):
    dim = jsonstat.JsonStatDimension("year", 8, 0, None)
    r = re.compile("dimension 'year': index \d+ is greater than size 8")
    with pytest.raises(jsonstat.JsonStatException) as excinfo:
        dim.from_string(json_str_hole_in_index)
    assert r.match(str(excinfo.value))


def test_size_one(json_str_size_one):
    dim = jsonstat.JsonStatDimension("country", 1, 0, None)
    dim.from_string(json_str_size_one)
    assert u'country' == dim.label
    assert 1 == len(dim)


def test_exception_mismatch_index_and_label(json_str_label_and_index):
    dim = jsonstat.JsonStatDimension("year", 4, 0, None)
    with pytest.raises(jsonstat.JsonStatMalformedJson) as excinfo:
        dim.from_string(json_str_label_and_index)
    expected = "dimension 'year': label 'Canada' is associated with index 'CA' that not exists!"
    assert str(excinfo.value) == expected


#
# queries methods
#  JsonstatDimension.category()
#

def test_idx2pos(json_str_only_index):
    dim = jsonstat.JsonStatDimension("year", 12, 0, None)
    dim.from_string(json_str_only_index)
    assert dim._idx2pos("2003") == 0
    assert dim._idx2pos("2014") == 11


def test_pos2cat(json_str_only_index):
    dim = jsonstat.JsonStatDimension("year", 12, 0, None)
    dim.from_string(json_str_only_index)

    assert dim._pos2cat(0).index == "2003"
    assert dim._pos2cat(11).index == "2014"
    assert dim.category(0).index == "2003"
    assert dim.category(0).label is None


# def test_get_index(self):
#     dim = jsonstat.JsonStatDimension("year", 12, 0, None)
#     dim.from_string(self.json_str_only_index)
#
#     expected = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
#     result = dim.get_index()
#     self.assertEqual(expected, result)


#
# print/info/external representation
#

def test_info(json_str_only_index):
    dim = jsonstat.JsonStatDimension("year", 12, 0, None)
    dim.from_string(json_str_only_index)
    expected = (
        "+-----+--------+-------+\n"
        "| pos | idx    | label |\n"
        "+-----+--------+-------+\n"
        "| 0   | '2003' | ''    |\n"
        "| 1   | '2004' | ''    |\n"
        "| 2   | '2005' | ''    |\n"
        "| 3   | '2006' | ''    |\n"
        "| 4   | '2007' | ''    |\n"
        "| 5   | '2008' | ''    |\n"
        "| 6   | '2009' | ''    |\n"
        "| 7   | '2010' | ''    |\n"
        "| 8   | '2011' | ''    |\n"
        "| 9   | '2012' | ''    |\n"
        "| 10  | '2013' | ''    |\n"
        "| 11  | '2014' | ''    |\n"
        "+-----+--------+-------+"
    )
    assert expected == dim.__str__()


def test_info_with_label(json_str_size_one):
    dim = jsonstat.JsonStatDimension("concept", 1, 0, None)
    dim.from_string(json_str_size_one)
    expected = (
        "+-----+------+----------+\n"
        "| pos | idx  | label    |\n"
        "+-----+------+----------+\n"
        "| 0   | 'CA' | 'Canada' |\n"
        "+-----+------+----------+"
    )
    assert expected == dim.__str__()
