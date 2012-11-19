.. PSP Validator documentation master file, created by
   sphinx-quickstart on Mon Nov 19 14:04:47 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PSP validátor
=============

.. contents::

.. toctree::
   :maxdepth: 2

Ve zkratce
----------

  Program validuje ``PSP`` balíček, nebo celý adresář ``PSP`` balíčků.

  ``PSP`` se používá k uchování digitálních informací o periodikách a monografiích. 
  Tento balíček používá `Národní knihovna <http://www.nkp.cz>`_ k digitalizaci a uchování informací o periodikách a monografiích.

  Podrobnosti o formátech použitých v ``PSP`` balíčku jsou na stránkách `Národní knihovny <http://www.ndk.cz/digitalizace/vystavena-nova-verze-definice-metadat-pro-periodika-a-monografie>`_.

  Program je vystaven v repozitáři `Google Code <https://code.google.com/p/psp-validator/>`_.

   * umi jednu verzi schematu
   * schema se vyvyji
   * budou chodit emaily
   * komunikace v cestine
   * repozitar na code.google.com
   * software bude v anglictine
   * prubezne verze standardu se nebudou publikovat
   * zapojeni krajske knihovny do testovani - posilali by testovaci data pro testovani
   * program by nemel skoncit na prvni chybe. protoze se schema vyvyji a neco uz nemusi byt chybou
   * tentyz program by mel byt k dispozici na webu pro krajske knihovny, aby si mohly dopredu zkontrolovat data
   * program bude mit volbu:

     * kontrolovat jen metadata (mets soubor)
     * zkontrolvoat vsechno, vcetne metadat
     * vypnout kontrolu ciselniku

   * udelat instalator pro windows
   * vystup bude v textovem souboru

Co umí
------

   - [X] validuje hlavní soubor ``METS`` podle schematu ``METS``
   - [X] validuje položky ``dc`` v hlavním souboru ``METS`` podle schematu ``Dublin Core``
   - [X] validuje soubory v adresáři ``amdSec`` podle schematu ``METS``
   - [X] validuje jednotlivé části ``premis:object`` a ``mix:mix`` v souborech v adresáři ``amdsec``
   - [X] zkontroluje, že všechny linky, které jsou v souboru ``METS``, existují
   - [X] zkontroluje ``MD5`` součet všech souborů, na které se soubor ``METS`` odkazuje
   - [X] validuje soubory v adresáři ``ALTO`` podle schematu ``ALTO``

   Program vypisuje informace o průběhu validací na konzoli a současně do souboru ``log/messages.log``.
     
   Pokud program validuje více balíčků, tak ke každému balíčku doplní samostatný log soubor s výpisy průběhu validace.

   Validovaný balíček rozbaluje do adresáře ``tmp``.

   Pokud se programu místo souboru zadá adresář, předpokládá, že v něm jsou ``PSP`` souboru. Ty všechny zvaliduje.

Instalace
---------
Windows
.......

#. instalace python 2.7

   * stáhnout aktuální verzi pythonu http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi
     a nainstalovat ji.
   * nastavit cesty k binárkám pythonu
     aby se dal volat python v ``cmd``.

#. instalace lxml

   * instalace binárek
     http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
      
     vybere se lxml-X.X.X.win*.exe
     Ten se nainstaluje.

#. instalace programu

     - uloží se ``zip`` balíček ze sekce https://code.google.com/p/psp-validator/downloads/list
     - rozbalí se do adresáře ``C:\Opt``
     
     Takže program bude v adresáři: ``C:\Opt\psp-validator``

     - do proměnné ``PATH`` se doplní cesta k programu: ``C:\Opt\psp-validator\bin``

Volání
------
   Pokud jsme ve *Windows*, tak se k cestě k programu přidá název disku: ``C:\Opt\psp-validator\bin\validate-psp.py --help`` ::

     usage: validate-psp.py [-h] [-m] [-v] [--version] [-l] [-d] [-i INFO] [-p PARTIAL] [-s] [--normdir] [-a] [PSP]

     Program validuje PSP balíček.

     Umí validovat na třech úrovních:
     - METS soubor
     - hodnoty z číselníků existují
     - linky, na ktere se v balíčku odkazuje existují

     Každá z těchto voleb se dá vypnout.

     Program rozbalí zadaný PSP balíček do adresáře /opt/psp-validator/tmp/PSP-Validation-2012-11-19-3wRkot

     Pokud je zadaný adresář, tak vezme všechny soubory, co mají příponu =.zip=
     a pokusí se je zkontrolovat.

     Pokud se při kontrole souborů v adresáři amdSec, ... objeví chyba,
     program skončí u prvního souboru s chybou.
     Většinou se chyby opakují a tak by bylo hodně stejných chyb.

     positional arguments:
     PSP                   cesta k PSP balíčku. Muze to byt soubor, nebo adresar. Pokud to je adresar, 
                           vezme všechny soubory a zvaliduje je.

     optional arguments:
     -h, --help            show this help message and exit
     -m, --mets            zkontroluje METS soubor
     -v, --verbose         hlášky programu budou podrobnější
     --version             verze programu. Vypíše i verzi dokumentace, co popisuje strukturu PSP balíčku
     -l, --list-validators
                           zobrazí seznam validací, co program umí
     -d, --debug           zobrazí ladici hlasky
     -i INFO, --info INFO  zobrazí popis vybrané validace
     -p PARTIAL, --partial PARTIAL
                        zavola jen jeden kontretni krok validace. Seznam validaci vypisuje argument -l
     -s, --summary         na konci vypíše přehled testů, co provedl a s jakým skončily výsledkem.
     --normdir             na konci se maže pracovní adresář. S tímto argumentem se adresář nesmaže.
     -a, --all-files       Kdyz se validuji soubory v adresari, probere vsechny soubory, i kdyz se objevi chyba.

Přehled dostupných validací
...........................

argument ``-l`` pomůže ::

   /opt/psp-validator/bin/validate-psp.py -l

   seznam validací:
    	01_mets
    	01_mets_dc
    	01_mets_mods
    	02_links_checksums
    	02_links_exist
    	03_techspecs
    	03_techspecs_premis_mix
    	04_altos

příklad validace METS souboru
.............................

program má validovat jen hlavní ``metadata`` ::

   /opt/psp-validator/bin/validate-psp.py -v -s /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip 2>&1

   2012-10-28 21:24:52,381 PSP_VALIDATION	INFO 	- budu validovat soubor /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip
   2012-10-28 21:24:52,381 PSP_VALIDATION	INFO 	- pracuji v adresari: /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI
   2012-10-28 21:24:52,381 PSP_VALIDATION	INFO 	- validator: validace hlavního METS souboru                                                 *01_mets*
   2012-10-28 21:24:55,745 PSP_VALIDATION	INFO 	- validator: validace vnitřku METS souboru, specifikace DC                                  *01_mets_dc*
   2012-10-28 21:24:56,723 PSP_VALIDATION	INFO 	- validator: validace vnitřku hlavního METS souboru                                        *01_mets_mods*
   2012-10-28 21:24:56,737 PSP_VALIDATION	INFO 	- validator: kontrola CHECKSUM všech souborů na které se v hlavním METS souboru odkazuje *02_links_checksums*
   2012-10-28 21:24:57,591 PSP_VALIDATION	INFO 	- validator: validace linek v hlavním METS souboru                                          *02_links_exist*
   2012-10-28 21:24:57,653 PSP_VALIDATION	INFO 	- validator: validace souborů ve složce amdSec                                             *03_techspecs*
   2012-10-28 21:24:57,716 PSP_VALIDATION	INFO 	- validator: validace souborů ve složce amdSec na technická metadata                      *03_techspecs_premis_mix*
   2012-10-28 21:24:57,731 PSP_VALIDATION	ERROR 	- chyba validace: chyby validace souboru /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml: /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:11:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:11:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.|/opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:64:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:64:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.|/opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:117:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0001.xml:117:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.
   2012-10-28 21:24:57,805 PSP_VALIDATION	ERROR 	- chyba validace: chyby validace souboru /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml: /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:11:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:11:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.|/opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:64:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:64:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.|/opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:117:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_4_2: Element '{info:lc/xmlns/premis-v2}object', attribute '{http://www.w3.org/2001/XMLSchema-instance}type': The QName value 'file' of the xsi:type attribute does not resolve to a type definition.
   /opt/psp-validator/tmp/PSP-Validation-2012-10-28-gQT1JI/complete_NDK-000000000008_1350896484227/amdSec/AMD_METS_cb6edb20-19ae-11e2-aff6-005056827e51_0038.xml:117:0:ERROR:SCHEMASV:SCHEMAV_CVC_TYPE_2: Element '{info:lc/xmlns/premis-v2}object': The type definition is abstract.
   2012-10-28 21:24:57,806 PSP_VALIDATION	INFO 	- validator: validace souborů v adresáři =ALTO=                                           *04_altos*
   2012-10-28 21:24:57,835 PSP_VALIDATION	INFO 	- vysledky validace:
	   01_mets                : OK
	   01_mets_dc             : OK
	   01_mets_mods           : OK
	   02_links_checksums     : OK
	   02_links_exist         : OK
	   03_techspecs           : OK
	   03_techspecs_premis_mix: Error
	   04_altos               : OK


Jednotlivé validace
-------------------

Informace o jednotlivých validacích si můžeme zobrazit volbou ``-i`` ::

     /opt/psp-validator/bin/validate-psp.py -i 01_mets

        validace hlavního METS souboru
             validuje hlavní METS soubor podle specifikace METS



přehled
.......

  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 01_mets                 | validace hlavního METS souboru                                                  | validuje hlavní METS soubor podle specifikace METS                                                                       |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 01_mets_dc              | validace vnitřku METS souboru, specifikace DC                                   | validuje vnitřní položky DC v METS soubor podle specifikace Dublin Core                                                  |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 01_mets_mods            | validace vnitřku hlavního METS souboru, specifikace MODS                        | validuje vnitřní položky MODS v hlavním METS soubor podle specifikace MODS                                               |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 02_links_checksums      | kontrola CHECKSUM všech souborů na které se v hlavním METS souboru odkazuje     | zkontroluje, zda mají soubory, na které linky odkazují, správnou CHECKSUM.                                               |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 02_links_exist          | validace linek v hlavním METS souboru                                           | zkontroluje, zda existují všechny soubory na které se odkazují linky v hlavním souboru METS.                             |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 03_techspecs            | validace souborů ve složce amdSec                                               | zkontroluje předběžně jednotlivé soubory ve složce =amdSec= podle formátu METS                                           |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
  | 03_techspecs_premis_mix | validace souborů ve složce amdSec na technická metadata                         | zkontroluje, zda jednotlivé soubory odpovídají použitým schematům.                                                       |
  |                         |                                                                                 | To je formát METS a vevnitřs jsou polozky =premis:object= podle schematu PREMIS v2.1. a položky =mix:mix= ve formatu MIX |
  +-------------------------+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+


rady
----

Chci přehledný výpis
....................

Program na konci vypíše jen přehled provedených validací. 
    
Při validaci jednotlivých souborů skončí při první chybě. ::

      /opt/psp-validator/bin/validate-psp.py -s -o DIR
        
Chci validovat jen hlavní ``METS`` soubor
............................................

Program provede jen validace spojené s hlavním =METS= souborem. ::

      /opt/psp-validator/bin/validate-psp.py -m -s /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip
    
Chci vidět seznam validací, co program umí
...........................................

Program vypíše seznam dostupných validací. ::

     /opt/psp-validator/bin/validate-psp.py -l
    
Chci vidět informace o jedné validaci
.....................................

Program vypíše podrobné informace o vybrané validaci. ::

     /opt/psp-validator/bin/validate-psp.py -i 04_altos

Chci vidět pouze výsledky na konci
..................................

Program na konci vypíše přehled provedených validací a jejich výsledek. ::

     /opt/psp-validator/bin/validate-psp.py -s /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip

Chci vidět výsledky i průběh validace
.....................................

Program bude průběžně informovat o tom, co provádí a na konci vypíše přehled provedených validací a jejich výsledek. ::

     /opt/psp-validator/bin/validate-psp.py -v -s /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip


Chci provést jen určitou validaci
.................................

Program provede jen vybranou validaci a skončí. ::

     /opt/psp-validator/bin/validate-psp.py -p 03_techspecs /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip

Chci zachovat rozbalený balíček
...............................

Program na konci ponechá rozbalený balíček. ::

     /opt/psp-validator/bin/validate-psp.py -s -p 03_techspecs --normdir /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip


Když program vypisuje hodně chyb
.................................

    - pustím program se souhrnným výpisem na konci
    - zjistím, které validace neprošly
    - pustím program s dotyčnou validací a aby skončil při první chybě a zachoval rozbalený balíček ::

	/opt/psp-validator/bin/validate-psp.py -v -s -p 03_techspecs --normdir /opt/psp-validator/tmp/complete_NDK-000000000008_1350896484227.zip

..
  (defun run()
     (interactive)
     (with-current-buffer "*shell*"
        (end-of-buffer)
	(insert "make html")
	(comint-send-input)
	)
     )
