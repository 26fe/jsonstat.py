# This file is part of jsonstat.py
#
# jsonstat
#
from __future__ import print_function
from jsonstat.istat.istat_dataset import IstatDataset
from jsonstat.istat.istat_exception import IstatException

#
# Represent a Area. An Area contains dataset
#
class IstatArea:
    def __init__(self, istat_helper, area):
        self.__istat_helper = istat_helper
        self.__area = area
        self.__cod2dataset = None

    #
    # name of the area
    #
    def name(self):
        return self.__area['Desc']

    #
    # print some info about the area
    #
    def info(self):
        msg = "{}:{}".format(self.__area['Id'], self.__area['Desc'])
        print(msg)

    #
    # get a IstatDataset by name
    #
    def dataset(self, name):
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset[name]

    #
    # Return a list of datasets
    #
    def datasets(self):
        if self.__cod2dataset is None:
            self.__download_datasets()
        return self.__cod2dataset.values()


    def __download_datasets(self):
        self.__cod2dataset = {}
        json_data = self.__istat_helper.dslist(self.__area['Id'], show=False)
        if json_data is not None:
            # print "-------------------------"
            # print u"area: {} '{}' nr. dataset {}".format(self.area['Id'], self.area['Desc'], len(json_data))
            for dataset in json_data:
                # self.show_dim(dataset)
                # print dataset
                self.__cod2dataset[dataset['Cod']] = IstatDataset(self.__istat_helper, dataset)
        else:
            msg = "cannot retrieve info for area {}".format(self.__area)
            raise IstatException(msg)

