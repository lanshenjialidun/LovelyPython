#!/bin/python
#coding:utf-8
'''cdays+1-exercise-2.py 
    @note: 利用ConfigParser解析ini格式
    @see: 文档参见http://pydoc.org/2.4.1/ConfigParser.html, 其他例子http://effbot.org/librarybook/configparser-example-1.py
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''
import os
import sys
from ConfigParser import RawConfigParser

def iniTT(size_file):
    ''' 按照.ini的格式，存储size_file
    '''
    cfg = RawConfigParser()
    print size_file
    index = 1
    for (s, f) in size_file:
        cfg.add_section("%d" % index)                   #增加一个section
        cfg.set("%d" % index, 'Filename', f)            #在该section设置Filename及其值
        cfg.set("%d" % index, 'FileSize', s)            #在该section设置FileSize及其值
        index += 1

    cfg.write(open('cdays+1-result.txt',"w"))

def gtt(path):
    ''' 获取给定路径中文件大小最大的三个
    @param path: 指定路径
    @return 返回一个list，每项为 (size, filename)
    '''
    all_file = {}
    for root, dirs, files in os.walk(path):             #遍历path
        for onefile in files:
            fname = os.path.join(root, onefile)         #获得当前处理文件的完整名字
            fsize = os.stat(fname).st_size              #获得当前处理文件大小
            if all_file.has_key(fsize):                 #按照文件大小存储
                all_file[fsize].append(fname)
            else:
                all_file[fsize] = [fname]
    fsize_key = all_file.keys()                         #得到所有的文件大小
    fsize_key.sort()                                    #排序，从小到大
    result = []
    for i in [-1, -2, -3]:                              #依次取最大的三个
        for j in all_file[fsize_key[i]]:                #保存
            result.append((fsize_key[i], j))
    return result[:3]                                   #返回前三个

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython cdays+1-exercise-2.py path'
    else:
        abs_path = os.path.abspath(sys.argv[1])
        if not os.path.isdir(abs_path):
            print '%s is not exist' % abs_path
        else:
            #from cdays+1-exercise-1 import get_top_three as gtt
            iniTT(gtt(abs_path))

