#!/bin/python
#coding:utf-8
'''cdays-5-exercise-2.py basic operation and math library
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

x = 12*34+78-132/6		#表达式计算
y = (12*(34+78)-132)/6
z = (8.6/4)**5

print '12*34+78-132/6 = %d' % x
print '(12*(34+78)-132)/6 = %d' % y
print '(8.6/4)**5 = %f' % z

import math				#导入数学计算模块

a = math.fmod(145, 23)		#求余函数
b = math.sin(0.5)			#正弦函数
c = math.cos(0.5)			#余弦函数

print '145/23的余数 = %d' % a
print 'sin(0.5) = %f' %b
print 'cos(0.5) = %f' %c
