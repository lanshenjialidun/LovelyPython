#!/bin/python
#coding:utf-8

for index in range(1, 6):
	if index > 3:
		index = 2*3 -index
	print ' '*(3-index),
	print '*'*(2*index - 1)
