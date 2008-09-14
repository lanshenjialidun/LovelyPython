import os
from shutil import *

os.mkdir('example')
print 'BEFORE:', os.listdir('example')
copy('pcs-212-2.py', 'example')
print 'AFTER:', os.listdir('example')