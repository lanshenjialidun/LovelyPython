#!/bin/python
#coding:utf-8
'''cdays-5-exercise-2.py 求表达式的值
    @note: 基本表达式运算, 格式化输出, math模块
    @see: math模块使用可参考http://docs.python.org/lib/module-math.html
'''

x = 12*34+78-132/6      #表达式计算
y = (12*(34+78)-132)/6
z = (86/4)**5

print '12*34+78-132/6 = %d' % x
print '(12*(34+78)-132)/6 = %d' % y
print '(86/40)**5 = %f' % z

import math             #导入数学计算模块

a = math.fmod(145, 23)  #求余函式
b = math.sin(0.5)       #正弦函式
c = math.cos(0.5)       #余弦函式

print '145/23的余数 = %d' % a
print 'sin(0.5) = %f' %b
print 'cos(0.5) = %f' %c
