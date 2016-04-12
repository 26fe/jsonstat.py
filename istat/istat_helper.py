# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
from pprint import pprint
import json
from io import StringIO
# from io import BytesIO
import os
import sys

# packages
import requests

# jsonstat
import jsonstat


class IstatHelper:
    """Helper class useful to invoke istat api (api.istat.it)
    Each methods of this class is mapped to an api call
    """

    def __init__(self, downloader, lang=1):
        """
        :param downloader:
        :param lang:
        :return:
        """

        self.__dwl = downloader
        self.__lang = lang

    def lang(self, lg):
        self.__lang = lg

    def __lang2str(self):
        if self.__lang == 0:
            return "it"
        else:
            return "en"

    def cache_dir(self):
        return self.__dwl.cache_dir()

    def help(self):
        uri = 'http://apistat.istat.it/?q=help&lang={}'.format(self.__lang)
        html = requests.get(uri).text
        print(html)

    def area(self, show=True):
        """returns all the 'area' of istat.

        It perform api call to http://apistat.istat.it/?q=getarea&lang=1
        # q=getarea
        # La funzione restituisce le aree tematiche di I.Stat supporta i seguenti parametri:
        #
        # lang=x lang  0   italiano o o 1 inglese
        # es:http://apistat.istat.it/?q=getarea&lang=1
        :param show: if true print diagnosti output
        :return: json structure
        """
        uri = 'http://apistat.istat.it/?q=getarea&lang={}'.format(self.__lang)
        filename = "istat-area-{}.json".format(self.__lang2str())
        json_string = self.__dwl.download(uri, filename)
        json_data = json.loads(json_string)
        if show:
            dump = json.dumps(json_data, sort_keys=True, indent=4)
            print(dump)
        return json_data

    def dslist(self, area, show=True):
        """
        Returns a list of datasets contained into the area
        It perform the api calls http://apistat.istat.it/?q=getdslist&area=15&lang=1

        # q=getdslist
        # La funzione restituisce i dataset afferenti all'area tematica indicata.
        #
        # area=xx area tematica
        # lang=x lang uguale a 0 o 1 per italiano o inglese
        # es:http://apistat.istat.it/?q=getdslist&area=15&lang=1

        :param area: code of the area
        :param show: if true show some info on stdout
        :return: json structure
        """
        uri = 'http://apistat.istat.it/?q=getdslist&area={}&lang={}'.format(area, self.__lang)
        filename = "istat-area-{}-{}.json".format(area, self.__lang2str())
        json_string = self.__dwl.download(uri, filename)

        json_data = json.loads(json_string)
        if show:
            dump = json.dumps(json_data, sort_keys=True, indent=4)
            print(dump)
        return json_data

    def dim(self, dataset, show=True):
        """
        Returns the dimension of the dataset <dataset>
        It perform the api calls http://apistat.istat.it/?q=getdim&dataset=DCIS_POPRES&lang=0

        # q=getdim
        # La funzione restituisce le dimensioni del dataset specificato.
        #
        # dataset=xxxxxx codice del dataset
        # lang=x lang 0=italiano 1=inglese
        #
        # es:http://apistat.istat.it/?q=getdim&dataset=DCIS_POPRES&lang=0
        :param dataset:
        :param show:
        :return:
        """
        uri = 'http://apistat.istat.it/?q=getdim&dataset={}&lang={}'.format(dataset, self.__lang)
        filename = "istat-dim-{}-{}.json".format(dataset, self.__lang2str())
        try:
            json_string = self.__dwl.download(uri, filename)

            # extract order using ijson

            # if sys.version_info < (3,):
            #     json_string = unicode(json_string, "utf-8")
            #
            # parser = ijson.parse(StringIO(json_string))
            # name2pos = {}
            # i = 0
            # for prefix, event, value in parser:
            #     # print prefix,event,value
            #     if prefix == '' and event =='map_key':
            #         # print "{}: {}".format(i, value)
            #         name2pos[value] = i
            #         i += 1

            # preserve dimension order using object_pairs_hook
            from collections import OrderedDict
            json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
            if show:
                dump = json.dumps(json_data, sort_keys=True, indent=4)
                print(dump)
            return json_data
        except ValueError:
            return None

    def table(self, dataset, dim, show=True):
        """
        Returns dataset using dimensions dim
        It perform the api calls
        http://apistat.istat.it/?q=gettable&dataset=<dataset>&dim=<dim>&lang=0

        # q=gettable
        # La funzione restituisce la tavola dati.
        # Supporta i seguenti parametri:
        # <ul>
        # dataset=xxxxxx codice del dataset
        #
        # dim=valori di ciascuna delle dimensioni separata da virgola.
        # L'ordine riflette quello ottenuto con il metodo getdim.
        # Il valore 0 sta ad indicare che per quella dimensione verranno presi tutti i valori.
        # Al momento possibile avere al pi tre zeri.
        #
        # lang=x lang uguale a 0 o 1 per italiano o inglese
        #
        # tr=x
        # Il parametro tr consente di invertire l'ordine delle prime due dimensioni della tavola.
        # Se la tavola a due dimensioni, scambia le righe con le colonne
        #
        # te=x Il parametro ts non  supportato
        #
        # es:http://apistat.istat.it/?q=gettable&dataset=DCIS_POPORESBIL&dim=82,0,0,0&lang=0&tr=&te=

        :param dataset:
        :param dim:
        :param show:
        :return:
        """
        uri = 'http://apistat.istat.it/?q=gettable&dataset={}&dim={}&lang={}'.format(dataset, dim, self.__lang)
        filename = "istat-table-{}-{}-{}.json".format(dataset, dim, self.__lang2str())
        try:
            json_string = self.__dwl.download(uri, filename)
            json_data = json.loads(json_string)
            if show:
                dump = json.dumps(json_data, indent=4)
                print(dump)
        except ValueError as e:
            print(e)
            print(uri)

    def gettableterr(self):
        """
        # q=gettableterr
        # La funzione restituisce la tavola dati.
        # In questo caso, i dati vengono forniti andando a selezionare tutte le province della regione specificata.
        #
        # dataset=xxxxxx codice del dataset
        #
        # dim=
        # valori di ciascuna delle dimensioni separata da virgola. L'ordine riflette quello ottenuto con il metodo getdim.
        # Il valore 0 sta ad indicare che per quella dimensione verranno presi tutti i valori.
        # Al momento possibile avere al pi tre zeri.
        #
        # lang=x lang uguale a 0 o 1 per italiano o inglese
        #
        # tr=x
        # Il parametro tr consente di invertire l'ordine delle prime due dimensioni della tavola.
        # Se la tavola a due dimensioni, scambia le righe con le colonne
        #
        # ts=x Il parametro ts non supportato
        #
        # es:http://apistat.istat.it/?q=gettableterr&amp;dataset=DCIS_INDDEMOG&amp;dim=82,0,0&amp;lang=0&amp;tr=&amp;te=
        :return:
        """
        pass

    def datajson(self, dataset, dim, show=True):
        """
        returns dataset 'dataset' using dimensions 'dim'
        It perform the api calls http://apistat.istat.it/?q=getdatajson&dataset=<dataset>&dim=<dim>&lang=0

        # q=getdatajson
        # La funzione restituisce il dataset dati secondo lo schema Json-stat. http://www.json-stat.org.
        # Questo l'output CONSIGLIATO!! vedi anche www.vincenzopatruno.org/json-stat
        #
        # dataset=xxxxxx codice del dataset
        #
        # dim=
        # valori di ciascuna delle dimensioni separata da virgola.
        # L'ordine riflette quello ottenuto con il metodo getdim.
        # Il valore 0 sta ad indicare che per quella dimensione verranno presi tutti i valori.
        # Al momento  possibile avere al piu tre zeri.
        #
        # lang=x lang uguale a 0 o 1 per italiano o inglese
        #
        # tr=x Il parametro tr consente di invertire l'ordine delle prime due dimensioni della tavola.
        # Se la tavola  a due dimensioni, scambia le righe con le colonne
        #
        # ts=x Il parametro ts non supportato
        #
        # es:http://apistat.istat.it/?q=getdatajson&dataset=DCIS_POPSTRRES1&dim=1,1,3,0,0&lang=0&tr=&te=
        :param dataset: dataset code (identifiers)
        :param dim:
        :param show:
        :return:
        """
        uri = 'http://apistat.istat.it/?q=getdatajson&dataset={}&dim={}&lang={}'.format(dataset, dim, self.__lang)
        filename = "istat-datajson-{}-{}-{}.json".format(dataset, dim, self.__lang2str())
        try:
            json_string = self.__dwl.download(uri, filename)
            json_data = json.loads(json_string)
            if show:
                dump = json.dumps(json_data, indent=4)
                print(dump)
            return json_data
        except ValueError as e:
            print(e)
        return None

    def tablelist(self):
        """
        # q=gettablelist
        # La funzione restituisce una una data regione, le tavole disponibili per la sezione pagine regionali di www.istat.it
        # Viene dato in output il nome della tavola e l'uri per poterla ottenere.
        #
        # La funzione <b>get_tavola.php</b> contenuta nell'uri  soltanto una app per la visualizzazione della tavola, che pu essere resa visibile
        # in json elimindo la parte get_tavola.php dall'uri
        #
        #
        # <li>reg=codice della regione
        # </li>
        # <li>lang=x lang e uguale a 0 o 1 per italiano o inglese
        # </li>
        # </ul>
        #
        #
        # es:http://apistat.istat.it/?q=gettablelist&amp;area=08&amp;reg=82
        :return:
        """
        pass

    def getregions(self):
        """
        # q=getregions
        # La funzione restituisce codice regione e descrizione delle regioni italiane<br>
        #
        # lang=x lang uguale a 0 o 1 per italiano o inglese
        #
        # es: http://apistat.istat.it/?q=getregions&lang=0
        #
        :return:
        """
        pass
