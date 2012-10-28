#!/usr/bin/python
from settings import schema_catalog, logger
from lxml import etree

class Catalog(object):
    def __init__(self):
        self._namespaces = None
        self._mets = None
        self._mods = None
        self._dc = None
        self._premis = None
        self._mix = None
        self._alto = None

    @property
    def mets(self):
        if not self._mets:
            schema = schema_catalog['mets']
            logger.debug("nacitam schema: " + schema['location'])
            self._mets = etree.XMLSchema(file=schema['location'])
        return self._mets

    @property
    def dc(self):
        if not self._dc:
            schema = schema_catalog['dc']
            logger.debug("nacitam schema: " + schema['location'])
            self._dc = etree.XMLSchema(file=schema['location'])
        return self._dc

    @property
    def mods(self):
        if not self._mods:
            schema = schema_catalog['mods']
            logger.debug("nacitam schema: " + schema['location'])
            self._mods = etree.XMLSchema(file=schema['location'])
        return self._mods
    
    @property
    def premis(self):
        if not self._premis:
            schema = schema_catalog['premis']
            logger.debug("nacitam schema: " + schema['location'])
            self._premis = etree.XMLSchema(file=schema['location'])
        return self._premis

    @property
    def mix(self):
        if not self._mix:
            schema = schema_catalog['mix']
            logger.debug("nacitam schema: " + schema['location'])
            self._mix = etree.XMLSchema(file=schema['location'])
        return self._mix

    @property
    def alto(self):
        if not self._alto:
            schema = schema_catalog['alto']
            logger.debug("nacitam schema: " + schema['location'])
            self._alto = etree.XMLSchema(file=schema['location'])
        return self._alto
    
    @property
    def namespaces(self):
        if not self._namespaces:
            namespaces = {}
            for item in schema_catalog:
                namespaces[item] = schema_catalog[item]['uri']
            self._namespaces = namespaces
        return self._namespaces
