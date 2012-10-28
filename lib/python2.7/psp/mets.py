# -*- coding: utf-8 -*-

from lxml import etree
from settings import schema_catalog

class Mets(object):
    def __init__(self,fname):
        self.fname = fname
        self._etree = None

    @property
    def etree(self):
        if not self._etree:
            self._etree = etree.parse(self.fname)
        return self._etree

    def xpath(self,path,namespaces = {}):
        return self.etree.xpath( path, namespaces = namespaces)
