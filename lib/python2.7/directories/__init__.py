#!/usr/bin/python
#-*- coding: utf-8 -*-

import tempfile, datetime, os, sys

class WorkDir(object):
    def __init__(self, tmpbase):
        self.tmpbase = tmpbase
        self.tmpdir = tempfile.mkdtemp(dir=tmpbase, prefix = datetime.datetime.now().strftime("PSP-Validation-%Y-%m-%d-"))
        
    def __str__(self):
        return self.tmpdir
    
    def join(self,path):
        return os.path.join(self.tmpdir,path)
    
    def mkdir(self,path):
        result = os.path.join(self.tmpdir,path)
        os.mkdir(result)
        return result
