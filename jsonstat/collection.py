# This file is part of jsonstat.py

# stdlib
import json
import urllib2
# jsonstat
from jsonstat.dataset import JsonStatDataSet


class JsonStatCollection:
    def __init__(self):
        self.__url = None
        self.__name2dataset = {}
        self.__pos2dataset = None

    def dataset(self, spec):
        """returns a dataset beloging to the collection
        :param spec:
        :return:
        """
        if type(spec) is str:
            return self.__name2dataset[spec]
        elif type(spec) is int:
            return self.__pos2dataset[spec]
        raise ValueError()

    def info(self):
        for i in self.__name2dataset.values():
            print "dataset: '{}'".format(i.name())

    def from_file(self, filename):
        with open(filename) as f:
            json_string = f.read()
            self.from_string(json_string)

    def from_url(self, url):
        self.__url = url
        json_string = urllib2.urlopen(self.__url).read()
        self.from_string(json_string)

    def from_string(self, json_string):
        json_data = json.loads(json_string)
        self.from_json(json_data)

    def from_json(self, json_data):

        if "version" in json_data:
            self.__from_json_v2(json_data)
        else:
            # jsonstat version 1.0
            self.__from_json_v1(json_data)

    def __from_json_v1(self, json_data):
        #         parser = ijson.parse(StringIO(json_string))
        # name2pos = {}
        # i = 0
        # for prefix, event, value in parser:
        #     # print prefix,event,value
        #     if prefix == '' and event =='map_key':
        #         # print "{}: {}".format(i, value)
        #         name2pos[value] = i
        #         i += 1

        for ds in json_data.items():
            dataset_name = ds[0]
            dataset = JsonStatDataSet(dataset_name)
            dataset.from_json(ds[1])
            self.__name2dataset[dataset_name] = dataset

    def __from_json_v2(self, json_data):
        # jsonstat version 2.0
        # "version" : "2.0",
        # "class" : "collection",
        # "href" : "http://json-stat.org/samples/oecd-canada-col.json",
        # "label" : "OECD-Canada Sample Collection",
        # "updated" : "2015-12-24",
        json_data_ds = json_data["link"]["item"]
        self.__pos2dataset = len(json_data_ds) * [None]
        for pos, ds in enumerate(json_data_ds):
            dataset = JsonStatDataSet()
            dataset.from_json(ds,version=2)
            self.__pos2dataset[pos] = dataset
