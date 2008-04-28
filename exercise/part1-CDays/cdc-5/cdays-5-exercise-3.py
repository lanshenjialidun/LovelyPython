#!/bin/python
#coding:utf-8
'''cdays-5-exercise-3.py 求0~100之间的所有素数
    @note: for循环, 列表类型
    @see: math模块使用可参考http://docs.python.org/lib/module-math.html
'''

from math import sqrt

N = 100
#基本的方法
result1 = []
for num in range(2, N):
    f = True
    for snu in range(2, int(sqrt(num))+1):
        if num % snu == 0:
           f = False
           break
    if f:
        result1.append(num)
print result1

#更好的方法
result2 = [ p for p in range(2, N) if 0 not in [ p% d for d in range(2, int(sqrt(p))+1)] ]
print result2
