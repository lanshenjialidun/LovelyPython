from commands import *
from shutil import *

print 'BEFORE:'
print getoutput('ls -rlast ./example_other')
copytree('example', './example_other')
print 'AFTER:'
print getoutput('ls -rlast ./example_other')