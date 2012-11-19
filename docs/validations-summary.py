#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re

sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'lib','python2.7'))
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'etc'))

from validator import Validator

def get_info(v):
    result = Validator.desc_of_validator(v)
    lines = [ l.strip() for l in  re.split("[\ \t]*\n[\ \t]*",result,re.MULTILINE) ]
    return {
        'validator': v,
        'short': lines[0],
        'desc': lines[1:]
        }

available_validators = Validator.validators()
# print Validator.desc_of_validator(available_validators[0])
# print [ str(get_info(v)) for v in available_validators ]
infos = [ get_info(v) for v in available_validators ]

widths = {
    'validator': max([len(i['validator']) for i in infos]),
    'short': max([len(i['short']) for i in infos]),
    'desc': max([len(i['short']) for i in infos]),
    }

format_line = "| {:<%d} | {:<%d} | {:<%d} |" % (widths['validator'],
                                                widths['short'],
                                                widths['desc'])

format_line = "| {:<%d} | {:<%d} | {:<%d} |" % (widths['validator'],
                                                widths['short'],
                                                widths['desc'])

print "+" + "+".join(["-"*(widths['validator']+2),
                      "-"*(widths['short']+2),
                      "-"*(widths['desc']+2)]) + "+"
for info in infos:
    desc = info['desc']
    line = desc[0]
    print format_line.format(info['validator'],info['short'],line.strip())

    for line in desc[1:]:
        print format_line.format("","",line.strip())

    print "+" + "+".join(["-"*(widths['validator']+2),
                          "-"*(widths['short']+2),
                          "-"*(widths['desc']+2)]) + "+"
    
                    



