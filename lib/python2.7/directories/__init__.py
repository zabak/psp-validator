#!/usr/bin/python
#-*- coding: utf-8 -*-

import tempfile, datetime, os, sys, shutil

class WorkDir(object):
    def __init__(self, tmpbase):
        self.tmpbase = tmpbase
        self.tmpdir = tempfile.mkdtemp(dir=tmpbase, prefix = datetime.datetime.now().strftime("PSP-Validation-%Y-%m-%d-"))
        #self.tmpdir = "/opt/psp-validator/tmp/PSP-Validation-2012-10-28-DWKjQC"
        
    def __str__(self):
        return self.tmpdir
    
    def join(self,*paths):
        return os.path.join(self.tmpdir,*paths)
    
    def mkdir(self,path):
        result = os.path.join(self.tmpdir,path)
        os.mkdir(result)
        return result

    def rmdir(self):
        """smaze se"""
        shutil.rmtree(self.tmpdir)
        
