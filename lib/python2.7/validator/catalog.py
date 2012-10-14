#!/usr/bin/python
from settings import schema_catalog, logger
from lxml import etree

class Catalog(object):
    def __init__(self):
        self._mets = None
        self._mods = None
        self._dc = None

    @property
    def mets(self):
        if not self._mets:
            schema = schema_catalog['mets']
            logger.info("nacitam schema: " + schema['location'])
            self._mets = etree.XMLSchema(file=schema['location'])
        return self._mets

    @property
    def dc(self):
        if not self._dc:
            schema = schema_catalog['dc']
            logger.info("nacitam schema: " + schema['location'])
            self._dc = etree.XMLSchema(file=schema['location'])
        return self._dc

    @property
    def mods(self):
        if not self._mods:
            schema = schema_catalog['mods']
            logger.info("nacitam schema: " + schema['location'])
            self._mods = etree.XMLSchema(file=schema['location'])
        return self._mods
    
