#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse, os, sys, tempfile,traceback
import glob

# pridame lokalni knihovny
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','python2.7'))
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'etc'))
if 'XML_catalog_files' in os.environ:
       os.environ['XML_CATALOG_FILES'] = os.environ['XML_CATALOG_FILES'] + " " + os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','schema','catalog.xml')
else:
       os.environ['XML_CATALOG_FILES'] = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','schema','catalog.xml')

from directories import WorkDir
from psp import PSP
from validator import Validator
from settings import workdir, get_logger, get_file_log_handler
import logging

# http://www.cafeconleche.org/books/effectivexml/chapters/47.html
logger = get_logger()
parser = argparse.ArgumentParser(description="""Program validuje PSP balicky.

Umi validovat na trech urovnich:
- METS soubor
- hodnoty z ciselniku existuji
- linky, na ktere se v balicku odkazuje existuji

  Kazda z techto voleb se da vypnout.

Program rozbali zadany/zadane PSP balicek/balicky do adresare %s

Pokud je zadany adresar, tak ho bere jako rozbaleny PSP balicek
a pokusi se je zkontrolovat.

Pokud se pri kontrole souboru v adresari amdSec, ... objevi chyba,
program skonci u prvniho souboru s chybou.
Vetsinou se chyby opakuji a tak by bylo hodne stejnych chyb.
""" % (str(workdir), ),
                                 formatter_class = argparse.RawTextHelpFormatter
                                 )
parser.add_argument('-m','--mets',
                    help='zkontroluje METS soubor', 
                    action='store_true',
                    required=False)

parser.add_argument('-v','--verbose',
                    help='hlasky programu budou podrobnejsi', 
                    action="store_true",
                    required=False)

parser.add_argument('--version',
                    help='verze programu. Vypise i verzi dokumentace, co popisuje strukturu PSP balicku', 
                    action='version',
                    version = "%(prog)s verze 0.1")

parser.add_argument('PSP',
                    help="cesta k PSP balicku. Muze to byt soubor, nebo adresar. Pokud to je adresar, bere ho jako rozbaleny PSP balicek. Muze byt zadano vice PSP balicku.",
                    nargs='+'
                    )

parser.add_argument('-l',
                    '--list-validators',
                    help = 'zobrazi seznam validaci, co program umi',
                    action = "store_true",
                    default = False,
                    required = False
                    )

parser.add_argument('-d',
                    '--debug',
                    help = 'zobrazi ladici hlasky',
                    required = False,
                    action = "store_true",
                    default = False
                    )

parser.add_argument('-i',
                    '--info',
                    help = 'zobrazi popis vybrane validace',
                    required = False
                    )

parser.add_argument('-p',
                    '--partial',
                    help = 'zavola jen jeden kontretni krok validace. Seznam validaci vypisuje argument -l',
                    required = False,
                    default = None
                    )

parser.add_argument('-s','--summary',
                    help='na konci vypise prehled testu, co provedl a s jakym skoncily vysledkem.', 
                    action='store_true',
                    required=False)

parser.add_argument('--normdir',
                    help='na konci se maze pracovni adresar. S timto argumentem se adresar nesmaze.',
                    action='store_true',
                    default=False,
                    required=False)

parser.add_argument('-a','--all-files',
                    help='Kdyz se validuji soubory v adresari, probere vsechny soubory, i kdyz se objevi chyba.',
                    action='store_true',
                    default=False,
                    required=False)

args = parser.parse_args()

# file:///usr/share/doc/python-lxml-doc/html/xpathxslt.html

if args.info:
    print Validator.desc_of_validator(args.info)
    workdir.rmdir()
    sys.exit(0)
    
if args.list_validators:
    print "seznam validaci:\n\t",
    print "\n\t".join(Validator.validators())
    workdir.rmdir()
    sys.exit(0)


root_logger = logging.getLogger()

if args.verbose:
    root_logger.setLevel(logging.INFO)
if args.debug:
    root_logger.setLevel(logging.DEBUG)

# print vars(args)
# sys.exit(1)

# logger.debug("pracovni adresar je: " + str(workdir))
# psps = (os.path.isdir(args.PSP) and  glob.glob(os.path.join(args.PSP,'*.zip'))) \
#     or (os.path.isfile(args.PSP) and [args.PSP]) 

# if not psps:
#        logger.error(str(args.PSP) + " neexistuje")
#        workdir.rmdir()
#        sys.exit(1)

summaries = []
for psp in args.PSP:
       basename = os.path.basename(os.path.splitext(os.path.splitext(psp)[0])[0])
       file_log_handler = get_file_log_handler(fpath=os.path.join(os.path.dirname(psp),basename+".log"))
       logger.addHandler(file_log_handler)
       try: 
              validator = Validator(psp = PSP(fpath=psp), logger=logger, **vars(args))
              condition = lambda name: True
              if args.partial:
                     condition = lambda name: name==args.partial
                     pass
              if args.mets:
                     condition = lambda name: '_mets' in name
                     pass
              validator.validate(condition)
              if args.summary:
                     def prepare_setFixedWidth(max_width):
                            def formatter(s):
                                   format_string = "{:<" + str(max_width) + "}"
                                   return format_string.format(s)
                            return formatter
                                                        
                     logger.setLevel(logging.INFO)
                     formatter = prepare_setFixedWidth(max([len(ii['validator']) for ii in validator.summary]))
                     logger.info("vysledky validace:\n\t" + "\n\t".join([ "%s: %s" %( formatter(ii['validator']), ii['result'] and 'OK' or 'Error') for ii in validator.summary]))
                     summaries.append({ 'psp': psp, 'result': False not in [ii['result'] for ii in validator.summary] })
       except:
              logger.error("chyba pri validaci souboru: %s\n\t%s" % (psp, traceback.format_exc()))
              sys.exc_clear()
       logger.removeHandler(file_log_handler)
       file_log_handler.close()

if args.summary:
       def prepare_setFixedWidth(max_width):
              def formatter(s):
                     format_string = "{:<" + str(max_width) + "}"
                     return format_string.format(s)
              return formatter
       
       logger.setLevel(logging.INFO)
       formatter = prepare_setFixedWidth(max([len(ss['psp']) for ss in summaries]))
       logger.info("vysledky validace souboru:\n\t" + "\n\t".join([ "%s: %s" %( formatter(ss['psp']), ss['result'] and 'OK' or 'Error') for ss in summaries]))
       
if not args.normdir:
    workdir.rmdir()
else:
    logger.info("vsechny rozbalene balicky jsou v adresari: " + str(workdir))
