import os
from shutil import *

print 'BEFORE:', os.listdir(os.getcwd())
copyfile('pcs-212-1.py', 'pcs-212-1.py.copy')
print 'AFTER:', os.listdir(os.getcwd())
