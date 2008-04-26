#!/bin/python
#coding:utf-8
'''cdays-5-exercise-3.py print out and for expression
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

for index in range(1, 6):
	if index > 3:	
		index = 2*3 -index		#调整index
	print ' '*(3-index),			#输出每行空格个数
	print '*'*(2*index - 1)			#输出每行*的个数
