#!/usr/bin/python
#-*- coding: utf-8 -*-

import logging, argparse, os, sys, tempfile

# pridame lokalni knihovny
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','python2.7'))
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'etc'))

from directories import WorkDir
from psp import PSP
from validator import Validator
from settings import logger, workdir

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
                    help='Zkontroluje METS soubor', 
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

parser.add_argument('-i',
                    '--info',
                    help = 'zobrazí popis vybrané validace',
                    required = False
                    )

args = parser.parse_args()

if args.info:
    print Validator.desc_of_validator(args.info)
    sys.exit(0)
    
if args.list_validators:
    print "seznam validací:\n\t",
    print "\t\n".join(Validator.validators())
    sys.exit(0)

validator = Validator(psp = PSP(fname=args.PSP), **vars(args))
logger.info("budu validovat soubor %s" % ( str(validator.psp), ))
validator.validate()
