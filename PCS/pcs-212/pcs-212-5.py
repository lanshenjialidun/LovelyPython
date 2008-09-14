import os
from shutil import *
import time

def show_file_info(filename):
    stat_info = os.stat(filename)
    print '\tMode    :', stat_info.st_mode
    print '\tCreated :', time.ctime(stat_info.st_ctime)
    print '\tAccessed:', time.ctime(stat_info.st_atime)
    print '\tModified:', time.ctime(stat_info.st_mtime)

print 'BEFORE:'
show_file_info('file_to_change.txt')
copystat('pcs-212-5.py', 'file_to_change.txt')
print 'AFTER :'
show_file_info('file_to_change.txt')