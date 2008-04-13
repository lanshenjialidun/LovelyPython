# coding : utf-8
import os
for root, dirs, files in os.walk('/media/cdrom0'):
    open('mycd.cdc', 'a').write(root+dirs+files)


