#!/bin/python
import sys
import os

def get_top_three(path):
    all_file = {}
    for root, dirs, files in os.walk(path):
        for onefile in files:
            fname = os.path.join(root, onefile)
            fsize = os.stat(fname).st_size
            if all_file.has_key(fsize):
                all_file[fsize].append(fname)
            else:
                all_file[fsize] = [fname]
    fsize_key = all_file.keys()
    fsize_key.sort()
    result = []
    for i in [-1, -2, -3]:
        for j in all_file[fsize_key[i]]:
            result.append((fsize_key[i], j))
    return result[:3]
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython CDays1-1.py path'
    else:
        abs_path = os.path.abspath(sys.argv[1])
        if not os.path.isdir(abs_path):
            print '%s is not exist' % abs_path
        else:
            top = get_top_three(abs_path)
            for (s, f) in top:
                print '%s\t->\t%s' % (s, f)
            
            
