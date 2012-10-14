#!/usr/bin/python
#-*- coding: utf-8 -*-

from settings import logger, workdir
import zipfile, os
from .mets import Mets

class NoMetsException(Exception):
    pass

class PSP(object):
    """ umí rozbalit balíček do zadaného pracovního adresáře.
    Umí poskytovat přístup k jednotlivým částem balíčku"""

    def __init__(self, fname):
        self.fname = fname
        self.archive = zipfile.ZipFile(self.fname,"r")
        self.dirname = workdir.join('PSP')
        self._unzipped = False
        
    def __str__(self):
        return self.fname

    def _unzip(self):
        self.archive.extractall(workdir.mkdir('PSP'))
        self._unzipped = True
        
    @property
    def mets(self):
        if not self._unzipped:
            self._unzip()

        fnames = [ff for ff in os.listdir(self.dirname) if 'METS' in ff]
        if not fnames:
            raise NoMetsException(str(self))

        return Mets(os.path.join(self.dirname,fnames[0]))
        
        
