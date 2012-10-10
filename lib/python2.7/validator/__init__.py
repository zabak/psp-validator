# -*- coding: utf-8 -*-
from settings import logger
import re

def get_short_description(doc):
    result = re.search("^[\ \t]*([^\n]+)", doc, re.MULTILINE)
    return result.group(1)

class Validator(object):
    def __init__(self, psp, **kwargs):
        self.psp = psp
        self.kwargs = kwargs
        
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
        
    def run_validator(self,name):
        methods = [ 'validate_' . v for v in self.validators() if v == name ]
        if methods:
            m = methods[0]
            logger.info("validator: %s" % (get_short_description(m.__doc__)))
            m()
        pass
        
    def validate(self):
        """ zavola vsechny validace, co odpovidaji argumentum programu """
        method_names = [ m for m in dir(self) if 'validate_' in m ]
        method_names.sort()
        methods = [ getattr(self,m) for m in method_names ]
        for m in methods:
            logger.info("validator: %s" % (get_short_description(m.__doc__)))
            m()
        pass

    def validate_01_mets(self):
        """ validace METS souboru
        @group: mets
        validuje METS soubor podle specifikace """
        logger.info("validuji mets")
        mets = self.psp.mets
        pass

