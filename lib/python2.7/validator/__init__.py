# -*- coding: utf-8 -*-
from settings import logger, schema_catalog
import re
from .catalog import Catalog

def get_short_description(doc):
    result = re.search("^[\ \t]*([^\n]+)", doc, re.MULTILINE)
    return result.group(1)

class Validator(object):
    def __init__(self, psp, **kwargs):
        self.psp = psp
        self.kwargs = kwargs
        self.catalog = Catalog()

    @classmethod
    def short_desc_of_validator(self,name):
        methods = [ 'validate_' + v for v in self.validators() if v == name ]
        if methods:
            m = getattr(self,methods[0])
            return get_short_description(m.__doc__)
        return None
    @classmethod
    def desc_of_validator(self,name):
        methods = [ 'validate_' + v for v in self.validators() if v == name ]
        if methods:
            m = getattr(self,methods[0])
            return m.__doc__
        return None

    @classmethod
    def validators(self):
        method_names = [ m for m in dir(self) if 'validate_' in m ]
        method_names.sort()
        return [ m.split("validate_")[1] for m in method_names ]
        
    def run_validator(self, name):
        methods = [ 'validate_' . v for v in self.validators() if v == name ]
        if methods:
            m = methods[0]
            logger.info("validator: %s" % (get_short_description(m.__doc__)))
            m()
        pass
        
    def validate(self,method=None):
        """ zavola vsechny validace, co odpovidaji argumentum programu.
        Pokud je zadana metoda. Zavola jen jedno dotycnou validaci.
        napr: 01_mets
        """
        if method:
            logger.debug('vybrana metoda validace: ' + method)
        method_names = [ m for m in dir(self) if 'validate_' in m ]
        method_names.sort()
        methods = [ getattr(self,m) for m in method_names if (method and m == ('validate_' + method)) or (not method) ]
        for m in methods:
            logger.info("validator: %s" % (get_short_description(m.__doc__)))
            m()
        pass

    def validate_01_mets(self):
        """ validace METS souboru
        @group: mets
        validuje METS soubor podle specifikace METS"""
        mets = self.psp.mets
        schema = self.catalog.mets
        logger.debug("volam schema.validate")
        result = schema.validate(mets.etree)
        logger.debug("vysledek schema.validate:" + str(result))
        if not result:
            logger.error("validace souboru %s skoncila s chybou: %s" % (str(mets), schema.error_log))
        return result

    def validate_02_mets_mods(self):
        """ validace vnitrku METS souboru
        @group: mets
        validuje vnitrni polozky MODS v METS soubor podle specifikace MODS"""
        mets = self.psp.mets
        mods = mets.etree.xpath("//mods:mods",  
                                namespaces = { 'mods': schema_catalog['mods']['uri'],
                                               'mets': schema_catalog['mets']['uri'],
                                               }
                                )
        if len(mods) == 0:
            logger.error("nenasel jsem zadnou mods polozku")
            return False

        logger.debug('nalezene mods elementy: ' + str(mods))
        
        schema = self.catalog.mods
        results = [ schema.validate(m) or schema.error_log for m in mods ]
        logger.debug("vysledky schema.validate:" + str(results))
        some_error = 'Error' in [ r and 'Error' for r in results ]
        if some_error:
            logger.error('chyby validace: ' + str([r for r in results if r]))
            return False
        
        return True
