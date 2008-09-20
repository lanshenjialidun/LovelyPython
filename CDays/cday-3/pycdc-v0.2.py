# -*- coding: utf-8 -*-
'''Lovely Python -3 PyDay 
    PyCDC v0.2
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
    #判别sys.argv[2]中是否有目录，以便进行自动创建
    cdWalker(CDROM,sys.argv[2])
    print "记录光盘信息到 %s" % sys.argv[2]
elif "-d"==sys.argv[1]:
    if "-k"==sys.argv[3]:
        #进行文件搜索
    else:
        print '''PyCDC 使用方式:
        python pycdc.py -d cdc -k 中国火
        #搜索 cdc 目录中的光盘信息，寻找有“中国火”字样的文件或是目录，在哪张光盘中
        '''
else:
    print '''PyCDC 使用方式:
    python pycdc.py -e mycd1-1.cdc
    #将光盘内容记录为 mycd1-1.cdc
    '''
