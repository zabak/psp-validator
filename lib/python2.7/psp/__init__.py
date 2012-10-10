#!/usr/bin/python
#-*- coding: utf-8 -*-

from settings import logger, workdir
import zipfile

class PSP(object):
    """ umí rozbalit balíček do zadaného pracovního adresáře.
    Umí poskytovat přístup k jednotlivým částem balíčku"""

    def __init__(self, fname):
        self.fname = fname
        self.archive = zipfile.ZipFile(self.fname,"r")
        self._unzipped = False
        
    def __str__(self):
        return self.fname

    def _unzip(self):
        self.archive.extractall(workdir.mkdir('PSP'))
        self._unzipped = True
        
    @property
    def mets(self):
        if not self._unzip:
            self._unzip()
        return "ahoj"
        
        
