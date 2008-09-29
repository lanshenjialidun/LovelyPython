#!/bin/python
#coding:utf-8
'''cdays-3-exercise-2.py 字典的使用
    @not: 使用sys.args, 字典操作, 函式调用
    @see: sys模块参见help(sys)
'''

import sys                                          #导入sys模块

def collect(file):
    ''' 改变 key-value对为value-key对
    @param file: 文件对象
    @return: 一个dict包含value-key对
    '''
    result = {}
    for line in file.readlines():                   #依次读取每行
        left, right = line.split()                  #将一行以空格分割为左右两部分
        if result.has_key(right):                   #判断是否已经含有right值对应的key
            result[right].append(left)              #若有，直接添加到result[right]的值列表
        else:
            result[right] = [left]                  #没有，则新建result[right]的值列表
    return result

if __name__ == "__main__":
    if len(sys.argv) == 1:                          #判断参数个数
        print 'usage:\n\tpython cdays-3-exercise-2.py cdays-3-test.txt'
    else:
        result = collect(open(sys.argv[1], 'r'))    #调用collect函式，返回结果
        for (right, lefts) in result.items():       #输出结果
            print "%d '%s'\t=>\t%s" % (len(lefts), right, lefts)

