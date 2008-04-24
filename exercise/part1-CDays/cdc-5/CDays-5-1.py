#!/bin/python
#coding:utf-8

x = 12*34+78-132/6
y = (12*(34+78)-132)/6
z = (8.6/4)**5

print '12*34+78-132/6 = %d' % x
print '(12*(34+78)-132)/6 = %d' % y
print '(8.6/4)**5 = %f' % z

import math

a = math.fmod(145, 23)
b = math.sin(0.5)
c = math.cos(0.5)

print '145/23的余数 = %d' % a
print 'sin(0.5) = %f' %b
print 'cos(0.5) = %f' %c
