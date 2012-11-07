# -*- coding: utf-8 -*-
import logging, sys, os
from lxml import etree
import logging.handlers

from directories import WorkDir
project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

_workdir = None

def get_logger(name=None):
    logger = logging.getLogger(name and "psp_validation."+name or "psp_validation")
        # %d (%F{1}:%L)         %-15c   - %p - %m %n
    formatter = logging.Formatter('%(levelname)s \t- %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    tfh = logging.handlers.TimedRotatingFileHandler(os.path.join(project_dir,"log","messages.log"), when='midnight', backupCount=7)
    tfh.setFormatter(formatter)
    logger.addHandler(tfh)
    return logger

def get_file_log_handler(fpath):
    """ logger for psp validator. It appends logs into local file """
    formatter = logging.Formatter('%(levelname)s \t- %(message)s')
    fh = logging.FileHandler(fpath, mode='w')
    fh.setFormatter(formatter)
    return fh
        
    

def get_workdir():
    global _workdir
    if not _workdir:
        _workdir = WorkDir(tmpbase = os.path.join(project_dir,'tmp'))
    return _workdir

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

