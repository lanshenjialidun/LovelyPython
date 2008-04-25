# -*- coding: utf-8 -*-
import os
import sys
from ConfigParser import RawConfigParser

def iniTT(size_file):
    cfg = RawConfigParser()
    print size_file
    index = 1
    for (s, f) in size_file:                            #some problem is: in resultfile, index is not ordering
        cfg.add_section("%d" % index)
        cfg.set("%d" % index, 'Filename', f)
        cfg.set("%d" % index, 'FileSize', s)
        index += 1

    cfg.write(open('result_tt',"w"))
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython CDays1-2.py path'
    else:
        abs_path = os.path.abspath(sys.argv[1])
        if not os.path.isdir(abs_path):
            print '%s is not exist' % abs_path
        else:
            from CDays1 import get_top_three as gtt
            iniTT(gtt(abs_path))

