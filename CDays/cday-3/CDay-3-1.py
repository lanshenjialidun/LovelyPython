# coding : utf-8
import os
def cdWalker(cdrom,cdcfile):
    export = ""
    for root, dirs, files in os.walk(cdrom):
        export+="\n %s;%s;%s" % (root,dirs,files)
    open(cdcfile, 'w').write(export)

cdWalker('/media/cdrom0','cd1.cdc')
cdWalker('/media/cdrom0','cd2.cdc')
