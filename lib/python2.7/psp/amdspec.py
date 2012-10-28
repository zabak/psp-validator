# -*- coding: utf-8 -*-

from lxml import etree

class AmdSpec(object):
    def __init__(self,fname):
        self.fname = fname
        self._etree = None

    @property
    def etree(self):
        if not self._etree:
            self._etree = etree.parse(self.fname)
        return self._etree

    def xpath(self,path):
        return self.etree.xpath(path, namespaces = { 'mods': schema_catalog['mods']['uri'],
                                                     'mets': schema_catalog['mets']['uri'],
                                                     'dc': schema_catalog['dc']['uri'],
                                                     'premis': schema_catalog['premis']['uri'],
                                                     'xlink': schema_catalog['xlink']['uri'],
                                                     }
                                )
