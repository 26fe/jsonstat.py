
Notebook: using jsonstat.py to explore Istat data
-------------------------------------------------

This Jupyter notebook shows how to use
`jsonstat.py <http://github.com/26fe/jsonstat.py>`__ python library to
explore Istat data. `Istat <http://www.istat.it/en/about-istat>`__ is
Italian National Institute of Statistics. It publishs a rest api for
querying italian statistics.

.. code:: python

    from __future__ import print_function
    import os
    import pandas as ps
    import jsonstat
    import jsonstat.istat as istat

Setting a cache dir to store json files download by Istat api

.. code:: python

    cache_dir = os.path.abspath(os.path.join("..", "tmp", "istat_cached"))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    print("cache_dir is '{}'".format(cache_dir))


.. parsed-literal::

    cache_dir is '/Users/26fe_nas/prj.python/jsonstat.py/tmp/istat_cached'


List all istat areas

.. code:: python

    i = istat.Istat(cache_dir)
    for istat_area in i.areas():
        print(istat_area)


.. parsed-literal::

    CEN:2011 Population and housing census
    ENT:Enterprises
    ENV:Environment and Energy
    POP:Population and Households
    HOU:Households Economic Conditions and Disparities
    HEA:Health statistics
    WEL:Social Security and Welfare
    EDU:Education and training
    COM:Communication, culture and leisure
    JUS:Justice and Security
    OPI:Citizens' opinions and satisfaction with life
    SOC:Social participation
    ACC:National Accounts
    AGR:Agriculture
    IND:Industry and Construction
    SER:Services
    PUB:Public Administrations and Private Institutions
    EXT:External Trade and Internationalisation
    PRI:Prices
    LAB:Labour


List all datasets contained into area ``Prices``

.. code:: python

    istat_area_name = 'Prices'
    istat_area = i.area(istat_area_name)
    
    for istat_dataset in istat_area.datasets():
        print(u"{}({}):{}".format(istat_dataset.cod(), istat_dataset.nrdim(), istat_dataset.name()))


.. parsed-literal::

    DCSP_FOI2(5):FOI  Annual average  until 2010
    DCSP_FOI3(4):FOI  Weights until 2010
    DCSP_FOI1(5):FOI  Monthly data until 2010
    DCSP_NICDUE(5):NIC  Annual average until 2010
    DCSP_NICTREB2010(4):NIC  Weights from 2011 onwards
    DCSP_FOI3B2010(4):FOI  Weights from 2011 onwards
    DCSP_IPAB(5):House price index 
    DCSP_NICUNOBB2010(5):NIC  Monthly data from 2011 onwards
    DCSC_PREZPRODSERV_1(5):Services producer prices index
    DCSC_FABBRESID_1(5):Construction costs index - monthly data
    DCSP_NICTRE(4):NIC  Weights  until 2010
    DCSP_NICUNOB(5):NIC  Monthly data until 2010
    DCSP_IPCA1(5):HICP  Monthly data from 2001 onwards (base 2005=100)
    DCSP_IPCA2(5):HICP  Annual average from 2001 onwards (base 2005=100) 
    DCSP_IPCA3(4):HICP  Weights from 2001 onwards
    DCSP_IPCATC2(5):HICP at constant tax rates  Annual average from 2002 onwards (base 2005=100) 
    DCSP_IPCATC1(5):HICP at constant tax rates  Monthly data from 2002 onwards (base 2005=100) 
    DCSP_FOI1B2010(5):FOI  Monthly data from 2011 onwards
    DCSP_NICDUEB2010(5):NIC  Annual average from 2011 onwards
    DCSC_PREZZPIND_1(6):Producer price index for industrial products - monthly data
    DCSP_FOI2B2010(5):FOI  Annual average from 2011  onwards


List all dimension for dataset ``DCSP_IPAB`` (House price index)

.. code:: python

    istat_dataset_name = 'DCSP_IPAB'
    istat_dataset = istat_area.dataset(istat_dataset_name)
    istat_dataset.info_dimensions()


.. parsed-literal::

    dim 0 'Territory' (1:'Italy')
    dim 1 'Index type' (18:'house price index (base 2010=100) - quarterly data', 19:'house price index (base 2010=100) - annual average', 20:'house price index (base 2010=100) - weights')
    dim 2 'Measure' (8:'annual average rate of change', 4:'index number', 22:'not applicable', 6:'percentage changes on the previous period', 7:'percentage changes on the same period of the previous year')
    dim 3 'Purchases of dwellings' (4:'H1 - all items', 5:'H11 - new dwellings', 6:'H12 - existing dwellings')
    dim 4 'Time and frequency' (2178:'Q3-2014', 2182:'Q4-2014', 2186:'2015', 2188:'Q1-2015', 2192:'Q2-2015', 2197:'Q3-2015', 2091:'2010', 2093:'Q1-2010', 2097:'Q2-2010', 2102:'Q3-2010', 2106:'Q4-2010', 2110:'2011', 2112:'Q1-2011', 2116:'Q2-2011', 2121:'Q3-2011', 2125:'Q4-2011', 2129:'2012', 2131:'Q1-2012', 2135:'Q2-2012', 2140:'Q3-2012', 2144:'Q4-2012', 2148:'2013', 2150:'Q1-2013', 2154:'Q2-2013', 2159:'Q3-2013', 2163:'Q4-2013', 2167:'2014', 2169:'Q1-2014', 2173:'Q2-2014')


Extract data from dataset ``DCSP_IPAB`` with dimension "1,18,0,0,0"
where the first dimension is Territory, etc. Below is the mapping: -
Territory 1 -> Italy - Type 18 -> 'house price index (base 2010=100) -
quarterly data' - Measure 0 -> ALL - Purchase of dwelling 0 -> ALL -
Time and frequency 0 -> ALL

.. code:: python

    json_stat_data = istat_dataset.getvalues("1,18,0,0,0")

Convert istat dataset into jsonstat collection and print some info

.. code:: python

    collection = jsonstat.JsonStatCollection()
    collection.from_json(json_stat_data)
    collection.info()


.. parsed-literal::

    0: dataset 'IDMISURA1*IDTYPPURCH*IDTIME'
    


From the jsonstat collection print some info of one dataset

.. code:: python

    jsonstat_dataset = collection.dataset('IDMISURA1*IDTYPPURCH*IDTIME')
    jsonstat_dataset.info()


.. parsed-literal::

    name:   'IDMISURA1*IDTYPPURCH*IDTIME'
    label:  'House price index  by Measure, Purchases of dwellings and Time and frequency - Italy - house price index (base 2010=100) - quarterly data'
    size: 207
    3 dimensions:
      0: dim id/name: 'IDMISURA1' size: '3' role: 'None'
      1: dim id/name: 'IDTYPPURCH' size: '3' role: 'None'
      2: dim id/name: 'IDTIME' size: '23' role: 'None'
    

