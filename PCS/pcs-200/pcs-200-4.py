import os.path

for path in [ 'filename.txt', 'filename', '/path/to/filename.txt', '/', '' ]:
    print '"%s" :' % path, os.path.splitext(path)