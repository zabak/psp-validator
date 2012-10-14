# -*- coding: utf-8 -*-
import logging, sys, os
from lxml import etree

from directories import WorkDir
project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

_logger = None
_workdir = None

def set_logger_level(level):
    _logger.setLevel(level)

def get_logger():
    global _logger
    if not _logger:
        _logger = logging.getLogger("PSP_VALIDATION")
        # %d (%F{1}:%L)         %-15c   - %p - %m %n
        formatter = logging.Formatter('%(asctime)s %(name)s\t%(levelname)s \t- %(message)s')
        _logger.setLevel(logging.ERROR)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        _logger.addHandler(ch)
    return _logger

def get_workdir():
    global _workdir
    if not _workdir:
        _workdir = WorkDir(tmpbase = os.path.join(project_dir,'tmp'))
    return _workdir

logger = get_logger()
workdir = get_workdir()

fname = os.path.join(project_dir,"lib","schema","mets.xsd")

def withSchemaDir(schema):
    return os.path.join(project_dir,"lib","schema",schema)

schema_catalog = { 
    'mets': { 'uri': "http://www.loc.gov/METS/",
              'location': withSchemaDir("mets.xsd"),
              },
    'dc':   { 'uri': "http://www.openarchives.org/OAI/2.0/oai_dc/",
              'location': withSchemaDir("oai_dc.xsd"),
              },
    'mods': { 'uri':"http://www.loc.gov/mods/v3",
              'location': withSchemaDir("mods-3-4.xsd"),
              },
    'xlink': {'uri': "http://www.w3.org/1999/xlink",
              'location': ""
        }
    }

