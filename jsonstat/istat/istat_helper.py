# -*- coding: utf-8 -*-
# This file is part of jsonstat.py

# stdlib
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import json
from io import StringIO
# from io import BytesIO

# packages
import ijson


#
# jsonstat
#
import jsonstat

#
# Each methods is mapped to an api call
#
class IstatHelper:
    def __init__(self, cache_dir, lang=1):
        self.dwl = jsonstat.Downloader(cache_dir)
        self.lang = lang

    def __lang2str(self):
        if self.lang == 0:
            return "it"
        else:
            return "en"

    def help(self):
        uri = 'http://apistat.istat.it/?q=help&lang={}'.format(self.lang)
        html = urllib2.urlopen(uri).read()
        print(uri)
        print(html)

    # q=getarea
    # La funzione restituisce le aree tematiche di I.Stat supporta i seguenti parametri:
    #
    # lang=x lang  0   italiano o o 1 inglese
    # es:http://apistat.istat.it/?q=getarea&lang=1
    def area(self, show=True):
        uri = 'http://apistat.istat.it/?q=getarea&lang={}'.format(self.lang)
        filename ="istat-area-{}.json".format(self.__lang2str())
        json_string = self.dwl.download(uri,filename)
        json_data = json.loads(json_string)
        if show:
            # print "----------------------------------------------"
            # print uri
            # print html
            # print json_data
            # print string
            print(json.dumps(json_data, sort_keys=True, indent=4))
        return json_data

    # q=getdslist
    # La funzione restituisce i dataset afferenti all'area tematica indicata.
    #
    # area=xx area tematica
    # lang=x lang uguale a 0 o 1 per italiano o inglese
    # es:http://apistat.istat.it/?q=getdslist&amp;area=15&amp;lang=1
    def dslist(self,area, show=True):
        uri = 'http://apistat.istat.it/?q=getdslist&area={}&lang={}'.format(area,self.lang)
        filename = "istat-area-{}-{}.json".format(area, self.__lang2str())
        json_string = self.dwl.download(uri, filename)

        json_data = json.loads(json_string)
        if show:
            print("----------------------------------------------")
            # print uri
            # print html
            print(json.dumps(json_data, sort_keys=True, indent=4))
        return json_data

    # q=getdim
    # La funzione restituisce le dimensioni del dataset specificato.
    #
    # dataset=xxxxxx codice del dataset
    # lang=x lang 0=italiano 1=inglese
    #
    # es:http://apistat.istat.it/?q=getdim&dataset=DCIS_POPRES&lang=0
    def dim(self,dataset,show=True):
        uri = 'http://apistat.istat.it/?q=getdim&dataset={}&lang={}'.format(dataset,self.lang)
        filename="istat-dim-{}-{}.json".format(dataset, self.__lang2str())
        try:
            json_string = self.dwl.download(uri,filename)

            # extract order using ijson

            if sys.version_info < (3,):
                json_string = unicode(json_string, "utf-8")

            parser = ijson.parse(StringIO(json_string))
            name2pos = {}
            i = 0
            for prefix, event, value in parser:
                # print prefix,event,value
                if prefix == '' and event =='map_key':
                    # print "{}: {}".format(i, value)
                    name2pos[value] = i
                    i += 1

            # it is possible preserve order using object_pairs_hook
            from collections import OrderedDict
            json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
            if show:
                print("----------------------------------------------")
                print(json_data)
            return (name2pos, json_data)
        except ValueError:
            return None



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
    def table(self,dataset,dim,show=True):
        uri = 'http://apistat.istat.it/?q=gettable&dataset={}&dim={}&lang={}'.format(dataset,dim,self.lang)
        filename = "istat-table-{}-{}-{}.json".format(dataset, dim, self.__lang2str())
        try:
            json_string = self.dwl.download(uri, filename)
            json_data = json.loads(json_string)
            if show:
                print("----------------------------------------------")
                # print uri
                # print page
                print(json.dumps(json_data, indent=4))
        except ValueError as e:
            print(e)
            print(uri)

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
    def gettableterr(self):
        pass

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
    def datajson(self,dataset,dim,show=False):
        uri = 'http://apistat.istat.it/?q=getdatajson&dataset={}&dim={}&lang={}'.format(dataset,dim,self.lang)
        filename = "istat-datajson-{}-{}-{}.json".format(dataset, dim, self.__lang2str())
        try:
            json_string = self.dwl.download(uri, filename)
            json_data = json.loads(json_string)
            if show:
                print(uri)
                print(json_string)
                print(json.dumps(json_data, indent=4))
            return json_data
        except ValueError as e:
            print(e)
        return None


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
    # </p>
    #
    def tablelist(self):
        pass

    # q=getregions
    # La funzione restituisce codice regione e descrizione delle regioni italiane<br>
    #
    # lang=x lang uguale a 0 o 1 per italiano o inglese
    #
    # es: http://apistat.istat.it/?q=getregions&lang=0
    #
    def getregions(self):
        pass


    def list_dim(self, dataset):
        json_data = self.dim(dataset['Cod'], show=False)
        if json_data is not None:
            # if len(json_data) <= 3:
            msg = u"dataset: '{}' '{}' dim: {}".format(dataset['Cod'], dataset['Desc'], len(json_data))
            print(msg)
        else:
            print("cannot retrieve info for dataset: {}".format(dataset))

    def list_dataset_dim(self, area):
        """
        ex di area: {'Desc': 'Censimento popolazione e abitazioni 2011', 'Id': '3', 'Cod': 'CEN'}
        :param area:
        :return:
        """
        json_data = self.dslist(area['Id'], show=False)
        if json_data is not None:
            print("-------------------------")
            msg = u"area: {} '{}' nr. dataset {}".format(area['Id'], area['Desc'], len(json_data))
            print(msg)
            for dataset in json_data:
                self.list_dim(dataset)
        else:
            print("--------------")
            print("cannot retrieve info for area {}".format(area))

    def list_area_dataset_dim(self):
        json_data = self.area(show=False)
        for area in json_data:
            self.list_dataset_dim(area)


if __name__ == "__main__":
    MAIN_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "..")
    cache_dir = os.path.normpath(os.path.join(MAIN_DIRECTORY, "tmp", "istat_cached"))
    istat = IstatHelper(cache_dir,lang=1)

    istat.list_area_dataset_dim()

    # istat.help()

    # istat.area()
    # istat.show_area()
    # istat.show_area_dataset_dim()
    # ...
    # {
    #      "Cod": "LAB",
    #      "Desc": "Lavoro",
    #      "Id": 26
    #  }
    # ...

    # istat.dslist(26)
    # istat.show_dateset_dim(26)
    # ...
    # {
    #     "Cod": "DCCV_TAXDISOCCUDE",
    #     "Desc": "Tasso di disoccupazione - dati destagionalizzati",
    #     "Id": 14
    # },
    # ...

    # istat.dim("DCCV_TAXDISOCCUDE")
    # istat.show_dim("DCCV_TAXDISOCCUDE")
    # ...
    # {
    # "Territorio"        :[{"Cod":1,"Desc":" Italia"},{"Cod":3,"Desc":" Nord"},{"Cod":62,"Desc":" Centro"},{"Cod":88,"Desc":" Mezzogiorno"},{"Cod":89,"Desc":" Sud"}],
    # "Tipo dato"         :[{"Cod":6,"Desc":" tasso di disoccupazione"}],
    # "Misura"            :[{"Cod":1,"Desc":" valori percentuali"},{"Cod":9,"Desc":" valori assoluti"}],
    # "Sesso"             :[{"Cod":1,"Desc":" maschi"},{"Cod":2,"Desc":" femmine"},{"Cod":3,"Desc":" totale"}],
    # "Classe di et\u00e0":[{"Cod":4,"Desc":" 15-24 anni"},{"Cod":28,"Desc":" 15 anni e pi\u00f9"}],
    # "Edizione"          :[ {"Cod":2330,"Desc":" 30-Set-2011"},
    #                        ...
    #                        {"Cod":3112,"Desc":" 01-Set-2015"},{"Cod":3127,"Desc":" 11-Dic-2015"}
    #                      ],
    # "Tempo e frequenza":[  {"Cod":1764,"Desc":" T4-1992"},{"Cod":1770,"Desc":" T1-1993"},{"Cod":1774,"Desc":" T2-1993"},{"Cod":1779,"Desc":" T3-1993"},{"Cod":1783,"Desc":" T4-1993"},{"Cod":1789,"Desc":" T1-1994"},
    #                        ...
    #                        {"Cod":2192,"Desc":" T2-2015"},{"Cod":2197,"Desc":" T3-2015"}
    #                     ]}
    # ...


    # istat.datajson('DCCV_TAXDISOCCUDE',"1,6,9,0,0") # "1,6,9,0,0,3127,0"
    # istat.table('DCCV_TAXDISOCCUDE',"1,6,9,0,0")


    # istat.dim('DCCV_MONQUALARIA')
    # istat.datajson('DCCV_MONQUALARIA', "0,0,0")
    # istat.table('DCCV_MONQUALARIA', "1,0,0")
