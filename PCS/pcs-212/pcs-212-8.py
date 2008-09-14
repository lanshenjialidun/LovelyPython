import os
from shutil import *

print 'BEFORE: example : ', os.listdir('example')
move('example', 'example2')
print 'AFTER : example2: ', os.listdir('example2')