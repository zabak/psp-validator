# -*- coding: utf-8 -*-
import logging, sys, os

# pridame lokalni knihovny
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','python2.7'))

from directories import WorkDir

_logger = None
_workdir = None

def get_logger():
    global _logger
    if not _logger:
        _logger = logging.getLogger("PSP_VALIDATION")
        # %d (%F{1}:%L)         %-15c   - %p - %m %n
        formatter = logging.Formatter('%(asctime)s %(name)s\t%(levelname)s \t- %(message)s')
        _logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        _logger.addHandler(ch)
    return _logger

def get_workdir():
    global _workdir
    if not _workdir:
        _workdir = WorkDir(tmpbase = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'tmp'))
    return _workdir

logger = get_logger()
workdir = get_workdir()

