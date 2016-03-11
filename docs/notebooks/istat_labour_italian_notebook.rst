
Notebook: using jsonstat.py to explore ISTAT data (unemployment)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This Jupyter notebook shows how to use
`jsonstat.py <http://github.com/26fe/jsonstat.py>`__ python library to
explore Istat data. `Istat <http://www.istat.it/en/about-istat>`__ is
the Italian National Institute of Statistics. It publishs a rest api for
browsing italian statistics. This api can return results in jsonstat
format.

La forza lavoro e composta da occupati e disoccupati. La popolozione
sopra i 15 anni e composta da forza lavoro ed inatttivi.

.. math:: Popolozoine = ForzaLavoro + Inattivi

.. math:: Forzalav = Occupati + Disoccupati

.. math:: Inattivi = NonVoglioLavorare + Scoraggiati

Tasso disoccupazione = Disoccupati/Occupati

download dataset from Istat
---------------------------

.. code:: python

    from __future__ import print_function
    import os
    import pandas as pd
    from IPython.core.display import HTML
    import matplotlib.pyplot as plt
    %matplotlib inline
    
    import istat
    
    # Next step is to set a cache dir where to store json files downloaded from Istat. 
    # Storing file on disk speeds up development, and assures consistent results over time. 
    # Eventually, you can delete donwloaded files to get a fresh copy.
    
    cache_dir = os.path.abspath(os.path.join("..", "tmp", "istat_cached"))
    istat.cache_dir(cache_dir)
    istat.lang(0)  #italian
    print("cache_dir is '{}'".format(istat.cache_dir()))


.. parsed-literal::

    cache_dir is '/Users/26fe_nas/gioprj.on_mac/prj.python/jsonstat.py/tmp/istat_cached'




.. code:: python

    # List all datasets contained into area `LAB` (Labour)
    HTML(istat.area('LAB').datasets_as_html())




.. raw:: html

    <table><tr><th>cod</th><th>name</th><th>dim</th></tr><tr><td>DCCV_COMPL</td><td>Indicatori complementari</td><td>12</td></td></tr><tr><td>DCCV_DISOCCUPT</td><td>Disoccupati</td><td>10</td></td></tr><tr><td>DCCV_DISOCCUPTDE</td><td>Disoccupati - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_DISOCCUPTMENS</td><td>Disoccupati - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_FORZLV</td><td>Forze di lavoro</td><td>8</td></td></tr><tr><td>DCCV_FORZLVDE</td><td>Forze di lavoro - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_FORZLVMENS</td><td>Forze lavoro - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_INATTIV</td><td>Inattivi</td><td>11</td></td></tr><tr><td>DCCV_INATTIVDE</td><td>Inattivi - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_INATTIVMENS</td><td>Inattivi - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_NEET</td><td>NEET (giovani non occupati e non in istruzione e formazione)</td><td>10</td></td></tr><tr><td>DCCV_OCCUPATIMENS</td><td>Occupati - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_OCCUPATIT</td><td> Occupati                                                      </td><td>14</td></td></tr><tr><td>DCCV_OCCUPATITDE</td><td>Occupati - dati destagionalizzati</td><td>8</td></td></tr><tr><td>DCCV_ORELAVMED</td><td>Occupati per ore settimanali lavorate e numero di ore settimanali lavorate procapite</td><td>12</td></td></tr><tr><td>DCCV_TAXATVT</td><td>Tasso di attività</td><td>8</td></td></tr><tr><td>DCCV_TAXATVTDE</td><td>Tasso di attività - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_TAXATVTMENS</td><td>Tasso di attività - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_TAXDISOCCU</td><td>Tasso di disoccupazione</td><td>9</td></td></tr><tr><td>DCCV_TAXDISOCCUDE</td><td>Tasso di disoccupazione - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_TAXDISOCCUMENS</td><td>Tasso di disoccupazione - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_TAXINATT</td><td>Tasso di inattività</td><td>8</td></td></tr><tr><td>DCCV_TAXINATTDE</td><td>Tasso di inattività - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_TAXINATTMENS</td><td>Tasso di inattività - dati mensili</td><td>8</td></td></tr><tr><td>DCCV_TAXOCCU</td><td>Tasso di occupazione</td><td>8</td></td></tr><tr><td>DCCV_TAXOCCUDE</td><td>Tasso di occupazione - dati destagionalizzati</td><td>7</td></td></tr><tr><td>DCCV_TAXOCCUMENS</td><td>Tasso di occupazione - dati mensili</td><td>8</td></td></tr><tr><td>DCIS_RICSTAT</td><td>Ricostruzione statistica delle serie regionali di popolazione del periodo 1/1/2002-1/1/2014</td><td>6</td></td></tr><tr><td>DCSC_COSTLAVSTRUT_1</td><td>Struttura del costo del lavoro (indagine quadriennale)</td><td>6</td></td></tr><tr><td>DCSC_COSTLAVULAOROS_1</td><td>Indicatori del costo del lavoro per Ula - dati trimestrali</td><td>5</td></td></tr><tr><td>DCSC_GI_COS</td><td>Costo del lavoro nelle imprese con almeno 500 dipendenti - dati mensili</td><td>6</td></td></tr><tr><td>DCSC_GI_OCC</td><td>Occupazione dipendente, tassi di ingresso e uscita nelle imprese con almeno 500 dipendenti - dati mensili</td><td>6</td></td></tr><tr><td>DCSC_GI_ORE</td><td>Ore lavorate nelle imprese con almeno 500 dipendenti - dati mensili</td><td>6</td></td></tr><tr><td>DCSC_GI_RE</td><td>Retribuzione lorda nelle imprese con almeno 500 dipendenti - dati mensili</td><td>6</td></td></tr><tr><td>DCSC_ORE10_1</td><td>Ore lavorate nelle imprese con almeno 10 dipendenti - dati trimestrali</td><td>5</td></td></tr><tr><td>DCSC_OROS_1</td><td>Indice delle posizioni lavorative alle dipendenze  - dati trimestrali</td><td>5</td></td></tr><tr><td>DCSC_POSTIVAC_1</td><td>Tasso di posti vacanti - dati trimestrali</td><td>5</td></td></tr><tr><td>DCSC_RETRATECO1</td><td>Retribuzioni contrattuali per Ateco 2007</td><td>6</td></td></tr><tr><td>DCSC_RETRCASSCOMPPA</td><td>Retribuzione contrattuale di cassa e di competenza per dipendente della pubblica amministrazione per contratto - dati annuali -  euro</td><td>7</td></td></tr><tr><td>DCSC_RETRCONTR1C</td><td>Retribuzioni contrattuali per contratto - dati mensili e annuali   .</td><td>6</td></td></tr><tr><td>DCSC_RETRCONTR1O</td><td>Orario contrattuale annuo lordo, netto, ferie e altre ore di riduzione </td><td>6</td></td></tr><tr><td>DCSC_RETRCONTR1T</td><td>Indicatori di tensione contrattuale - dati mensili e annuali</td><td>6</td></td></tr><tr><td>DCSC_RETRULAOROS_1</td><td>Indice delle retribuzioni lorde per Ula  - dati trimestrali</td><td>5</td></td></tr></table>



Download - nroccupati - nrdisoccupati - forza lavoro controllare che
nroccupati + nrdisoccupati = forza lavoro

Occupati
~~~~~~~~

.. code:: python

    # DCCV_OCCUPATIT
    istat_occupatit = istat.dataset('LAB', 'DCCV_OCCUPATIT')
    # HTML(istat_occupatit.info_dimensions_as_html(show_values=0))

.. code:: python

    spec = { 
        'Territorio':              'Italia',                            
        'Sesso':                   'totale',                           
        'Classe di età':           '15 anni e più',                            
        'Titolo di studio':        'totale', 
        'Cittadinanza':            'totale',                         
        'Ateco 2002' :             '0010 totale',
        'Ateco 2007' :             '0010 totale',
        'Posizione professionale': 'totale',
        'Profilo professionale':   'totale',
        'Professione 2001':        'totale',
        'Professione 2011':        'totale',
        'Regime orario':           'totale',
        'Carattere occupazione':   'totale',
        'Tempo e frequenza': 0                    
    }
    
    df_occupatit = istat_occupatit.getvalues(spec).dataset(0).to_table(rtype=pd.DataFrame)
    df_occupatit[df_occupatit['Tempo e frequenza'].str.contains(r'^T.*')]
    df_occupatit.tail(6)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Tempo e frequenza</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>187</th>
          <td>T2-2014</td>
          <td>22316.76</td>
        </tr>
        <tr>
          <th>188</th>
          <td>T3-2014</td>
          <td>22398.30</td>
        </tr>
        <tr>
          <th>189</th>
          <td>T4-2014</td>
          <td>22374.93</td>
        </tr>
        <tr>
          <th>190</th>
          <td>T1-2015</td>
          <td>22158.45</td>
        </tr>
        <tr>
          <th>191</th>
          <td>T2-2015</td>
          <td>22496.79</td>
        </tr>
        <tr>
          <th>192</th>
          <td>T3-2015</td>
          <td>22645.07</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_occupatit.ix[192]




.. parsed-literal::

    Tempo e frequenza    T3-2015
    Value                22645.1
    Name: 192, dtype: object



Disoccupati
~~~~~~~~~~~

.. code:: python

    istat_disoccupt = istat.dataset('LAB', 'DCCV_DISOCCUPT')
    HTML(istat_disoccupt.info_dimensions_as_html(show_values=3))




.. raw:: html

    <table><tr><th>nr</th><th>name</th><th>nr. values</th><th>values (first 3 values)</th></tr><tr><td>0</td><td>Territorio</td><td>136</td><td>1:'Italia', 3:'Nord', 4:'Nord-ovest' ...</td></td></tr><tr><td>1</td><td>Tipo dato</td><td>1</td><td>2:'numero di persone in cerca di occupazione 15 anni e oltre (valori in migliaia)'</td></td></tr><tr><td>2</td><td>Misura</td><td>1</td><td>9:'valori assoluti'</td></td></tr><tr><td>3</td><td>Sesso</td><td>3</td><td>1:'maschi', 2:'femmine', 3:'totale' ...</td></td></tr><tr><td>4</td><td>Classe di età</td><td>11</td><td>17:'45-54 anni', 4:'15-24 anni', 21:'55-64 anni' ...</td></td></tr><tr><td>5</td><td>Titolo di studio</td><td>5</td><td>11:'laurea e post-laurea', 12:'totale', 3:'licenza di scuola elementare, nessun titolo di studio' ...</td></td></tr><tr><td>6</td><td>Cittadinanza</td><td>3</td><td>1:'italiano-a', 2:'straniero-a', 3:'totale' ...</td></td></tr><tr><td>7</td><td>Condizione professionale</td><td>4</td><td>3:'disoccupati ex-occupati', 4:'disoccupati ex-inattivi', 5:'disoccupati senza esperienza di lavoro' ...</td></td></tr><tr><td>8</td><td>Durata disoccupazione</td><td>2</td><td>2:'12 mesi o più', 3:'totale'</td></td></tr><tr><td>9</td><td>Tempo e frequenza</td><td>193</td><td>1536:'T4-1980', 2049:'T4-2007', 1540:'1981' ...</td></td></tr></table>



.. code:: python

    spec = { 
        'Territorio':               'Italia',      
        'Tipo dato' :               'numero di persone in cerca di occupazione 15 anni e oltre (valori in migliaia)',
        'Misura':                   'valori assoluti',
        'Sesso':                    'totale',                           
        'Classe di età':            '15 anni e più',                            
        'Titolo di studio':         'totale', 
        'Cittadinanza':             'totale',   
        'Condizione professionale': 'totale',
        'Durata disoccupazione':    'totale',
        'Tempo e frequenza': 0                    
    }
    
    df_disoccupt = istat_disoccupt.getvalues(spec).dataset(0).to_table(rtype=pd.DataFrame)
    df_disoccupt[df_disoccupt['Tempo e frequenza'].str.contains(r'^T.*')]
    df_disoccupt.tail(6)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Tempo e frequenza</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>187</th>
          <td>T2-2014</td>
          <td>3102.39</td>
        </tr>
        <tr>
          <th>188</th>
          <td>T3-2014</td>
          <td>2975.40</td>
        </tr>
        <tr>
          <th>189</th>
          <td>T4-2014</td>
          <td>3419.51</td>
        </tr>
        <tr>
          <th>190</th>
          <td>T1-2015</td>
          <td>3301.81</td>
        </tr>
        <tr>
          <th>191</th>
          <td>T2-2015</td>
          <td>3101.50</td>
        </tr>
        <tr>
          <th>192</th>
          <td>T3-2015</td>
          <td>2676.55</td>
        </tr>
      </tbody>
    </table>
    </div>




Forza Lavoro
~~~~~~~~~~~~

.. code:: python

    istat_forzlv = istat.dataset('LAB', 'DCCV_FORZLV')
    HTML(istat_forzlv.info_dimensions_as_html(show_values=3))




.. raw:: html

    <table><tr><th>nr</th><th>name</th><th>nr. values</th><th>values (first 3 values)</th></tr><tr><td>0</td><td>Territorio</td><td>136</td><td>1:'Italia', 3:'Nord', 4:'Nord-ovest' ...</td></td></tr><tr><td>1</td><td>Tipo dato</td><td>1</td><td>3:'numero di forze di lavoro15 anni e oltre (valori in migliaia)'</td></td></tr><tr><td>2</td><td>Misura</td><td>1</td><td>9:'valori assoluti'</td></td></tr><tr><td>3</td><td>Sesso</td><td>3</td><td>1:'maschi', 2:'femmine', 3:'totale' ...</td></td></tr><tr><td>4</td><td>Classe di età</td><td>10</td><td>17:'45-54 anni', 4:'15-24 anni', 21:'55-64 anni' ...</td></td></tr><tr><td>5</td><td>Titolo di studio</td><td>5</td><td>11:'laurea e post-laurea', 12:'totale', 3:'licenza di scuola elementare, nessun titolo di studio' ...</td></td></tr><tr><td>6</td><td>Cittadinanza</td><td>3</td><td>1:'italiano-a', 2:'straniero-a', 3:'totale' ...</td></td></tr><tr><td>7</td><td>Tempo e frequenza</td><td>193</td><td>1536:'T4-1980', 2049:'T4-2007', 1540:'1981' ...</td></td></tr></table>



.. code:: python

    spec = { 
        'Territorio':       'Italia',                            
        'Tipo dato':        'numero di forze di lavoro15 anni e oltre (valori in migliaia)',
        'Misura':           'valori assoluti',               
        'Sesso':            'totale',                           
        'Classe di età':    '15 anni e più',                            
        'Titolo di studio': 'totale', 
        'Cittadinanza':     'totale',                         
        'Tempo e frequenza': 0                    
    }
    
    df_forzlv = istat_forzlv.getvalues(spec).dataset(0).to_table(rtype=pd.DataFrame)
    # df_forzlv

.. code:: python

    # df_forzlv = df_forzlv.dropna()
    df_forzlv = df_forzlv[df_forzlv['Tempo e frequenza'].str.contains(r'^T.*')]
    df_forzlv.tail(6)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Tempo e frequenza</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>187</th>
          <td>T2-2014</td>
          <td>25419.15</td>
        </tr>
        <tr>
          <th>188</th>
          <td>T3-2014</td>
          <td>25373.70</td>
        </tr>
        <tr>
          <th>189</th>
          <td>T4-2014</td>
          <td>25794.44</td>
        </tr>
        <tr>
          <th>190</th>
          <td>T1-2015</td>
          <td>25460.25</td>
        </tr>
        <tr>
          <th>191</th>
          <td>T2-2015</td>
          <td>25598.29</td>
        </tr>
        <tr>
          <th>192</th>
          <td>T3-2015</td>
          <td>25321.61</td>
        </tr>
      </tbody>
    </table>
    </div>



Inattivi
~~~~~~~~

.. code:: python

    istat_inattiv = istat.dataset('LAB', 'DCCV_INATTIV')
    HTML(istat_inattiv.info_dimensions_as_html(show_values=0))




.. raw:: html

    <table><tr><th>nr</th><th>name</th><th>nr. values</th><th>values (first 0 values)</th></tr><tr><td>0</td><td>Territorio</td><td>136</td><td>1:'Italia', 3:'Nord', 4:'Nord-ovest', 5:'Piemonte', 6:'Torino', 7:'Vercelli', 8:'Biella', 9:'Verbano-Cusio-Ossola', 10:'Novara', 11:'Cuneo', 12:'Asti', 13:'Alessandria', 14:'Valle d'Aosta / Vallée d'Aoste', 15:'Valle d'Aosta / Vallée d'Aoste', 16:'Liguria', 17:'Imperia', 18:'Savona', 19:'Genova', 20:'La Spezia', 21:'Lombardia', 22:'Varese', 23:'Como', 24:'Lecco', 25:'Sondrio', 26:'Milano', 27:'Bergamo', 28:'Brescia', 29:'Pavia', 30:'Lodi', 31:'Cremona', 32:'Mantova', 33:'Nord-est', 34:'Trentino Alto Adige / Südtirol', 35:'Provincia Autonoma Bolzano / Bozen', 37:'Provincia Autonoma Trento', 39:'Veneto', 40:'Verona', 41:'Vicenza', 42:'Belluno', 43:'Treviso', 44:'Venezia', 45:'Padova', 46:'Rovigo', 47:'Friuli-Venezia Giulia', 48:'Pordenone', 49:'Udine', 50:'Gorizia', 51:'Trieste', 52:'Emilia-Romagna', 53:'Piacenza', 54:'Parma', 55:'Reggio nell'Emilia', 56:'Modena', 57:'Bologna', 58:'Ferrara', 59:'Ravenna', 60:'Forlì-Cesena', 61:'Rimini', 62:'Centro', 63:'Toscana', 64:'Massa-Carrara', 65:'Lucca', 66:'Pistoia', 67:'Firenze', 68:'Prato', 69:'Livorno', 70:'Pisa', 71:'Arezzo', 72:'Siena', 73:'Grosseto', 74:'Umbria', 75:'Perugia', 76:'Terni', 77:'Marche', 78:'Pesaro e Urbino', 79:'Ancona', 80:'Macerata', 81:'Ascoli Piceno', 82:'Lazio', 83:'Viterbo', 84:'Rieti', 85:'Roma', 86:'Latina', 87:'Frosinone', 88:'Mezzogiorno', 90:'Abruzzo', 91:'L'Aquila', 92:'Teramo', 93:'Pescara', 94:'Chieti', 95:'Molise', 96:'Isernia', 97:'Campobasso', 98:'Campania', 99:'Caserta', 100:'Benevento', 101:'Napoli', 102:'Avellino', 103:'Salerno', 104:'Puglia', 105:'Foggia', 106:'Bari', 107:'Taranto', 108:'Brindisi', 109:'Lecce', 110:'Basilicata', 111:'Potenza', 112:'Matera', 113:'Calabria', 114:'Cosenza', 115:'Crotone', 116:'Catanzaro', 117:'Vibo Valentia', 118:'Reggio di Calabria', 120:'Sicilia', 121:'Trapani', 122:'Palermo', 123:'Messina', 124:'Agrigento', 125:'Caltanissetta', 126:'Enna', 127:'Catania', 128:'Ragusa', 129:'Siracusa', 130:'Sardegna', 131:'Sassari', 132:'Nuoro', 133:'Cagliari', 134:'Oristano', 135:'Olbia-Tempio', 136:'Ogliastra', 137:'Medio Campidano', 138:'Carbonia-Iglesias', 146:'Monza e della Brianza', 147:'Fermo', 148:'Barletta-Andria-Trani'</td></td></tr><tr><td>1</td><td>Tipo dato</td><td>2</td><td>3:'numero di forze di lavoro15 anni e oltre (valori in migliaia)', 4:'numero di inattivi (valori in migliaia)'</td></td></tr><tr><td>2</td><td>Misura</td><td>1</td><td>9:'valori assoluti'</td></td></tr><tr><td>3</td><td>Sesso</td><td>3</td><td>1:'maschi', 2:'femmine', 3:'totale'</td></td></tr><tr><td>4</td><td>Classe di età</td><td>12</td><td>1:'0-14 anni', 4:'15-24 anni', 7:'15-34 anni', 8:'25-34 anni', 10:'35-64 anni', 14:'35-44 anni', 17:'45-54 anni', 21:'55-64 anni', 22:'15-64 anni', 25:'65 anni e più', 28:'15 anni e più', 29:'totale'</td></td></tr><tr><td>5</td><td>Titolo di studio</td><td>5</td><td>11:'laurea e post-laurea', 12:'totale', 3:'licenza di scuola elementare, nessun titolo di studio', 4:'licenza di scuola media', 7:'diploma'</td></td></tr><tr><td>6</td><td>Cittadinanza</td><td>3</td><td>1:'italiano-a', 2:'straniero-a', 3:'totale'</td></td></tr><tr><td>7</td><td>Condizione professionale</td><td>9</td><td>6:'inattivi in età lavorativa', 7:'cercano lavoro non attivamente', 8:'cercano lavoro ma non disponibili a lavorare', 9:'non cercano ma disponibili a lavorare', 10:'non cercano e non disponibili a lavorare', 11:'inattivi in età non lavorativa', 12:'non forze di lavoro fino a 14 anni', 13:'non forze di lavoro di 65 anni e più', 14:'totale'</td></td></tr><tr><td>8</td><td>Motivo inattività</td><td>7</td><td>1:'scoraggiamento', 2:'motivi familiari', 3:'studio, formazione professionale', 4:'aspetta esiti passate azioni di ricerca', 5:'pensione, non interessa anche per motivi di età', 6:'altri motivi', 7:'totale'</td></td></tr><tr><td>9</td><td>Condizione dichiarata</td><td>8</td><td>1:'occupato', 6:'disoccupato alla ricerca di nuova occupazione', 7:'in cerca di prima occupazione', 8:'casalinga-o', 9:'studente', 10:'ritirato-a dal lavoro', 11:'in altra condizione', 12:'totale'</td></td></tr><tr><td>10</td><td>Tempo e frequenza</td><td>193</td><td>1536:'T4-1980', 2049:'T4-2007', 1540:'1981', 2053:'2008', 1542:'T1-1981', 2055:'T1-2008', 1546:'T2-1981', 2059:'T2-2008', 1551:'T3-1981', 2064:'T3-2008', 1555:'T4-1981', 2068:'T4-2008', 1559:'1982', 2072:'2009', 1561:'T1-1982', 2074:'T1-2009', 1565:'T2-1982', 2078:'T2-2009', 1570:'T3-1982', 2083:'T3-2009', 1574:'T4-1982', 2087:'T4-2009', 1578:'1983', 2091:'2010', 1580:'T1-1983', 2093:'T1-2010', 1584:'T2-1983', 2097:'T2-2010', 1589:'T3-1983', 2102:'T3-2010', 1593:'T4-1983', 2106:'T4-2010', 1597:'1984', 2110:'2011', 1599:'T1-1984', 2112:'T1-2011', 1603:'T2-1984', 2116:'T2-2011', 1608:'T3-1984', 2121:'T3-2011', 1612:'T4-1984', 2125:'T4-2011', 1616:'1985', 2129:'2012', 1618:'T1-1985', 2131:'T1-2012', 1622:'T2-1985', 2135:'T2-2012', 1627:'T3-1985', 2140:'T3-2012', 1631:'T4-1985', 2144:'T4-2012', 1635:'1986', 2148:'2013', 1637:'T1-1986', 2150:'T1-2013', 1641:'T2-1986', 2154:'T2-2013', 1646:'T3-1986', 2159:'T3-2013', 1650:'T4-1986', 2163:'T4-2013', 1654:'1987', 2167:'2014', 1656:'T1-1987', 2169:'T1-2014', 1660:'T2-1987', 2173:'T2-2014', 1665:'T3-1987', 2178:'T3-2014', 1669:'T4-1987', 2182:'T4-2014', 1673:'1988', 1675:'T1-1988', 2188:'T1-2015', 1679:'T2-1988', 2192:'T2-2015', 1684:'T3-1988', 2197:'T3-2015', 1688:'T4-1988', 1692:'1989', 1694:'T1-1989', 1698:'T2-1989', 1703:'T3-1989', 1707:'T4-1989', 1711:'1990', 1713:'T1-1990', 1717:'T2-1990', 1722:'T3-1990', 1726:'T4-1990', 1730:'1991', 1732:'T1-1991', 1736:'T2-1991', 1741:'T3-1991', 1745:'T4-1991', 1749:'1992', 1751:'T1-1992', 1755:'T2-1992', 1760:'T3-1992', 1764:'T4-1992', 1768:'1993', 1770:'T1-1993', 1774:'T2-1993', 1779:'T3-1993', 1783:'T4-1993', 1787:'1994', 1789:'T1-1994', 1793:'T2-1994', 1798:'T3-1994', 1802:'T4-1994', 1806:'1995', 1808:'T1-1995', 1812:'T2-1995', 1817:'T3-1995', 1821:'T4-1995', 1825:'1996', 1827:'T1-1996', 1831:'T2-1996', 1836:'T3-1996', 1840:'T4-1996', 1844:'1997', 1846:'T1-1997', 1850:'T2-1997', 1855:'T3-1997', 1859:'T4-1997', 1863:'1998', 1865:'T1-1998', 1869:'T2-1998', 1874:'T3-1998', 1878:'T4-1998', 1882:'1999', 1884:'T1-1999', 1888:'T2-1999', 1893:'T3-1999', 1897:'T4-1999', 1901:'2000', 1903:'T1-2000', 1907:'T2-2000', 1912:'T3-2000', 1916:'T4-2000', 1920:'2001', 1922:'T1-2001', 1926:'T2-2001', 1931:'T3-2001', 1935:'T4-2001', 1939:'2002', 1941:'T1-2002', 1945:'T2-2002', 1950:'T3-2002', 1954:'T4-2002', 1958:'2003', 1960:'T1-2003', 1964:'T2-2003', 1969:'T3-2003', 1973:'T4-2003', 1464:'1977', 1977:'2004', 1466:'T1-1977', 1979:'T1-2004', 1470:'T2-1977', 1983:'T2-2004', 1475:'T3-1977', 1988:'T3-2004', 1479:'T4-1977', 1992:'T4-2004', 1483:'1978', 1996:'2005', 1485:'T1-1978', 1998:'T1-2005', 1489:'T2-1978', 2002:'T2-2005', 1494:'T3-1978', 2007:'T3-2005', 1498:'T4-1978', 2011:'T4-2005', 1502:'1979', 2015:'2006', 1504:'T1-1979', 2017:'T1-2006', 1508:'T2-1979', 2021:'T2-2006', 1513:'T3-1979', 2026:'T3-2006', 1517:'T4-1979', 2030:'T4-2006', 1521:'1980', 2034:'2007', 1523:'T1-1980', 2036:'T1-2007', 1527:'T2-1980', 2040:'T2-2007', 1532:'T3-1980', 2045:'T3-2007'</td></td></tr></table>



.. code:: python

    spec = { 
        'Territorio':        'Italia',                            
        'Tipo dato':         'numero di inattivi (valori in migliaia)',                           
        'Misura':            'valori assoluti',               
        'Sesso':             'totale',                               
        'Classe di età':     '15 anni e più', 
        'Titolo di studio':  'totale', 
        'Cittadinanza' : 'totale',
        'Condizione professionale': 'totale',
        'Motivo inattività': 'totale',
        'Condizione dichiarata': 'totale',
        'Tempo e frequenza': 0                    
    }
    
    df_inattiv = istat_inattiv.getvalues(spec).dataset(0).to_table(rtype=pd.DataFrame)
    # df_inattiv

.. code:: python

    df_inattiv = df_inattiv[df_inattiv['Tempo e frequenza'].str.contains(r'^T.*')]
    df_inattiv.tail(6)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Tempo e frequenza</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>187</th>
          <td>T2-2014</td>
          <td>26594.57</td>
        </tr>
        <tr>
          <th>188</th>
          <td>T3-2014</td>
          <td>26646.90</td>
        </tr>
        <tr>
          <th>189</th>
          <td>T4-2014</td>
          <td>26257.15</td>
        </tr>
        <tr>
          <th>190</th>
          <td>T1-2015</td>
          <td>26608.07</td>
        </tr>
        <tr>
          <th>191</th>
          <td>T2-2015</td>
          <td>26487.67</td>
        </tr>
        <tr>
          <th>192</th>
          <td>T3-2015</td>
          <td>26746.26</td>
        </tr>
      </tbody>
    </table>
    </div>


