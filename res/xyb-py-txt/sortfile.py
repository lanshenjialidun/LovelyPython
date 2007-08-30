#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heapq import heappop, heappush
LINES = 2

def split_sort(filename):
    f = file(filename)
    num = 0
    while True:
        lines = []
        for i in range(LINES):
            line = f.readline()
            if not line:
                break
            lines.append(line)
        if not lines:
            break
        lines.sort()
        num += 1
        file(filename + '.%d'%num, 'w').writelines(lines)
    return num

def merge_sorted(filename, num):
    lines = []
    for i in range(num):
        f = file(filename + '.%d'%(i+1))
        line = f.readline()
        if line:
            heappush(lines, (line, f))
    while lines:
        line, f = heappop(lines)
        yield line
        line = f.readline()
        if line:
            heappush(lines, (line, f))

if __name__ == '__main__':
    import sys
    num = split_sort(sys.argv[1])
    for line in merge_sorted(sys.argv[1], num):
        sys.stdout.write(line)
