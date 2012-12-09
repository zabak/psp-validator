#!/usr/bin/python
#-*- coding: utf-8 -*-

from settings import workdir
import zipfile, os, os.path
from .mets import Mets
from .amdspec import AmdSpec

class NoMetsException(Exception):
    pass

class NoProperDirectoryInZipFile(Exception):
    pass

class PSP(object):
    """ umí rozbalit balíček do zadaného pracovního adresáře.
    Umí poskytovat přístup k jednotlivým částem balíčku.
    
    Pokud je fpath adresar, bere to jako rozbaleny PSP balicek.
    """

    def __init__(self, fpath):
        self.fpath = fpath
        self.archive = None
        self._unzipped = False
        self.basename = os.path.basename(os.path.splitext(os.path.splitext(self.fpath)[0])[0])

        if not os.path.isdir(fpath):
            self.archive = zipfile.ZipFile(self.fpath,"r")
            # self.dirname is known after zip file is unzipped
        else:
            self.dirname = fpath
            self._unzipped = True
        
    def __str__(self):
        return self.fpath

    def _unzip(self):
        self.archive.extractall(str(workdir))
        self.dirname = workdir.join(self.basename)
        self._unzipped = True
        
    @property
    def mets(self):
        if not self._unzipped:
            self._unzip()

        if not os.path.isdir(self.dirname):
            raise NoProperDirectoryInZipFile(self.dirname)
            
        fnames = [ff for ff in os.listdir(self.dirname) if 'METS' in ff]
        if not fnames:
            raise NoMetsException(self.dirname)

        return Mets(os.path.join(self.dirname,fnames[0]))

    @property
    def amdspecs(self):
        if not self._unzipped:
            self._unzip()

        fnames = [ff for ff in os.listdir(os.path.join(self.dirname,'amdSpec')) if 'AMD_METS' in ff]
        if not fnames:
            raise NoAmdSpecException(str(self))

        return [ AmdSpec(os.path.join(self.dirname,'amdSpec',fname)) for fname in fnames ]
        
    def join(self,fpath):
        return os.path.join(self.dirname,fpath)

    def exists(self,fpath):
        return os.path.exists(os.path.join(self.dirname,fpath))
    
