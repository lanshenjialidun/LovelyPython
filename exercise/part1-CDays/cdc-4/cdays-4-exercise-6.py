#!/bin/python
#coding:utf-8
'''cdays-4-exercise-6.py 文件操作
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

f = open('cdays-4-test.txt', 'r')							#以读方式打开文件
result = list()
for line in f.readlines():								#依次读取每行
	line = line.strip()								#去掉每行头尾空白
	if not len(line) or line.startswith('#'):				#判断是否是空行或注释行
		continue										#是的话，跳过不处理
	result.append(line)								#保存
result.sort()											#排序结果
#print result
open('cdays-4-result.txt', 'w').write('%s' % '\n'.join(result))	#保存入结果文件

