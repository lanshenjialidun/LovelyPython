# coding : utf-8
'''Lovely Python -4 PyDay 
    example 2
'''
import os
for root, dirs, files in os.walk('/media/cdrom0'):
    print root,dirs,files

