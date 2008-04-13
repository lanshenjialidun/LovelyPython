# coding : utf-8
'''Lovely Python -4 PyDay 
    example 4
'''
import os
export = ""
for root, dirs, files in os.walk('/media/cdrom0'):
    export+="\n %s;%s;%s" % (root,dirs,files)
open('mycd2.cdc', 'w').write(export)

