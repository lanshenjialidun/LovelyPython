#!/bin/python
#coding:utf-8

"""字典排序几种实现
@see : http://wiki.woodpecker.org.cn/moin/MiscItems/2008-07-01
"""

myDict = {'c':13, 'b':14, 'a':12}

# 按照字典关键词升序排列
for k, v in sorted(myDict.items(), key=lambda x:x[0]):
    print k, v

print '++++++'
# 按照字典关键词降序排列
for k, v in sorted(myDict.items(), key=lambda x:x[0], reverse=True):
    print k, v

print '++++++'
# 一种更好的方法
from operator import itemgetter
# 按照字典关键词升序排列
print sorted(myDict.iteritems(), key=itemgetter(0))
print '++++++'
# 按照字典关键词升序排列
print sorted(myDict.iteritems(), key=itemgetter(0), reverse=True)
