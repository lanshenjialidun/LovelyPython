from commands import *
from shutil import *

print 'BEFORE:', getstatus('file_to_change.txt')
copymode('pcs-212-4.py', 'file_to_change.txt')
print 'AFTER :', getstatus('file_to_change.txt')