
Notebook: using jsonstat.py with eurostat api
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This Jupyter notebook shows the python library
`jsonstat.py <http://github.com/26fe/jsonstat.py>`__ in action. It shows
how to explore dataset downloaded from a data provider. This notebook
uses some datasets from Eurostat. Eurostat provides a rest api to
download its datasets. You can find details about the api
`here <http://ec.europa.eu/eurostat/web/json-and-unicode-web-services>`__
It is possible to use a `query
builder <http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/query-builder>`__
for discovering the rest api parameters. The following image shows the
query builder:

.. code:: python

    # all import here
    from __future__ import print_function
    import os
    import pandas as pd
    import jsonstat
    
    import matplotlib as plt
    %matplotlib inline

1 - Exploring data with one dimension (time) with size > 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following cell downloads a datataset from eurostat. If the file is
already downloaded use the copy presents on the disk. Caching file is
useful to avoid downloading dataset every time notebook runs. Caching
can speed the development, and provides consistent results. You can see
the raw data
`here <http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM>`__

.. code:: python

    url_1 = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/nama_gdp_c?precision=1&geo=IT&unit=EUR_HAB&indic_na=B1GM'
    file_name_1 = "eurostat-name_gpd_c-geo_IT.json"
    
    file_path_1 = os.path.abspath(os.path.join("..", "tests", "fixtures", "www.ec.europa.eu_eurostat", file_name_1))
    if os.path.exists(file_path_1):
        print("using already donwloaded file {}".format(file_path_1))
    else:
        print("download file")
        jsonstat.download(url_1, file_name_1)
        file_path_1 = file_name_1


.. parsed-literal::

    using already donwloaded file /Users/26fe_nas/gioprj.on_mac/prj.python/jsonstat.py/tests/fixtures/www.ec.europa.eu_eurostat/eurostat-name_gpd_c-geo_IT.json


Initialize JsonStatCollection with eurostat data and print some info
about the collection.

.. code:: python

    collection_1 = jsonstat.from_file(file_path_1)
    collection_1




.. raw:: html

    JsonstatCollection contains the following JsonStatDataSet:</br><table><tr><td>pos</td><td>dataset</td></tr><tr><td>0</td><td>'nama_gdp_c'</td></tr></table>



Previous collection contains only a dataset named '``nama_gdp_c``'

.. code:: python

    nama_gdp_c_1 = collection_1.dataset('nama_gdp_c')
    nama_gdp_c_1




.. raw:: html

    name:   'nama_gdp_c'</br>title:  'GDP and main components - Current prices'</br>size: 4</br><table><tr><td>pos</td><td>id</td><td>label</td><td>size</td><td>role</td></tr><tr><td>0</td><td>unit</td><td>unit</td><td>1</td><td></td></tr><tr><td>1</td><td>indic_na</td><td>indic_na</td><td>1</td><td></td></tr><tr><td>2</td><td>geo</td><td>geo</td><td>1</td><td></td></tr><tr><td>3</td><td>time</td><td>time</td><td>69</td><td></td></tr></table>



All dimensions of the dataset '``nama_gdp_c``' are of size 1 with
exception of ``time`` dimension. Let's explore the time dimension.

.. code:: python

    nama_gdp_c_1.dimension('time')




.. raw:: html

    <table><tr><td>pos</td><td>idx</td><td>label</td></tr><tr><td>0</td><td>'1946'</td><td>'1946'</td></tr><tr><td>1</td><td>'1947'</td><td>'1947'</td></tr><tr><td>2</td><td>'1948'</td><td>'1948'</td></tr><tr><td>3</td><td>'1949'</td><td>'1949'</td></tr><td>...</td><td>...</td><td>...</td></table>



Get value for year 2012.

.. code:: python

    nama_gdp_c_1.value(time='2012')




.. parsed-literal::

    25700



Convert the jsonstat data into a pandas dataframe.

.. code:: python

    df_1 = nama_gdp_c_1.to_data_frame('time', content='id')
    df_1.tail()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>unit</th>
          <th>indic_na</th>
          <th>geo</th>
          <th>Value</th>
        </tr>
        <tr>
          <th>time</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>25700.0</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>26000.0</td>
        </tr>
        <tr>
          <th>2012</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>25700.0</td>
        </tr>
        <tr>
          <th>2013</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>25600.0</td>
        </tr>
        <tr>
          <th>2014</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



Adding a simple plot

.. code:: python

    df_1 = df_1.dropna() # remove rows with NaN values
    df_1.plot(grid=True, figsize=(20,5))




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x114bc12b0>




.. image:: eurostat_files/eurostat_15_1.png


2 - Exploring data with two dimensions (geo, time) with size > 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download or use the jsonstat file cached on disk. The cache is used to
avoid internet download during the devolopment to make the things a bit
faster. You can see the raw data
`here <http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/nama_gdp_c?precision=1&geo=IT&geo=FR&unit=EUR_HAB&indic_na=B1GM>`__

.. code:: python

    url_2 = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/nama_gdp_c?precision=1&geo=IT&geo=FR&unit=EUR_HAB&indic_na=B1GM'
    file_name_2 = "eurostat-name_gpd_c-geo_IT_FR.json"
    
    file_path_2 = os.path.abspath(os.path.join("..", "tests", "fixtures", "www.ec.europa.eu_eurostat", file_name_2))
    if os.path.exists(file_path_2):
        print("using alredy donwloaded file {}".format(file_path_2))
    else:
        print("download file and storing on disk")
        jsonstat.download(url, file_name_2)
        file_path_2 = file_name_2


.. parsed-literal::

    using alredy donwloaded file /Users/26fe_nas/gioprj.on_mac/prj.python/jsonstat.py/tests/fixtures/www.ec.europa.eu_eurostat/eurostat-name_gpd_c-geo_IT_FR.json


.. code:: python

    collection_2 = jsonstat.from_file(file_path_2)
    nama_gdp_c_2 = collection_2.dataset('nama_gdp_c')
    nama_gdp_c_2




.. raw:: html

    name:   'nama_gdp_c'</br>title:  'GDP and main components - Current prices'</br>size: 4</br><table><tr><td>pos</td><td>id</td><td>label</td><td>size</td><td>role</td></tr><tr><td>0</td><td>unit</td><td>unit</td><td>1</td><td></td></tr><tr><td>1</td><td>indic_na</td><td>indic_na</td><td>1</td><td></td></tr><tr><td>2</td><td>geo</td><td>geo</td><td>2</td><td></td></tr><tr><td>3</td><td>time</td><td>time</td><td>69</td><td></td></tr></table>



.. code:: python

    nama_gdp_c_2.dimension('geo')




.. raw:: html

    <table><tr><td>pos</td><td>idx</td><td>label</td></tr><tr><td>0</td><td>'FR'</td><td>'France'</td></tr><tr><td>1</td><td>'IT'</td><td>'Italy'</td></tr></table>



.. code:: python

    nama_gdp_c_2.value(time='2012',geo='IT')




.. parsed-literal::

    25700



.. code:: python

    nama_gdp_c_2.value(time='2012',geo='FR')




.. parsed-literal::

    31100



.. code:: python

    df_2 = nama_gdp_c_2.to_table(content='id',rtype=pd.DataFrame)
    df_2.tail()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>unit</th>
          <th>indic_na</th>
          <th>geo</th>
          <th>time</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>133</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>2010</td>
          <td>25700.0</td>
        </tr>
        <tr>
          <th>134</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>2011</td>
          <td>26000.0</td>
        </tr>
        <tr>
          <th>135</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>2012</td>
          <td>25700.0</td>
        </tr>
        <tr>
          <th>136</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>2013</td>
          <td>25600.0</td>
        </tr>
        <tr>
          <th>137</th>
          <td>EUR_HAB</td>
          <td>B1GM</td>
          <td>IT</td>
          <td>2014</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_FR_IT = df_2.dropna()[['time', 'geo', 'Value']]
    df_FR_IT = df_FR_IT.pivot('time', 'geo', 'Value')
    df_FR_IT.plot(grid=True, figsize=(20,5))




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x114c0f0b8>




.. image:: eurostat_files/eurostat_23_1.png


.. code:: python

    df_3 = nama_gdp_c_2.to_data_frame('time', content='id', blocked_dims={'geo':'FR'})
    df_3 = df_3.dropna()
    df_3.plot(grid=True,figsize=(20,5))




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x1178e7d30>




.. image:: eurostat_files/eurostat_24_1.png


.. code:: python

    df_4 = nama_gdp_c_2.to_data_frame('time', content='id', blocked_dims={'geo':'IT'})
    df_4 = df_4.dropna()
    df_4.plot(grid=True,figsize=(20,5))




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x117947630>




.. image:: eurostat_files/eurostat_25_1.png

