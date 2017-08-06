# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016-2017 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os

# external modules
import pytest

# jsonstat
import jsonstat

fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope='module')
def json_missing_value():
    return '''
        {
            "label" : "three dimensions"
        }
        '''


@pytest.fixture(scope='module')
def json_empty_value():
    return '''
        {
            "label" : "three dimensions",
            "value" : []
        }
        '''


@pytest.fixture(scope='module')
def json_missing_dimension():
    return '''
        {
            "label" : "three dimensions",
            "value" : [1,2]
        }
        '''


@pytest.fixture(scope='module')
def json_incorrect_data_size():
    return '''
        {
            "label" : "Unemployment rate in the OECD countries 2003-2014",
            "source" : "Economic Outlook No 92 - December 2012 - OECD Annual Projections",
            "value" : [1, 2, 3, 4],
            "dimension" : {
                "id" : ["area", "year"],
                "size" : [4, 12],
                "area" : {
                    "category" : { "index" : { "AU" : 0, "AT" : 1, "BE" : 2, "CA" : 3 } }
                },
                "year" : {
                    "category" : {
                        "index" : {
                            "2003" : 0, "2004" : 1, "2005" : 2, "2006" : 3, "2007" : 4,
                            "2008" : 5, "2009" : 6,
                            "2010" : 7, "2011" : 8, "2012" : 9, "2013" : 10, "2014" : 11
                        }
                    }
                }
            }
        }
        '''


#
# test exceptions
#

def test_exception_not_valid():
    dataset = jsonstat.JsonStatDataSet("canada")
    with pytest.raises(jsonstat.JsonStatException):
        dataset.data(year="2003", area="CA")


def test_empty_value(json_empty_value):
    dataset = jsonstat.JsonStatDataSet("canada")
    with pytest.raises(jsonstat.JsonStatMalformedJson) as excinfo:
        dataset.from_string(json_empty_value)
    expected = "dataset 'canada': field 'value' is empty"
    assert expected == str(excinfo.value)


def test_missing_value_field(json_missing_value):
    dataset = jsonstat.JsonStatDataSet("canada")
    with pytest.raises(jsonstat.JsonStatMalformedJson) as excinfo:
        dataset.from_string(json_missing_value)
    expected = "dataset 'canada': missing 'value' key"
    assert expected == str(excinfo.value)


def test_missing_dimension(json_missing_dimension):
    dataset = jsonstat.JsonStatDataSet("canada")
    with pytest.raises(jsonstat.JsonStatMalformedJson) as excinfo:
        dataset.from_string(json_missing_dimension)
    expected = "dataset 'canada': missing 'dimension' key"
    assert expected == str(excinfo.value)


def test_exception_dataset_size(json_incorrect_data_size):
    dataset = jsonstat.JsonStatDataSet("canada")
    with pytest.raises(jsonstat.JsonStatException) as excinfo:
        dataset.from_string(json_incorrect_data_size)
    expected = "dataset 'canada': size 4 is different from calculate size 48 by dimension"
    assert expected == str(excinfo.value)


def test_exception_no_existent_dimension():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    assert dataset.dimension("year").did == "year"
    with pytest.raises(jsonstat.JsonStatException) as excinfo:
        dataset.dimension("not existent dim")
    expected = "dataset 'canada': unknown dimension 'not existent dim' know dimensions ids are: serie, year, area"
    assert expected == str(excinfo.value)


#
# test
#

def test_name():
    dataset = jsonstat.JsonStatDataSet("canada")
    assert dataset.name == "canada"


def test_dimensions():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    assert len(dataset.dimensions()) == 3


def test_info():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)
    expected = (
        "name:   'canada'\n"
        "label:  'Unemployment rate in the OECD countries'\n"
        "source: 'Unemployment rate in the OECD countries'\n"
        "size: 12\n"
        "+-----+-------+--------------------------------+------+------+\n"
        "| pos | id    | label                          | size | role |\n"
        "+-----+-------+--------------------------------+------+------+\n"
        "| 0   | serie | serie                          | 1    |      |\n"
        "| 1   | year  | 2012-2014                      | 3    | time |\n"
        "| 2   | area  | OECD countries, EU15 and total | 4    | geo  |\n"
        "+-----+-------+--------------------------------+------+------+"
    )
    assert expected, dataset.__str__()


#
# test
#   dataset.data()
#   dataset.value()
#   dataset.status()
#

def test_data_with_three_dimensions():
    json_pathname = os.path.join(fixture_dir, "dataset", "three_dim_v1.json")
    dataset = jsonstat.JsonStatDataSet()
    dataset.from_file(json_pathname)

    data = dataset.data(one="one_1", two="two_1", three="three_1")
    assert data.value == 111
    assert data.status is None

    data = dataset.data(one="one_2", two="two_2", three="three_2")
    assert data.value == 222

    # using a bit different file
    json_pathname = os.path.join(fixture_dir, "dataset", "three_dim_size_as_string_v1.json")
    dataset = jsonstat.JsonStatDataSet()
    dataset.from_file(json_pathname)

    data = dataset.data(one="one_1", two="two_1", three="three_1")
    assert data.value == 111
    assert data.status is None

    data = dataset.data(one="one_2", two="two_2", three="three_2")
    assert data.value == 222

    # using a bit different file
    json_pathname = os.path.join(fixture_dir, "dataset", "three_dim_size_as_string_v2.json")
    dataset = jsonstat.JsonStatDataSet()
    dataset.from_file(json_pathname)

    data = dataset.data(one="one_1", two="two_1", three="three_1")
    assert data.value == 111
    assert data.status is None

    data = dataset.data(one="one_2", two="two_2", three="three_2")
    assert data.value == 222


def test_data_with_unemployment():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    data = dataset.data(area="AU", year="2012")
    assert data.value == 11

    # using label Australia instead of index AU
    data = dataset.data(area="Australia", year="2012")
    assert data.value == 11

    # using dictionary
    data = dataset.data({'area': "Australia", 'year': "2012"})
    assert data.value == 11

    data = dataset.data({'area': "AU", 'year': "2012"})
    assert data.value == 11

    data = dataset.data({"OECD countries, EU15 and total": "AU", 'year': '2012'})
    assert data.value == 11

    data = dataset.data(area="BE", year="2014")
    assert data.value == 33
    assert data.status is None


def test_data_with_oecd_canada():
    json_pathname = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "oecd-canada.json")
    collection = jsonstat.JsonStatCollection()
    collection.from_file(json_pathname)
    oecd = collection.dataset('oecd')

    data = oecd.data(concept='UNR', area='AU', year='2004')
    assert 5.39663128 == data.value
    assert data.status is None

    # first position with status at idx 10
    dcat = {'concept': 'UNR', 'area': 'AU', 'year': '2013'}
    data = oecd.data(dcat)
    assert data.status == "e"

    data = oecd.data(10)
    assert data.status == "e"

    data = oecd.data([0, 0, 10])
    assert data.status == "e"


#
# test dataset indexes transform functions
#

def test_dcat_to_lint():
    json_pathname = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "oecd-canada.json")
    collection = jsonstat.JsonStatCollection()
    collection.from_file(json_pathname)
    oecd = collection.dataset('oecd')

    dcat = {'concept': 'UNR', 'area': 'AU', 'year': '2013'}
    lint = oecd.dcat_to_lint(dcat)
    assert lint == [0, 0, 10]

    idx = oecd.lint_as_idx(lint)
    assert idx == 10


def test_idx_as_lint():
    json_pathname = os.path.join(jsonstat._examples_dir, "www.json-stat.org", "oecd-canada.json")
    collection = jsonstat.JsonStatCollection()
    collection.from_file(json_pathname)
    oecd = collection.dataset('oecd')

    lint = oecd.idx_as_lint(10)
    assert lint == [0, 0, 10]


#
# enumeration function
# all_pos test
#

def test_all_pos():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    result = list(dataset.all_pos())
    # fist digit is serie always 0
    # second digit is year from 0 to 2
    # third digit is area from 0 to 3
    # order is ["serie", "year", "area"]
    expected = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3],  # first digit 0
                [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3],  # first digit 1
                [0, 2, 0], [0, 2, 1], [0, 2, 2], [0, 2, 3]]  # first digit 2
    assert result == expected


def test_all_pos_reorder():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    result = list(dataset.all_pos(order=["area", "year", "serie"]))
    # fist digit is serie always 0
    # second digit is year from 0 to 2
    # third digit is area from 0 to 3
    # first changing digit is year (second digit)
    expected = [[0, 0, 0], [0, 1, 0], [0, 2, 0],  # last digit 0
                [0, 0, 1], [0, 1, 1], [0, 2, 1],  # last digit 1
                [0, 0, 2], [0, 1, 2], [0, 2, 2],  # last digit 2
                [0, 0, 3], [0, 1, 3], [0, 2, 3]]  # last digit 3
    assert result == expected


def test_all_pos_with_block():
    json_pathname = os.path.join(fixture_dir, "dataset", "dataset_unemployment_v1.json")
    dataset = jsonstat.JsonStatDataSet("canada")
    dataset.from_file(json_pathname)

    result = list(dataset.all_pos({"area": "IT"}))
    expected = [[0, 0, 3], [0, 1, 3], [0, 2, 3]]
    assert result == expected

    dataset.generate_all_vec(area="IT")

    result = list(dataset.all_pos({"year": "2014"}))
    expected = [[0, 2, 0], [0, 2, 1], [0, 2, 2], [0, 2, 3]]
    assert result == expected

    dataset.generate_all_vec(year='2014')


def test_all_pos_with_three_dim():
    json_pathname = os.path.join(fixture_dir, "dataset", "three_dim_v1.json")
    dataset = jsonstat.JsonStatDataSet()
    dataset.from_file(json_pathname)

    # test 1
    result = list(dataset.all_pos({'one': 'one_1'}))
    expected = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3],
        [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3],
        [0, 2, 0], [0, 2, 1], [0, 2, 2], [0, 2, 3]]

    assert result == expected

    # test 2
    dataset.generate_all_vec(one='one_1')
    result = list(dataset.all_pos({"two": "two_2"}))
    expected = [
        [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3],
        [1, 1, 0], [1, 1, 1], [1, 1, 2], [1, 1, 3]
    ]
    assert result == expected
