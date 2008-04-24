#!/bin/python

f = open('test', 'r')
result = list()
for line in f.readlines():
	line = line.strip()
	if not len(line) or line.startswith('#'):
		continue
	result.append(line)
result.sort()
open('test_result', 'w').write('%s' % '\n'.join(result))

