#!/usr/bin/python
#-*- coding: utf-8 -*-

import logging, argparse, os, sys, tempfile

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
from settings import logger, workdir, set_logger_level, set_file_handler

# http://www.cafeconleche.org/books/effectivexml/chapters/47.html

parser = argparse.ArgumentParser(description="""Program validuje PSP balíček.

Umí validovat na třech úrovních:
- METS soubor
- hodnoty z číselníků existují
- linky, na ktere se v balíčku odkazuje existují

  Každá z těchto voleb se dá vypnout.

Program rozbalí zadaný PSP balíček do adresáře %s
""" % (str(workdir), ),
                                 formatter_class = argparse.RawTextHelpFormatter
                                 )
parser.add_argument('-m','--mets',
                    help='zkontroluje METS soubor', 
                    action='store_true',
                    required=False)

parser.add_argument('-v','--verbose',
                    help='hlášky programu budou podrobnější', 
                    action="store_true",
                    required=False)

parser.add_argument('--version',
                    help='verze programu. Vypíše i verzi dokumentace, co popisuje strukturu PSP balíčku', 
                    action='version',
                    version = "%(prog)s verze 0.1")

parser.add_argument('PSP',
                    help="cesta k PSP balíčku",
                    nargs='?'
                    )

parser.add_argument('-l',
                    '--list-validators',
                    help = 'zobrazí seznam validací, co program umí',
                    action = "store_true",
                    default = False,
                    required = False
                    )

parser.add_argument('-d',
                    '--debug',
                    help = 'zobrazí ladici hlasky',
                    required = False,
                    action = "store_true",
                    default = False
                    )

parser.add_argument('-i',
                    '--info',
                    help = 'zobrazí popis vybrané validace',
                    required = False
                    )

parser.add_argument('-p',
                    '--partial',
                    help = 'zavola jen jeden kontretni krok validace. Seznam validaci vypisuje argument -l',
                    required = False,
                    default = None
                    )

parser.add_argument('-s','--summary',
                    help='na konci vypíše přehled testů, co provedl a s jakým skončily výsledkem.', 
                    action='store_true',
                    required=False)

parser.add_argument('--normdir',
                    help='na konci se maže pracovní adresář. S tímto argumentem se adresář nesmaže.',
                    action='store_true',
                    default=False,
                    required=False)

args = parser.parse_args()

# file:///usr/share/doc/python-lxml-doc/html/xpathxslt.html

if args.info:
    print Validator.desc_of_validator(args.info)
    sys.exit(0)
    
if args.list_validators:
    print "seznam validací:\n\t",
    print "\n\t".join(Validator.validators())
    sys.exit(0)

if args.verbose:
    set_logger_level(logging.INFO)
if args.debug:
    set_logger_level(logging.DEBUG)

validator = Validator(psp = PSP(fname=args.PSP), **vars(args))
set_file_handler(validator.psp.basename)
logger.info("budu validovat soubor %s" % ( str(validator.psp), ))
logger.info("pracuji v adresari: %s" % (str(workdir),))
if args.partial:
    logger.info("budu volat jen jeden krok validace: %s" % (args.partial,))

validator.validate(method = args.partial)
if args.summary:
    def prepare_setFixedWidth(max_width):
        def formatter(s):
            format_string = "{:<" + str(max_width) + "}"
            return format_string.format(s)
        return formatter

    set_logger_level(logging.INFO)
    formatter = prepare_setFixedWidth(max([len(ii['validator']) for ii in validator.summary]))
    logger.info("vysledky validace:\n\t" + "\n\t".join([ "%s: %s" %( formatter(ii['validator']), ii['result'] and 'OK' or 'Error') for ii in validator.summary]))

if not args.normdir:
    workdir.rmdir()
else:
    logger.info("rozbalený balíček je v adresáři: " + str(workdir))
