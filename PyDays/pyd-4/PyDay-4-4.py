# coding : utf-8
'''Lovely Python -4 PyDay 
    example 4
'''
import os
for root, dirs, files in os.walk('/media/cdrom0'):
    open('mycd.txt', 'a').write("%s %s %s" % (root,dirs,files))

