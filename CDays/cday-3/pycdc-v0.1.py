# -*- coding: utf-8 -*-
'''Lovely Python -3 PyDay 
    PyCDC v0.1
'''
import os,sys
CDROM = '/media/cdrom0'
def cdWalker(cdrom,cdcfile):
    export = ""
    for root, dirs, files in os.walk(cdrom):
        export+="\n %s;%s;%s" % (root,dirs,files)
    open(cdcfile, 'w').write(export)
#cdWalker('/media/cdrom0','cd1.cdc')
if "-e"==sys.argv[1]:
    cdWalker(CDROM,sys.argv[2])
    print "记录光盘信息到 %s" % sys.argv[2]
else:
    print '''PyCDC 使用方式:
    python pycdc.py -e mycd1-1.cdc
    #将光盘内容记录为 mycd1-1.cdc
    '''
