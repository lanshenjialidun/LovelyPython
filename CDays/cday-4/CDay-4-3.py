# coding : utf-8
'''Lovely Python -4 PyDay 
    example 3
'''
import os
for root, dirs, files in os.walk('/media/cdrom0'):
    open('mycd.cdc', 'a').write(root+dirs+files)


