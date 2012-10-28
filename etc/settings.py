# -*- coding: utf-8 -*-
import logging, sys, os
from lxml import etree
import logging.handlers

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

        tfh = logging.handlers.TimedRotatingFileHandler(os.path.join(project_dir,"log","messages.log"), when='midnight', backupCount=7)
        tfh.setFormatter(formatter)
        _logger.addHandler(tfh)
        
    return _logger

def set_file_handler(psp_name):
    logger = get_logger()
    formatter = logging.Formatter('%(asctime)s %(name)s\t%(levelname)s \t- %(message)s')
    ff = logging.FileHandler(workdir.join(psp_name + ".log"))
    ff.setFormatter(formatter)
    logger.addHandler(ff)
    

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
    'xsi': { 'uri':"http://www.w3.org/2001/XMLSchema-instance",
             'location': withSchemaDir("XMLSchema.xsd"),
             },
    'xlink': {'uri': "http://www.w3.org/1999/xlink",
              'location': withSchemaDir("xlink.xsd")
              },
    'mix': { 'uri': "http://www.loc.gov/mix/v20",
             'location': withSchemaDir("mix20.xsd"),
             },
    'premis': { 'uri': "info:lc/xmlns/premis-v2",
             	'location': withSchemaDir("premis-v2-1.xsd"),
                },
    'alto': { 'uri': "http://www.loc.gov/standards/alto/ns-v2#",
              'location': withSchemaDir("alto-v2.0.xsd"),
              },
    }

